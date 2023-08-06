import asyncio
from datetime import datetime
import logging
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Union, Any, List, Optional

import aiosql
from aiosql.aiosql import _ADAPTERS
import click
from aiosql.queries import Queries
from click import Context

from aiosqlembic.models.cli import (
    Version,
    MigrateRevision,
    MigrationResult,
    MigrationError,
    RevisionPath,
)
from aiosqlembic.utils import (
    get_revision_tree,
    print_version,
    get_connection,
    camel2snake,
    templateEnv,
    get_next_revision,
    get_current_revision,
    get_aiosqlembic_queries,
)

MIN_VERSION = 0
MAX_VERSION = 2 ** (64 - 1) - 1  # ie max size of sqlite3 integer and postgresql bigint

logging.basicConfig(format="%(levelname)-8s: %(filename)10s:%(lineno)4d: %(message)s")
logger = logging.getLogger("aiosqlembic")


def coro(f):  # type: ignore
    @wraps(f)
    def wrapper(*args, **kwargs):  # type: ignore
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@dataclass
class AiosqlembicContext:
    debug: bool
    migration_directory: Path
    driver: str
    driver_adapter: Union[str, Any]
    dsn: str
    logger: logging.Logger
    aiosqlembic_queries: Queries
    current_version: Version


class AiosqlembicException(Exception):
    pass


@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Prints aiosqlembic version and exits",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Sets the logging level to DEBUG or let it at INFO",
)
@click.option(
    "-m",
    "--migration-directory",
    default=Path("."),
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    help="Where migrations files will be",
)
@click.argument("driver", required=True, type=click.Choice(["asyncpg"]))
@click.argument("dsn", required=True)
@click.pass_context
@coro
async def cli(
    ctx: Context, debug: bool, migration_directory: Path, driver: str, dsn: str
) -> None:
    """
    Main entry point for the application
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("logging set to DEBUG")
    else:
        logger.setLevel(logging.INFO)
        logger.debug("logging set to INFO")

    driver_adapter = _ADAPTERS[driver]
    aiosqlembic_queries = get_aiosqlembic_queries(driver=driver)
    try:
        async with get_connection(driver, dsn) as connection:
            conn_db_table = await aiosqlembic_queries.check_aiosqlembic(connection)
            if not conn_db_table.exists:
                logger.debug("aiosqlembic table doesn't exist")
                await aiosqlembic_queries.create_schema(connection)
                applied = True if driver == "asyncpg" else 1
                await aiosqlembic_queries.insert_revision(
                    connection, version_id=0, is_applied=applied
                )
                logger.debug("inserted 1st revision with version_id=0")
            else:
                click.echo(
                    click.style("Connected to: ") + click.style(f"{dsn}", fg="green")
                )

            current_version = await aiosqlembic_queries.get_version(connection)
            ctx.obj = AiosqlembicContext(
                debug=debug,
                migration_directory=Path(migration_directory),
                driver=driver,
                dsn=dsn,
                logger=logger,
                driver_adapter=driver_adapter,
                aiosqlembic_queries=aiosqlembic_queries,
                current_version=current_version,
            )
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        pass


@cli.command()
@click.pass_obj
@coro
async def status(settings: AiosqlembicContext) -> None:
    """Prints the status of revisions and if those are applied or not"""
    logger.debug(
        f"status with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    revision_tree = get_revision_tree(
        settings.migration_directory, MIN_VERSION, MAX_VERSION
    )
    headers = ["current", "time", "applied at", "revision"]
    table = []
    table.append(headers)

    current: Version = await get_current(settings)
    current_revision = get_current_revision(revision_tree, current.version_id)
    async with get_connection(settings.driver, settings.dsn) as connection:
        for revision in revision_tree:
            line = []
            migrate_revision: MigrateRevision = (
                await settings.aiosqlembic_queries.migrate_revision(
                    connection, version_id=revision.version_id
                )
            )

            if migrate_revision is not None and migrate_revision.is_applied:
                applied_ts = migrate_revision.tstamp.isoformat()
            else:
                applied_ts = "pending"
            # col 0 current rev
            if current_revision == revision:
                line.append("[*]")
            else:
                line.append("")
            # col1 date
            line.append(datetime.utcnow().isoformat())
            # col2 applied timestamp
            line.append(applied_ts)
            # col3 revision filename
            if revision.file is not None:
                line.append(revision.file.name)
            else:
                line.append("")
            table.append(line)

        def print_table(table: List[List[str]]) -> None:
            longest_cols = [
                (max([len(str(row[i])) for row in table]) + 3)
                for i in range(len(table[0]))
            ]
            row_format = "".join(
                ["{:>" + str(longest_col) + "}" for longest_col in longest_cols]
            )
            for i, row in enumerate(table):
                if i == 0:
                    click.echo(
                        click.style(row_format.format(*row), fg="blue", bg="yellow")
                    )

                else:
                    if row[2] == "pending":
                        click.echo(click.style(row_format.format(*row), fg="red"))
                    else:
                        click.echo(row_format.format(*row))

    print_table(table)
    logger.debug("status print")
    return


@cli.command()
@click.option("--name", "-n", required=True)
@click.option("--version_id", "-v", required=False)
@click.option("--auto", "-a", required=False, default=False, type=click.BOOL)
@click.pass_obj
def create(
    settings: AiosqlembicContext, name: str, version_id: int, auto: bool
) -> None:
    """Create a revision file"""
    logger.debug(
        f"create with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    version_id_s = str(version_id)
    if not version_id:
        version_id_s = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    logger.debug(f"create file with version_id: {version_id_s}")
    nospacename = name.replace(" ", "_")
    expected_revision_file = (
        settings.migration_directory / f"{version_id_s}_{camel2snake(nospacename)}.sql"
    )
    logger.debug(f"file: {expected_revision_file} created")
    expected_revision_file.touch()
    revision_template = "revision.sql"
    template = templateEnv.get_template(revision_template)

    # if auto:
    #     click.echo(
    #         "Attempt at generating sql statements! Please review them once written!"
    #     )
    #     # we load in theorical db the current list of revisions up the latest one
    #     async with create_test_database(
    #         settings.dsn, "theorical_aiosqlembic"
    #     ) as theorical:
    #         try:
    #             # putting theorical up to date with revision files
    #             revision_queries: Queries = aiosql.from_path(
    #                 settings.migration_directory, settings.driver
    #             )
    #             up_queries = [
    #                 x for x in revision_queries.available_queries if "up" in x
    #             ]
    #             pool_theorical = await asyncpg.create_pool(theorical)
    #             if up_queries:
    #                 for up in up_queries:
    #                     await getattr(revision_queries, up)(pool_theorical)
    #
    #             pool_current = await asyncpg.create_pool(settings.dsn)
    #             # up
    #             up_mig = await Amigration().create(pool_theorical, pool_current)
    #             up_mig.set_safety(False)
    #             up_mig.add_all_changes()
    #             logger.debug(up_mig.statements)
    #             up_ss = up_mig.sql
    #             upgrade_statements = up_ss
    #             # down
    #             down_mig = await Amigration().create(pool_current, pool_theorical)
    #             down_mig.set_safety(False)
    #             down_mig.add_all_changes()
    #             logger.debug(down_mig.statements)
    #             down_ss = down_mig.sql
    #             downgrade_statements = down_ss
    #         except Exception as e:
    #             logger.error(e)
    #             raise e
    #         finally:
    #             await pool_current.close()
    #             await pool_theorical.close()

    # else:
    upgrade_statements = "SELECT 'upgrade sql query here';"
    downgrade_statements = "SELECT 'downgrade sql query here';"

    output = template.render(
        upgrade_statements=upgrade_statements,
        downgrade_statements=downgrade_statements,
    )
    expected_revision_file.write_text(output)
    click.echo(f"Created: {expected_revision_file}")


async def get_current(settings: AiosqlembicContext) -> Version:
    async with get_connection(settings.driver, settings.dsn) as connection:
        versions: List[Version] = await settings.aiosqlembic_queries.get_version(
            connection
        )
    for version in versions:
        if version.is_applied:  # pragma: no cover
            return version
    return Version(version_id=-1, is_applied=False)


async def downTo(settings: AiosqlembicContext, version_id: int) -> MigrationResult:
    revision_tree = get_revision_tree(
        settings.migration_directory, MIN_VERSION, MAX_VERSION
    )
    current: Version = await get_current(settings)
    current_revision = get_current_revision(revision_tree, current.version_id)
    if current_revision is not None and current_revision.file is not None:
        revision_query = aiosql.from_path(current_revision.file, settings.driver)
        async with get_connection(settings.driver, settings.dsn) as connection:
            try:
                if settings.driver == "asyncpg":
                    async with connection.transaction():
                        result = await revision_query.down(connection)
                        logger.debug(f"down revision result: {result}")
                        await settings.aiosqlembic_queries.delete_revision(
                            connection, version_id=current_revision.version_id
                        )
                mr = MigrationResult(
                    error=MigrationError(error=None, file=None),
                    revision_applied=current_revision.version_id,
                )
            except Exception as e:
                logger.error(e)
                error = MigrationError(error=str(e), file=current_revision.file)
                mr = MigrationResult(error=error, revision_applied=None)
    else:
        error = MigrationError(error="You're at min rev", file=None)
        mr = MigrationResult(error=error, revision_applied=None)
    return mr


async def runUp(
    settings: AiosqlembicContext, next_revision: Optional[RevisionPath]
) -> MigrationResult:
    if next_revision is not None:
        revision_query = aiosql.from_path(next_revision.file, settings.driver)
        async with get_connection(settings.driver, settings.dsn) as connection:
            try:
                if settings.driver == "asyncpg":
                    async with connection.transaction():
                        result = await revision_query.up(connection)
                        logger.debug(f"up revision result: {result}")
                        await settings.aiosqlembic_queries.insert_revision(
                            connection,
                            version_id=next_revision.version_id,
                            is_applied=True,
                        )
                mr = MigrationResult(
                    error=MigrationError(error=None, file=None),
                    revision_applied=next_revision.version_id,
                )
            except Exception as e:
                logger.error(e)
                error = MigrationError(error=str(e), file=next_revision.file)
                mr = MigrationResult(error=error, revision_applied=None)
    else:
        error = MigrationError(error="You're at max up revision", file=None)
        mr = MigrationResult(error=error, revision_applied=None)
    return mr


async def upTo(settings: AiosqlembicContext, version_id: int) -> List[MigrationResult]:
    current: Version = await get_current(settings)
    revision_tree = get_revision_tree(
        settings.migration_directory, current.version_id, version_id
    )
    mrs = []
    for _ in revision_tree:
        current = await get_current(settings)
        next_revision = get_next_revision(revision_tree, current.version_id)
        mr = await runUp(settings=settings, next_revision=next_revision)
        mrs.append(mr)
    return mrs


@cli.command()
@click.option("--version_id", "-v", required=False)
@click.pass_obj
@coro
async def up(settings: AiosqlembicContext, version_id: int) -> None:
    """Upgrade database to latest revision or specified version id if provided"""
    logger.debug(
        f"up with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    if version_id is None:
        mrs = await upTo(settings, MAX_VERSION)
    else:
        current: Version = await get_current(settings)
        versions = [
            r.version_id
            for r in get_revision_tree(
                settings.migration_directory, current.version_id, version_id
            )
        ]
        if version_id not in versions:
            click.Abort(f"Version id should be in {versions}")
        else:
            mrs = await upTo(settings, version_id)
    if all([mr.error.error is None for mr in mrs]):
        click.echo(
            click.style(
                f"\u25b2\u25b2 applied revisions up \u25b2\u25b2: {[mr.revision_applied for mr in mrs]}",
                fg="green",
            )
        )

    else:
        for mr in mrs:
            if mr.error.error is not None:
                click.echo(
                    click.style(
                        f"Error: {mr.error.error} on file: {mr.error.file}", fg="red"
                    )
                )
        raise AiosqlembicException("Up failed")


@cli.command()
@click.pass_obj
@coro
async def up1(settings: AiosqlembicContext) -> None:
    """Upgrade database by one single revision"""
    logger.debug(
        f"up by one with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    revision_tree = get_revision_tree(
        settings.migration_directory, MIN_VERSION, MAX_VERSION
    )
    current: Version = await get_current(settings)
    next_revision = get_next_revision(revision_tree, current.version_id)
    mr = await runUp(settings=settings, next_revision=next_revision)
    if mr.error.error:
        click.echo(
            click.style(f"Error: {mr.error.error} on file: {mr.error.file}", fg="red")
        )
    else:
        click.echo(
            click.style(
                f"\u25b2\u25b2 applied revisions up \u25b2\u25b2: {mr.revision_applied}",
                fg="green",
            )
        )


@cli.command()
@click.pass_obj
@coro
async def down(settings: AiosqlembicContext) -> None:
    logger.debug(
        f"down with debug: {settings.debug} - migrations: {settings.migration_directory} - driver: {settings.driver} - dsn: {settings.dsn}"
    )
    mr = await downTo(settings, MAX_VERSION)
    if mr.error.error:
        click.echo(
            click.style(f"Error: {mr.error.error} on file: {mr.error.file}", fg="red")
        )
        raise AiosqlembicException("Down failed")
    else:
        click.echo(
            click.style(
                f"\u25bc\u25bc applied revisions down \u25bc\u25bc: {mr.revision_applied}",
                fg="green",
            )
        )


def main() -> None:
    cli()


if __name__ == "__main__":
    main()

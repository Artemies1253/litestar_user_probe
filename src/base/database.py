from advanced_alchemy.config import AlembicAsyncConfig
from click import Group
from litestar.plugins import CLIPluginProtocol
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from sqlalchemy import text
from src.base.settings import SQLALCHEMY_DATABASE_URL

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=SQLALCHEMY_DATABASE_URL,
    before_send_handler="autocommit",
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=True,
    alembic_config=AlembicAsyncConfig(
        script_location="./migrations/"
    ),

)
advanced_alchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)


class ApplicationCore(CLIPluginProtocol):

    def on_cli_init(self, cli: Group) -> None:

        @cli.command('check-db-status')
        def check_db_status() -> None:
            import anyio
            async def _check_db_status() -> None:
                async with sqlalchemy_config.get_session() as db_session:
                    a_value = await db_session.execute(text("SELECT 1"))
                    if a_value.scalar_one() == 1:
                        print("Database is healthy")
                    else:
                        print("Database is not healthy")

            anyio.run(_check_db_status)

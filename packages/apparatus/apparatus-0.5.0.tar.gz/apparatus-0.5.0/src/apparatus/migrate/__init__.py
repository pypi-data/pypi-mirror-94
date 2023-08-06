import logging
import os
from typing import Optional, List

from pydantic import Field
from retry import retry

from apparatus.base import Command, read_config

log = logging.getLogger(__name__)

try:
    import alembic.config
    import sqlalchemy
except ImportError:
    pass
else:

    class Migrate(Command):
        init: str = Field(
            "migrations/init.sql",
            description="path to the database initialization SQL script",
            required=False,
        )
        key: str = Field(
            "database",
            description="key for the database configuration in the config map",
            required=False,
        )
        separate: bool = Field(
            False,
            description="execute each migration in a separate transaction",
            required=False,
        )
        env: Optional[str] = Field(None, description="the environment", required=False)

        RETRY_PARAMS = {
            "exceptions": sqlalchemy.exc.OperationalError,
            "tries": 20,
            "max_delay": 1,
            "delay": 0.2,
            "backoff": 1.5,
        }
        ALEMBIC_ARGS = ["upgrade", "head"]
        HELP = "Perform database migrations"

        def run(self, remainder: List[str]) -> None:
            config = read_config(self.env)
            url = self._database_url(config)
            self._init(url)
            self._run_alembic(url, remainder)

        def _database_url(self, config) -> str:
            config = config[self.key]
            return "{dialect}://{user}:{password}@{host}:{port}/{database}".format(
                dialect=config.get("dialect", "postgresql"),
                user=config["user"],
                password=config["password"],
                host=config["host"],
                port=config["port"],
                database=config["database"],
            )

        def _init(self, url: str) -> None:
            engine = sqlalchemy.create_engine(url)

            @retry(**self.RETRY_PARAMS, logger=None)
            def connect():
                return engine.connect()

            log.info("Waiting at most %.02f seconds for connection", self._wait_for())
            conn = None
            try:
                conn = connect()
                if os.path.isfile(self.init):
                    with open(self.init) as h:
                        sql = h.read()

                    log.info("Applying %s to %r", self.init, engine.url)
                    conn.execute(sql)
                else:
                    log.info("No file at %s", self.init)
            finally:
                if conn is not None:
                    conn.close()

        @classmethod
        def _wait_for(cls) -> float:
            delay = cls.RETRY_PARAMS["delay"]
            backoff = cls.RETRY_PARAMS["backoff"]
            max_delay = cls.RETRY_PARAMS["max_delay"]
            result = 0
            for i in range(cls.RETRY_PARAMS["tries"] + 1):
                result += min(delay * (backoff ** i), max_delay)
            return result

        def _run_alembic(self, url: str, remainder: List[str]) -> None:
            alembic_args = remainder or self.ALEMBIC_ARGS
            alembic_args = ["-x", f"url={url}"] + alembic_args
            if self.separate is True and alembic_args[:2] == ["upgrade", "head"]:
                while True:
                    try:
                        alembic.config.main(alembic_args)
                    except SystemExit:
                        # The alembic console runner did not produce anymore migrations
                        # TODO: Do not print an alembic ERROR to the log
                        # This is likely difficult to fix when using the default alembic command
                        # line program. Finding a proper solution probably requires understanding
                        # the internals of alembic better.
                        break
            else:
                os.environ["URL"] = url
                alembic.config.main(alembic_args)

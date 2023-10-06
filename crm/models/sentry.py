import os
import sentry_sdk
import logging
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import LoggingIntegration

load_dotenv()


class Sentry:
    def sentry_skd(self):
        """The function init sentry_sdk for logging.

        Returns:
            _type_: _description_
        """
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Niveau de logging à capturer (ou un autre niveau au besoin)
            event_level=logging.INFO,  # Niveau d'événement à envoyer à Sentry
        )

        return sentry_sdk.init(dsn=os.getenv("DNS_SENTRY"), traces_sample_rate=1.0, integrations=[sentry_logging])

    def logger(self):
        """The function setup logger info to display in sentry dashbord

        Returns:
            _type_: Logger
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f"{__name__}.log", mode="w")
        formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

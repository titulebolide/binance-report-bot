import logging
import datetime as dt
import apprise
import brb.conf as conf
import os

log_level = logging.DEBUG if os.environ.get("BRB_DEBUG") is not None else logging.WARNING

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=log_level
)
logger = logging.getLogger(__name__)

notifier = None
if len(conf.APPRISE_URLS) > 0:
    notifier = apprise.Apprise()
    for url in conf.APPRISE_URLS:
        notifier.add(url)

    class ErrorAppriseNotifier(logging.Handler):
        def __init__(self):
            """
            Logging Handler that sends an apprise notification when an error is raised
            """
            super().__init__()

        def emit(self, record):
            if record.levelno >= 30:  # warning, critical or error
                date = str(dt.datetime.fromtimestamp(int(record.created)))
                notifier.notify(
                    body=f"```{date} - {record.name} - {record.levelname} - {record.msg}```",
                )

    logger.addHandler(ErrorAppriseNotifier())

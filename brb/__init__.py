import logging
import datetime as dt
import apprise
import conf

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)

notifier = None
if conf.APPRISE_URL != "":
    notifier = apprise.Apprise()
    notifier.add(conf.APPRISE_URL)

    class ErrorAppriseNotifier(logging.Handler):
        def __init__(self):
            """
            Logging Handler that sends an apprise notification when an error is raised
            """
            super().__init__()
        def emit(self, record):
            if record.levelno >= 40: #critical or error
                date = str(dt.datetime.fromtimestamp(int(record.created)))
                notifier.notify(
                    body = f"{date} - {record.name} - {record.levelname} - {record.msg}",
                )

    logger.addHandler(ErrorAppriseNotifier())

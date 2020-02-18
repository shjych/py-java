from logging import getLogger, Formatter, handlers, DEBUG
import os.path


class Logger:
    def __init__(self, name, file='logs/app.logs'):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')

        (dir_name, _) = tuple(file.split("/"))
        if os.path.exists(file) is False and os.path.isdir(dir_name) is False:
            os.mkdir("logs")

        handler = handlers.RotatingFileHandler(
            filename=file,
            maxBytes=1048576,
            backupCount=3
        )
        handler.setFormatter(formatter)
        handler.setLevel(DEBUG)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

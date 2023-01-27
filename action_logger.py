import logging
import time
import sys


logger = logging.getLogger("user_action_logger")
logger.setLevel(level=logging.DEBUG)

log_file_formatter = logging.Formatter(f"%(levelname) - 4s %(message)s")
file_handler = logging.FileHandler(filename='user_action_log.log')
file_handler.setFormatter(log_file_formatter)
file_handler.setLevel(level=logging.DEBUG)

stream_log_formatter = logging.Formatter(f"%(levelname)-4s %(message)s")
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(stream_log_formatter)
console_handler.setLevel(level=logging.DEBUG)


class UserLog:
    def __init__(self, action_type):
        self.action_type = action_type
        self.user_id = action_type.from_user.id
        self.user_full_name = action_type.from_user.full_name
        self.formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    def log_action(self, command):
        return logger.info(f'{self.formatted_time} [ID: {self.user_id}] [NAME: {self.user_full_name}] - {command} ')


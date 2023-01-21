import logging
import time


logging.basicConfig(level=logging.INFO)


class UserLog:
    def __init__(self, action_type):
        self.action_type = action_type
        self.user_id = action_type.from_user.id
        self.user_name = action_type.from_user.first_name
        self.user_full_name = action_type.from_user.full_name

    def log_action(self, command):
        return logging.info(f' {time.asctime()} | CMD: {command} | ID: {self.user_id} | NAME: {self.user_full_name}')


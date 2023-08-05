# pylint: disable=useless-super-delegation

from joinnector.service.base_sdk_service import BaseSDKService


class TaskService(BaseSDKService):
    def __init__(self, name):
        super().__init__(name)


task_service = TaskService("task")

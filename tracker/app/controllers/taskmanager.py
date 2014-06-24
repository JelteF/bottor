from app.controllers.job import JobController
from app.controllers.task import TaskController
from app.constants import Constants


class TaskManager:

    @staticmethod
    def getTask(peer_id):
        TaskManager.cancelLongRunningTasks()
        job = JobController.getJobWithFreeTask()

        if not job:
            return 0

        task = JobController.getTask(job, peer_id)

        return task

    @staticmethod
    def cancelLongRunningTasks():
        tasks = TaskController.getLongRunningTasks(Constants.MAX_TASK_TIME)

        for task in tasks:
            TaskController.cancelTask(task.id)
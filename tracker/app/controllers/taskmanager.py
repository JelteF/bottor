from app.controllers.job import Job
from app.controllers.task import Task

class TaskManager:

    @staticmethod
    def getTask(peer_id):
        job = JobController.getJobWithFreeTask()

        if not job:
            return 0

        task = JobController.getTask(job, peer_id)

        return task

    @staticmethod
    def setResult(peer_id, task_id, row, col, value):
        task = TaskController.get(task_id)

        # NOG CHECKEN VOOR AFZENDER PEER_ID

        TaskController.setResult(task, row, col, value)
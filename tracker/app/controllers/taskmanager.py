from app.controllers.job import JobController
from app.controllers.task import TaskController

class TaskManager:

    @staticmethod
    def getTask(peer_id):
        job = JobController.getJobWithFreeTask()

        if not job:
             return 0

        task = JobController.getTask(job, peer_id)

        return task


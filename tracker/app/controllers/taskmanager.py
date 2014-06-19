from app.controllers.job import JobController


class TaskManager:

    @staticmethod
    def getTask(peer_id):
        print('a1')
        job = JobController.getJobWithFreeTask()
        print('a2')

        if not job:
            return 0
        print('a3')

        task = JobController.getTask(job, peer_id)
        print('a4')

        return task

from BotMatrix import BotMatrix
from Job import Job

matrixA = BotMatrix("../sample_matrices/A50")
matrixB = BotMatrix("../sample_matrices/B50")

jobManager = JobManager()
job = Job(matrixA, matrixB)

jobManager.addJob(job)
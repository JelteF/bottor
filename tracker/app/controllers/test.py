from app.controllers.matrix import MatrixController

matrix = MatrixController.create("../sample_matrices/A50")

array = MatrixController.loadAsArray(matrix)

MatrixController.writeArrayToFile(array, "../sample_matrices/test")

MatrixController.delete(matrix)

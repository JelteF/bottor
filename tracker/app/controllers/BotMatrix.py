class InvalidMatrixError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


class BotMatrix:
    def __init__(self, filename):
        mFile = open(filename, "r")
        file_contents = mFile.readlines()
        self.matrix = []

        rowCnt = len(file_contents);
        colCnt = 0;

        for line in file_contents:
            columns = line.split()
            if colCnt is 0:
                colCnt = len(columns)
            else:
                if colCnt is not len(columns):
                    raise InvalidMatrixError("Different column lengths found")
            self.matrix.append(columns)
           

        self.rows = rowCnt
        self.cols = colCnt

        mFile.close()

    def dump(self):
        for i in range(self.rows):
            print "[",
            for j in range(self.cols):
                print self.matrix[i][j],
            print "]"

    def getRow(self, i):
        if i >= self.rows:
            return 0

        return self.matrix[i]

    def getColumn(self, j):
        result = []

        if j >= self.cols:
            return 0

        for i in range(self.rows):
            result.append(self.matrix[i][j])

        return result
class Cities:
    def __init__(self):
        self._coordinates = dict()
        with open('coordinates.txt') as file:
            index = 0
            for line in file:
                if index == 0:
                    continue
                city, x, y = line.strip().split()
                self._coordinates[city] = (x, y)
        self._solution = list()
        with open('solution.txt') as file:
            for line in file:
                self._solution.append(int(line))

    def getCity(self, city):
        return self._coordinates[city]

    def getSolution(self):
        return self._solution


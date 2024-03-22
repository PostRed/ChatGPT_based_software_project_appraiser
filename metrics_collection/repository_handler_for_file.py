import csv

from repository_handler import RepozitoryHandler


class RepozitoryHandlerForFile:
    def __init__(self, path_to_file: str, username: str, token: str):
        self.repozitories = []
        self.path_to_file = path_to_file
        self.username = username
        self.token = token
        self.fill_repozitories()

    def fill_repozitories(self):
        with open(self.path_to_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                repository_name = row[0]
                repository_handler = RepozitoryHandler(repository_name, self.username, self.token)
                self.repozitories.append(repository_handler)


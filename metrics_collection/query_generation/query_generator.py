import csv
import os
from string import Template


class QueryGenerator:
    def __init__(self):
        self.data = self.read_csv_file("files/metrics.csv")
        self.generate_queries()

    def read_csv_file(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        return data

    def generate_queries(self):
        for file_name in os.listdir('../text_queries'):
            file_path = os.path.join('../text_queries', file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Все запросы удалены")

        templates_path = "query_generation/templates/"
        for row in self.data:
            for i in range(1, 2):
                template_file = templates_path + f"template_{i}.txt"
                with open(template_file, 'r') as file:
                    template_content = file.read()
                    template = Template(template_content)
                    query = template.substitute(row)
                    rep_name = '_'.join(row['Repozitory_name'].split('/'))
                    file_name = f"../text_queries/{rep_name}_query_{i}.txt"
                    with open(file_name, 'w+') as file:
                        file.write(query)
                    print(f"Создан запрос {rep_name}_query_{i}.txt")


import ast
import csv

import javalang
import requests
from datetime import datetime

from pycparser import parse_file
from radon.complexity import cc_visit

from code_metrics import CodeMetrics


class RepozitoryHandler:
    def __init__(self, repozitory_name: str, username: str, token: str):
        self.average_cc_method = 0
        self.number_of_days_since_last_change = 0
        self.gh_session = requests.Session()
        self.gh_session.auth = (username, token)
        self.info = None
        self.total_lines = 0
        self.stars_count = 0
        self.trees = []
        self.count_of_contributors = 0
        self.forks_count = 0
        self.count_of_open_issues = 0
        self.count_of_closed_issue = 0
        self.count_of_merged_pull_requests = 0
        self.count_of_comment_lines = 0
        self.cyclomatic_complexity = 0
        self.count_of_commit_comment_lines = 0
        self.syntax_errors = 0
        self.total_cc = []
        self.api_link = 'https://api.github.com/repos/'
        self.repozitory_name = repozitory_name
        self.get_info_from_github_api()
        self.calculate_metrics()
        self.save_metrics()

    def save_metrics(self):
        with open('files/metrics.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.repozitory_name, self.total_lines,
                             self.number_of_days_since_last_change,
                             self.stars_count, self.count_of_contributors, self.forks_count,
                             self.count_of_open_issues, self.count_of_closed_issue,
                             self.count_of_merged_pull_requests,
                             self.count_of_comment_lines, self.cyclomatic_complexity,
                             self.count_of_commit_comment_lines, self.syntax_errors, self.average_cc_method
                             ])

    def calculate_metrics(self):
        if not self.info is None:
            self.number_of_days_since_last_change = self.get_number_of_days_since_last_change()
            print(
                f'repository = {self.repozitory_name}\t'
                f'number_of_days_since_last_change = {self.number_of_days_since_last_change}')
            self.stars_count = self.get_stars_count()
            print(f'repository = {self.repozitory_name}\tstars_count = {self.stars_count}')
            self.count_of_contributors = self.get_count_of_contributors()
            print(f'repository = {self.repozitory_name}\tcount_of_contributors = {self.count_of_contributors}')
            self.forks_count = self.get_forks_count()
            print(f'repository = {self.repozitory_name}\tforks_count = {self.forks_count}')
            self.count_of_open_issues = self.get_count_of_open_issues()
            print(f'repository = {self.repozitory_name}\tcount_of_open_issues = {self.count_of_open_issues}')
            self.count_of_closed_issue = self.get_count_of_closed_issues()
            print(f'repository = {self.repozitory_name}\tcount_of_closed_issue = {self.count_of_closed_issue}')
            self.count_of_merged_pull_requests = self.get_count_of_merged_pull_requests()
            print(
                f'repository = {self.repozitory_name}\t'
                f'count_of_merged_pull_requests = {self.count_of_merged_pull_requests}')

            self.get_cyclomatic_complexity(f"{self.api_link}{self.repozitory_name}/contents/")
            if len(self.total_cc) > 0:
                self.cyclomatic_complexity = sum(self.total_cc) / len(self.total_cc)
            print(f'repository = {self.repozitory_name}\tcyclomatic_complexity = {self.cyclomatic_complexity}')
            print(f'repository = {self.repozitory_name}\tcount_of_lines = {self.total_lines}')
            print(f'repository = {self.repozitory_name}\tcount_of_comment_lines = {self.count_of_comment_lines}')
            self.count_of_commit_comment_lines = self.get_count_of_commit_comment_lines()
            print(
                f'repository = {self.repozitory_name}\t'
                f'count_of_commit_comment_lines = {self.count_of_commit_comment_lines}')
            print(f'repository = {self.repozitory_name}\tsyntax_errors = {self.syntax_errors}')
            self.average_cc_method = self.calculate_average_cognitive_complexity()
            print(f'repository = {self.repozitory_name}\taverage Cognitive Complexity of a Method: {self.average_cc_method}')
            if len(self.trees) != 0:
                code_metrics = CodeMetrics(self.trees, self.repozitory_name)


    def get_info_from_github_api(self):
        result = self.gh_session.get(f'{self.api_link}{self.repozitory_name}')
        if result.status_code == 200:
            self.info = result.json()
        else:
            print('Невозможно получить данные репозитория')

    def get_number_of_days_since_last_change(self):
        last_update_date_str = self.info["updated_at"]
        last_update_date = datetime.strptime(last_update_date_str, "%Y-%m-%dT%H:%M:%SZ")
        today = datetime.now()
        days_since_last_update = (today - last_update_date).days
        return days_since_last_update

    def get_stars_count(self):
        return self.info['stargazers_count']

    def get_count_of_contributors(self):
        contributors_url = self.info["contributors_url"]
        contributors_info = self.gh_session.get(contributors_url).json()
        return len(contributors_info)

    def get_forks_count(self):
        return self.info["forks_count"]

    def get_count_of_open_issues(self):
        return self.info["open_issues_count"]

    def get_count_of_closed_issues(self):
        url = f"{self.api_link}{self.repozitory_name}/issues?state=closed"
        response = self.gh_session.get(url)
        if response.status_code == 200:
            data = response.json()
            closed_issues_count = len(data)
            return closed_issues_count
        else:
            return None

    def get_count_of_merged_pull_requests(self):
        url = f"{self.api_link}{self.repozitory_name}/pulls?state=closed&sort=updated&direction=desc"
        response = self.gh_session.get(url)

        if response.status_code == 200:
            data = response.json()
            merged_pull_requests_count = 0
            for pr in data:
                if pr["merged_at"] is not None:
                    merged_pull_requests_count += 1
            return merged_pull_requests_count
        else:
            print("Невозможно получить кодичество merged pull requests")
            return None

    def get_cyclomatic_complexity(self, url: str):
        response = self.gh_session.get(url)

        if response.status_code == 200:
            files = response.json()
            for file in files:
                if file['type'] == 'file' and file['name'].endswith('.java') or file['name'].endswith('.py') \
                        or file['name'].endswith('.c') or file['name'].endswith('.cs') \
                        or file['name'].endswith('.swift') or file['name'].endswith('.cpp'):
                    file_url = file['download_url']
                    file_response = self.gh_session.get(file_url)
                    if file_response.status_code == 200:
                        file_content = file_response.text

                        lines = file_content.split('\n')
                        self.total_lines += len(lines)
                        for line in lines:
                            if line.strip().startswith('#') or line.strip().startswith('//'):
                                self.count_of_comment_lines += 1
                        try:
                            if file['name'].endswith('.py'):
                                tree = ast.parse(file_content)
                                complexity = 1
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.If) or \
                                            isinstance(node, ast.For) or \
                                            isinstance(node, ast.While) or \
                                            isinstance(node, ast.With):
                                        complexity += 1
                                    elif isinstance(node, ast.Try) or isinstance(node, ast.ExceptHandler):
                                        complexity += 1
                                self.total_cc.append(complexity)
                            elif file['name'].endswith(('.c', '.cpp', '.cs', '.swift')):
                                ast_tree = parse_file(file_content)
                                self.total_cc.append(ast_tree.show(showcoord=False).count('Compound'))
                            elif file['name'].endswith('.java'):
                                tree = javalang.parse.parse(file_content)
                                self.trees.append(tree)
                                complexity = 1
                                for path, node in tree:
                                    if isinstance(node, javalang.tree.IfStatement):
                                        complexity += 1
                                    elif isinstance(node, javalang.tree.ForStatement):
                                        complexity += 1
                                self.total_cc.append(complexity)
                        except SyntaxError as exc:
                            self.syntax_errors += 1
                            print(f'Синтаксическая ошибка в файле:\n{file_url}')
                            print(f'Информация об ошибке: {type(exc)}\n{exc.args}')
                        except Exception as exc:
                            print(f'Невозможно посчитать cyclomatic complexity в файле:\n{file_url}')
                            print(f'Информация об ошибке: {type(exc)}\n{exc.args}')

                if file["type"] == 'dir':
                    self.get_cyclomatic_complexity(file['url'])

    def calculate_average_cognitive_complexity(self):
        total_methods = 0
        total_cc_methods = 0

        for file_cc in self.total_cc:
            total_methods += 1
            total_cc_methods += file_cc

        if total_methods > 0:
            average_cc_method = total_cc_methods / total_methods
            return average_cc_method
        else:
            return 0

    def get_count_of_commit_comment_lines(self):
        url = f"{self.api_link}{self.repozitory_name}/commits"
        response = self.gh_session.get(url)
        if response.status_code == 200:
            commits = response.json()

            total_comment_lines = 0

            for commit in commits:
                comment_lines = commit['commit']['message'].count('\n') + 1
                total_comment_lines += comment_lines

            return total_comment_lines
        print("Невозможно получить количество строк в комментариях к коммитам")
        return None

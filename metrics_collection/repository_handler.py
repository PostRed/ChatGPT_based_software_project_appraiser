import requests
from datetime import datetime
from radon.complexity import cc_visit


class RepozitoryHandler:
    def __init__(self, repozitory_name: str, username: str, token: str):
        self.number_of_days_since_last_change = 0
        self.gh_session = requests.Session()
        self.gh_session.auth = (username, token)
        self.info = None
        self.total_lines = 0
        self.stars_count = 0
        self.count_of_contributors = 0
        self.forks_count = 0
        self.count_of_open_issues = 0
        self.count_of_closed_issue = 0
        self.count_of_merged_pull_requests = 0
        self.count_of_comment_lines = 0
        self.cyclomatic_complexity = 0
        self.count_of_commit_comment_lines = 0
        self.total_cc = 0
        self.total_methods = 0
        self.api_link = 'https://api.github.com/repos/'
        self.repozitory_name = repozitory_name
        self.get_info_from_github_api()
        self.calculate_metrics()

    def calculate_metrics(self):
        if not self.info is None:
            self.get_count_of_lines(f'{self.api_link}{self.repozitory_name}/contents')
            print(f'repository = {self.repozitory_name}\tcount_of_lines = {self.total_lines}')
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
            self.get_count_of_comment_lines(f"{self.api_link}{self.repozitory_name}/contents/")
            print(f'repository = {self.repozitory_name}\tcount_of_comment_lines = {self.count_of_comment_lines}')
            self.get_cyclomatic_complexity(f"{self.api_link}{self.repozitory_name}/contents/")
            self.cyclomatic_complexity = self.total_cc / self.total_methods
            print(f'repository = {self.repozitory_name}\tcyclomatic_complexity = {self.cyclomatic_complexity}')
            self.count_of_commit_comment_lines = self.get_count_of_commit_comment_lines()
            print(
                f'repository = {self.repozitory_name}\t'
                f'count_of_commit_comment_lines = {self.count_of_commit_comment_lines}')


    def get_info_from_github_api(self):
        result = self.gh_session.get(f'{self.api_link}{self.repozitory_name}')
        if result.status_code == 200:
            self.info = result.json()
        else:
            print('Невозможно получить данные репозитория')

    def get_count_of_lines(self, url: str):
        response = self.gh_session.get(url)
        if response.status_code == 200:
            data = response.json()
            for file_data in data:
                if file_data["type"] == "file":
                    file_url = file_data["download_url"]
                    file_response = self.gh_session.get(file_url)
                    if file_response.status_code == 200:
                        file_content = file_response.text
                        self.total_lines += len(file_content.split("\n"))
                if file_data["type"] == 'dir':
                    self.get_count_of_lines(file_data['url'])
        else:
            print("Невозможно получить количество строк")

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

    def get_count_of_comment_lines(self, url: str):
        response = self.gh_session.get(url)

        if response.status_code == 200:
            files = response.json()
            for file in files:
                if file['type'] == 'file':
                    file_url = file['download_url']
                    file_response = self.gh_session.get(file_url)

                    if file_response.status_code == 200:
                        lines = file_response.text.split('\n')
                        for line in lines:
                            if line.strip().startswith('#') or line.strip().startswith('//'):
                                self.count_of_comment_lines += 1
                if file["type"] == 'dir':
                    self.get_count_of_comment_lines(file['url'])
        else:
            print('Невозможно получить количество строк в комментария')

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
                        try:
                            blocks = cc_visit(file_content)
                            for block in blocks:
                                self.total_cc += block.complexity
                                self.total_methods += 1
                        except Exception:
                            print('Невозможно посчитать cyclomatic complexity')
                if file["type"] == 'dir':
                    self.get_cyclomatic_complexity(file['url'])

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

import requests
from datetime import datetime

class RepozitoryHandler:
    def __init__(self, repozitory_name: str, login: str, password: str):
        self.auth = (login, password)
        self.info = None
        self.total_lines = 0
        self.api_link = 'https://api.github.com/repos/'
        self.repozitory_name = repozitory_name
        self.get_info_from_github_api()
        self.calculate_metrics()

    def calculate_metrics(self):
        self.get_count_of_lines(f'{self.api_link}{self.repozitory_name}')
        number_of_days_since_last_change = self.get_number_of_days_since_last_change()
        stars_count = self.get_stars_count()
        count_of_contributors = self.get_count_of_contributors()
        forks_count = self.get_forks_count()
        count_of_open_issues = self.get_count_of_open_issues()
        count_of_closed_issue = self.get_count_of_closed_issues()
        count_of_merged_pull_requests = self.get_count_of_merged_pull_requests()

        # count_of_comment_lines = self.get_count_of_comment_lines()
        # cyclomatic_complexity = self.get_cyclomatic_complexity()
        # count_of_commit_comment_lines = self.get_count_of_commit_comment_lines()
        print(self.total_lines)
        # print(number_of_days_since_last_change, stars_count, count_of_contributors, forks_count, count_of_open_issues, count_of_closed_issue, count_of_merged_pull_requests)

    def get_info_from_github_api(self):
        result = requests.get(f'{self.api_link}{self.repozitory_name}', auth=self.auth)
        print(result.text)
        self.info = result.json()


    # def get_contents_of_dir(self, url: str):
    #     response = requests.get(url, auth=self.auth)

    def get_count_of_lines(self, old_url: str):
        url = f"{old_url}/contents"
        response = requests.get(url, auth=self.auth)
        print(url, response)
        if response.status_code == 200:
            data = response.json()
            for file_data in data:
                if file_data["type"] == "file":
                    print(file_data["name"])
                    file_url = file_data["download_url"]
                    file_response = requests.get(file_url, auth=self.auth)
                    if file_response.status_code == 200:
                        file_content = file_response.text
                        self.total_lines += len(file_content.split("\n"))
                if file_data["type"] == 'dir':
                    print(file_data)
                    new_url = file_data['html_url']
                    new_url_list = new_url.split('/')[3:]
                    new_url = f'{self.api_link}{"/".join(new_url_list)}'
                    print(new_url)
                    self.get_count_of_lines(new_url)



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
        contributors_info = requests.get(contributors_url, auth=self.auth).json()
        return len(contributors_info)

    def get_forks_count(self):
        return self.info["forks_count"]

    def get_count_of_open_issues(self):
        return self.info["open_issues_count"]

    def get_count_of_closed_issues(self):
        url = f"{self.api_link}{self.repozitory_name}/issues?state=closed"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            data = response.json()
            closed_issues_count = len(data)
            return closed_issues_count
        else:
            return None

    def get_count_of_merged_pull_requests(self):
        url = f"https://api.github.com/repos/{self.repozitory_name}/pulls?state=closed&sort=updated&direction=desc"
        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            data = response.json()
            merged_pull_requests_count = 0
            for pr in data:
                if pr["merged_at"] is not None:
                    merged_pull_requests_count += 1
            return merged_pull_requests_count
        else:
            return None


    def get_count_of_comment_lines(self):
        pass

    def get_cyclomatic_complexity(self):
        pass

    def get_count_of_commit_comment_lines(self):
        pass

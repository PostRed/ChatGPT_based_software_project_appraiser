import csv

from metrics_collection.repository_handler import RepozitoryHandler


class MetricsSaver:
    def __init__(self, repositories: [RepozitoryHandler]):
        self.repositories = repositories

    def save_metrics_file(self):
        with open('metrics.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Repozitory_name', 'total_lines', 'number_of_days_since_last_change', 'stars_count',
                             'count_of_contributors', 'forks_count',
                             'count_of_open_issues', 'count_of_closed_issue', 'count_of_merged_pull_requests',
                             'count_of_comment_lines',
                             'cyclomatic_complexity', 'count_of_commit_comment_lines', 'total_cc', 'total_methods'])

            for repo_handler in self.repositories:
                writer.writerow([repo_handler.repozitory_name, repo_handler.total_lines,
                                 repo_handler.number_of_days_since_last_change,
                                 repo_handler.stars_count, repo_handler.count_of_contributors, repo_handler.forks_count,
                                 repo_handler.count_of_open_issues, repo_handler.count_of_closed_issue,
                                 repo_handler.count_of_merged_pull_requests,
                                 repo_handler.count_of_comment_lines, repo_handler.cyclomatic_complexity,
                                 repo_handler.count_of_commit_comment_lines,
                                 repo_handler.total_cc, repo_handler.total_methods])



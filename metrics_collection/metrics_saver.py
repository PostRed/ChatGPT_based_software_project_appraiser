import csv

from metrics_collection.repository_handler import RepozitoryHandler


class MetricsSaver:
    def __init__(self):
        self.files_name = os.getcwd() + '/metrics_collection/files/metrics.csv'
        with open(os.getcwd() + '/metrics_collection/files/metrics.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Repozitory_name', 'total_lines', 'number_of_days_since_last_change', 'stars_count',
                             'count_of_contributors', 'forks_count',
                             'count_of_open_issues', 'count_of_closed_issue', 'count_of_merged_pull_requests',
                             'count_of_comment_lines',
                             'cyclomatic_complexity', 'count_of_commit_comment_lines', 'syntax_errors'])

    def save_metrics_file(self, repository: RepozitoryHandler):
        with open(self.files_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([repository.repozitory_name, repository.total_lines,
                             repository.number_of_days_since_last_change,
                             repository.stars_count, repository.count_of_contributors, repository.forks_count,
                             repository.count_of_open_issues, repository.count_of_closed_issue,
                             repository.count_of_merged_pull_requests,
                             repository.count_of_comment_lines, repository.cyclomatic_complexity,
                             repository.count_of_commit_comment_lines, repository.syntax_errors
                             ])



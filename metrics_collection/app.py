import csv

from metrics_collection.repository_handler_for_file import RepozitoryHandlerForFile
from repository_handler import RepozitoryHandler
from query_generation.query_generator import QueryGenerator
import argparse


if __name__ == '__main__':
    with open('files/metrics.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Repozitory_name', 'total_lines', 'number_of_days_since_last_change', 'stars_count',
                         'count_of_contributors', 'forks_count',
                         'count_of_open_issues', 'count_of_closed_issue', 'count_of_merged_pull_requests',
                         'count_of_comment_lines',
                         'cyclomatic_complexity', 'count_of_commit_comment_lines', 'syntax_errors'])

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--count_metrics_file', type=str, help='Укажите путь к файлу для подсчета метрик.')
    parser.add_argument('--count_metrics_rep', type=str, help='Укажите имя репозитория для подсчета метрик.')
    parser.add_argument('--token', type=str, help='Токен для доступа к репозиторию.', required=False)
    parser.add_argument('--username', type=str, help='Имя пользователя для доступа к репозиторию.', required=False)
    args = parser.parse_args()
    args.count_metrics_file = '/Users/anastasiakolomnikova/Documents/GitHub/ChatGPT_based_software_project_appraiser/repositories_test.csv'
    args.username = 'PostRed'
    args.token = ''
    repositories = []
    if args.count_metrics_file:
        repozitory_handler_for_file = RepozitoryHandlerForFile(args.count_metrics_file, args.username, args.token)
        repositories = repozitory_handler_for_file.repozitories
    elif args.count_metrics_rep:
        repositories = [RepozitoryHandler(args.count_metrics_rep, args.username, args.token)]
    QueryGenerator()


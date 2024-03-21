import csv

from repository_handler_for_file import RepozitoryHandlerForFile
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
                         'cyclomatic_complexity', 'count_of_commit_comment_lines', 'syntax_errors', 'average_cc_method'])

    with open('files/java_metrics.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Repozitory_name', 'min_nooa', 'max_nooa', 'aver_nooa',
                            'min_nosa', 'max_nosa', 'aver_nosa',
                            'min_nocc', 'max_nocc', 'aver_nocc',
                            'min_noom', 'max_noom', 'aver_noom',
                            'min_nocm', 'max_nocm', 'aver_nocm',
                            'min_ncss', 'max_ncss', 'aver_ncss',
                            'min_noii', 'max_noii', 'aver_noii',
                            'min_napc', 'max_napc', 'aver_napc',
                            'min_notp', 'max_notp', 'aver_notp',
                            'min_final', 'max_final', 'aver_final',
                            'min_noca', 'max_noca', 'aver_noca',
                            'min_varcomp', 'max_varcomp', 'aver_varcomp',
                            'min_mhf', 'max_mhf', 'aver_mhf',
                            'min_smhf', 'max_smhf', 'aver_smhf',
                            'min_ahf', 'max_ahf', 'aver_ahf',
                            'min_sahf', 'max_sahf', 'aver_sahf',
                            'min_nomp', 'max_nomp', 'aver_nomp',
                            'min_nosmp', 'max_nosmp', 'aver_nosmp',
                            'min_mxnomp', 'max_mxnomp', 'aver_mxnomp',
                            'min_mxnosmp', 'max_mxnosmp', 'aver_mxnosmp',
                            'min_nom', 'max_nom', 'aver_nom',
                            'min_nop', 'max_nop', 'aver_nop',
                            'min_nulls', 'max_nulls', 'aver_nulls',
                            'min_doer', 'max_doer', 'aver_doer'])

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--count_metrics_file', type=str, help='Укажите путь к файлу для подсчета метрик.')
    parser.add_argument('--count_metrics_rep', type=str, help='Укажите имя репозитория для подсчета метрик.')
    parser.add_argument('--token', type=str, help='Токен для доступа к репозиторию.', required=False)
    parser.add_argument('--username', type=str, help='Имя пользователя для доступа к репозиторию.', required=False)
    args = parser.parse_args()
    repositories = []
    if args.count_metrics_file:
        repozitory_handler_for_file = RepozitoryHandlerForFile(args.count_metrics_file, args.username, args.token)
        repositories = repozitory_handler_for_file.repozitories
    elif args.count_metrics_rep:
        repositories = [RepozitoryHandler(args.count_metrics_rep, args.username, args.token)]
    QueryGenerator("files/metrics.csv")
    QueryGenerator("files/java_metrics.csv")


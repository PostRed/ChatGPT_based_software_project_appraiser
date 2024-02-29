from metrics_collection.metrics_saver import MetricsSaver
from metrics_collection.repository_handler_for_file import RepozitoryHandlerForFile
from repository_handler import RepozitoryHandler
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--count_matrics_file', type=str, help='Укажите путь к файлу для подсчета метрик.')
    parser.add_argument('--count_metrics_rep', type=str, help='Укажите имя репозитория для подсчета метрик.')
    parser.add_argument('--token', type=str, help='Токен для доступа к репозиторию.', required=False)
    parser.add_argument('--username', type=str, help='Имя пользователя для доступа к репозиторию.', required=False)
    args = parser.parse_args()
    args.count_metrics_rep = 'PostRed/TINCOFF'
    args.username = 'PostRed'
    args.token = ''
    repositories = []
    if args.count_matrics_file:
        repozitory_handler_for_file = RepozitoryHandlerForFile(args.count_matrics_file, args.username, args.token)
        repositories = repozitory_handler_for_file.repozitories
    elif args.count_metrics_rep:
        repositories = [RepozitoryHandler(args.count_metrics_rep, args.username, args.token)]
    metrics_saver = MetricsSaver(repositories)
    metrics_saver.save_metrics_file()


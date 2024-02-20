from repository_handler import RepozitoryHandler
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--count_matrics_file', type=str, help='Укажите путь к файлу для подсчета метрик.')
    parser.add_argument('--count_metrics_rep', type=str, help='Укажите имя репозитория для подсчета метрик.')
    parser.add_argument('--token', type=str, help='Токен для доступа к репозиторию.', required=True)
    parser.add_argument('--username', type=str, help='Имя пользователя для доступа к репозиторию.', required=True)
    args = parser.parse_args()
    # args.count_metrics_rep = 'JimiSmith/PinnedHeaderListView'
    # args.username = 'PostRed'
    # args.token = ''
    if args.count_matrics_file:
        pass
    elif args.count_metrics_rep:
        RepozitoryHandler(args.count_metrics_rep, args.username, args.token)


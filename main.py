import csv

import xmltodict
import json
import os
import subprocess

from GptAppraiser.GptAppraiser import GptAppraiser

def readConfrg():
    with open('settings.conf') as settings:
        config = xmltodict.parse(settings.read())['Config']
    if 'GptAppraiserSettings' not in config or 'MetricsCollectionSettings'not in config:
        print("GptAppraiserSettings или MetricsCollectionSettings не описаны в конфигурационном файле.")
        return None

    for tag in ['x_folder_id', 'Api_Key', 'resending']:
        if tag not in config['GptAppraiserSettings']:
            print("x_folder_id или Api_Key не описаны в конфигурационном файле.")
            return None

    for tag in ['token', 'username']:
        if tag not in config['MetricsCollectionSettings']:
            print("token или username не описаны в конфигурационном файле.")
            return None
    if (('count_metrics_rep' not in config['MetricsCollectionSettings'] or not config['MetricsCollectionSettings']['count_metrics_rep'])
        and ('count_metrics_file' not in config['MetricsCollectionSettings'] or not config['MetricsCollectionSettings']['count_metrics_file'])):
        print("count_metrics_rep или count_metrics_file должны быть описаны в конфигурационном файле.")
        return None

    return config


def main():
    config = readConfrg()

    if not config:
        return

    if config['MetricsCollectionSettings']['count_metrics_rep']:
        count_metrics = f"--count_metrics_rep {config['MetricsCollectionSettings']['count_metrics_rep']}"
    else:
        count_metrics = f"--count_metrics_file {config['MetricsCollectionSettings']['count_metrics_file']}"
    command = f"python metrics_collection/app.py {count_metrics} --token {config['MetricsCollectionSettings']['token']} --username {config['MetricsCollectionSettings']['username']}"

    process = subprocess.Popen(command, shell=True)
    process.wait()
    gpt_appraiser = GptAppraiser(config)
    with open(os.getcwd() + '/result.csv', mode='w', newline='') as file:
        print(file)
        writer = csv.writer(file)
        writer.writerow(['Repozitory_name', 'Quality_control'])
        for filename in os.listdir('text_queries/'):
            if filename == 'examples':
                continue

            predict_list = gpt_appraiser.predict(filename)
            if len(predict_list) == 0:
                print('Ошибка отправки запроса')
            else:
                ind = filename.find('_query')
                filename = filename[:ind]
                filename = filename.replace('_', '/')
                res = sum(predict_list) / len(predict_list)
                print(f'Оценка для {filename} ChatGPT:')
                print(res)
                writer.writerow([filename, res])


if __name__ == '__main__':
    main()

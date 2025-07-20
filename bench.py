import argparse
import requests
import time
import re
import sys


def testing(host, count, data_file):
    response_times = []
    success = 0
    failed = 0
    errors = 0
    minimum = 0
    maximum = 0
    average = 0

    for i in range(count):
        try:
            start_time = time.time()
            response = requests.get(host)
            response_times.append(time.time() - start_time)

            if 200 <= response.status_code < 300:
                success += 1
            else:
                failed += 1

        except requests.exceptions.RequestException as error:
            errors += 1
            print(f'В запросе на хост {host} произошла ошибка:\n{error}\n', file=data_file)

    if response_times:
        minimum = min(response_times)
        maximum = max(response_times)
        average = sum(response_times)/len(response_times)

    print(f'ВЫВОД ДЛЯ ХОСТА: {host}', file=data_file)
    print(f'Success: {success}', file=data_file)
    print(f'Failed: {failed}', file=data_file)
    print(f'Errors: {errors}', file=data_file)
    print(f'Min time: {minimum}', file=data_file)
    print(f'Max time: {maximum}', file=data_file)
    print(f'Avg time: {average}\n', file=data_file)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', '--hosts')
    group.add_argument('-F', '--file')
    parser.add_argument('-C', '--count', type=int, default=1)
    parser.add_argument('-O', '--output')
    arguments = parser.parse_args()

    hosts = []
    expression = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

    if arguments.output:
        data_file = open(arguments.output, 'w', encoding='utf-8')
    else:
        data_file = sys.stdout

    if arguments.hosts:
        hosts_list = arguments.hosts.split(',')
    else:
        try:
            with open(arguments.file, 'r', encoding='utf-8') as f:
                hosts_list = f.readlines()
        except FileNotFoundError:
            print(f'{arguments.file} не найден')
            return

    for host in hosts_list:
        host = host.strip()
        if re.match(expression, host) is None:
            print(f'Хост {host} имеет неверный формат', file=data_file)
        else:
            hosts.append(host)

    if not hosts:
        return

    for host in hosts:
        testing(host, arguments.count, data_file)

    if arguments.output:
        data_file.close()


if __name__ == '__main__':
    main()

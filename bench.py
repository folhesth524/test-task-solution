import argparse
import requests
import time
import re
import sys
from concurrent.futures import ThreadPoolExecutor

def making_request(host):
    try:
        start = time.perf_counter()
        response = requests.get(host, timeout=10)
        duration = time.perf_counter() - start

        if 200 <= response.status_code < 300:
            return host, 'success', duration
        elif 400 <= response.status_code < 600:
            return host, 'failed', duration
        else:
            return host, 'other', duration

    except requests.exceptions.RequestException:
        return host, 'error', 0

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', '--hosts')
    group.add_argument('-F', '--file')
    parser.add_argument('-C', '--count', type=int, default=1)
    parser.add_argument('-O', '--output')
    args = parser.parse_args()

    if args.hosts:
        user_hosts = args.hosts.split(',')
    else:
        user_hosts = []

    if args.file:
        try:
            with open(args.file, 'r') as f:
                user_hosts = []
                for line in f:
                    if line.strip():
                        user_hosts.append(line.strip())
        except FileNotFoundError:
            print(f'Ваш файл {args.file} не найден')
            return

    if args.output:
        output_stream = open(args.output, 'w', encoding='utf-8')
    else:
        output_stream = sys.stdout

    total_hosts = []
    for x in user_hosts:
        if re.match(r'^https?://(?:[-\w.]|%[\da-fA-F]{2})+', x):
            total_hosts.append(x)
        else:
            print('-' * 20, file=output_stream)
            print(f'Хост {x} имеет неверный формат', file=output_stream)

    if not total_hosts:
        print('Не найдено ни одного корректного хоста для проверки')
        if args.output:
            output_stream.close()
        return

    all_requests = []
    for x in total_hosts:
        for i in range(args.count):
            all_requests.append(x)

    results = []
    with ThreadPoolExecutor(max_workers=25) as executor:
        for x in executor.map(making_request, all_requests):
            results.append(x)

    values = {}
    for host, status, duration in results:
        if host not in values:
            values[host] = {
                'times': [],
                'success': 0,
                'failed': 0,
                'errors': 0
            }

        if status == 'success':
            values[host]['success'] += 1
            values[host]['times'].append(duration)
        elif status == 'failed':
            values[host]['failed'] += 1
            values[host]['times'].append(duration)
        elif status == 'error':
            values[host]['errors'] += 1

    for host, data in values.items():
        times = data['times']

        if times:
            Min = min(times)
            Max = max(times)
            Avg = sum(times) / len(times)
        else:
            Min = Max = Avg = 0

        print('-' * 20, file=output_stream)
        print(f'Host:    {host}', file=output_stream)
        print(f'Success: {data['success']}', file=output_stream)
        print(f'Failed:  {data['failed']}', file=output_stream)
        print(f'Errors:  {data['errors']}', file=output_stream)
        print(f'Min:     {Min:.5f}s', file=output_stream)
        print(f'Max:     {Max:.5f}s', file=output_stream)
        print(f'Avg:     {Avg:.5f}s\n', file=output_stream)

    if args.output:
        output_stream.close()
        print(f'Результаты записаны в файл {args.output}')

if __name__ == '__main__':
    main()

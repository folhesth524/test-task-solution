# Тестирование доступности серверов

**Ссылка на репозиторий в GitHub:** [https://github.com/folhesth524/test-task-solution.git](https://github.com/folhesth524/test-task-solution.git)

Была реализована консольная программа для тестирования доступности серверов по HTTP протоколу.
Программа замеряет время выполнения запроса и выводит итоговую статистику по скорости ответа сервера, используя для этого потоки.

Также были выполнены дополнительные задания и задание с повышенной сложностью, используя потоки.

### Состав проекта:
* **bench.py** — код решения тестового задания;
* **hosts.txt** — список адресов для проверки;
* **data.txt** — результаты работы программы;
* **requirements.txt** — библиотека, которую необходимо установить для работы.

---

### ПРИМЕРЫ РАБОТЫ ПРОГРАММЫ
Для запуска программы необходимо установить библиотеку `requests` и вводить команды:
---

### ПРИМЕР #1
**Команда** — Проверка доступности двух хостов с 5 запросами:
```bash
python bench.py -H https://ya.ru,https://google.com -C 5
```
Результат вывода:
```bash
--------------------
Host:    https://ya.ru
Success: 5
Failed:  0
Errors:  0
Min:     0.16302s
Max:     0.38436s
Avg:     0.28519s

--------------------
Host:    https://google.com
Success: 5
Failed:  0
Errors:  0
Min:     0.31231s
Max:     0.33191s
Avg:     0.32131s
```
### ПРИМЕР #2
**Команда** - Один из переданных хостов содержит ошибку в формате:
```bash
python bench.py -H https://ya.ru,htttps://google.com -C 5
```
Результат вывода:
```bash
--------------------
Хост htttps://google.com имеет неверный формат
--------------------
Host:    https://ya.ru
Success: 5
Failed:  0
Errors:  0
Min:     0.17984s
Max:     0.35563s
Avg:     0.26562s
```
### ПРИМЕР #3
**Команда** - Проверка одного хоста:
```bash
python bench.py -H https://google.com
```
Результат вывода:
```bash
--------------------
Host:    https://google.com
Success: 1
Failed:  0
Errors:  0
Min:     0.35031s
Max:     0.35031s
Avg:     0.35031s
```
### ПРИМЕР #4
**Команда** - Загрузка списка хостов из файла:
```bash
python bench.py -F hosts.txt -C 5
```
Результат вывода:
```bash
--------------------
Host:    https://ya.ru
Success: 5
Failed:  0
Errors:  0
Min:     0.15602s
Max:     0.20914s
Avg:     0.16959s

--------------------
Host:    https://google.com
Success: 5
Failed:  0
Errors:  0
Min:     0.32256s
Max:     0.33822s
Avg:     0.33156s
```
### ПРИМЕР #5
**Команда** - Попытка загрузить хосты из несуществующего файла:
```bash
python bench.py -F aaa.txt
```
Результат вывода:
```bash
Ваш файл aaa.txt не найден
```
### ПРИМЕР #6
**Команда** - Запись результата в файл data.txt:
```bash
python bench.py -H https://ya.ru,https://google.com -C 5 -O data.txt
```
Появилось уведомление в консоли:
```bash
Результаты записаны в файл data.txt
```
А в файл data.txt был записан вывод работы:
```bash
--------------------
Host:    https://ya.ru
Success: 5
Failed:  0
Errors:  0
Min:     0.14404s
Max:     0.19425s
Avg:     0.16017s

--------------------
Host:    https://google.com
Success: 5
Failed:  0
Errors:  0
Min:     0.31742s
Max:     0.41899s
Avg:     0.34816s
```
### ПРИМЕР #7
**Команда** - Загрузка списка хостов из файла, но файл пуст:
```bash
python bench.py -F hosts.txt -C 5
```
Результат - Уведомление в консоль:
```bash
Не найдено ни одного корректного хоста для проверки
```

### ПРИМЕР #8
**Команда** - Проверка несуществующего хоста:
```bash
python bench.py -H https://hellohello2343533.com -C 5
```
Результат вывода:
```bash
--------------------
Host:    https://hellohello2343533.com
Success: 0
Failed:  0
Errors:  5
Min:     0.00000s
Max:     0.00000s
Avg:     0.00000s
```
### ПРИМЕР #9
**Команда** - Проверка хоста, но путь неверный:
```bash
python bench.py -H https://google.com/hello -C 5
```
Результат вывода:
```bash
--------------------
Host:    https://google.com/hello
Success: 0
Failed:  5
Errors:  0
Min:     0.23700s
Max:     0.27292s
Avg:     0.25638s
```
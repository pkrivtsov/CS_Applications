# ------------------------------------1-----------------------------------------------

my_dict = {'разработка': '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
           'сокет': '\u0441\u043e\u043a\u0435\u0442',
           'декоратор': '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'}
for i, v in my_dict.items():
    print(i, type(i), v, type(v))

# ------------------------------------2------------------------------------------------

my_list = ['class', 'function', 'method']
for i in my_list:
    print(f"{bytes(i, 'utf-8')}, Тип: {type(bytes(i, 'utf-8'))}, Длина: {len(bytes(i, 'utf-8'))}")

# ------------------------------------3------------------------------------------------

my_list = ['attribute', 'класс', 'функция', 'type']
for i in my_list:
    print(i.encode('utf-8'))

# ------------------------------------4------------------------------------------------

my_list = ['разработка', 'администрирование', 'protocol', 'standard']
b_list = [i.encode('utf-8') for i in my_list]
str_list = [i.decode('utf-8') for i in b_list]
print(f'{b_list}\n{str_list}')

# ------------------------------------5------------------------------------------------

import subprocess

args = ['ping', 'google.com']
subprocess_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subprocess_ping.stdout:
    print(line.decode('utf-8', 'ignore'))

# ------------------------------------6------------------------------------------------

my_list = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w') as w_t:
    for i in my_list:
        w_t.write(f'{i}\n')

with open("test_file.txt") as r_t:
    print (r_t.read().encode('utf-8', 'ignore'))


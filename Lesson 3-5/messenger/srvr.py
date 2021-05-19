# Сервер для получения json от клиента и отправки ответа по протоколу JIM
from socket import socket, AF_INET, SOCK_STREAM
import argparse
import pickle
import time
import sys

import logging
import log.srvr_log_config


# https://jenyay.net/Programming/Argparse
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default='7777')
    parser.add_argument('-a', '--addr', default='0.0.0.0')
    parser.error = myerror

    return parser


def myerror(message):
    log = logging.getLogger()
    log.error(f'Применен недопустимый аргумент {message}')


def checking_data(message):
    if len(message) > 640:  # проверка длины пакета
        return {
            'response': 400,
            'time': time.ctime(),
            'error': 'Длинна объекта больше 640 символов',
        }  # неправильный запрос/JSON-объект;

    dict_of_commands = {
        'authenticate': authenticate,
        'presence': presence,
        'msg': msg,
        'quit': quit_s,  # т.к. в python есть ф-я quit - определил для ф-и
        'join': join,
        'leave': leave,
        'crate': create,
    }
    data = pickle.loads(message)
    action = data['action']
    if action not in dict_of_commands:
        return {'response': 404, 'time': time.ctime(), 'error': 'Неизвестная команда'}
    processing_the_action = dict_of_commands[action]  # находим в словаре
    return processing_the_action(**data)  # выполняем нужную функцию


authorized_users = []
chat_rooms = {}


def authenticate(*kwargs):  # пароль не запрашивается
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        return {
            'response': 409,
            'time': time.ctime(),
            'alert': f'Уже имеется подключение с указанным логином {user_name}'
        }
    authorized_users.append(user_name)
    return {'response': 200, 'time': time.ctime(), 'alert': f'Пользователь {user_name} аут-н'}


def presence(**kwargs):
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        return {
            'response': 200,
            'time': time.ctime(),
            'alert': f'Хорошо, {user_name} присутствует в списке подключенных'
        }
    return {'response': 404, 'time': time.ctime(), 'error': f'Пользователь {user_name} не авторизован'}


def msg(**kwargs):
    from_user = kwargs['from']
    to_user = kwargs['to']
    if from_user not in authorized_users:
        return {'response': 401, 'time': time.ctime(), 'error': f'Пользователь {from_user} не авторизован'}

    if to_user[0] == '#':
        chat = to_user[1:]
        if chat not in chat_rooms:
            return {'response': 404, 'time': time.ctime(), 'error': f'Чат {chat} не найден'}
        return {
            'response': 200,
            'time': time.time(),
            'alert': f'Сообщение от {from_user} успешно доставлено в чат {chat_rooms}',
        }
    if to_user not in authorized_users:
        return {'response': 404, 'time': time.ctime(), 'alert': f'Пользователь {to_user} не авторизован'}
    return {'response': 200, 'time': time.ctime(),
            'alert': f'Сообщение от пользователь {from_user} доставлено {to_user}'}


def quit_s(**kwargs):
    user_name = kwargs['user']['account_name']
    if user_name in authorized_users:
        authorized_users.remove(user_name)
        return {'response': 200, 'time': time.ctime(), 'alert': 'Пользователь {user_name} успешно вышел'}
    return {'response': 404, 'time': time.ctime(), 'error': 'Пользователь {user_name} не найден'}


def join(**kwargs):
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        return {'response': 404, 'time': time.ctime(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        if user not in chat_rooms[chat_name]:
            chat_rooms[chat_name].append(user)
            return {
                'response': 200,
                'time': time.ctime(),
                'alert': f'Пользователь {user} длбавлен в {chat_name}',
            }
        return {
            'response': 409,
            'time': time.ctime(),
            'alert': f'Пользователь {user} уже присутствует в чате {chat_name}',
        }
    return {
        'response': 409,
        'time': time.ctime(),
        'alert': f'Чат {chat_name} пока не создан',
    }


def leave(**kwargs):
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        return {'response': 404, 'time': time.ctime(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        if user in chat_rooms[chat_name]:
            chat_rooms[chat_name].remove(user)
            return {
                'response': 200,
                'time': time.ctime(),
                'alert': f'Пользователь {user} удален из {chat_name}',
            }
        return {
            'response': 409,
            'time': time.ctime(),
            'alert': f'Пользователя {user} нет в чате {chat_name}',
        }
    return {
        'response': 409,
        'time': time.ctime(),
        'alert': f'Чат {chat_name} пока не создан',
    }


def create(**kwargs):
    chat_name = kwargs['chat_name']
    user = kwargs['from']
    if user not in authorized_users:
        return {'response': 404, 'time': time.ctime(), 'error': f'Пользователь {user} не авторизован'}
    if chat_name in chat_rooms:
        return {
            'response': 409,
            'time': time.ctime(),
            'alert': f'уже имеется чат с указанным названием {chat_name}',
        }
    chat_rooms[chat_name] = [user]  # создает чат и список его участников
    return {'response': 200, 'time': time.ctime(), 'alert': f'Чат {chat_name}'}


if __name__ == '__main__':
    log = logging.getLogger()
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((namespace.addr, int(namespace.port)))
    s.listen(5)

    while True:
        client, addr = s.accept()
        message = client.recv(1024)
        print('Сообщение:', pickle.loads(message), ', было отправлено клиентом')
        response = checking_data(message)
        client.send(pickle.dumps(response))
        client.close()


""" 
команды quit, presence, authenticate, принимают словарь со вложенным словарем:
{"action": "authenticate",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "DЭ6ug_M@$ter",
        "password": "C0rrЭc+P@$$w0rd"
    }
}
остальные команды используют:
msg = {"action": "msg",
    "time": time.time(),
    "to": "DЭ6ug_M@$ter",
    "from": "user_1",
    "encoding": "ascii",
    "message": "message"
}
"""
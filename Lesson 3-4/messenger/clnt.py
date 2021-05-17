# Клиент для отправки JSON серверу и получения ответа по протоколу JIM
import argparse
import pickle
import time
import sys
from socket import socket, AF_INET, SOCK_STREAM


# https://jenyay.net/Programming/Argparse
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default='7777')
    parser.add_argument('-a', '--addr', default='localhost')

    return parser


def myerror(message):
    print(f'Применен недопустимый аргумент {message}')


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((namespace.addr, int(namespace.port)))
    msg = {"action": "presence",
           "time": time.time(),
           "type": "status",
           "user": {
               "account_name": "DЭ6ug_M@$ter",
               "status": "Yep, I am here!"
           }
    }
    s.send(pickle.dumps(msg))
    data = s.recv(1024)
    print(f'Сообщение от сервера: {pickle.loads(data)}, длинной {len(data)} байт')
    s.close()

"""
msg = {"action": "authenticate",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "DЭ6ug_M@$ter",
        "password": "C0rrЭc+P@$$w0rd"
    }
}

msg = {"action": "quit",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "DЭ6ug_M@$ter",
        "status": "Yep, I am here!"
    }
}

msg = {"action": "presence",
    "time": time.time(),
    "type": "status",
    "user": {
        "account_name": "DЭ6ug_M@$ter",
        "status": "Yep, I am here!"
    }
}

msg = {"action": "msg",
    "time": time.time(),
    "to": "DЭ6ug_M@$ter",
    "from": "user_1",
    "encoding": "ascii",
    "message": "message"
}

msg = {"action": "create",
    "time": time.time(),
    "from": "DЭ6ug_M@$ter",
    "chat_name": "my_chat"
}

msg = {"action": "join",
    "time": time.time(),
    "from": "user_1",
    "chat_name": "my_chat"
}

msg = {"action": "leave",
    "time": time.time(),
    "from": "DЭ6ug_M@$ter",
    "chat_name": "my_chat"
}

"""

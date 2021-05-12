# Клиент для отправки json серверу и получения ответа 
from socket import *
import pickle

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 7777))
msg = {"action": "presence",
       "time": "<unix timestamp>",
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

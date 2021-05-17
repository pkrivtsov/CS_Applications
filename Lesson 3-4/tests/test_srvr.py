# pip install pytest
import time
om socket import socket, AF_INET, SOCK_STREAM
import argparse
import pickle

from messenger.srvr import createParser, checking_data


def test_create_parser():
    parser = argparse.ArgumentParser()
    assert type(createParser()) == type(parser)



def test_server_is_runing():
    msg = {"action": "presence",
           "time": time.time(),
           "type": "status",
           "user": {
               "account_name": "DЭ6ug_M@$ter",
               "status": "Yep, I am here!"
           }
    }
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 7777))
    res=s.send(pickle.dumps(msg))
    assert res.status['responce'] == 404


def checking_data_on_big_string():
    message = 's' * 1000
    assert checking_data(message)['response'] == 400


def test_checking_data_action_not_in_dict():
    message = pickle.dumps({'message': 'Hi', 'action': 'return'})
    assert checking_data(message)['response'] == 404

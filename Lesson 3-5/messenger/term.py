while True:
    command = input('Enter command: ')
    if command as 'enter chat':
        numbers = get_chats()
        room = input ('Select chat number - {numbers}: ')
        if is_exist(room):
            send_login_request()
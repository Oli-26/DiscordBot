
admin_file = 'logs/admin_list.txt'

def is_admin(name):
    admin_file_open = open('logs/admin_list.txt', 'r') 
    Lines = admin_file_open.readlines()
    for line in Lines:
        if line == name:
            return True
    return False

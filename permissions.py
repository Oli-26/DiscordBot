from encryption import decrypt, encrypt, str_to_dict, dict_to_str
admin_file = 'logs/admin_list.txt'

def add_user(dict):
    str_dict = dict_to_str(dict)
    estr_dict = encrypt(str_dict)
    str_dict = estr_dict.decode()
    
    perms_file_open = open('logs/permissions.txt', 'a') 
    perms_file_open.write(str_dict+'\n')
    perms_file_open.close()
    
def find_user(name):
    perms_file_open = open('logs/permissions.txt', 'r') 
    Lines = perms_file_open.readlines()
    i = 0
    for line in Lines:
        decrypted_line = decrypt(line.rstrip().encode())
        temp_dict = str_to_dict(decrypted_line)
        if temp_dict['name'] == name:
            return i
        i = i + 1
    return -1

def get_info(name):
    perms_file_open = open('logs/permissions.txt', 'r') 
    Lines = perms_file_open.readlines()
    for line in Lines:
        decrypted_line = decrypt(line.rstrip().encode())
        temp_dict = str_to_dict(decrypted_line)
        if temp_dict['name'] == name:
            return temp_dict
    return {}
    
def change_permission(dict):
    name = dict['name']
    i = find_user(name)
    
    perms_file_open = open('logs/permissions.txt', 'r') 
    data = perms_file_open.readlines()
    perms_file_open.close()
    
    str_dict = dict_to_str(dict)
    estr_dict = encrypt(str_dict)
    str_dict = estr_dict.decode()
    data[i] = str_dict+'\n'
    
    perms_file_open = open('logs/permissions.txt', 'w') 
    for line in data:
        perms_file_open.write(line)
    perms_file_open.close()    
    
def permission_level(name):
    try:
        return get_info(name)['level'] 
    except:
        return -1
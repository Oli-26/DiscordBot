from encryption import decrypt, encrypt, str_to_dict, dict_to_str
admin_file = 'logs/admin_list.txt'

def add_user(dict):
    '''
        This function adds a user to the permissions file
        
        :param dict dict: the user dictionary to be added to database, taking the form {name(str), id(int), level(int)}
        :return: None
    '''
    str_dict = dict_to_str(dict)
    estr_dict = encrypt(str_dict)
    str_dict = estr_dict.decode()
    
    perms_file_open = open('logs/permissions.txt', 'a') 
    perms_file_open.write(str_dict+'\n')
    perms_file_open.close()
    
def find_user_by_id(id):
    '''
        This function finds a users position in the permissions file. This is used to find the user when they need to have their details modified.
        
        :param int id: the id of the user to be located
        :return: index of user data
        :rtype: int
    '''
    perms_file_open = open('logs/permissions.txt', 'r') 
    Lines = perms_file_open.readlines()
    i = 0
    for line in Lines:
        decrypted_line = decrypt(line.rstrip().encode())
        temp_dict = str_to_dict(decrypted_line)
        if temp_dict['id'] == id:
            return i
        i = i + 1
    return -1
    
def find_id_by_name(name):
    '''
        This function returns a user id from the permissions file.
        
        :param str name: the name of the user being searched for
        :return: user_id
        :rtype: int
    '''
    perms_file_open = open('logs/permissions.txt', 'r') 
    Lines = perms_file_open.readlines()
    for line in Lines:
        decrypted_line = decrypt(line.rstrip().encode())
        temp_dict = str_to_dict(decrypted_line)
        #print("searching: " + temp_dict['name'] + "(" + str(temp_dict['level']) + ")")
        if temp_dict['name'] == name:
            return temp_dict['id']
    return -1
    
def get_info(id):
    '''
        This function returns a user dictionary from the permissions file
        
        :param int id: the id of the dictionary to be returned
        :return: user_dict
        :rtype: dict
    '''
    if id == -1:
        return {}
    perms_file_open = open('logs/permissions.txt', 'r') 
    Lines = perms_file_open.readlines()
    for line in Lines:
        decrypted_line = decrypt(line.rstrip().encode())
        temp_dict = str_to_dict(decrypted_line)
        if temp_dict['id'] == id:
            return temp_dict
    return {}
    
def change_permission(dict):
    '''
        This function is used to modify the permissions level of a user
        
        :param dict user_dict: the modified dictionary of the user
        :return: None
    '''
    id = dict['id']
    i = find_user_by_id(id)
    
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
    
def permission_level(id):
    '''
        This function will return the permission level of a user based off their id.
        
        :param int user_id: the id of the user whose permissions are needed.
        :return: permissions_level
        :rtype: int
    '''
    try:
        return get_info(id)['level'] 
    except:
        print("Failed to find user")
        return -1
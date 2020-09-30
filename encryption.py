from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from flask import json

load_dotenv()
crypto = Fernet(os.getenv('STORAGE_KEY'))

def decrypt(bytes):
    return (crypto.decrypt(bytes)).decode()
    
def encrypt(str):
    estr = str.encode()
    return crypto.encrypt(estr)
    
def dict_to_str(dict):
    str = json.dumps(dict)
    return str
    
def str_to_dict(str):
    dict = json.loads(str)
    return dict
    
    
def write_dict_to_file(dict, file_name):
    try:
        str = dict_to_str(dict)
        estr = encrypt(str)
        str = estr.decode()
        f = open(file_name, "a")
        f.write(str+'\n')
        f.close()
    except:
        print('saving dictionary to file failed.')

#write_dict_to_file({'name':'BigBoiBot', 'level':2}, 'logs/permissions.txt') 
#write_dict_to_file({'name':'Oli26', 'level':1}, 'logs/permissions.txt') 
#write_dict_to_file({'name':'test', 'level':0}, 'logs/permissions.txt')     
from datetime import datetime

log_file = 'logs/primary_log.txt'

def record(rec_str):
    with open(log_file,'a') as f:
        t = datetime.now()
        now = str(t)[:19]

        f.write(now + ' || ' + rec_str+"\n")
        
    
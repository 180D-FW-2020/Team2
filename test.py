import paramiko
from paramiko import SSHClient

if __name__ == "__main__":
    ip = '192.168.4.70'
    port=22
    user='pi'
    pw='raspberry'

    cmd = 'ls && cd Team2 && ls'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, pw)
    print('got here')
    ftp_client = ssh.open_sftp()
    ftp_client.put('../', '/home/pi') #need to change permissions on folder?
    ftp_client.close()
    stdin,stdout,stderr=ssh.exec_command(cmd)
    outlines=stdout.readlines()
    resp=''.join(outlines)
    print(resp)
#conda install -c anaconda paramiko

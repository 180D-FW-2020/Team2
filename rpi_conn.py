import paramiko
from paramiko import SSHClient
import os

class rpi_conn():
 # Find all the directories you want to upload already in files.
    def get_all_files_in_local_dir(self, local_dir):
      all_files = list()

      if os.path.exists(local_dir):
       files = os.listdir(local_dir)
       for x in files:
        filename = os.path.join(local_dir, x)
        # isdir
        if os.path.isdir(filename):
         all_files.extend(self.get_all_files_in_local_dir(filename))
        else:
         all_files.append(filename)
      return all_files

    def upload_files(self, rel_path):
        local_dir = os.path.split(os.path.abspath(rel_path))[0]
        print(local_dir)
        all_files = self.get_all_files_in_local_dir(os.path.abspath(rel_path))
        for x in all_files:
            filename = os.path.split(x)[-1]
            remote_file = os.path.split(x)[0].replace(local_dir, self.remote_dir)
            path = remote_file.replace('\\', '/')
            stdin, stdout, stderr = self.ssh.exec_command('mkdir -p ' + path)
            print(stderr.read())
            remote_filename = path + '/' + filename
            self.ftp_client.put(x, remote_filename)

    def run(self):
        self.remote_dir = '/home/pi/Team2'

        f = open('rpi.txt', 'r')
        ip = f.readline().split('=')[1].replace('\n', '')
        port = int(f.readline().split('=')[1].replace('\n', ''))
        user = f.readline().split('=')[1].replace('\n', '')
        pw = f.readline().split('=')[1].replace('\n', '')
        f.close()

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, port, user, pw)
        self.ssh.exec_command('rm -rf ' + self.remote_dir)
        self.ssh.exec_command('mkdir ' + self.remote_dir)
        self.ftp_client = self.ssh.open_sftp()
        if self.remote_dir[-1] == '/':
            self.remote_dir = self.remote_dir[0:-1]

        self.upload_files('./IMU')
        self.upload_files('./Matrix')
        self.upload_files('./MQTT')

        self.ftp_client.put(os.path.abspath('./rpi-main.py'), self.remote_dir + '/rpi-main.py')
        self.ftp_client.put(os.path.abspath('./ID.txt'), self.remote_dir + '/ID.txt')
        self.ftp_client.close()
        stdin,stdout,stderr=self.ssh.exec_command('cd Team2 && python3 rpi-main.py', get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
        self.ssh.close()

#conda install -c anaconda paramiko

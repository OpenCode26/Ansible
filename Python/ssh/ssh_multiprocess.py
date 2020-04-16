import paramiko
import concurrent.futures

cmd = "uptime"


def get_list_of_servers(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    return lines


def login_and_exec(host, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username="root", password='india@123')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.read()
    print(outlines)


list_s = get_list_of_servers("listofservers.txt")

with concurrent.futures.ProcessPoolExecutor() as executor:
    f1 = [executor.submit(login_and_exec, h, cmd) for h in list_s]
    for f in concurrent.futures.as_completed(f1):
        print(f.result())

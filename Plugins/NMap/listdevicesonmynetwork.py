import os
import subprocess

# Subprocess Info
info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0

host_list = 'host_list.xml'

with open('./nmap_config.conf', 'r') as fo:
    for line in fo:
        if line.startswith('DEFAULT_GATEWAY: '):
            default_gateway = line.replace('DEFAULT_GATEWAY: ', '')
            print('found default gateway in config:', default_gateway)
            idx = default_gateway.rfind('.', 1)
            default_gate_prepared = default_gateway[:idx]

cmd = 'nmap -sL '+default_gate_prepared+'.0/24 -oX '+host_list
print('command:', cmd)

xcmd = subprocess.check_call(cmd, shell=False, startupinfo=info)

if os.path.exists(host_list):
    hostListRead = open(host_list, 'r')
    for line in hostListRead:
        txt = '<hostname name='
        if line.startswith(txt):
            line = line.strip()
            line = line[16:]
            line = line.split('"')[0]
            print('Found Host: ', line)
    hostListRead.close()

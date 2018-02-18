import os
import win32com.client
import subprocess

# Subprocess Info
info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0

# Windows Text To Speech API
speaker = win32com.client.Dispatch("SAPI.SpVoice")

host_list = 'host_list.xml'

with open('./nmap_config.conf', 'r') as fo:
    for line in fo:
        if line.startswith('DEFAULT_GATEWAY: '):
            default_gateway = line.replace('DEFAULT_GATEWAY: ', '')
            print('found default gateway in config:', default_gateway)
            idx = default_gateway.rfind('.', 1)
            default_gate_prepared = default_gateway[:idx]

cmd = 'runas /savecred /user:Benjamin "nmap -sL '+default_gate_prepared+'.0/24 -oX '+host_list+'"'
print('command:', cmd)

xcmd = subprocess.check_call(cmd, shell=False, startupinfo=info)

device_count = 0
if os.path.exists(host_list):
    hostListRead = open(host_list, 'r')
    for line in hostListRead:
        txt = '<hostname name='
        if line.startswith(txt):
            device_count += 1
    hostListRead.close()

if device_count > 1:
    device_plural_singular = 'devices'
elif device_count <=1:
    device_plural_singular = 'device'

device_count = str(device_count)
print('device count:', device_count)
speaker.Speak('there are' + device_count + 'network' + device_plural_singular)

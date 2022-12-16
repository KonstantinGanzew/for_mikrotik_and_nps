import netmiko
from netmiko import ConnectHandler
import datetime

date = datetime.datetime.now().strftime('%m-%d-%Y')
date1 = datetime.datetime.now().strftime('%m-%Y')
date3 = datetime.datetime.now().strftime('%Y%m')[2:]
mac_list = list()
with open(f'\\\\10.10.0.2\\c$\\Windows\\System32\\LogFiles\\IN{date3}.log', 'r', encoding="utf8") as file:
        for item in file:
            mac_list.append(item.split(','))


def mac_sep(mac: str):
    mac = mac.split('@cap')[0].replace(':', '-')
    true = False
    for item in mac_list:
        for item1 in item:
            if mac in item1:
                true = True
                pass
        if true:
            mac = item[6]
            pass
    return mac

commands = '/log print'

mikrotik = {
    'device_type': 'mikrotik_routeros',
    'host': '10.50.0.2',
    'port': '22',
    'username': 'for_bot',
    'password': '1234azq'
}

sshCli = ConnectHandler(**mikrotik)
output = list(sshCli.send_command(commands).split('\n'))
old = list()
new = list()
# На тот случай если такого файла нет
try:
    with open(f'\\\\10.10.0.2\\c$\\Mikrotik_log\\{str(date1)}-log.txt', 'r') as f:
        for item in f.readlines():
            old.append(item.replace('\n', ''))
except Exception:
    pass

for item in output:
    if 'caps,info' in item:
        c = item.replace('\n', '').split(' ')
        if c[1] == 'caps,info':
            c.append(mac_sep(c[2]))
        else:
            c.append(mac_sep(c[3]))
        c.append('\n')
        c.insert(0, date)
        new.append(c)


with open(f'\\\\10.10.0.2\\c$\\Mikrotik_log\\{str(date1)}-log.txt', 'w') as f:
    for item in old:
        f.write(f'{item}\n')
    for item in new:
        f.write(' '.join(item))

commands = '/system logging action set memory memory-lines=1'
sshCli.send_command(commands)
commands = '/system logging action set memory memory-lines=1000'
sshCli.send_command(commands)
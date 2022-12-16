import netmiko
from netmiko import ConnectHandler
import datetime


# Собераем не обходимые временые интервалы для работы
date = datetime.datetime.now().strftime('%m-%d-%Y')
date1 = datetime.datetime.now().strftime('%m-%Y')
date3 = datetime.datetime.now().strftime('%Y%m')[2:]


# Лист с маками из лога NPS
mac_list = list()


# Собераем лог в список
with open(f'\\\\10.10.0.2\\c$\\Windows\\System32\\LogFiles\\IN{date3}.log', 'r', encoding="utf8") as file:
        for item in file:
            mac_list.append(item.split(','))


# Метод для переобразования из мака в логин DC
def mac_sep(mac: str):
    mac = mac.split('@cap')[0].replace(':', '-')
    true = True
    for item in mac_list:
        if true:
            for item1 in item:
                if mac in item1:
                    true = False
                    mac_item = item[6]
                    pass
    return mac_item


# Данные для подключения к микротику
mikrotik = {
    'device_type': 'mikrotik_routeros',
    'host': '10.50.0.2',
    'port': '22',
    'username': 'for_bot',
    'password': '1234azq'
}


# Устанавливаем подключение к микротику
sshCli = ConnectHandler(**mikrotik)


# Получаем список из команды
output = list(sshCli.send_command('/log print').split('\n'))
old = list()
new = list()


# На тот случай если такого файла нет
try:
    # Забираем старый лог из файла этого месяца и добавляем в список
    with open(f'\\\\10.10.0.2\\c$\\Mikrotik_log\\{str(date1)}-log.txt', 'r') as f:
        for item in f.readlines():
            old.append(item.replace('\n', ''))
except Exception:
    pass


# Перебераем выходные данные из лога микротика и добавляем данные от DC
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


# Открываем поток на запись в файл лога этого месяца либо создаем новый файл 
with open(f'\\\\10.10.0.2\\c$\\Mikrotik_log\\{str(date1)}-log.txt', 'w') as f:
    # Перезаписываем старые и дописываем новый лог
    for item in old:
        f.write(f'{item}\n')
    for item in new:
        f.write(' '.join(item))


# Чистим лог в микротике
sshCli.send_command('/system logging action set memory memory-lines=1')
sshCli.send_command('/system logging action set memory memory-lines=1000')
import matplotlib.pyplot as plt
import numpy as np

temp = 35.42
rh = 0.436

print('SHT30波形仿真工具。By @Jiu_xiao')

print('###############################################################')
print('模拟温度：' + str(temp) + '°C 模拟湿度：' + str(rh) + '%')

raw_temp = int((temp + 45) / 175 * 65535)
raw_rh = int(rh * 65535 / 100)

print('###############################################################')
print('uint16: 温度：' + str(raw_temp) + 'U 湿度：' + str(raw_rh) + 'U')

raw_temp_tab = []
raw_rh_tab = []

crc_temp_tab = []
crc_rh_tab = []

for i in range(16):
    raw_temp_tab.append(int(raw_temp % 2))
    raw_rh_tab.append(int(raw_rh % 2))
    raw_temp_tab.append(int(raw_temp % 2))
    raw_rh_tab.append(int(raw_rh % 2))
    raw_temp = int(raw_temp / 2)
    raw_rh = int(raw_rh / 2)

raw_temp_tab = raw_temp_tab[::-1]
raw_rh_tab = raw_rh_tab[::-1]

for i in range(16):
    crc_temp_tab.append(raw_temp_tab[i] + raw_temp_tab[i + 16])
    crc_rh_tab.append(raw_rh_tab[i] + raw_rh_tab[i + 16])

for i in range(16):
    if crc_temp_tab[i] == 2:
        crc_temp_tab[i] = 0
    if crc_rh_tab[i] == 2:
        crc_rh_tab[i] = 0

sda_idle = [1, 1]
sck_idle = [1, 1]

sda_start = [1, 0]
scl_start = [1, 1]

sda_stop = [0, 1]
scl_stop = [1, 1]

scl_cycle = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

sda_addr_w = [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
sda_addr_r = [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1]

sda_cmd_msb = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sda_cmd_lsb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

scl_ack = [0, 1]
sda_ack = [0, 0]
sda_no_ack = [1, 1]

scl_tab = [scl_start, scl_cycle, scl_ack, scl_cycle, scl_ack, scl_cycle, scl_ack,
           scl_start, scl_cycle, scl_ack,
           scl_cycle, scl_ack, scl_cycle, scl_ack, scl_cycle, scl_ack,
           scl_cycle, scl_ack, scl_cycle, scl_ack, scl_cycle, scl_ack, scl_stop]

sda_tab = [sda_start, sda_addr_w, sda_ack, sda_cmd_msb, sda_ack, sda_cmd_lsb, sda_ack,
           sda_start, sda_addr_r, sda_ack,
           raw_temp_tab[0:16], sda_ack, raw_temp_tab[16:32], sda_ack, crc_temp_tab, sda_ack,
           raw_rh_tab[0:16], sda_ack, raw_rh_tab[16:32], sda_ack, crc_rh_tab, sda_no_ack, sda_stop]

scl = []
sda = []

for i in scl_tab:
    for j in i:
        scl.append(j)

for i in sda_tab:
    for j in i:
        sda.append(j)

print('###############################################################')
print('原始数据')

print(scl)
print(sda)

magic_tab = [[2, 'start'], [16, 'addr_w'], [2, 'ack'], [16, 'cmd_msb'], [2, 'ack'], [16, 'cmd_lsb'], [2, 'ack'],
             [2, 'start'], [16, 'addr_r'], [2, 'ack'],
             [16, 'temp_msb'], [2, 'ack'], [16, 'temp_lsb'], [2, 'ack'], [16, 'crc'], [2, 'ack'],
             [16, 'rh_msb'], [2, 'ack'], [16, 'rh_lsb'], [2, 'ack'], [16, 'crc'], [2, 'no_ack'], [2, 'stop'], ]

count = 0
index = 0

print('###############################################################')
print('波形预览', end='')

print('\r\nscl', end='')

for i in range(len(scl)):
    if count == i:
        count = count + magic_tab[index][0]
        print(' '+magic_tab[index][1]+':', end='')
        index = index + 1

    if scl[i] == 1:
        print('\033[0;31;40m-\033[0m', end='')
    else:
        print('\033[0;31;40m_\033[0m', end='')

count = 0
index = 0
print('\r\nsda', end='')

for i in range(len(sda)):
    if count == i:
        count = count + magic_tab[index][0]
        print(' '+magic_tab[index][1]+':', end='')
        index = index + 1

    if sda[i] == 1:
        print('\033[0;31;40m-\033[0m', end='')
    else:
        print('\033[0;31;40m_\033[0m', end='')

print('\r\n###############################################################')
print('Verilog二进制数据', end='')

print('\r\nscl:\n\t' + str(len(scl)) + '\'b', end='')
for i in range(len(scl)):
    print(scl[i], end='')

print('\r\nsda:\n\t' + str(len(sda)) + '\'b', end='')
for i in range(len(sda)):
    print(sda[i], end='')
print('\r\n###############################################################')
print('感谢使用')

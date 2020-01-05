# -*- coding: utf8 -*
#24dec19kg
#python 3.7.1
#psutil 5.4.8

import subprocess
import socket
from multiprocessing import Process
from time import sleep
import psutil


'''
proc.py - работа с процессами
'''



def kill_1C():
    '''
    name_pr - строка с именем
    *
    убивает все процессы(+дочерние) с определенным именем
    '''
    try:
        for p in psutil.process_iter():
            p_name = p.name()
            if p_name == '1cv8.exe' or p_name == '1cv8c.exe':
                print("! kill: " + p_name + '\n')
                proc("Taskkill /IM " + p_name + " /F")
    except:
        print('ERROR kill proc')



def search_pid(curr_pid, kill_all = False):
    '''
    curr_pid - номер процесса
    kill_all - флаг, True убивает все процессы 1С при завершении
    *
    если в текущих процессах есть процесс то ждем секунду и снова проверяем то же самое
    если прождали 1200 секунд (20 минут) то убиваем процесс
    '''
    count = 0
    flag_proc_exist = False

    while count <= 1200:
        for proc in psutil.process_iter():
            if proc.pid == curr_pid:
                flag_proc_exist = True
                print("! wait pid: " + str(curr_pid) + " - proc exist" + '\n')
                break
        if flag_proc_exist == False:
            break
        count = count + 1
        print("! wait pid: count: " + str(count) + '\n')
        flag_proc_exist = False
        sleep(1)
    if kill_all:
        sleep(1)
        kill_1C()



def wait_1c(p_1c, kill_all=False):
    '''
    p_1c - строка, имя процесса 1с, который нужно отследить ('1cv8.exe' - конфигуратор, '1cv8c.exe' - режим предприятия)
    kill_all - флаг, True убивает все процессы 1С при завершении
    *
    нужна, что бы определить главный процесс, что бы ждать именно его (менеджер, а не клиент тестирования)
    из всех процессов выбирает все совпадающие с именем аргумента функции,
    сортирует их по времени создания,
    за текущий процесс считает последний созданный на момент выборки.
    ждет его исполнения около 20 минут
    '''
    p_1c_list = []
    for proc in psutil.process_iter():
        if proc.name() == p_1c:
            p_1c_list.append(
                    {'pid' : proc.pid, 'time_start' : proc.create_time()}
            )

    if len(p_1c_list) == 0:
        return
    else:
        sort_p_1c_list = sorted(p_1c_list, key=lambda x: x['time_start'])

        print('DEBUG: 1cv8.exe sorting by time \n')
        [print(i) for i in sort_p_1c_list]

        curr_pid = sort_p_1c_list[-1]['pid']
        search_pid(curr_pid, kill_all)



def proc_prior(proc, p_class):
    '''
    proc -  процесса
    p_class - "H"(высокий) или "R"(реального времени) класс процесса
    *
    назначает процессам приоритет
    '''
    try:
        for p in psutil.process_iter():
            if p.name() == proc:
                if p_class == 'H':
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                elif p_class == 'R':
                    p.nice(psutil.REALTIME_PRIORITY_CLASS)
    except:
        print('ERROR ' + p_class + ' class \n')



def servo():

    def inner_cicle(data_list, kill):
        count = 0
        flag = False
        name_proc = data_list[1]

        while count <= 1200:
            for p in psutil.process_iter():
                if p.name() == name_proc:
                    flag = True
                    proc_prior(name_proc,'H')
                    wait_1c(name_proc, kill)
                    break
            if flag:
                break
            else:
                count = count + 1


    sock = socket.socket()
    sock.bind(('localhost', 9080))
    sock.listen(1)
    conn, addr = sock.accept()

    while True:

        data = conn.recv(1024)
        data = data.decode()
        data_list = data.split('@')

        if len(data_list) == 2:
            command_to_servo = data_list[0]
            if command_to_servo == 'wait':
                inner_cicle(data_list, False)
                conn.send("1".encode())
            elif command_to_servo == 'wait_and_kill':
                inner_cicle(data_list, True)
                conn.send("1".encode())
            elif command_to_servo == 'shutdown':
                conn.close()
                sock.close()
            else:
                conn.send("0".encode())



def start_servo():
    def dif_proc(func, args_list):
        p = Process(target=func, args=args_list)
        p.start()
        return p

    return dif_proc(servo, [])



def start_client():
    sock = socket.socket()
    sock.connect(('localhost', 9080))
    return sock



def proc(command, p_1c='', kill_all=False, sock=None):
    '''
    command - принимает строку консольной команды.
    p_1c - строка, имя процесса, который нужно ждать.
    kill_all - флаг, True убивает все процессы 1С при завершении
    *
    запускает и ожидает завершение процесса.
    '''
    try:
        if p_1c != '':
            if p_1c == 'servo_kill':
                print("SERVO KILL \n")
                sock.send('shutdown@none')
                sock.close()
                exit()
                return
    
            if kill_all:
                print("SERVO WAIT AND KILL " + p_1c + '\n')
                str_comm = 'wait_and_kill@' + p_1c
                sock.send(str_comm.encode())
            else:
                print("SERVO WAIT " + p_1c + '\n')
                str_comm = 'wait@' + p_1c
                sock.send(str_comm.encode())
    
        process = subprocess.Popen(command, shell=True)
        process.communicate()
    
        if p_1c != '':
            data = sock.recv(1024)
            data = data.decode()
            if data == "0":
                print('error: '+ command + '\n')
                proc('', 'servo_kill', sock=sock)

    except:
        print('error: '+ command)
        proc('', 'servo_kill', sock=sock)

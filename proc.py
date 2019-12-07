# -*- coding: utf8 -*
#28nov19kg
#python 3.7.1
#psutil 5.4.8

import subprocess
from time import sleep
import psutil


'''
proc.py - работа с процессами
'''



def kill_1C():
    '''
    name_pr - строка с именем
    *
    убивает все процессы с определенным именем
    '''
    try:
        for proc in psutil.process_iter():
            if proc.name() == '1cv8.exe' or proc.name() == '1cv8c.exe':
                proc.kill()
    except:
        print('ERROR kill proc')



def rec_search_pid(curr_pid, count, kill_all = False):
    '''
    curr_pid - номер процесса
    count - сколько секунд мы уже прождали
    kill_all - флаг, True убивает все процессы 1С при завершении
    *
    рекурсивная функция
    если в текущих процессах есть процесс с номером аргумента то ждем секунду и снова проверяем то же самое
    если прождали 1200 секунд (20 минут) то убиваем процесс
    '''
    if count == 999:
        try:
            for proc in psutil.process_iter():
                if proc.pid == curr_pid:
                    if kill_all:
                        kill_1C()
                    else:
                        proc.kill()
        except:
            print('ERROR kill proc')

    for proc in psutil.process_iter():
        if proc.pid == curr_pid:
            sleep(1)
            count = count + 1
            rec_search_pid(curr_pid, count, kill_all)
            break
    if kill_all:
        kill_1C()



def wait_1c(p_1c, kill_all = False):
    '''
    p_1c - строка, имя процесса 1с, который нужно отследить ('1cv8.exe' - конфигуратор, '1cv8c.exe' - режим предприятия)
    kill_all - флаг, True убивает все процессы 1С при завершении
    *
    из всех процессов выбирает все совпадающие с именем аргумента функции,
    сортирует их по времени создания,
    за текущий процесс считает последний созданный на момент выборки.
    ждет его исполнения около 20 минут
    '''
    p_1c_list = []
    PROCNAME = p_1c

    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            p_1c_list.append(
                    {'pid' : proc.pid, 'time_start' : proc.create_time()}
            )

    if len(p_1c_list) == 0:
        return
    else:
        sort_p_1c_list = sorted(p_1c_list, key=lambda x: x['time_start'])

        print('DEBUG: 1cv8.exe sorting by time')
        [print(i) for i in sort_p_1c_list]

        curr_pid = sort_p_1c_list[-1]['pid']
        rec_search_pid(curr_pid, 0, kill_all)
        sleep(3)



def proc_prior(proc, p_class):
    '''
    proc - pid процесса
    p_class - "H"(высокий) или "R"(реального времени) класс процесса
    *
    назначает процессам приоритет
    '''
    try:
        for p in psutil.process_iter():
            if p.pid == proc:
                if p_class == 'H':
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                elif p_class == 'R':
                    p.nice(psutil.REALTIME_PRIORITY_CLASS)
                break
    except:
        print('процессу не установлен ' + p_class + ' класс')



def proc(command, p_1c = '', kill_all = False):
    '''
    command - принимает строку консольной команды.
    p_1c - строка, имя процесса, который нужно ждать.
    kill_all - флаг, True убивает все процессы 1С при завершении
    *
    запускает и ожидает завершение процесса.
    '''
    try:
        proc = subprocess.Popen(command, shell=True)
        proc.communicate()
        proc_prior(proc, 'R')
    except:
        print('error: '+ command)
        exit()
    if p_1c != '':
        if p_1c == '1cv8c.exe':
            kill_all = True
        wait_1c(p_1c, kill_all)



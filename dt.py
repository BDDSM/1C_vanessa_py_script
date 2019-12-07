# -*- coding: utf8 -*
#25nov19kg
#python 3.7.1

from shutil import copyfile
from os import mkdir, path

from proc import proc
from test_pars import va_params
from prepare import write_string_file, del_path


'''
dt.py - работа с 1С через командную строку
'''



def just_do_it(command, wait_1c='', about=''):
    '''
    command - консольная команда
    wait_1c - имя процесса 1с, если нужно ждать 1с
    about - строка описыват что делаем
    *
    запускает консольную команду в процессе
    '''
    proc('chcp 65001')
    proc(command, wait_1c)
    print('\n' + about + ' :\n' + command)
    print('----------------------------------------------- \n')



def create_base(param_dict, base_use, name_dir=''):
    '''
    param_dict - словарь параметров
    base_use - строка, вид базы manager или client
    name_dir - имя папки с базой
    *
    создает пустую базу
    '''
    path = ''
    if base_use == 'manager':
        path = param_dict['WORK_PATH_BASE_M']
    elif base_use == 'client':
        param_dict['WORK_PATH_BASE_CURR'] = param_dict['WORK_PATH_BASE_C'] + '\\' + name_dir
        path = param_dict['WORK_PATH_BASE_CURR']

    comm_str = param_dict['START_PL_1C'] + ' CREATEINFOBASE File=' + path
    just_do_it(comm_str, '', 'СОЗДАЛА БАЗУ: ' + base_use)



def eat_dt(param_dict, base_use, usr=''):
    '''
    param_dict - словарь параметров
    base_use - строка, вид базы manager или client
    usr - пользователь базы
    *
    загружает dt файл в базу
    '''
    if base_use == 'manager':
        dt = param_dict['MODEL_ON_RUNNER'] + 'manager.dt'
        path = param_dict['WORK_PATH_BASE_M']
    elif base_use == 'client':
        dt = param_dict['MODEL_ON_RUNNER_CURRENT_DT']
        path = param_dict['WORK_PATH_BASE_CURR']

    comm_str = param_dict['START_1cestart'] + ' DESIGNER /F ' +\
        path + ' /N"'+usr+'" /P"" /RestoreIB ' + dt + ' /Out ' + param_dict['LOG_PATH'] + ' /Visible'
    just_do_it(comm_str, '1cv8.exe', 'ЗАГРУЗИЛА DT: ' + base_use)



def eat_cf(param_dict):
    '''
    param_dict - словарь параметров
    *
    загружает и обновляет cf файл 
    '''
    comm_str = param_dict['START_1cestart'] + ' DESIGNER /F ' +\
        param_dict['WORK_PATH_BASE_CURR'] + ' /N"'+param_dict['MODEL_ADMIN_USER']+'" /P"" /LoadCfg ' + param_dict['WORK_PATH'] + '1Cv8.cf /Out ' + param_dict['LOG_PATH'] + ' /Visible'
    just_do_it(comm_str, '1cv8.exe', 'ЗАГРУЗИЛА CF')

    comm_str = param_dict['START_1cestart'] + ' DESIGNER /F ' +\
        param_dict['WORK_PATH_BASE_CURR'] + ' /N"'+param_dict['MODEL_ADMIN_USER']+'" /P"" /UpdateDBCfg /Out ' + param_dict['LOG_PATH'] + ' /Visible'
    just_do_it(comm_str, '1cv8.exe', 'ОБНОВИЛА НА CF')



def start_vanessa(param_dict, test_name, wait_1c=''):
    '''
    param_dict - словарь параметров
    test_name - имя теста, присваивается автоматически в зависимости от тэгов расставленых в фича-файле
    например: "@_$Наценка-сумма-строка"
    wait_1c - нужно ли ждать завершения работы 1с после ее старта
    *
    подготавливает конфиг для Ванессы
    запускает Ванессу с нужным тестом
    создает лог запуска теста
    '''
    VAParams = va_params(param_dict, test_name)
    path_VAParams = param_dict['TESTS_ON_RUNNER'] + 'VAParams.json'
    path_VAParams = path_VAParams.replace('\\', '\\\\')

    write_string_file(path_VAParams, 'w', VAParams)

    comm_str = param_dict['START_1cestart'] + ' ENTERPRISE /F ' +\
        param_dict['WORK_PATH_BASE_M'] + ' /DEBUG /AllowExecuteScheduledJobs -Off /DisableStartupDialogs /DisableStartupMessages /N"'+'Администратор'+\
        '" /P"" /Execute ' + param_dict['VANNESSA_EPF'] + ' /TESTMANAGER /C"StartFeaturePlayer;VBParams=' + path_VAParams + '" /Out ' + param_dict['LOG_PATH']

    just_do_it(comm_str, wait_1c, 'ПРИГЛАСИЛА ВАНЕССУ')

    log_name = param_dict['WORK_PATH'] + 'log\\' + test_name + '_LOG.txt'
    print('СOPY .CD file ...')
    copyfile(param_dict['LOG_PATH'] , log_name)
    print('CREATE LOG: ' + log_name)
    print('----------------------------------------------- \n')



def reject_cd(param_dict, dt_name=''):
    '''
    param_dict - словарь параметров
    *
    копирует CD файл клиентской базы в каталог шаблонов
    '''
    storage_path = param_dict['MODEL_ON_RUNNER'] + 'storage_' + dt_name + '\\'
    if not path.exists(storage_path):
        mkdir(storage_path)
    print('COPY : ' + param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD', storage_path + '1Cv8.1CD')
    copyfile(param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD', storage_path + '1Cv8.1CD')
    param_dict['STORAGE_CURR_1CD'] = 'storage_' + dt_name
    print('----------------------------------------------- \n')



def push_cd_client(param_dict):
    '''
    param_dict - словарь параметров
    *
    удаляет файлы клиентской базы
    копирует CD файл клиентской базы из каталога шаблонов в расположение клиентской базы
    '''
    del_path(param_dict['WORK_PATH_BASE_CURR'])
    mkdir(param_dict['WORK_PATH_BASE_CURR'])

    curr_path_cd = param_dict['MODEL_ON_RUNNER'] + '\\' + param_dict['STORAGE_CURR_1CD'] + '\\1Cv8.1CD'
    copyfile(curr_path_cd, param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD')
    print('COPY : ' + curr_path_cd, param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD')
    print('----------------------------------------------- \n')

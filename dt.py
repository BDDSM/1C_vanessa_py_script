# -*- coding: utf8 -*
#25dec19kg
#python 3.7.1

from shutil import copyfile
from os import mkdir, path

from proc import proc
from test_pars import va_params
from prepare import write_string_file, del_path, get_cd_directory


'''
dt.py - работа с 1С через командную строку
'''



def just_do_it(command, wait_1c='', about='', kill=False, sock=None):
    '''
    command - консольная команда
    wait_1c - имя процесса 1с, если нужно ждать 1с
    about - строка описыват что делаем
    kill - если нужно убить процесс
    *
    запускает консольную команду в процессе
    '''
    print('\n' + about + ' :\n' + command)
    proc(command, wait_1c, kill, sock=sock)
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

    just_do_it(comm_str, '1cv8.exe', 'CREATE BASE: ' + base_use, False, param_dict['CLIENT'])



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

    just_do_it(comm_str, '1cv8.exe', 'LOAD DT: ' + base_use, False, param_dict['CLIENT'])



def dump_cf(param_dict):
    '''
    param_dict - словарь параметров
        *
    выгружает cf
    '''
    comm_str = param_dict['START_1cestart'] + ' DESIGNER /F ' +\
        param_dict['WORK_PATH_BASE_CURR'] + ' /N"' + param_dict['MODEL_ADMIN_USER'] +\
        '" /P"" /DumpCfg ' + param_dict['WORK_PATH'] + '1Cv8.cf /Out ' + param_dict['LOG_PATH'] + ' /Visible'

    just_do_it(comm_str, '1cv8.exe', 'DUMP CF', False, param_dict['CLIENT'])



def updt(param_dict):
    '''
    param_dict - словарь параметров
        *
    обновляет базу
    '''
    comm_str = param_dict['START_1cestart'] + ' DESIGNER /F ' +\
        param_dict['WORK_PATH_BASE_CURR'] + ' /N"'+param_dict['MODEL_ADMIN_USER']+\
        '" /P"" /UpdateDBCfg /Out ' + param_dict['LOG_PATH'] + ' /Visible'

    just_do_it(comm_str, '1cv8.exe', 'UPDT CF', False, param_dict['CLIENT'])



def eat_cf(param_dict):
    '''
    param_dict - словарь параметров
    *
    загружает и обновляет cf файл 
    '''
    comm_str = param_dict['START_1cestart'] + ' DESIGNER /F ' +\
        param_dict['WORK_PATH_BASE_CURR'] + ' /N"'+param_dict['MODEL_ADMIN_USER']+\
        '" /P"" /LoadCfg ' + param_dict['WORK_PATH'] + '1Cv8.cf /Out ' + param_dict['LOG_PATH'] + ' /Visible'

    just_do_it(comm_str, '1cv8.exe', 'LOAD CF', False, param_dict['CLIENT'])
    updt(param_dict)



def upd_from_repo(param_dict):
    '''
    param_dict - словарь параметров
    *
    обновляет базу из хранилища
    '''
    comm_str = param_dict['START_PL_1C'] + r' DESIGNER /F "'+ param_dict['WORK_PATH_BASE_CURR'] +\
        r'" /N"' + param_dict['MODEL_ADMIN_USER']+ r'" /P"" /ConfigurationRepositoryF"' + param_dict['REPO_PATH'] +\
        r'" /ConfigurationRepositoryN"' + param_dict['REPO_USER'] + r'" /ConfigurationRepositoryP"'  +\
        param_dict['REPO_PASSWORD'] + r'" /ConfigurationRepositoryUpdateCfg -v"' + param_dict['REPO_VER'] +\
        '" /Visible /Out ' + param_dict['LOG_PATH']

    just_do_it(comm_str, '1cv8.exe', 'UPD FROM REPO', False, param_dict['CLIENT'])
    updt(param_dict)



def start_vanessa(param_dict, test_name):
    '''
    param_dict - словарь параметров
    test_name - имя теста, присваивается автоматически в зависимости от тэгов расставленых в фича-файле
    например: "@_$Наценка-сумма-строка"
    *
    подготавливает конфиг для Ванессы
    запускает Ванессу с нужным тестом
    создает лог запуска теста
    '''
    VAParams = va_params(param_dict, test_name)
    path_VAParams = param_dict['TESTS_ON_RUNNER'] + 'VAParams.json'
    path_VAParams = path_VAParams.replace('\\', '\\\\')

    write_string_file(path_VAParams, 'w', VAParams)

    comm_str = param_dict['START_PL_1C'] + ' ENTERPRISE /F ' + param_dict['WORK_PATH_BASE_M'] +\
        ' /DEBUG /AllowExecuteScheduledJobs -Off /DisableStartupDialogs /DisableStartupMessages /N"'+'Администратор'+\
        '" /P"" /Execute ' + param_dict['VANNESSA_EPF'] + ' /TESTMANAGER /C"StartFeaturePlayer;VBParams=' +\
        path_VAParams + '" /Out ' + param_dict['LOG_PATH']

    just_do_it(comm_str, '1cv8.exe', 'CALL VANESSA', True, param_dict['CLIENT'])

    log_name = param_dict['WORK_PATH'] + 'log\\' + test_name + '_LOG.txt'
    print('CREATE LOG: ' + log_name)
    copyfile(param_dict['LOG_PATH'] , log_name)
    print('----------------------------------------------- \n')



def reject_cd(param_dict, dt_name=''):
    '''
    param_dict - словарь параметров
    dt_name - ('role.dt') имя базы-эталона для данного тестирования
    *
    копирует CD файл клиентской базы в каталог шаблонов
    '''
    storage_path = param_dict['MODEL_ON_RUNNER'] + 'storage_' + dt_name + '\\'
    if not path.exists(storage_path):
        mkdir(storage_path)
    print('DUMP CD AFTER UPDATE : ' + param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD', storage_path + '1Cv8.1CD')
    copyfile(param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD', storage_path + '1Cv8.1CD')
    param_dict['STORAGE_CURR_1CD'] = 'storage_' + dt_name
    print('----------------------------------------------- \n')



def push_cd_client(param_dict, dt_name=''):
    '''
    param_dict - словарь параметров
    dt_name - ('role.dt') имя базы-эталона для данного тестирования
    *
    удаляет файлы клиентской базы
    копирует CD файл клиентской базы из каталога шаблонов в расположение клиентской базы
    '''
    if param_dict['PREPARE_MODE'] == '' and dt_name != '':
        param_dict['WORK_PATH_BASE_CURR'] = get_cd_directory(dt_name, param_dict['WORK_PATH_BASE_C'])
        param_dict['STORAGE_CURR_1CD'] = 'storage_' + dt_name

    #del_path(param_dict['WORK_PATH_BASE_CURR'])
    #mkdir(param_dict['WORK_PATH_BASE_CURR'])

    curr_path_cd = param_dict['MODEL_ON_RUNNER'] + '\\' + param_dict['STORAGE_CURR_1CD'] + '\\1Cv8.1CD'

    print('PUSH CD FROM STORAGE : ' + curr_path_cd, param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD')
    copyfile(curr_path_cd, param_dict['WORK_PATH_BASE_CURR'] + '\\1Cv8.1CD')
    print('----------------------------------------------- \n')

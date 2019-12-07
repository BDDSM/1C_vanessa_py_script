# -*- coding: utf8 -*
#15nov19kg
#python 3.7.1

from proc import proc
from shutil import rmtree
from os import path, listdir, mkdir


'''
prepare.py - консольные команды копирования, подключения, удаление, чтение и запись файлов
'''



def del_path(cur_path):
    '''
    cur_path - директория которую нужно удалить
    *
    удаляет директорию
    '''
    if path.exists(cur_path):
        rmtree(cur_path)
        print('DEL ' + cur_path)
        print('----------------------------------------------- \n')
    else:
        print('NOT DEL ' + cur_path)
        print('----------------------------------------------- \n')



def create_log_dir(param_dict):
    '''
    param_dict - словарь параметров
    *
    создает рабочую директорию и директорию для лог файлов
    '''
    WORK_PATH = param_dict['WORK_PATH']
    log_dir = WORK_PATH + 'log'

    if not path.exists(log_dir):
        TEST_CATALOG = param_dict['TEST_CATALOG']
        if not path.exists(TEST_CATALOG):
            print('CREATE : ' + TEST_CATALOG)
            mkdir(TEST_CATALOG)
            if not path.exists(WORK_PATH):
                print('CREATE : ' + WORK_PATH)
                mkdir(WORK_PATH)
        print('CREATE : ' + log_dir)
        mkdir(log_dir)
        print('----------------------------------------------- \n')



def prepare_st(param_dict):
    '''
    param_dict - словарь параметров
    *
    устанавливает кодировку в консоли для русских символов
    подключается к указанным компьютерам
    копирует платформу на компьютер где будет прохолить тест
    копирует Ванессу на компьютер где будет прохолить тест
    копирует тесты, конфигурацию и эталоны на компьютер где будет прохолить тест
    создает директорию для логфайлов
    '''
    proc('chcp 65001')
    proc('net use')
    proc('net use /delete * /y')

    proc('net use '+param_dict['BUILD_FILES_Trunk']+' /PERSISTENT:NO /User:'+param_dict['NET_DOMAIN']+'\\'+param_dict['NET_USER']+' '+param_dict['NET_PASSWORD'])
    proc('net use '+param_dict['REPO_PATH']+' /PERSISTENT:NO /User:'+param_dict['NET_DOMAIN']+'\\'+param_dict['NET_USER']+' '+param_dict['NET_PASSWORD'])
    proc('net use')
    print('----------------------------------------------- \n')

    print('XCOPY ' + param_dict['PLATFORM_PATH']+' ---> '+param_dict['PLATFORM_PATH_ON_RUNNER'] + '\n')
    proc('XCOPY \"'+param_dict['PLATFORM_PATH']+'\" \"'+param_dict['PLATFORM_PATH_ON_RUNNER']+'\"  /H /Y /C /R /S')
    print('----------------------------------------------- \n')

    print('XCOPY ' + param_dict['VANESSA_PATH']+' ---> '+param_dict['VANESSA_ON_RUNNER'] + '\n')
    proc('XCOPY \"'+param_dict['VANESSA_PATH']+'\" \"'+param_dict['VANESSA_ON_RUNNER']+'\"  /H /Y /C /R /S')
    print('----------------------------------------------- \n')

    print('XCOPY ' + param_dict['VANESSA_TOOLS']+' ---> '+param_dict['VANESSA_TOOLS_ON_RUNNER'] + '\n')
    proc('XCOPY \"'+param_dict['VANESSA_TOOLS']+'\" \"'+param_dict['VANESSA_TOOLS_ON_RUNNER']+'\"  /H /Y /C /R /S')
    print('----------------------------------------------- \n')

    print('XCOPY ' + param_dict['TESTS_PATH']+' ---> '+param_dict['TESTS_ON_RUNNER'] + '\n')
    proc('XCOPY \"'+param_dict['TESTS_PATH']+'\" \"'+param_dict['TESTS_ON_RUNNER']+'\"  /H /Y /C /R /S')
    print('----------------------------------------------- \n')

    print('XCOPY \"'+param_dict['MODEL_PATH']+'\" \"'+param_dict['MODEL_ON_RUNNER']+'\"  /H /Y /C /R /S\n')
    proc('XCOPY \"'+param_dict['MODEL_PATH']+'\" \"'+param_dict['MODEL_ON_RUNNER']+'\"  /H /Y /C /R /S')
    print('----------------------------------------------- \n')

    print('XCOPY \"'+param_dict['CF_PATH']+'\" \"'+param_dict['WORK_PATH']+'\"  /H /Y /C /R /S\n')
    proc('XCOPY \"'+param_dict['CF_PATH']+'\" \"'+param_dict['WORK_PATH']+'\"  /H /Y /C /R /S')
    print('----------------------------------------------- \n')

    create_log_dir(param_dict)



def write_string_file(filename, param_write, wr_str):
    '''
    filename - полный путь с именем до файла
    param_write - параметр записа 'w' - заменяет содержимое в файле 'a' - добавляет к содержимому в файле
    wr_str - строка которую записываем в файл
    *
    записывает строку в файл на компьютере
    '''
    with open(filename, param_write, encoding="utf8") as my_file:
        my_file.write(wr_str)
    my_file.close()



def write_list_file(enter_list, filename, param_write):
    '''
    enter_list - список со строками
    filename - полный путь с именем до файла
    param_write - параметр записа 'w' - заменяет содержимое в файле 'a' - добавляет к содержимому в файле
    *
    записывает список состоящий из строк в файл на компьютере
    '''
    with open(filename, param_write, encoding="utf8") as my_file:
        for i in enter_list:
            my_file.write(i)
    my_file.close()



def open_file_r(filename, enc="utf8"):
    '''
    filename - полный путь с именем до файла
    *
    читает файл на компьютере
    *
    return file_list - возвращает список с прочитанными строками
    '''
    file_list = []
    with open(filename, "r", encoding=enc) as my_file:
        for line in my_file:
            file_list.append(line)
    my_file.close()

    if len(file_list) == 0:
        print("empty file: " + filename)
        exit()

    return file_list



def get_list_tests(params):
    '''
    params - словарь параметров
    *
    смотрит в папке с тестами по префиксу "@_" в названии файлы с тестами
    *
    return tests_list - возвращает список имен этих файлов
    '''
    test_path = params['TESTS_ON_RUNNER']
    doc_list = listdir(test_path)
    tests_list = []
    for i in doc_list:
        if i.find('@_') != -1:
            tests_list.append(i)
    if len(tests_list) == 0:
        print('\nТЕСТЫ НЕ БЫЛИ СОЗДАНЫ')
    return tests_list

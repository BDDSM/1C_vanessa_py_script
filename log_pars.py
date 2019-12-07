# -*- coding: utf8 -*
#27nov19kg
#python 3.7.1

from os import listdir, path, mkdir, remove
from re import findall, split
from shutil import copyfile

from prepare import open_file_r, write_list_file, write_string_file



def parse_log_path(params):
    '''
    params - словарь параметров
    *
    парсит лог файлы каждого теста
    берет от каждого лога название и его последние 6 строк если в нем были ошибки
    *
    return [list_for_tests_with_error, list_for_final_data] - возвращает список из списка ошибочных тестов 
    и списка строк финального лога
    '''
    list_for_final_data = []
    list_for_tests_with_error = []
    list_for_current_log = []
    curr_final_list = []

    log_path = params['WORK_PATH'] + 'log\\'
    doc_list = listdir(log_path)
    error_flag = False

    for i in doc_list:
        if i.find('_LOG') != -1:
            log_list = open_file_r(log_path + i, 'windows-1251')

            for x in log_list:
                time_list = findall(r'\d{2}.\d{2}.\d{4}', x)
                if len(time_list) > 0:
                    list_for_current_log.append(x)
                if x.find("БЫЛИ ОШИБКИ") != -1:
                    error_flag = True

            if error_flag == True:
                curr_final_list.append('----------------------------------------------- \n')
                curr_final_list.append('\t' + i + ' : \n')
                curr_final_list.append('                       *** \n')
                for z in list_for_current_log[-14:]:
                    curr_final_list.append(z)
                curr_final_list.append('----------------------------------------------- \n')

                list_for_final_data.append(curr_final_list.copy())
                list_for_tests_with_error.append(i)
            error_flag = False
            list_for_current_log.clear()
            curr_final_list.clear()

    return [list_for_tests_with_error, list_for_final_data]



def create_final(params, add_h='', add_t=''):
    '''
    params - словарь параметров
    add_h - если к тесту, где были ошибки, нужно присоедтнять начало то имя файла
    add_t - если к тесту, где были ошибки, нужно присоедтнять конец то имя файла
    *
    парсит лог файлы выбирает информацию о тестах и ошибках
    помещает в каталог FINAL_LOG сводную информацию об ошибках 
    и тесты в коротрых были ошибки
    '''
    final_list = parse_log_path(params)
    error_logs = final_list[0]
    final_list = final_list[1]

    if len(error_logs) != 0:
        TESTS_PATH = params['TESTS_ON_RUNNER']
        FINAL_LOG = params['FINAL_LOG']
        OUT_CD = FINAL_LOG + 'OUT_CD\\'
        TESTS_WITH_ERROR = FINAL_LOG + 'TESTS_WITH_ERROR\\'

        if not path.exists(FINAL_LOG):
            print('CREATE : ' + FINAL_LOG)
            mkdir(FINAL_LOG)
        if not path.exists(TESTS_WITH_ERROR):
            print('CREATE : ' + TESTS_WITH_ERROR)
            mkdir(TESTS_WITH_ERROR)
        write_string_file(FINAL_LOG + 'FINAL_LOG.txt', 'w', '')
        if not path.exists(OUT_CD):
            print('CREATE : ' + OUT_CD)
            mkdir(OUT_CD)

        for i in final_list:
            write_list_file(i, FINAL_LOG + 'FINAL_LOG.txt', 'a')

        tests_with_errors = []
        for i in error_logs:
            curr_lst = split('_LOG', i)
            tests_with_errors.append(curr_lst[0])

        tests_list = listdir(TESTS_PATH)

        head = TESTS_PATH + add_h + '.txt'
        if path.exists(head):
            copyfile(head, TESTS_WITH_ERROR + add_h + '.txt')
        tail = TESTS_PATH + add_t + '.txt'
        if path.exists(tail):
            copyfile(tail, TESTS_WITH_ERROR + add_t + '.txt')

        for x in tests_list:
            if x.find("@_") != -1:
                for y in tests_with_errors:
                    if x == y:
                        path_for_test = TESTS_WITH_ERROR + '!CD' + params['STORAGE_CURR_1CD'] + 'CD!!ADDH' + add_h + 'ADDH!!ADDT' + add_t + 'ADDT!' + x
                        print('COPY : ' + x + ' ---> ' + path_for_test)
                        copyfile(TESTS_PATH + x, path_for_test)
                        break
                remove(TESTS_PATH + x)

        print('БЫЛИ ОШИБКИ\n')
        print('FINAL_LOG : ' + FINAL_LOG)
        print('----------------------------------------------- \n')

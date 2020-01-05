# -*- coding: utf8 -*
#28nov19kg
#python 3.7.1

from os import listdir, path
from re import findall
from shutil import copyfile

from dt import start_vanessa
from prepare import open_file_r
from test_pars import print_cat, write_curr_test
from proc import proc



def test(params, test_name):
    '''
    params - словарь параметров
    test_name - имя запускаемого теста
    *
    запускает тест по названию
    *
    '''
    print('----------------------------------------------- \n')
    print(test_name)
    user = findall('%(.*).feature', test_name)
    cd_path = findall('!CD(.*)CD!', test_name)
    addit_strings_head = findall('!ADDH(.*)ADDH!', test_name)
    addit_strings_tail = findall('!ADDT(.*)ADDT!', test_name)
    if len(user) != 0 and len(cd_path) != 0: 
        user = user[0]
        cd_path = cd_path[0]
        addit_strings_head =addit_strings_head[0]
        addit_strings_tail = addit_strings_tail[0]
        print('USER : ' + user)
        print('PATH : ' + cd_path)
        print('HEAD : ' + addit_strings_head)
        print('TAIL : ' + addit_strings_tail)
        print('----------------------------------------------- \n')

        params['MODEL_USER'] = user
        OUT_CD = params['FINAL_LOG'] + 'OUT_CD'
        print('СOPY .CD file ...')
        copyfile(params['MODEL_ON_RUNNER'] + cd_path  + '\\1Cv8.1CD', OUT_CD  + '\\1Cv8.1CD')
        print('COPY: ' + params['MODEL_ON_RUNNER'] + cd_path + ' ---> ' + OUT_CD)
        params['WORK_PATH_BASE_CURR'] = OUT_CD
        params['TESTS_ON_RUNNER'] = params['FINAL_LOG'] + 'TESTS_WITH_ERROR\\'
        params['ESC_VANESSA'] = 'Ложь'
        params['ESC_TEST_CLIENT'] = 'Ложь'

        test_lst = open_file_r(params['TESTS_ON_RUNNER'] + test_name)
        curr_test = []
        flag = False
        for i in test_lst:
            if i.find('!$') != -1:
                flag = True
            if flag == True:
                curr_test.append(i)

        write_curr_test(params, 
                        curr_test, 
                        'out', 
                        params['TESTS_ON_RUNNER'] + 'out.feature', 
                        addit_strings_head, addit_strings_tail)

        start_vanessa(params, 'out.feature')

        print('----------------------------------------------- \n')
    else:
        print('ERROR: USER OR PATH')



def start_debug_tests(params):
    '''
    params - словарь параметров
    *
    бесконечный цикл, выводит пронумерованный список тестов с ошибками
    запускает тест в зависимости от номера
    '''
    dict_menu_tests = {}
    TESTS_WITH_ERROR = params['FINAL_LOG'] + 'TESTS_WITH_ERROR\\'
    if path.exists(TESTS_WITH_ERROR):
        tests_lst = listdir(TESTS_WITH_ERROR)
    else:
        print('PATH : ' + TESTS_WITH_ERROR + 'NOT EXISTS')

    count = 0
    for i in tests_lst:
        count = count + 1
        dict_menu_tests.update(
            {str(count):i}
        )

    flag = True
    test_name = ''
    while flag:
        print_cat()
        print('START_TIME: ' + params['START_TIME'])
        print('END_TIME: ' + params['END_TIME'])
        print('                       *** ')
        for k, v in dict_menu_tests.items():
            pr_v_lst = findall('!@_(.*)', v)
            if len(pr_v_lst) == 0:
                pr_v = v
            else:
                pr_v = pr_v_lst[0]
            print(k + '  --->  ' + pr_v)
        print('                       *** \n')
        num = input('номер теста или 0 для выхода : ')
        if num == '0':
            flag = False
            break
        for k, v in dict_menu_tests.items():
            if k == num:
                test_name = v
                break
        test(params, test_name)

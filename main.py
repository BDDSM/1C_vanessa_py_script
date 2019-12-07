# -*- coding: utf8 -*
#28nov19kg
#python 3.7.1

from datetime import datetime

from param import ret_param_dict, return_scenario
from prepare import (prepare_st, 
                     del_path, 
                     write_string_file, 
                     get_list_tests,
                     create_log_dir)
from dt import (create_base, 
                eat_cf, 
                eat_dt, 
                start_vanessa, 
                reject_cd,
                push_cd_client)
from test_pars import update_test, prepare_tests, parse_name, print_cat
from proc import kill_1C, proc_prior
from log_pars import create_final
from test_start import start_debug_tests


'''
main.py - основные функции программы
'''


def update_dt(params):
    '''
    params - словарь параметров
    *
    обновляет базу на cf
    собирает тест для обновления в режиме предприятия
    запускает Ванессу для обновления базы в режиме предприятие
    '''

    eat_cf(params)

    test_string = update_test(params)
    write_string_file(params['TESTS_ON_RUNNER'] + 'prepare.feature', 
                      'w', 
                      test_string
                      )

    start_vanessa(params, 'prepare.feature', '1cv8c.exe')



def start_tests(params, test_name, addit_strings_head_rmk, addit_strings_tail):
    '''
    params - словарь параметров
    test_name - имя общего теста который запускаем
    addit_strings_head - имя файла с тестом, тест прикрепляющийся к началу основного теста, если нужно
    addit_strings_tail - имя файла с тестом, тест прикрепляющийся к концу основного теста, если нужно
    *
    собирает основные тесты для запуска
    на обнавленном эталоне запускает тесты в цикле
    ''' 
    kill_1C()
    prepare_tests(params, test_name, addit_strings_head_rmk, addit_strings_tail)
    list_tests_names = get_list_tests(params)

    for name in list_tests_names:
        kill_1C()

        push_cd_client(params)
        start_vanessa(params, name, '1cv8c.exe')



def main_func():
    '''
    MaiN
    получает лист со сценарием тестирования
    получает словарь с параметрами
    очищает тестовый каталог
    выполняет сценарии
    '''
    print_cat()

    kill_1C()

    scenario_list = return_scenario()
    params = ret_param_dict()
    params['START_TIME'] = str(datetime.now())
    proc_prior(params['PID'], 'H')

    for test in scenario_list:
        if test['PREPARE_MODE']:
            del_path(params['TEST_CATALOG'])
            del_path(params['FINAL_LOG'])
            prepare_st(params)
            create_base(params, 'manager')

        DT = test['DT']
        params['MODEL_ON_RUNNER_CURRENT_DT'] = params['MODEL_ON_RUNNER'] + DT
        params['MODEL_ADMIN_USER'] = test['ADM_USER']
        params['MODEL_USER'] = test['USER']

        del_path(params['WORK_PATH_BASE_C'] + '\\' + DT)
        create_base(params, 'client', DT)

        create_log_dir(params)

        eat_dt(params, 'manager')
        eat_dt(params, 'client')

        update_dt(params)

        reject_cd(params, DT)

        start_tests(params,
                    test['TEST_FILE'],
                    test['ADD_HEAD'],
                    test['ADD_TAIL'])

        create_final(params, test['ADD_HEAD'], test['ADD_TAIL'])

    kill_1C()
    params['END_TIME'] = str(datetime.now())

    start_debug_tests(params)



if __name__ == "__main__":
    main_func()
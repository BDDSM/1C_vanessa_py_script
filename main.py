# -*- coding: utf8 -*
#25dec19kg
#python 3.7.1

from datetime import datetime
from os import path

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
                push_cd_client,
                upd_from_repo,
                dump_cf)
from test_pars import update_test, prepare_tests, parse_name, print_cat
from proc import kill_1C, proc_prior, proc, start_servo, start_client
from log_pars import create_final
from test_start import start_debug_tests


'''
main.py - основные функции программы
'''


def update_dt(params):
    '''
    params - словарь параметров
    *
    обновляет базу на cf или из репозитория
    собирает тест для обновления в режиме предприятия
    запускает Ванессу для обновления базы в режиме предприятие
    '''
    flag_cf = True
    if params['PREPARE_MODE'] == 'uprep':
        flag_cf = path.isfile(params['WORK_PATH']+'\1Cv8.cf')
        if flag_cf:
            eat_cf(params)
        else:
            upd_from_repo(params)
    else:
        eat_cf(params)

    test_string = update_test(params)
    write_string_file(params['TESTS_ON_RUNNER'] + 'prepare.feature', 
                      'w', 
                      test_string
                      )

    start_vanessa(params, 'prepare.feature')
    if flag_cf == False:
        dump_cf(params)



def start_tests(params, test_name, addit_strings_head_rmk, addit_strings_tail, dt=''):
    '''
    params - словарь параметров
    test_name - имя общего теста который запускаем
    addit_strings_head - имя файла с тестом, тест прикрепляющийся к началу основного теста, если нужно
    addit_strings_tail - имя файла с тестом, тест прикрепляющийся к концу основного теста, если нужно
    dt - имя dt базы
    *
    собирает основные тесты для запуска
    на обнавленном эталоне запускает тесты в цикле
    ''' 
    prepare_tests(params, test_name, addit_strings_head_rmk, addit_strings_tail)
    list_tests_names = get_list_tests(params)

    for name in list_tests_names:
        push_cd_client(params, dt)
        start_vanessa(params, name)



def env_prepare(params, DT):
    '''
    params - словарь параметров
    DT - ('role.dt') имя базы-эталона для данного тестирования
    *
    все действия подготовки к запуску тестов
    '''
    PREPARE_MODE = params['PREPARE_MODE']
    if PREPARE_MODE == 'cpcf' or PREPARE_MODE == 'uprep':
        del_path(params['TEST_CATALOG'])
        del_path(params['FINAL_LOG'])
        prepare_st(params)
        create_base(params, 'manager')
        create_base(params, 'client', DT)
        create_log_dir(params)
        eat_dt(params, 'manager')
        eat_dt(params, 'client')
        update_dt(params)
        reject_cd(params, DT)
        DT = ''
    elif PREPARE_MODE == 'ret':
        create_base(params, 'client', DT)
        create_log_dir(params)
        eat_dt(params, 'manager')
        eat_dt(params, 'client')
        update_dt(params)
        reject_cd(params, DT)
        DT = ''



def main_func():
    '''
    MaiN
    получает лист со сценарием тестирования
    получает словарь с параметрами
    очищает тестовый каталог
    выполняет сценарии
    '''
    proc('set PYTHONIOENCODING=utf-8')
    print_cat()

    kill_1C()
    servo = start_servo()
    print('SERVO PID : ' + str(servo.pid) + '\n')

    scenario_list = return_scenario()
    params = ret_param_dict()
    params['START_TIME'] = str(datetime.now())

    params['CLIENT'] = start_client()

    proc_prior(params['PID'], 'H')

    for test in scenario_list:
        DT = test['DT']
        params['MODEL_ON_RUNNER_CURRENT_DT'] = params['MODEL_ON_RUNNER'] + DT
        params['MODEL_ADMIN_USER'] = test['ADM_USER']
        params['MODEL_USER'] = test['USER']
        params['PREPARE_MODE'] = test['PREPARE_MODE']

        env_prepare(params, DT)

        start_tests(params,
                    test['TEST_FILE'],
                    test['ADD_HEAD'],
                    test['ADD_TAIL'],
                    DT)

        final_error_list = create_final(params, test['ADD_HEAD'], test['ADD_TAIL'])

    params['END_TIME'] = str(datetime.now())
    start_debug_tests(params)
    params['CLIENT'].close()



if __name__ == "__main__":
    main_func()
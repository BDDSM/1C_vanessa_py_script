# -*- coding: utf8 -*
#27nov19kg
#python 3.7.1

from re import split

from prepare import open_file_r, write_list_file, write_string_file


'''
test_pars.py - подготавливает служебные тесты и конфиги, парсит тесты
'''



def va_params(param_dict, test_name):
    '''
    param_dict - словарь параметров
    test_name - имя теста, присваивается автоматически в зависимости от тэгов расставленых в фича-файле
    *
    собирает содержание json файла с настройками запуска теста для Ванессы
    нужно изменять крайне внимательно
    *
    return params - возвращает строку с содержанием файла
    '''
    feature_path = param_dict['TESTS_ON_RUNNER'] + test_name

    feature_path = feature_path.replace('\\', '\\\\')
    platform = param_dict['PLATFORM_PATH_ON_RUNNER'].replace('\\', '\\\\')
    va = param_dict['VANESSA_ON_RUNNER'].replace('\\', '\\\\')
    tests = param_dict['TESTS_ON_RUNNER'].replace('\\', '\\\\')

    params = '''{
	"Lang": "ru",
	"DebugLog": true,
	"КаталогФич": "''' + feature_path + '''",
	"ДобавлятьКИмениСценарияУсловияВыгрузки": false,
	"ИмяТекущейСборки": "Тест",
	"ЗагрузкаФичПриОткрытии": "Загружать",
	"ВерсияПлатформыДляГенерацииEPF": "''' + platform + '''\\\\bin",
        "ВыполнитьСценарии": true,
        "ЗавершитьРаботуСистемы": "''' + param_dict['ESC_VANESSA'] + '''",
        "ЗакрытьTestClientПослеЗапускаСценариев": "''' + param_dict['ESC_TEST_CLIENT'] + '''",
	"ВыполнениеСценариев": {
		"ВыполнятьШагиАссинхронно": false,
		"ИнтервалВыполненияШагаЗаданныйПользователем": 0.1,
		"ОбновлятьСтатистикуВДереве": true,
		"ОбновлятьДеревоПриНачалеВыполненияСценария": true,
		"ОстановкаПриВозникновенииОшибки": false,
		"ПоказыватьНомерСтрокиДереваПриВозникновенииОшибки": true,
		"ПриравниватьPendingКFailed": false,
		"ТаймаутДляАсинхронныхШагов": 0,
		"КоличествоСекундПоискаОкна": 5,
		"КоличествоПопытокВыполненияДействия": 3,
		"БезопасноеВыполнениеШагов": true,
		"ПаузаПриОткрытииОкна": 0
	},
	"КлиентТестирования": {
		"ЗапускатьКлиентТестированияСМаксимизированнымОкном": true,
		"ТаймаутЗапуска1С": 120,
		"ДиапазонПортовTestclient": "48100-48200",
		"ЗапускатьТестКлиентВРежимеОтладки": false,
		"КлючиОтладки": "",
		"АдресОтладчика": "",
		"ДанныеКлиентовТестирования": [
		]
	},
	"ДелатьОтчетВФорматеАллюр": false,
	"ДелатьОтчетВФорматеjUnit": false,
	"ДелатьОтчетВФорматеCucumberJson": false,
	"ДелатьОтчетВФорматеСППР": false,
	"СоздаватьИнструкциюHTML": false,
	"СоздаватьИнструкциюMarkdown": false,
	"ДелатьОтчетВоВнутреннемФормате": false,
	"КаталогиБиблиотек": "''' + va + '''features\\\Libraries",
	"ДелатьЛогВыполненияСценариевВЖР": true,
	"ДелатьЛогВыполненияСценариевВТекстовыйФайл": false,
	"ВыводитьВЛогВыполнениеШагов": false,
	"ДелатьЛогОшибокВТекстовыйФайл": false,
	"СобиратьДанныеОСостоянииАктивнойФормыПриОшибке": false,
	"СобиратьДанныеОСостоянииВсехФормПриОшибке": false,
	"ИмяФайлаЛогВыполненияСценариев": "''' + tests + test_name + '''",
	"ИмяКаталогаЛогОшибок": "''' + tests + '''",
	"КомандаСделатьСкриншот": "''' + '' + '''",
	"ДелатьСкриншотПриВозникновенииОшибки": false,
	"СниматьСкриншотКаждогоОкна1С": false,
	"КаталогПроекта": "''' + tests + '''",
	"СоздаватьИнструкциюВидео": false,
	"ИспользоватьSikuliXСервер": false,
	"ИскатьЭлементыФормыПоИмени": false,
	"ДобавлятьПриНакликиванииМетаИнформацию": false,
	"ТегTreeВключенПоУмолчанию": true
}
    '''
    print(params)
    return params



def update_test(params, usr='adm'):
    '''
    params - словарь параметров
    usr - подставлять запуск от администратора или пользователя
    *
    собирает содержание файла с тестом: "Тест обновления программы"
    нужен для обновления эталонной базы
    *
    return test - возвращает строку с содержанием файла
    '''
    if usr == 'adm':
        user = params['MODEL_ADMIN_USER']
    elif usr == 'usr':
        user = params['MODEL_USER']
    else:
        user = ''

    test = '''#language: ru 
@tree
Функциональность: тест

Контекст: 
\tИ Я закрыл все окна клиентского приложения 

@КодСценария=000000001 
Сценарий: тест

\tКогда Я подключаю клиент тестирования с параметрами: 
\t\t| \'Имя\' | \'Синоним\' | \'Порт\' | \'Строка соединения\' | \'Логин\' | \'Пароль\' | \'Запускаемая обработка\' | \'Дополнительные параметры строки запуска\' |
\t\t| \'test\' | \'\' | \'\' | \'File="''' + params['WORK_PATH_BASE_CURR'] + '''";\' | \'''' + user + '''\' | \'\' | \'\' | \'\'|
\tКогда открылось окно \'Легальность получения обновлений\' 
\tИ я изменяю флаг \'Я подтверждаю легальность получения обновления в соответствии с вышеизложенными условиями\'
\tИ я нажимаю на кнопку \'Продолжить\'
\tИ я жду открытия окна "Что нового в конфигурации Розница, редакция 2.3" в течение 600 секунд
'''
    print(test)
    return test



def head_tail_test(what, params, name):
    '''
    what - cтрока определяет будет ли тест началом 'head' или концом 'tail'
    params - словарь параметров
    name - имя теста, присваивается автоматически в зависимости от тэгов расставленых в фича-файле
    *
    присоединяет шапку и сценарий запуска базы или присоединяет к концу сценарий закрытия базы
    *
    return list_str - возвращает строку сценария для добавления
    '''
    list_str = ''

    if what == 'head':
        list_str = '''#language: ru 
@tree
Функциональность: тест

Контекст: 
\tИ Я закрыл все окна клиентского приложения 

@КодСценария=000000666 
Сценарий: ''' + name + '''

\tКогда Я подключаю клиент тестирования с параметрами: 
\t\t| \'Имя\' | \'Синоним\' | \'Порт\' | \'Строка соединения\' | \'Логин\' | \'Пароль\' | \'Запускаемая обработка\' | \'Дополнительные параметры строки запуска\' |
\t\t| \'test\' | \'\' | \'\' | \'File="''' + params['WORK_PATH_BASE_CURR'] + '''";\' | \'''' + params['MODEL_USER'] + '''\' | \'\' | \'\' | \'\'|\n
'''
    elif what == 'tail':
        list_str = '''\tИ я закрываю сеанс TESTCLIENT'''

    return list_str



def parse_name(params, name):
    '''
    params - словарь параметров
    name - имя текщуго теста
    *
    если пользователь для эталона берется из названия сценария, 
    например: название "#!$пример_теста%1_Кассир.feature" -> пользователь "1_Кассир"
    '''
    usr_list = split(r'[%.]', name)
    user = usr_list[1]
    if len(user) == 0:
        print('не корректное имя теста')
        exit()
    params['MODEL_USER'] = user
    print('USER : ' + user)



def parse_dirty_test(file_list):
    '''
    file_list - список строк теста
    *
    парсит общий общий тест по меткам "разрезая" на отдельные тесты
    метка #!$ - начало нового теста
    метка #$! - конец нового теста
    *
    return all_tests_list - возвращает список с тестами
    '''
    one_test_list = []
    all_tests_list = []
    flag = 0
    
    for i in file_list:
        if i.find("#!$") != -1:
            flag = 1
        elif i.find("#$!") != -1:
            flag = 2
            
        if flag == 1:
            one_test_list.append(i)
        elif flag == 2:
            current_test_list = one_test_list.copy()
            all_tests_list.append(current_test_list)
            one_test_list.clear()

    return all_tests_list



def write_curr_test(params, test, name, current_test_path, addit_strings_head='', addit_strings_tail=''):
    '''
    params - словарь параметров
    test - список, содержание теста
    name - имя теста
    current_test_path - текущая директория + имя теста
    addit_strings_head - имя файла с тестом, тест прикрепляющийся к началу основного теста, если нужно
    addit_strings_tail - имя файла с тестом, тест прикрепляющийся к концу основного теста, если нужно
    *
    записывает текущий тест в файл
    '''
    test_path = params['TESTS_ON_RUNNER']
    write_string_file(current_test_path, 'w', '')

    if addit_strings_head != '':
        write_string_file(current_test_path, 'w', head_tail_test('head', params, name))
        if addit_strings_head != 'only_start':
            list_addit_stings = open_file_r(test_path + '\\' + addit_strings_head + '.txt')
            write_list_file(list_addit_stings, current_test_path, 'a')

    write_list_file(test, current_test_path, 'a')

    if addit_strings_tail != '':
        list_addit_stings = open_file_r(test_path + '\\' + addit_strings_tail + '.txt')
        write_list_file(list_addit_stings, current_test_path, 'a')
    write_string_file(current_test_path, 'a', head_tail_test('tail', params, name))



def prepare_tests(params, test_name, addit_strings_head='', addit_strings_tail=''):
    '''
    params - словарь параметров
    test_name - имя общего теста
    addit_strings_head - имя файла с тестом, тест прикрепляющийся к началу основного теста, если нужно
    addit_strings_tail - имя файла с тестом, тест прикрепляющийся к концу основного теста, если нужно
    *
    "режет" общий файл с тестом на N количество основных тестов для запуска
    прикрепляет к ним "голову" и "конец" если нужно
    '''
    test_path = params['TESTS_ON_RUNNER']

    USER = params['MODEL_USER']

    test_list = open_file_r(test_path + '\\' + test_name)
    all_tests = parse_dirty_test(test_list)

    for test in all_tests:
        if len(test) == 0:
            continue
        name_list = split('[$\n]', test[0])
        name = name_list[1]

        if USER == 'take_from_testname':
            if name.find("%") != -1:
                parse_name(params, name)
                current_test_path = test_path + '\\' + '@_' + name + '.feature'
            else:
                continue
        else:
            current_test_path = test_path + '\\' + '@_' + name + '%' + params['MODEL_USER'] + '.feature'

        print(current_test_path)

        write_curr_test(params, 
                        test, 
                        name, 
                        current_test_path, 
                        addit_strings_head, addit_strings_tail)

    print('----------------------------------------------- \n')



def print_cat():
    cat = '''\n
　　　　  　 ／＞　 フ
　　　 　　 | 　_　 _|
　  　　　 ／`ミ _x 彡
　 　 　 /　　　 　 |
 　　　 /　 ヽ　　 ﾉ
　／￣|　　 |　|　|
　| (￣ヽ＿_ヽ_)_)
　＼二つ
    \n'''
    print(cat)
#Версия autoload_with_def_v.1.1.py с автоматическим перелогиниванием

import os
import random
import time as timer

from datetime import datetime, date, time, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#==== Основные параметры ===
#Опции браузера
opts = Options()
#opts.headless = False
opts.add_argument("--headless")
opts.add_argument("window-size=1300,700")
#assert opts.headless  # без графического интерфейса.

MAIN_PAGE_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/' #'http://vniims.finecosoft.ru:8080/fundmetrology/cm/'
WORK_SPACE_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/lk/calibrations/work' #'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work'

LOGIN = '9067599747' #'R-Test-002@yandex.ru'
PASSWORD = 'v8a2d346' #'3Zqov4S1!'

SET_TIME = 110 #Установка времени до следующей авторизации (в минутах)

xml_1 = 232 #980
xml_100 = 194 #820
xml_1000 = 35 #145
xml_3000 = 8 #30
xml_5000 = 1 #25
total_xml = xml_1 + xml_100 + xml_1000 + xml_3000 + xml_5000

xml_list = ['xml_1', 'xml_100', 'xml_1', 'xml_1', 'xml_100', 'xml_1', 'xml_100', 'xml_1000', 'xml_100', 'xml_1', 'xml_3000', 'xml_1', 'xml_5000', 'xml_100']

file_index_1 = 14
file_index_2 = 12
file_index_3 = 2
file_index_4 = 1
file_index_5 = 6

filename = f'logfile_test_500_5.txt'
#=============

def start_time():
    #Время запуска автозагрузки (для вычисления времени перелогинивания)
    st_time = datetime.now()
    return st_time

def login():
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:

        print('Нажатие кнопки Войти в ЛК')

        log_txt_1 = f'=== Авторизация на сайте ===\n'
        log_txt_2 = f'{datetime.now()}: Нажатие кнопки Войти в ЛК\n'
        logfile = log_txt_1 + log_txt_2
        txt.write(logfile)

        try:
            browser.find_element_by_xpath('/html/body/div/header/div/div/div[4]/a[1]').click()
            timer.sleep(2)
        except ElementNotInteractableException:
            browser.find_element_by_xpath('/html/body/div/header/a').click()
            browser.find_element_by_xpath('/html/body/div/header/div/div/div[4]/a[1]').click()

        print('Подтверждение ЕСИА')
        logfile = f'{datetime.now()}: Подтверждение ЕСИА\n'
        txt.write(logfile)

        try:
            esia_check = browser.find_element_by_xpath('//*[@id="esia_agree"]')
            esia_check.click()
            timer.sleep(4)
        except ElementNotInteractableException:
            browser.find_element_by_xpath('//*[@id="esia"]/div/div/div[2]/div/label').click()
            WebDriverWait(browser, 60).until(EC.url_changes(browser.current_url))

        print('Нажатие кнопки Подтвердить условия ЕСИА')
        logfile = f'{datetime.now()}: Нажатие кнопки Подтвердить условия ЕСИА\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="esia_login"]').click()
        timer.sleep(4)

        try:
            print('Ввод логина и пароля в ЕСИА')
            logfile = f'{datetime.now()}: Ввод логина и пароля в ЕСИА\n'
            txt.write(logfile)
            login_form = browser.find_element_by_xpath('//*[@id="mobileOrEmail"]')
            login_form.send_keys(LOGIN)
            pass_form = browser.find_element_by_xpath('//*[@id="password"]')
            pass_form.send_keys(PASSWORD)
        except ElementNotInteractableException:
            print('Ввод пароля в ЕСИА')
            pass_form = browser.find_element_by_xpath('//*[@id="password"]')
            pass_form.send_keys(PASSWORD)

        try:
            print('Нажатие кнопки Войти')
            logfile = f'{datetime.now()}: Нажатие кнопки Войти\n'
            txt.write(logfile)

            browser.find_element_by_xpath('//*[@id="loginByPwdButton"]/span').click()
            timer.sleep(5)
        except TimeoutException:
            alert_phone = browser.find_element_by_xpath('//*[@id="authnFrm"]/div[1]/div[3]/dl[1]/dd/div/div/span')
            alert = browser.find_element_by_xpath('//*[@id="authnFrm"]/div[1]/div[3]/div[2]/div/span')
            logfile = f'{datetime.now()}: Ошибка: {alert.text if alert.text else alert_phone.text}\nВыход из программы.'
            txt.write(logfile)
            browser.close()
            quit()

        print('Переход В ЛК, в раздел Рабочая область')
        logfile = f'=== Завершение авторизации ===\n'
        txt.write(logfile)
        logfile = f'{datetime.now()}: Переход В ЛК, в раздел Рабочая область\n'
        txt.write(logfile)

def logout(time_to_logout):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        log_txt = f'{datetime.now()}: Время процесса загрузки достигло {time_to_logout} мин. Запущен процесс выхода из ЛК.\n'
        txt.write(log_txt)

        browser.find_element_by_xpath('//*[@id="app-top-nav"]/ul[3]/li[1]/a').click()

        logfile = f'{datetime.now()}: Нажата кнопка "Выход"\n'
        txt.write(logfile)
        timer.sleep(5)
        print('Выход из ЛК окончен')
        logfile = f'{datetime.now()}: Выход из ЛК окончен.\n'
        txt.write(logfile)

# def choose_xml():
#     if len(xml_list) >= 2:
#         choose_xml_type = xml_list[random.randint(0, len(xml_list)-1)]
#     else:
#         choose_xml_type = xml_list[0]
#         print('Список уменьшился до одного', choose_xml_type)

    # return choose_xml_type

def upload_xml(file_index, folder, xml_type):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'==== Начало загрузки заявки ====\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_500_{folder}_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        #Путь до файла xml
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/test_500/' + str(folder) + '/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)

        if xml_type == 'xml_1' or xml_type == 'xml_100':
            browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
            WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

            timer.sleep(2)

            print(f'Файл: {filename} загружен')
            logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
            txt.write(logfile)
            timer.sleep(2)

            print('Переход в ЛК, в раздел Рабочая область')
            log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
            log_txt_2 = f'=== Окончание загрузки заявки ===\n'
            logfile =  log_txt_1 + log_txt_2
            txt.write(logfile)

            browser.get(WORK_SPACE_URL)
            timer.sleep(2)
            return 1

        elif xml_type == 'xml_1000':
            browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
            WebDriverWait(browser, 800).until(EC.url_changes(browser.current_url))

            print(f'Файл: {filename} загружен')
            logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
            txt.write(logfile)
            timer.sleep(3)

            print('Переход в ЛК, в раздел Рабочая область')
            log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
            log_txt_2 = f'=== Окончание загрузки заявки ===\n'
            logfile =  log_txt_1 + log_txt_2
            txt.write(logfile)

            browser.get(WORK_SPACE_URL)
            timer.sleep(2)
            return 1

        elif xml_type == 'xml_3000' or xml_type == 'xml_5000':
            browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()

            timer.sleep(2)
            print(f'Файл: {filename} отправлен на загрузку')
            logfile = f'{datetime.now()}: Файл: {filename} отправлен на загрузку\n'
            txt.write(logfile)

            print('Переход в ЛК, в раздел Рабочая область')
            log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
            log_txt_2 = f'=== Окончание загрузки заявки ===\n'
            logfile =  log_txt_1 + log_txt_2
            txt.write(logfile)

            timer.sleep(2)
            browser.get(WORK_SPACE_URL)
            timer.sleep(2)
            return 1

# def xml(choose_xml_type, folder, file_index_1):
#     if choose_xml_type == 'xml_1' and xml_1 != 0:
#         folder = 1
#         process = upload_xml(file_index_1, folder, choose_xml_type)
#         xml_1 -= process
#         total_xml -= 1
#         file_index_1 += 1
#         print(f'Загрузка заявки из {choose_xml_type} выполнена')
#     elif choose_xml_type == 'xml_1' and xml_1 == 0:
#         xml_list.remove(choose_xml_type)
#         log_txt = f'{datetime.now()}: Загрузка всех заявок из {choose_xml_type} окончена\n'
#         logfile = log_txt
#         txt.write(logfile)
#         print(f'Загрузка всех заявок из {choose_xml_type} окончена')


if __name__ == "__main__":
    filename = filename
    FileFullPathInfo = os.path.join(os.getcwd(), filename)  #Путь сохранения лог-файла

    with open (FileFullPathInfo, 'w', encoding='utf-8') as txt: #Если новый файл то 'w', если дозапись в файл, то 'a'

        str_1 = 'Логирование загрузки заявок\n'
        str_2 = f'Начало в {datetime.now()}\n'
        str_3 = '===============================================\n'

        logfile = str_1 + str_2 + str_3
        txt.write(logfile)

    browser = webdriver.Chrome(options=opts)
    browser.implicitly_wait(10)
    browser.get(MAIN_PAGE_URL)
        #==========================================================
    #Начинаем с авторизации
    try:
        login()
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
        print('1.Ошибку поймал, нужен рестарт логина (ошибка в авторизации, либо редиректе)')
        logfile = f'{datetime.now()}: 1. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
        txt.write(logfile)
        browser.get(MAIN_PAGE_URL)
        login()

    begin_time = start_time()
    timer.sleep(2)

    while total_xml != 0:
        real_time = datetime.now()                                      #Вычисление прошедшего времени с начала загрузки заявок (не должно превышать 120 мин.)
        time_to_logout = (real_time - begin_time).total_seconds()
        time_to_logout = int(time_to_logout)//60

        logout_timer = SET_TIME - time_to_logout

        print(f'Время до выхода из ЛК: {logout_timer} мин.')

        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            if time_to_logout >= SET_TIME:  #Установка времени до перелогинивания в минутах
                print('Выход из ЛК начат')
                logout(time_to_logout)
                timer.sleep(5)
                try:
                    login()
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                    print('3.Ошибку поймал, нужен рестарт логина (ошибка в авторизации, либо редиректе)')
                    logfile = f'{datetime.now()}: 3. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
                    txt.write(logfile)
                    browser.get(MAIN_PAGE_URL)
                    login()
                begin_time = start_time()
                print('Повторная авторизация выполнена.')
                log_txt = f'{datetime.now()}: Повторная авторизация выполнена.\n'
                txt.write(log_txt)
                timer.sleep(5)
            else:
                print('продолжаем')
                if len(xml_list) >= 2:
                    choose_xml_type = xml_list[random.randint(0, len(xml_list)-1)]
                else:
                    choose_xml_type = xml_list[0]
                    print('Список уменьшился до одного', choose_xml_type)

                if choose_xml_type == 'xml_1' and xml_1 != 0:
                    folder = 1
                    try:
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                        browser.get(MAIN_PAGE_URL)
                        process = upload_xml(file_index_1, folder, choose_xml_type)

                    xml_1 -= process
                    total_xml -= 1
                    file_index_1 += 1
                    print('Загрузка заявки из xml_1 выполнена')
                elif choose_xml_type == 'xml_1' and xml_1 == 0:
                    xml_list.remove(choose_xml_type)
                    log_txt = f'{datetime.now()}: Загрузка всех заявок из xml_1 окончена\n'
                    logfile = log_txt
                    txt.write(logfile)
                    print(f'Загрузка всех заявок из xml_1 окончена')

                if choose_xml_type == 'xml_100' and xml_100 != 0:
                    folder = 100
                    try:
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                        browser.get(MAIN_PAGE_URL)
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    xml_100 -= process
                    total_xml -= 1
                    file_index_2 += 1
                    print('Загрузка заявки из xml_100 выполнена')
                elif choose_xml_type == 'xml_100' and xml_100 == 0:
                    xml_list.remove(choose_xml_type)
                    log_txt = f'{datetime.now()}: Загрузка всех заявок из xml_100 окончена\n'
                    logfile = log_txt
                    txt.write(logfile)
                    print(f'Загрузка всех заявок из xml_100 окончена')

                if choose_xml_type == 'xml_1000' and xml_1000 != 0:
                    folder = 1000
                    try:
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                        browser.get(MAIN_PAGE_URL)
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    xml_1000 -= process
                    total_xml -= 1
                    file_index_3 += 1
                    print('Загрузка заявки из xml_1000 выполнена')
                elif choose_xml_type == 'xml_1000' and xml_1000 == 0:
                    xml_list.remove(choose_xml_type)
                    log_txt = f'{datetime.now()}: Загрузка всех заявок из xml_1000 окончена\n'
                    logfile = log_txt
                    txt.write(logfile)
                    print(f'Загрузка всех заявок из xml_1000 окончена')

                if choose_xml_type == 'xml_3000' and xml_3000 != 0:
                    folder = 3000
                    try:
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                        browser.get(MAIN_PAGE_URL)
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    xml_3000 -= process
                    total_xml -= 1
                    file_index_4 += 1
                    print('Загрузка заявки из xml_3000 выполнена')
                elif choose_xml_type == 'xml_3000' and xml_3000 == 0:
                    xml_list.remove(choose_xml_type)
                    log_txt = f'{datetime.now()}: Загрузка всех заявок из xml_3000 окончена\n'
                    logfile = log_txt
                    txt.write(logfile)
                    print(f'Загрузка всех заявок из xml_3000 окончена')

                if choose_xml_type == 'xml_5000' and xml_5000 != 0:
                    folder = 5000
                    try:
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                        browser.get(MAIN_PAGE_URL)
                        process = upload_xml(file_index_1, folder, choose_xml_type)
                    xml_5000 -= process
                    total_xml -= 1
                    file_index_5 += 1
                    print('Загрузка заявки из xml_5000 выполнена')
                elif choose_xml_type == 'xml_5000' and xml_5000 == 0:
                    xml_list.remove(choose_xml_type)
                    log_txt = f'{datetime.now()}: Загрузка всех заявок из xml_5000 окончена\n'
                    logfile = log_txt
                    txt.write(logfile)
                    print(f'Загрузка всех заявок из xml_5000 окончена')

        print(f'Осталось загрузить заявок: {total_xml}')
        #Эти данные нужны для подстановки в переменные, в случае ошибки исполнения программы. (чтобы продолжить с места остановки)
        print(f'xml_1: {xml_1} \nxml_100: {xml_100} \nxml_1000: {xml_1000} \nxml_3000: {xml_3000} \nxml_5000: {xml_5000}')
        print(f'В очереди на загрузку: \nfile_index_1: {file_index_1} \nfile_index_2: {file_index_2} \nfile_index_3: {file_index_3} \nfile_index_4: {file_index_4} \nfile_index_5: {file_index_5}')
        #timer.sleep(10)
    else:
        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Загрузка записей окончена')
            log_line = f'=================================\n'
            log_txt = f'{datetime.now()}: Загрузка записей окончена\n'
            logfile = log_line + log_txt
            txt.write(logfile)
            browser.close()
            quit()
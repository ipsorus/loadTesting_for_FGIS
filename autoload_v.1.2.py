#Версия autoload_v.1.2.py с автоматическим перелогиниванием и загрузкой индексов заявок из файла

import os
import errno
import random
import time as timer

from datetime import datetime, date, time, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#==== Основные параметры ===
#Опции браузера
opts = Options()
opts.add_argument("--headless")
opts.add_argument("window-size=1300,700")


#Для стенда разработки
# MAIN_PAGE_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/'
# WORK_SPACE_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work'

# LOGIN = 'R-*****x.ru'
# PASSWORD = '*******'
# signCipher = 'ЯЯЯ'


# Для опытного стенда
MAIN_PAGE_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/'
WORK_SPACE_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/lk/calibrations/work'

LOGIN = '*****'
PASSWORD = '******'
signCipher = 'М'

#Установка времени до следующей авторизации (в минутах)
SET_TIME = 100

#Путь до каталога с файлами
root_folder = '/test_100/'

with open('for_upload.txt', 'r') as f:
    indexes = f.read().splitlines()

xml_data = {'xml_1' : {'count' : int(indexes[0]), 'file_index' : int(indexes[5]), 'folder' : 1},
            'xml_100': {'count' : int(indexes[1]), 'file_index' : int(indexes[6]), 'folder' : 100},
            'xml_1000': {'count' : int(indexes[2]), 'file_index' : int(indexes[7]), 'folder' : 1000},
            'xml_3000': {'count' : int(indexes[3]), 'file_index' : int(indexes[8]), 'folder' : 3000},
            'xml_5000': {'count' : int(indexes[4]), 'file_index' : int(indexes[9]), 'folder' : 5000}}

xml_list = ['xml_1', 'xml_100', 'xml_1', 'xml_1000', 'xml_1', 'xml_1', 'xml_3000', 'xml_1', 'xml_100', 'xml_100', 'xml_1', 'xml_1', 'xml_100', 'xml_5000', 'xml_1', 'xml_100', 'xml_100']

total_xml = xml_data['xml_1']['count'] + xml_data['xml_100']['count'] + xml_data['xml_1000']['count'] + xml_data['xml_3000']['count'] + xml_data['xml_5000']['count']


#Название лог-файла
log_filename = f'13-07_logfile_upload_100.txt'

#Префикс названия файла
prefix = '13-07_load_100_'

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
        log_txt = f'{datetime.now()}: Время загрузки достигло {time_to_logout} мин. Запущен процесс выхода из ЛК.\n'
        txt.write(log_txt)

        browser.find_element_by_xpath('//*[@id="app-top-nav"]/ul[3]/li[1]/a').click()

        logfile = f'{datetime.now()}: Нажата кнопка "Выход"\n'
        txt.write(logfile)
        timer.sleep(5)
        print('Выход из ЛК окончен')
        logfile = f'{datetime.now()}: Выход из ЛК окончен.\n'
        txt.write(logfile)

def for_print_log(xml_type, filename):
    if xml_type == 'xml_1' or xml_type == 'xml_100':
        print(f'Файл: {filename} загружен')
        logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
        txt.write(logfile)
        timer.sleep(2)

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)
    elif xml_type == 'xml_1000':
        print(f'Файл: {filename} загружен')
        logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
        txt.write(logfile)
        timer.sleep(3)

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)
    elif xml_type == 'xml_3000' or xml_type == 'xml_5000':
        print(f'Файл: {filename} отправлен на загрузку')
        logfile = f'{datetime.now()}: Файл: {filename} отправлен на загрузку\n'
        txt.write(logfile)

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)


def upload_xml(file_index, folder, xml_type):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'==== Начало загрузки заявки ====\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button')))

        upload_item = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button')
        upload_item.click()

        filename = f'{prefix}{folder}_{file_index}_signCipher_{signCipher}.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        #Путь до файла xml
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + root_folder + str(folder) + '/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)
        timer.sleep(2)

        if xml_type == 'xml_1' or xml_type == 'xml_100':
            WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button')))
            send_item = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button')
            send_item.click()
            WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

            timer.sleep(2)
            for_print_log(xml_type, filename)

            browser.get(WORK_SPACE_URL)
            timer.sleep(2)

        elif xml_type == 'xml_1000':
            WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button')))
            send_item = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button')
            send_item.click()
            WebDriverWait(browser, 800).until(EC.url_changes(browser.current_url))

            timer.sleep(2)
            for_print_log(xml_type, filename)

            browser.get(WORK_SPACE_URL)
            timer.sleep(2)

        elif xml_type == 'xml_3000' or xml_type == 'xml_5000':
            WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button')))
            send_item = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button')
            send_item.click()
            WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

            timer.sleep(2)
            for_print_log(xml_type, filename)

            timer.sleep(2)
            browser.get(WORK_SPACE_URL)
            timer.sleep(2)

def choose_xml():
    if len(xml_list) >= 2:
        choose_xml_type = xml_list[random.randint(0, len(xml_list)-1)]
    else:
        choose_xml_type = xml_list[0]
        print(f'Список уменьшился до одного типа заявок: {choose_xml_type}')
    xml_item = xml_data[choose_xml_type]
    if xml_item['count'] != 0:
        try:
            upload_xml(xml_item['file_index'], xml_item['folder'], choose_xml_type)
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            #with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Проверить загрузку файла')
            logfile = f'{datetime.now()}: Проверить загрузку файла\n'
            txt.write(logfile)
            browser.get(WORK_SPACE_URL)
            timer.sleep(2)
            #upload_xml(xml_item['file_index'], xml_item['folder'], choose_xml_type)
        xml_item['count'] -= 1
        xml_item['file_index'] += 1

        print(f'Загрузка заявки из {choose_xml_type} выполнена')
        return 1

    elif xml_item['count'] == 0:
        xml_list.remove(choose_xml_type)
        log_txt = f'{datetime.now()}: Загрузка всех заявок из {choose_xml_type} окончена\n'
        logfile = log_txt
        txt.write(logfile)
        print(f'Загрузка всех заявок из {choose_xml_type} окончена')
        return 0


if __name__ == "__main__":
    browser = webdriver.Chrome(options=opts)
    browser.implicitly_wait(10)
    browser.get(MAIN_PAGE_URL)

    l_filename = log_filename
    FileFullPathInfo = os.path.join(os.getcwd(), l_filename)  #Путь сохранения лог-файла

    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt: #Для записи лог-файла
        str_1 = 'Логирования загрузки заявок\n'
        str_2 = f'Начало в {datetime.now()}\n'
        str_3 = '===============================================\n'

        logfile = str_1 + str_2 + str_3
        txt.write(logfile)

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
                    print('2.Ошибку поймал, нужен рестарт логина (ошибка в авторизации, либо редиректе)')
                    logfile = f'{datetime.now()}: 2. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
                    txt.write(logfile)
                    browser.get(MAIN_PAGE_URL)
                    timer.sleep(5)
                    login()
                begin_time = start_time()
                print('Повторная авторизация выполнена.')
                log_txt = f'{datetime.now()}: Повторная авторизация выполнена.\n'
                txt.write(log_txt)
                timer.sleep(5)
            else:
                print('продолжаем')
                res = choose_xml()
                total_xml -= res

        print(f'Осталось загрузить заявок: {total_xml}')
        #Эти данные нужны для подстановки в переменные, в случае ошибки исполнения программы. (чтобы продолжить с места остановки)
        print(f"xml_1: {xml_data['xml_1']['count']}\nxml_100: {xml_data['xml_100']['count']}\nxml_1000: {xml_data['xml_1000']['count']}\nxml_3000: {xml_data['xml_3000']['count']}\nxml_5000: {xml_data['xml_5000']['count']}")
        print(f"В очереди на загрузку: \nfile_index_1: {xml_data['xml_1']['file_index']}\nfile_index_2: {xml_data['xml_100']['file_index']}\nfile_index_3: {xml_data['xml_1000']['file_index']}\nfile_index_4: {xml_data['xml_3000']['file_index']}\nfile_index_5: {xml_data['xml_5000']['file_index']}")
        #timer.sleep(10)

        #Запись индексов загруженных файлов для служебного файла.
        log_index_file = f'for_upload.txt'
        LogFullPath = os.path.join(os.getcwd(), log_index_file)

        with open (LogFullPath, 'w', encoding='utf-8') as upload_indexes:
            str_1 = f"{xml_data['xml_1']['count']}\n{xml_data['xml_100']['count']}\n{xml_data['xml_1000']['count']}\n{xml_data['xml_3000']['count']}\n{xml_data['xml_5000']['count']}"
            str_2 = f"{xml_data['xml_1']['file_index']}\n{xml_data['xml_100']['file_index']}\n{xml_data['xml_1000']['file_index']}\n{xml_data['xml_3000']['file_index']}\n{xml_data['xml_5000']['file_index']}"
            info_file = str_1 + '\n' + str_2
            upload_indexes.write(info_file)
    else:
        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Загрузка заявок окончена')
            log_line = f'=================================\n'
            log_txt = f'{datetime.now()}: Загрузка заявок окончена\n'
            logfile = log_line + log_txt
            txt.write(logfile)
            browser.close()
            quit()

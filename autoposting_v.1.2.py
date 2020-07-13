#Версия autoposting_v.1.2.py изменение логики сбора id и отправки заявок

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

# #============================
# #Для стенда разработки
MAIN_PAGE_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/'

#!!!Удалить в конце ссылки всё до слова "CREATED"
WORK_SPACE_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications?createDatePeriodBegin=2020-07-10&createDatePeriodEnd=2020-07-11&status=CREATED'
SINGLE_APPLIC_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/'

LOGIN = 'R-Test-002@yandex.ru'
PASSWORD = '3Zqov4S1!'
signCipher = 'ЯЯЯ'
# #============================

#============================
# Для опытного стенда
# MAIN_PAGE_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/'

# #!!!Удалить в конце ссылки всё до слова "CREATED"
# WORK_SPACE_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/lk/applications?createDatePeriodBegin=2020-07-08&createDatePeriodEnd=2020-07-09&status=CREATED'

# SINGLE_APPLIC_URL = 'https://fgis.gost.ru/fundmetrologytest/cm/lk/applications/'

# LOGIN = '9067599747'
# PASSWORD = 'v8a2d346'
# signCipher = 'М'
#===========================

#Установка времени до следующей авторизации (в минутах)
SET_TIME = 100

#Название лог-файла
log_filename = f'10-07_logfile_finecosoft_posting_100.txt'
#=============

def start_time():
    #Время запуска автопостинга (для вычисления времени перелогинивания)
    st_time = datetime.now()
    return st_time

def login():
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:

        print('Нажатие кнопки Войти в ЛК')

        log_txt_1 = f'========= Авторизация на сайте =========\n'
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
            logfile = f'{datetime.now()}: Ввод пароля в ЕСИА\n'
            txt.write(logfile)
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
        logfile = f'========= Завершение авторизации =========\n'
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

def public(item_id):
    timer.sleep(4)
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        item_url = f'{SINGLE_APPLIC_URL}{item_id}'
        browser.get(item_url)
        timer.sleep(3)
        WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button')))
        post = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div[1]/div/section/div/div/div[1]/div[3]/button')
        post.click()
        log_txt_1 = f'===================================================\n'
        log_txt_2 = f'{datetime.now()}: Заявка с id: {item_id} отправлена\n'
        log_string = log_txt_1 + log_txt_2
        txt.write(log_string)
        print(f'Заявка с id: {item_id} отправлена')

        timer.sleep(4)

        return item_id

def get_id():
    rows = 50 #Отображаемое количество записей на странице
    browser.get(f'{WORK_SPACE_URL}&rows={rows}')
    timer.sleep(5)
    zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')
    counter = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[1]/div[1]/div/div[1]/span').text
    symbols = counter.split(' ')
    total = symbols[-1]
    timer.sleep(10)
    print(f'Всего заявок: {total}')

    str_1 = f'{datetime.now()}: Получение количества заявок..\n'
    str_2 = f'{datetime.now()}: Количество заявок для публикации: {total}\n'
    logfile = str_1 + str_2
    txt.write(logfile)

    items = zayvki.find_elements_by_tag_name("tr")

    #Вычисление количества страниц
    pages = int(total) // rows
    last_page = int(total) % rows
    if last_page != 0:
        pages += 1

    #Запись id заявок в файл.
    items_file = 'autoposting_list_of_id.txt'
    ItemsFullPath = os.path.join(os.getcwd(), items_file)

    with open (ItemsFullPath, 'a', encoding='utf-8') as id_s:
        for i in range(pages):
            browser.get(f'{WORK_SPACE_URL}&page={i+1}&rows={rows}')
            timer.sleep(10)
            zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')
            items = zayvki.find_elements_by_tag_name("tr")

            for k in range(len(items)):
                item_id = items[k].get_attribute("id")
                item_id = item_id.lstrip('item_')
                if item_id not in id_list:
                    id_list.append(item_id)

                    info_file = f'{item_id}\n'
                    id_s.write(info_file)

            print(id_list)
            print('Длина списка', len(id_list))
            logfile = f'{datetime.now()}: Заявки добавлены, общее количество: {len(id_list)}.\n'
            txt.write(logfile)
        logfile = f'{datetime.now()}: Сборка списка id заявок окончена.\n'
        txt.write(logfile)
        print('Перемешивание списка..')
        logfile = f'{datetime.now()}: Перемешивание списка заявок..\n'
        txt.write(logfile)
        random.shuffle(id_list)
        print('Перемешивание списка окончено')
        logfile = f'{datetime.now()}: Перемешивание списка заявок окончено.\n'
        txt.write(logfile)


    return id_list

def get_next_item(items_list):
    nxt_item = items_list[0]
    return nxt_item

def rewrite_list(items_list):
    items_file = 'autoposting_list_of_id.txt'
    ItemsFullPath = os.path.join(os.getcwd(), items_file)

    with open (ItemsFullPath, 'w', encoding='utf-8') as id_s:
        for i in range(len(items_list)):
            info_file = f'{items_list[i]}\n'
            id_s.write(info_file)

if __name__ == "__main__":
    browser = webdriver.Chrome(options=opts)
    browser.implicitly_wait(10)
    browser.get(MAIN_PAGE_URL)

    l_filename = log_filename
    FileFullPathInfo = os.path.join(os.getcwd(), l_filename)  #Путь сохранения лог-файла

    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt: #Для записи лог-файла

        str_1 = '========= Логирование отправки заявок =========\n'
        str_2 = f'{datetime.now()}: Начало отправки заявок\n'
        str_3 = '===============================================\n'

        logfile = str_1 + str_2 + str_3
        txt.write(logfile)

        timer.sleep(4)

        #==========================================================
        #Авторизация
        try:
            login()
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            print('1. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).')
            logfile = f'{datetime.now()}: 1. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
            txt.write(logfile)
            browser.get(MAIN_PAGE_URL)
            login()

    begin_time = start_time()
    timer.sleep(2)

    id_list = []
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        try:
            with open('autoposting_list_of_id.txt', 'r') as f:
                spisok = f.read().splitlines()
                if len(spisok) == 0:
                    print('Список id был пуст. Список id для заявок будет собран из ЛК.')
                    res = get_id()
                    id_list = res
                else:
                    id_list = spisok
                    print('Список id для заявок получен из файла.')
                    logfile = f'{datetime.now()}: Список id для заявок получен из файла.\n'
                    txt.write(logfile)
        except OSError as e:
            res = get_id()
            id_list = res
            print('Список id для заявок собран из ЛК.')
            logfile = f'{datetime.now()}: Список id для заявок собран из ЛК.\n'
            txt.write(logfile)

        str_1 = '===============================================\n'
        str_2 = f'{datetime.now()}: Начало отправки заявок по списку\n'
        str_3 = '===============================================\n'

        logfile = str_1 + str_2 + str_3
        txt.write(logfile)


    while len(id_list) != 0:
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
                    print('2. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).')
                    logfile = f'{datetime.now()}: 2. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
                    txt.write(logfile)
                    browser.get(MAIN_PAGE_URL)
                    login()
                begin_time = start_time()
                print('Повторная авторизация выполнена.')
                log_txt = f'{datetime.now()}: Повторная авторизация выполнена.\n'
                txt.write(log_txt)
                timer.sleep(5)
            else:
                print('Отправка продолжается..')
                try:
                    next_id = get_next_item(id_list)
                    result = public(next_id)
                    id_list.remove(result)
                    rewrite_list(id_list)
                    print(f'id {result} удален из списка')
                    logfile = f'{datetime.now()}: id {result} удален из списка.\n'
                    txt.write(logfile)
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                    timer.sleep(20)
                    print('Повторная попытка отправки')
                    str_1 = f'{datetime.now()}: Повторная отправка заявки.\n'
                    next_id = get_next_item(id_list)
                    result = public(next_id)
                    id_list.remove(result)
                    rewrite_list(id_list)
                    print(f'id {result} удален из списка')
                    str_2 = f'{datetime.now()}: id {result} удален из списка.\n'
                    logfile = str_1 + str_2
                    txt.write(logfile)

                print(f'Всего осталось заявок: {len(id_list)}')

    else:
        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Отправка заявок окончена')
            log_line = f'=================================\n'
            log_txt = f'{datetime.now()}: Отправка заявок окончена\n'
            logfile = log_line + log_txt
            txt.write(logfile)
            browser.close()
            quit()
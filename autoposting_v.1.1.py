#Версия autoposting__with_def_v.1.1.py с автоматическим перелогиниванием и отправкой по одной заявке

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

opts.add_argument("--headless")
opts.add_argument("window-size=1300,700")


#Для стенда разработки
# MAIN_PAGE_URL = '***'
# WORK_SPACE_URL = '***'

# LOGIN = 'R-***u'
# PASSWORD = '**'
# signCipher = 'ЯЯЯ'


# Для опытного стенда
MAIN_PAGE_URL = '***'
WORK_SPACE_URL = '***'

LOGIN = '****'
PASSWORD = '***'
signCipher = 'М'


#Установка времени до следующей авторизации (в минутах)
SET_TIME = 100


#Список отправленных заявок по id
id_list = []

#Общее количество отправленных заявок
total_posted = 0

#Индекс для лог-файла, в случае повторной загрузки скрипта для продолжения

with open('logfile_index_posting.txt', 'r') as f:
    indexes = f.read().splitlines()

log_index = int(indexes[0])

#Название лог-файла
l_filename = f'logfile_loadTest_2000_posting_part_{log_index}.txt'

#Стартовый id заявки (для перезапуска скрипта)
id_index = int(indexes[1])
#=============

def start_time():
    #Время запуска автопостинга (для вычисления времени перелогинивания)
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

def public(item_id):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        item_url = 'https://fgis.gost.ru/fundmetrologytest/cm/lk/applications/' + item_id
        browser.get(item_url)
        timer.sleep(3)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div[1]/div/section/div/div/div[1]/div[3]/button').click()
        log_txt_1 = f'===================================================\n'
        log_txt_2 = f'{datetime.now()}: Заявка с id: {item_id} отправлена\n'
        log_string = log_txt_1 + log_txt_2
        txt.write(log_string)

        timer.sleep(4)

        id_list.append(item_id)

        log_txt_1 = f'{datetime.now()}: id: {item_id} добавлен в список\n'
        log_txt_2 = f'===================================================\n'
        log_string = log_txt_1 + log_txt_2
        txt.write(log_string)

        return item_id


def next_index():
    browser.get(WORK_SPACE_URL)
    timer.sleep(3)
    zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')

    items = zayvki.find_elements_by_tag_name("tr")
    item_id = items[0].get_attribute("id")
    item_id = item_id.lstrip('item_')

    return item_id

def next_index_long_sleep():
    browser.get(WORK_SPACE_URL)
    timer.sleep(5)
    zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')

    items = zayvki.find_elements_by_tag_name("tr")
    item_id = items[0].get_attribute("id")
    item_id = item_id.lstrip('item_')

    return item_id

def count_items():

    browser.get(WORK_SPACE_URL)
    timer.sleep(5)
    zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')
    items = zayvki.find_elements_by_tag_name("tr")

    counter = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[1]/div[1]/div/div[1]/span').text
    symbols = counter.split(' ')
    total = symbols[-1]

    print(f'Осталось заявок: {total}')

    return len(items), total

if __name__ == "__main__":
    browser = webdriver.Chrome(options=opts)
    browser.implicitly_wait(10)
    browser.get(MAIN_PAGE_URL)

    log_filename = l_filename
    FileFullPathInfo = os.path.join(os.getcwd(), log_filename)  #Путь сохранения лог-файла

    #Логирование отправленных заявок.
    log_id = f'logfile_record_id_part_{log_index}.txt'
    LogIdFullPath = os.path.join(os.getcwd(), log_id)

    with open (LogIdFullPath, 'w', encoding='utf-8') as posting_ids:
        log_index += 1

    with open (FileFullPathInfo, 'w', encoding='utf-8') as txt: #Если новый файл то 'w', если дозапись в файл, то 'a'

        str_1 = 'Логирование отправки заявок\n'
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

    try:
        len_items, total_item = count_items()
    except (TimeoutException, ElementClickInterceptedException):
        print('2.Ошибку поймал, нужен рестарт логина (ошибка во время проверки и подсчета списка заявок)')
        logfile = f'{datetime.now()}: 2. Аварийное завершение, повторная авторизация (ошибка во время проверки и подсчета списка заявок).\n'
        len_items, total_item = count_items()

    print(f'Количество строк записей для отправки {len_items}, всего заявок осталось {total_item}')

    while len_items != 0:
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
                try:
                    next_id = next_index()
                except IndexError:
                    next_id = next_index_long_sleep()

                #Счетчик попыток получения id у новой заявки
                count_try = 0

                while next_id == id_index:
                    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
                        try:
                            next_id = next_index()
                            print(f'Получение id {next_id}')
                        except IndexError:
                            next_id = next_index_long_sleep()
                            print(f'Получение id {next_id}')

                        if next_id == id_index:

                            if count_try <= 3:
                                print('Ждем 10 сек')
                                log_txt = f'{datetime.now()}: Количество попыток получения нового id {count_try}, ожидание 10 сек.\n'
                                txt.write(log_txt)
                                timer.sleep(10)
                            elif count_try >= 4:
                                print('Ждем 60 сек')
                                log_txt = f'{datetime.now()}: Количество попыток получения нового id {count_try}, ожидание 60 сек.\n'
                                txt.write(log_txt)
                                timer.sleep(60)
                            count_try += 1
                        else:
                            break

                try:
                    result_id = public(next_id)
                    print(f'Заявка с id {result_id} отправлена')
                except (IndexError):
                    result_id = public(next_id)
                    print('Произошла ошибка IndexError')
                    print(f'Заявка с id {result_id} отправлена')
                    log_txt = f'{datetime.now()}: Произошла ошибка IndexError. Повторная отправка на публикацию выполнена.\n'
                    txt.write(log_txt)

                #Присвоение переменной нового индекса (для последующего использования в цикле while)
                id_index = result_id

                #Логирование отправленных заявок.
                with open (LogIdFullPath, 'a', encoding='utf-8') as posting_ids:
                    info_file = f'{id_index}\n'
                    posting_ids.write(info_file)

                with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
                    total_posted += 1
                    print(f'Общее количество отправленных заявок: {total_posted}')
                    log_txt_1 = f'==========================================\n'
                    log_txt_2 = f'{datetime.now()}: Общее количество отправленных заявок: {total_posted}\n'
                    log_txt_3 = f'==========================================\n'
                    log_string = log_txt_1 + log_txt_2 + log_txt_3
                    txt.write(log_string)

                print('Поиск записи для публикации...')
                try:
                    len_items, total_item = count_items()
                except (TimeoutException, ElementClickInterceptedException, NoSuchElementException):
                    print('3.Ошибку поймал, нужен повторный поиск записи (ошибка во время проверки и подсчета списка заявок)')
                    logfile = f'{datetime.now()}: 3. Аварийное завершение, повторный поиск записи (ошибка во время проверки и подсчета списка заявок).\n'
                    timer.sleep(2)
                    len_items, total_item = count_items()
                print(f'Запись для публикации найдена {len_items}, всего осталось {total_item}')

                #Логирование индексов лог-файлов.
                log_index_file = f'logfile_index_posting.txt'
                LogFullPath = os.path.join(os.getcwd(), log_index_file)

                with open (LogFullPath, 'w', encoding='utf-8') as indexes:
                    info_file = f'{log_index}\n{id_index}\n'
                    indexes.write(info_file)

                # try:
                #     next_id = next_index()
                #     result_id = public(next_id)
                #     print(f'Заявка с id {next_id} отправлена')
                # except (IndexError, TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                #     next_id = next_index_long_sleep()
                #     result_id = public(next_id)
                #     print('Произошла ошибка IndexError')
                #     print(f'Заявка с id {next_id} отправлена')
                #     log_txt = f'{datetime.now()}: Произошла ошибка IndexError. Повторная отправка на публикацию выполнена.\n'
                #     txt.write(log_txt)

                # total_posted += 1
                # print(f'Общее количество отправленных заявок: {total_posted}')
                # log_txt_1 = f'==========================================\n'
                # log_txt_2 = f'{datetime.now()}: Общее количество отправленных заявок: {total_posted}\n'
                # log_txt_3 = f'==========================================\n'
                # log_string = log_txt_1 + log_txt_2 + log_txt_3
                # txt.write(log_string)

                # print(f'Проверка изменения id заявки для следующей публикации')
                # log_txt = f'{datetime.now()}: Проверка изменения id заявки для следующей публикации.\n'
                # txt.write(log_txt)

                # try:
                #     next_id = next_index()
                # except IndexError:
                #     next_id = next_index_long_sleep()

                # print(f'Запрошенный id: {next_id}')

                # print(id_list)

                # #Логирование отправленных заявок.
                # with open (LogFullPath, 'a', encoding='utf-8') as posting_ids:
                #     info_file = f'{next_id}\n'
                #     posting_ids.write(info_file)

                # #Счетчик попыток получения id у новой заявки
                # count_try = 0

                # while next_id in id_list:
                #     with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
                #         try:
                #             next_id = next_index()
                #             print(f'Получение id {next_id}')
                #         except IndexError:
                #             next_id = next_index_long_sleep()
                #             print(f'Получение id {next_id}')

                #         if count_try <= 2:
                #             print('Ждем 10 сек')
                #             log_txt = f'{datetime.now()}: Количество попыток получения нового id {count_try}, ожидание 10 сек.\n'
                #             txt.write(log_txt)
                #             timer.sleep(10)
                #         elif count_try == 3:
                #             print('Ждем 60 сек')
                #             log_txt = f'{datetime.now()}: Количество попыток получения нового id {count_try}, ожидание 60 сек.\n'
                #             txt.write(log_txt)
                #             timer.sleep(60)

                #     count_try += 1


                # print('Подсчет записей на странице...')
                # try:
                #     len_items = count_items()
                # except (TimeoutException, ElementClickInterceptedException):
                #     print('3.Ошибку поймал, нужен рестарт логина (ошибка во время проверки и подсчета списка заявок)')
                #     logfile = f'{datetime.now()}: 3. Аварийное завершение, повторная авторизация (ошибка во время проверки и подсчета списка заявок).\n'
                #     len_items = count_items()
                # print(f'Количество строк записей вычислено {len_items}')

                # #Логирование индексов лог-файлов.
                # log_index_file = f'logfile_index_posting.txt'
                # LogFullPath = os.path.join(os.getcwd(), log_index_file)

                # with open (LogFullPath, 'w', encoding='utf-8') as indexes:
                #     info_file = f'{log_index}\n{next_id}\n'
                #     indexes.write(info_file)


    else:
        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Отправка заявок окончена')
            log_line = f'=================================\n'
            log_txt = f'{datetime.now()}: Отправка заявок окончена\n'
            logfile = log_line + log_txt
            txt.write(logfile)
            browser.close()
            quit()

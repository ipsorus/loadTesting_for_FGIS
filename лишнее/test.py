
import os
import errno
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
#opts.add_argument("--headless")
opts.add_argument("window-size=1300,700")

#Для стенда разработки
MAIN_PAGE_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/'
WORK_SPACE_URL = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work'

LOGIN = 'R-Test-002@yandex.ru'
PASSWORD = '3Zqov4S1!'
signCipher = 'ЯЯЯ'

SET_TIME = 5 #Установка времени до следующей авторизации (в минутах)

log_filename = f'test_log.txt'

#======================================================================

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

def public(item_id):
    item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id
    browser.get(item_url)
    timer.sleep(3)
    #browser.find_element_by_xpath('//*[@id="app-wrapper"]/div[1]/div/section/div/div/div[1]/div[3]/button').click()
    return item_id


def get_id():
    #Количество записей на странице
    rows = 50
    browser.get(f'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications?createDatePeriodBegin=2020-06-22&createDatePeriodEnd=2020-06-23&status=CREATED&rows={rows}')
    timer.sleep(5)
    zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')
    counter = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[1]/div[1]/div/div[1]/span').text
    symbols = counter.split(' ')
    total = symbols[-1]

    print(f'Осталось заявок: {total}')

    items = zayvki.find_elements_by_tag_name("tr")

    pages = int(total) // rows
    last_page = int(total) % rows
    if last_page != 0:
        pages += 1
    #Логирование индексов лог-файлов.
    items_file = f'list_of_id.txt'
    ItemsFullPath = os.path.join(os.getcwd(), items_file)

    with open (ItemsFullPath, 'a', encoding='utf-8') as id_s:
        for i in range(pages):
            browser.get(f'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications?createDatePeriodBegin=2020-06-22&createDatePeriodEnd=2020-06-23&status=CREATED&page={i+1}&rows={rows}')
            timer.sleep(5)
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

    return id_list

def get_next_item(items_list):
    nxt_item = items_list[0]
    return nxt_item

def rewrite_list(items_list):
    items_file = f'list_of_id.txt'
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

        str_1 = 'Логирование загрузки заявок\n'
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

    id_list = []
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt: #Для записи лог-файла
        try:
            with open('list_of_id.txt', 'r') as f:
                id_list = f.read().splitlines()
                print('Список id для записей получен из файла.')
                logfile = f'{datetime.now()}: Список id для записей получен из файла.\n'
                txt.write(logfile)
        except OSError as e:
            res = get_id()
            id_list = res
            print('Список id для записей собран.')
            logfile = f'{datetime.now()}: Список id для записей собран.\n'
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
                print('Отправка продолжается..')
                try:
                    next_id = get_next_item(id_list)
                    result = public(next_id)
                    id_list.remove(result)
                    rewrite_list(id_list)
                    print(f'{result} удален из списка')
                except (NoSuchElementException, ElementClickInterceptedException):
                    next_id = get_next_item(id_list)
                    result = public(next_id)
                    id_list.remove(result)
                    rewrite_list(id_list)
                    print(f'{result} удален из списка')

                print(f'Всего осталось заявок: {len(id_list)}')

                # try:
                #     next_id = next_index()
                # except IndexError:
                #     next_id = next_index_long_sleep()

                # print(f'После выполнения функции {result}')

                # print(id_list)

                # count_try = 0

                # while next_id in id_list:
                #     try:
                #         next_id = next_index()
                #         print(f'Вычисление ид в цикле {next_id}')
                #     except IndexError:
                #         next_id = next_index_long_sleep()
                #         print(f'Вычисление ид в цикле {next_id}')

                #     if count_try <= 1:
                #         print('Ждем 10 сек')
                #         timer.sleep(5)
                #     elif count_try == 2:
                #         print('Ждем 60 сек')
                #         timer.sleep(60)

                #     count_try += 1

                # print('Подсчет записей на странице...')
                # try:
                #     len_items, total_item = count_items()
                # except (TimeoutException, ElementClickInterceptedException):
                #     print('2.Ошибку поймал, нужен рестарт логина (ошибка во время проверки и подсчета списка заявок)')
                #     logfile = f'{datetime.now()}: 2. Аварийное завершение, повторная авторизация (ошибка во время проверки и подсчета списка заявок).\n'
                #     len_items, total_item = count_items()
                # print(f'Количество строк записей вычислено {len_items}, всего осталось {total_item}')


    else:
        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Загрузка записей окончена')
            log_line = f'=================================\n'
            log_txt = f'{datetime.now()}: Загрузка записей окончена\n'
            logfile = log_line + log_txt
            txt.write(logfile)
            browser.close()
            quit()


#===============================================
# with open('logfile_indexes.txt', 'r') as f:
#     indexes = f.read().splitlines()

# xml_data = {'xml_1' : {'count' : indexes[0], 'file_index' : indexes[5], 'folder' : 1},
#             'xml_100': {'count' : indexes[1], 'file_index' : indexes[6], 'folder' : 100},
#             'xml_1000': {'count' : indexes[2], 'file_index' : indexes[7], 'folder' : 1000},
#             'xml_3000': {'count' : indexes[3], 'file_index' : indexes[8], 'folder' : 3000},
#             'xml_5000': {'count' : indexes[4], 'file_index' : indexes[9], 'folder' : 5000}}
# print(xml_data)
#==================================
# from random import randint, choice

# xml_data = {'xml_1' : {'count' : 10, 'file_index' : 1, 'folder' : 1}, 'xml_100': {'count' : 5, 'file_index' : 1, 'folder' : 100}}
# xml_list = ['xml_1', 'xml_100']

# total_xml = xml_data['xml_1']['count'] + xml_data['xml_100']['count']
# print (total_xml)

# def test_xml():
#     if len(xml_list) >= 2:
#         choose_xml_type = xml_list[randint(0, len(xml_list)-1)]
#     else:
#         choose_xml_type = xml_list[0]
#         print(f'Список уменьшился до одного типа заявок: {choose_xml_type}')
#     xml_item = xml_data[choose_xml_type]
#     if xml_item['count'] != 0:
#         #process = upload_xml(xml_item['file_index'], xml_item['folder'], choose_xml_type)
#         xml_item['count'] -= 1
#         xml_item['file_index'] += 1

#         print(f'Загрузка заявки из {choose_xml_type} выполнена')

#         print(xml_item['count'])
#         print(xml_item['file_index'])

#         return 1

#     elif xml_item['count'] == 0:
#         xml_list.remove(choose_xml_type)
#         #log_txt = f'{datetime.now()}: Загрузка всех заявок из xml_1 окончена\n'
#         #logfile = log_txt
#         #txt.write(logfile)
#         print(f'Загрузка всех заявок из {choose_xml_type} окончена')
#         return 0


# if __name__ == "__main__":
#     while total_xml != 0:
#         # if len(xml_list) >= 2:
#         #     choose_xml_type = xml_list[randint(0, len(xml_list)-1)]
#         # else:
#         #     choose_xml_type = xml_list[0]
#         #     print('Список уменьшился до одного', choose_xml_type)

#         res = test_xml()
#         total_xml -= res #process
#     else:
#         print('Загрузка всех записей окончена')
# ===============================================================================
# import os
# import requests
# from datetime import datetime, date, time, timedelta
# import time as timer

# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

# from random import randint, choice

# xml_list = ['xml_1', 'xml_100', 'xml_1000', 'xml_3000', 'xml_5000']

# xml_1 = 0
# xml_100 = 0
# xml_1000 = 0
# xml_3000 = 0
# xml_5000 = 0

# for i in range(150):
#     choose_xml_type = choice(xml_list)
#     if choose_xml_type == 'xml_1':
#         xml_1 += 1
#     elif choose_xml_type == 'xml_100':
#         xml_100 += 1
#     elif choose_xml_type == 'xml_1000':
#         xml_1000 += 1
#     elif choose_xml_type == 'xml_3000':
#         xml_3000 += 1
#     elif choose_xml_type == 'xml_5000':
#         xml_5000 += 1
# print(xml_1, xml_100, xml_1000, xml_3000, xml_5000)


# xml_list = ['xml_1', 'xml_100', 'xml_1000', 'xml_3000', 'xml_5000']

# xml_1 = 0
# xml_100 = 0
# xml_1000 = 0
# xml_3000 = 0
# xml_5000 = 0

# for i in range(150):
#     choose_xml_type = xml_list[randint(0, len(xml_list)-1)]
#     if choose_xml_type == 'xml_1':
#         xml_1 += 1
#     elif choose_xml_type == 'xml_100':
#         xml_100 += 1
#     elif choose_xml_type == 'xml_1000':
#         xml_1000 += 1
#     elif choose_xml_type == 'xml_3000':
#         xml_3000 += 1
#     elif choose_xml_type == 'xml_5000':
#         xml_5000 += 1
# print(xml_1, xml_100, xml_1000, xml_3000, xml_5000)




#start_time = datetime.now()
#start_time = start_time
# print(start_time)
# for i in range(10):
#     timer.sleep(60)

#     real_time = datetime.now() 

#     #real_time = result.strftime("%I:%M")
#     time_to_logout = (real_time - start_time).total_seconds()
#     time_to_logout = int(time_to_logout)//60
#     #time_to_logout.strftime("%I:%M")

#     print(time_to_logout)

#     if time_to_logout >= 9:
#         print('logout')
#     else:
#         print('продолжаем')

# last_page = 40



# middle_page = last_page//2
# end_page = last_page
# page_list = [1, middle_page, end_page]
# page_index = 0


# for i in range(10):
#     current_page = page_list[page_index]
#     page_index += 1
#     if page_index == 3:
#         page_index = 0
#     print(current_page)



        #print(choose_xml_type[1])
        #print(choose_xml_type[2])

        #total_xml -= 1


        #test_xml(choose_xml_type, xml_data[choose_xml_type][0], xml_data[choose_xml_type][1], xml_data[choose_xml_type][2])




    # xml_list = ['xml_1', 'xml_100', 'xml_1', 'xml_1', 'xml_100', 'xml_1', 'xml_100', 'xml_1000', 'xml_100', 'xml_1', 'xml_3000', 'xml_1', 'xml_5000', 'xml_100']
    # for i in range(len(xml_list)-1):
        
    #     choose_xml_type = xml_list[random.randint(0, len(xml_list)-1)]
    #     print(choose_xml_type)
    #     xml_list.remove(choose_xml_type)
    #     print(xml_list)


# for j in range(2):
#     print(j)
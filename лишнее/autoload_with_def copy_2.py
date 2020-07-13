import os
import random
import time as timer

from datetime import datetime, date, time, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

filename = 'logfile.txt'
FileFullPathInfo = os.path.join(os.getcwd(), filename)  #Путь сохранения лог-файла

with open (FileFullPathInfo, 'w', encoding='utf-8') as txt:

    str_1 = 'Логирование загрузки заявок\n'
    str_2 = f'Начало в {datetime.now()}\n'
    str_3 = '=========================================================\n'

    logfile = str_1 + str_2 + str_3
    txt.write(logfile)

opts = Options()
opts.set_headless()
assert opts.headless  # без графического интерфейса.

browser = webdriver.Chrome(options=opts)
browser.implicitly_wait(10)
browser.get("http://vniims.finecosoft.ru:8080/fundmetrology/cm/")
#time.sleep(5)


def login():
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:

        print('Нажатие кнопки Войти в ЛК')

        log_txt_1 = f'=== Авторизация на сайте ===\n'
        log_txt_2 = f'{datetime.now()}: Нажатие кнопки Войти в ЛК\n'
        logfile = log_txt_1 + log_txt_2
        txt.write(logfile)

        try:
            browser.find_element_by_xpath('/html/body/div/header/div/div/div[4]/a[1]').click()
            time.sleep(2)
        except ElementNotInteractableException:
            browser.find_element_by_xpath('/html/body/div/header/a').click()
            browser.find_element_by_xpath('/html/body/div/header/div/div/div[4]/a[1]').click()

        print('Подтверждение ЕСИА')
        logfile = f'{datetime.now()}: Подтверждение ЕСИА\n'
        txt.write(logfile)

        #time.sleep(2)
        esia_check = browser.find_element_by_xpath('//*[@id="esia_agree"]')
        #time.sleep(2)
        esia_check.click()

        print('Нажатие кнопки Подтвердить условия ЕСИА')
        logfile = f'{datetime.now()}: Нажатие кнопки Подтвердить условия ЕСИА\n'
        txt.write(logfile)
        #time.sleep(1)
        browser.find_element_by_xpath('//*[@id="esia_login"]').click()

        print('Ввод логина и пароля в ЕСИА')
        logfile = f'{datetime.now()}: Ввод логина и пароля в ЕСИА\n'
        txt.write(logfile)
        #time.sleep(5)
        login_form = browser.find_element_by_xpath('//*[@id="mobileOrEmail"]')
        login_form.send_keys('R-Test-002@yandex.ru')
        pass_form = browser.find_element_by_xpath('//*[@id="password"]')
        pass_form.send_keys('3Zqov4S1!')

        print('Нажатие кнопки Войти')
        logfile = f'{datetime.now()}: Нажатие кнопки Войти\n'
        txt.write(logfile)
        #time.sleep(1)
        browser.find_element_by_xpath('//*[@id="loginByPwdButton"]/span').click()

        logfile = f'{datetime.now()}: === Завершение авторизации ===\n'
        txt.write(logfile)

        print('Переход В ЛК, в раздел Рабочая область')
        logfile = f'{datetime.now()}: Переход В ЛК, в раздел Рабочая область\n'
        txt.write(logfile)
        #time.sleep(6)


def upload_xml_1(file_index):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'=== Начало загрузки заявки ===\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(4)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_1_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/1/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)
        #time.sleep(2)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
        WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

        timer.sleep(3)

        current_url = browser.current_url.rstrip('&sort=createDate%7Cdesc')
        #print(current_url)

        find_id_postn = current_url.find('id')
        item_id = current_url[find_id_postn : len(current_url)+1].lstrip('id=')
        #print(item_id)

        print(f'Файл: {filename} загружен')
        logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
        txt.write(logfile)
        timer.sleep(3)

        # zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]')

        # items = zayvki.find_elements_by_tag_name("tr")
        # item_id = items[1].get_attribute("id")
        # item_id = item_id.lstrip('item_')

        '''item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id
        print('Переход в заявку')
        logfile = f'{datetime.now()}: Переход в заявку\n'
        txt.write(logfile)
        browser.get(item_url)'''
        # time.sleep(3)
        # browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button').click()

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(2)
        browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
        #time.sleep(2)
        return 1

def upload_xml_100(file_index):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'=== Начало загрузки заявки ===\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(4)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_100_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/100/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)
        #time.sleep(2)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
        WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

        timer.sleep(3)

        current_url = browser.current_url.rstrip('&sort=createDate%7Cdesc')
        #print(current_url)

        find_id_postn = current_url.find('id')
        item_id = current_url[find_id_postn : len(current_url)+1].lstrip('id=')
        #print(item_id)

        print(f'Файл: {filename} загружен')
        logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
        txt.write(logfile)
        timer.sleep(3)

        # zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]')

        # items = zayvki.find_elements_by_tag_name("tr")
        # item_id = items[1].get_attribute("id")
        # item_id = item_id.lstrip('item_')

        '''item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id
        print('Переход в заявку')
        logfile = f'{datetime.now()}: Переход в заявку\n'
        txt.write(logfile)
        browser.get(item_url)'''
        # time.sleep(3)
        # browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button').click()

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(2)
        browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
        #time.sleep(2)
        return 1

def upload_xml_1000(file_index):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'=== Начало загрузки заявки ===\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(4)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_1000_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/1000/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)
        #time.sleep(2)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
        timer.sleep(5)
        '''WebDriverWait(browser, 400).until(EC.url_changes(browser.current_url))

        timer.sleep(3)

        current_url = browser.current_url.rstrip('&sort=createDate%7Cdesc')
        #print(current_url)

        find_id_postn = current_url.find('id')
        item_id = current_url[find_id_postn : len(current_url)+1].lstrip('id=')
        #print(item_id)'''

        print(f'Файл: {filename} загружен')
        logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
        txt.write(logfile)
        timer.sleep(3)

        # zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]')

        # items = zayvki.find_elements_by_tag_name("tr")
        # item_id = items[1].get_attribute("id")
        # item_id = item_id.lstrip('item_')

        '''item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id
        print('Переход в заявку')
        logfile = f'{datetime.now()}: Переход в заявку\n'
        txt.write(logfile)
        browser.get(item_url)'''
        # time.sleep(3)
        # browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button').click()

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(2)
        browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
        #time.sleep(2)
        return 1

def upload_xml_3000(file_index):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'=== Начало загрузки заявки ===\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(4)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_3000_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/3000/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)
        #time.sleep(2)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
        '''WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

        timer.sleep(3)

        #current_url = browser.current_url.rstrip('&sort=createDate%7Cdesc')
        #print(current_url)

        #find_id_postn = current_url.find('id')
        #item_id = current_url[find_id_postn : len(current_url)+1].lstrip('id=')
        #print(item_id)'''
        timer.sleep(2)
        print(f'Файл: {filename} отправлен на загрузку')
        logfile = f'{datetime.now()}: Файл: {filename} отправлен на загрузку\n'
        txt.write(logfile)
        timer.sleep(10)

        # zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]')

        # items = zayvki.find_elements_by_tag_name("tr")
        # item_id = items[1].get_attribute("id")
        # item_id = item_id.lstrip('item_')

        #item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id
        #print('Переход в заявку')
        #logfile = f'{datetime.now()}: Переход в заявку\n'
        #txt.write(logfile)
        #browser.get(item_url)
        # time.sleep(3)
        # browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button').click()

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)

        timer.sleep(2)
        browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
        timer.sleep(2)
        return 1

def upload_xml_5000(file_index):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'=== Начало загрузки заявки ===\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        #time.sleep(4)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_5000_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/5000/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)
        #time.sleep(2)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
        '''WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

        timer.sleep(3)

        current_url = browser.current_url.rstrip('&sort=createDate%7Cdesc')
        #print(current_url)

        find_id_postn = current_url.find('id')
        item_id = current_url[find_id_postn : len(current_url)+1].lstrip('id=')'''
        #print(item_id)

        timer.sleep(2)
        print(f'Файл: {filename} отправлен на загрузку')
        logfile = f'{datetime.now()}: Файл: {filename} отправлен на загрузку\n'
        txt.write(logfile)
        timer.sleep(3)

        # zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]')

        # items = zayvki.find_elements_by_tag_name("tr")
        # item_id = items[1].get_attribute("id")
        # item_id = item_id.lstrip('item_')

        '''item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id
        print('Переход в заявку')
        logfile = f'{datetime.now()}: === Переход в заявку ===\n'
        txt.write(logfile)
        browser.get(item_url)'''
        # time.sleep(3)
        # browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button').click()

        print('Переход в ЛК, в раздел Рабочая область')
        log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)

        timer.sleep(2)
        browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
        timer.sleep(2)
        return 1

#==========================================================
#Начинаем с авторизации
login()

xml_1 = 5
xml_100 = 1
xml_1000 = 0
xml_3000 = 0
xml_5000 = 0
total_xml = xml_1 + xml_100 + xml_1000 + xml_3000 + xml_5000

xml_list = ['xml_1', 'xml_100', 'xml_1000', 'xml_3000', 'xml_5000']

file_index_1 = 1
file_index_2 = 1
file_index_3 = 1
file_index_4 = 1
file_index_5 = 1

while total_xml != 0:
    if len(xml_list) >= 2:
        choose_xml_type = xml_list[random.randint(0, len(xml_list)-1)]
        print(choose_xml_type)
    else:
        choose_xml_type = xml_list[0]
        print('Список уменьшился до одного', choose_xml_type)

    if choose_xml_type == 'xml_1' and xml_1 != 0:
        process = upload_xml_1(file_index_1)
        xml_1 -= process
        total_xml -= 1
        file_index_1 += 1
        print('Загрузка заявки из xml_1 выполнена')
    elif choose_xml_type == 'xml_1' and xml_1 == 0:
        xml_list.remove(choose_xml_type)
        print(f'Загрузка всех заявок из xml_1 окончена')
        print(xml_list)

    if choose_xml_type == 'xml_100' and xml_100 != 0:
        process = upload_xml_100(file_index_2)
        xml_100 -= process
        total_xml -= 1
        file_index_2 += 1
        print('Загрузка заявки из xml_100 выполнена')
    elif choose_xml_type == 'xml_100' and xml_100 == 0:
        xml_list.remove(choose_xml_type)
        print(f'Загрузка всех заявок из xml_100 окончена')
        print(xml_list)

    if choose_xml_type == 'xml_1000' and xml_1000 != 0:
        process = upload_xml_1000(file_index_3)
        xml_1000 -= process
        total_xml -= 1
        file_index_3 += 1
        print('Загрузка заявки из xml_1000 выполнена')
    elif choose_xml_type == 'xml_1000' and xml_1000 == 0:
        xml_list.remove(choose_xml_type)
        print(f'Загрузка всех заявок из xml_1000 окончена')
        print(xml_list)

    if choose_xml_type == 'xml_3000' and xml_3000 != 0:
        process = upload_xml_3000(file_index_4)
        xml_3000 -= process
        total_xml -= 1
        file_index_4 += 1
        print('Загрузка заявки из xml_3000 выполнена')
    elif choose_xml_type == 'xml_3000' and xml_3000 == 0:
        xml_list.remove(choose_xml_type)
        print(f'Загрузка всех заявок из xml_3000 окончена')
        print(xml_list)

    if choose_xml_type == 'xml_5000' and xml_5000 != 0:
        process = upload_xml_5000(file_index_5)
        xml_5000 -= process
        total_xml -= 1
        file_index_5 += 1
        print('Загрузка заявки из xml_5000 выполнена')
    elif choose_xml_type == 'xml_5000' and xml_5000 == 0:
        xml_list.remove(choose_xml_type)
        print(f'Загрузка всех заявок из xml_5000 окончена')
        print(xml_list)

else:
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Загрузка записей окончена')
        log_line = f'=================================\n'
        log_txt = f'{datetime.now()}: Загрузка записей окончена\n'
        logfile = log_line + log_txt
        txt.write(logfile)
        browser.close()
        quit()
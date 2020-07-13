import os
import random
import time as timer

from datetime import datetime, date, time, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException

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
opts.headless = True
assert opts.headless  # без графического интерфейса.

browser = webdriver.Chrome(options=opts)
browser.implicitly_wait(10)
browser.get("http://vniims.finecosoft.ru:8080/fundmetrology/cm/")

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

        try:
            esia_check = browser.find_element_by_xpath('//*[@id="esia_agree"]')
            esia_check.click()
        except ElementNotInteractableException:
            browser.find_element_by_xpath('//*[@id="esia"]/div/div/div[2]/div/label').click()

        print('Нажатие кнопки Подтвердить условия ЕСИА')
        logfile = f'{datetime.now()}: Нажатие кнопки Подтвердить условия ЕСИА\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="esia_login"]').click()

        print('Ввод логина и пароля в ЕСИА')
        logfile = f'{datetime.now()}: Ввод логина и пароля в ЕСИА\n'
        txt.write(logfile)

        login_form = browser.find_element_by_xpath('//*[@id="mobileOrEmail"]')
        login_form.send_keys('R-Test-002@yandex.ru')
        pass_form = browser.find_element_by_xpath('//*[@id="password"]')
        pass_form.send_keys('3Zqov4S1!')

        try:
            print('Нажатие кнопки Войти')
            logfile = f'{datetime.now()}: Нажатие кнопки Войти\n'
            txt.write(logfile)

            browser.find_element_by_xpath('//*[@id="loginByPwdButton"]/span').click()
            WebDriverWait(browser, 10).until(EC.url_changes(browser.current_url))
        except TimeoutException:
            alert_phone = browser.find_element_by_xpath('//*[@id="authnFrm"]/div[1]/div[3]/dl[1]/dd/div/div/span')
            alert = browser.find_element_by_xpath('//*[@id="authnFrm"]/div[1]/div[3]/div[2]/div/span')
            print(alert.text)
            logfile = f'{datetime.now()}: Ошибка: {alert.text if alert.text else alert_phone.text}\nВыход из программы.'
            txt.write(logfile)
            browser.close()
            quit()

        print('Переход В ЛК, в раздел Рабочая область')
        logfile = f'=== Завершение авторизации ===\n'
        txt.write(logfile)
        logfile = f'{datetime.now()}: Переход В ЛК, в раздел Рабочая область\n'
        txt.write(logfile)

def upload_xml(file_index, folder, xml_type):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Загрузить в ЛК')

        log_line = f'=================================\n'
        log_txt_1 = f'=== Начало загрузки заявки ===\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Загрузить в ЛК\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

        filename = f'loadTest_{folder}_{file_index}_signCipher_М.xml'

        print(f'Выбран файл: {filename}')
        logfile = f'{datetime.now()}: Выбран файл: {filename}\n'
        txt.write(logfile)

        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/' + str(folder) + '/' + filename)

        print('Нажата кнопка Загрузить')
        logfile = f'{datetime.now()}: Нажата кнопка Загрузить\n'
        txt.write(logfile)

        if xml_type == 'xml_1' or xml_type == 'xml_100':
            browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
            WebDriverWait(browser, 300).until(EC.url_changes(browser.current_url))

            timer.sleep(3)

            print(f'Файл: {filename} загружен')
            logfile = f'{datetime.now()}: Файл: {filename} загружен\n'
            txt.write(logfile)
            timer.sleep(3)

            print('Переход в ЛК, в раздел Рабочая область')
            log_txt_1 = f'{datetime.now()}: Переход в ЛК, в раздел Рабочая область\n'
            log_txt_2 = f'=== Окончание загрузки заявки ===\n'
            logfile =  log_txt_1 + log_txt_2
            txt.write(logfile)

            timer.sleep(2)
            browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
            timer.sleep(2)
            return 1

        if xml_type == 'xml_1000':
            browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
            timer.sleep(5)
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

            timer.sleep(2)
            browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
            timer.sleep(2)
            return 1

        elif xml_type == 'xml_3000' or xml_type == 'xml_5000':
            browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()

            timer.sleep(2)
            print(f'Файл: {filename} отправлен на загрузку')
            logfile = f'{datetime.now()}: Файл: {filename} отправлен на загрузку\n'
            txt.write(logfile)
            timer.sleep(10)

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
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        if len(xml_list) >= 2:
            choose_xml_type = xml_list[random.randint(0, len(xml_list)-1)]
        else:
            choose_xml_type = xml_list[0]
            print('Список уменьшился до одного', choose_xml_type)

        if choose_xml_type == 'xml_1' and xml_1 != 0:
            folder = 1
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
            process = upload_xml(file_index_2, folder, choose_xml_type)
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
            process = upload_xml(file_index_3, folder, choose_xml_type)
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
            process = upload_xml(file_index_4, folder, choose_xml_type)
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
            process = upload_xml(file_index_5, folder, choose_xml_type)
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

else:
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Загрузка записей окончена')
        log_line = f'=================================\n'
        log_txt = f'{datetime.now()}: Загрузка записей окончена\n'
        logfile = log_line + log_txt
        txt.write(logfile)
        browser.close()
        quit()
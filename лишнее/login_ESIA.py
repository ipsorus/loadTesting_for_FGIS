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

filename = 'logfile_ESIA.txt'
FileFullPathInfo = os.path.join(os.getcwd(), filename)  #Путь сохранения лог-файла

with open (FileFullPathInfo, 'w', encoding='utf-8') as txt:

    str_1 = 'Логирование загрузки заявок\n'
    str_2 = f'Начало в {datetime.now()}\n'
    str_3 = '=========================================================\n'

    logfile = str_1 + str_2 + str_3
    txt.write(logfile)

# opts = Options()
# opts.set_headless()
# assert opts.headless  # без графического интерфейса.

browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get("https://fgis.gost.ru/fundmetrologytest/cm/")
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
        login_form.send_keys('9067599747')
        pass_form = browser.find_element_by_xpath('//*[@id="password"]')
        pass_form.send_keys('v8a2d346')

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
        browser.close()
        quit()

login()
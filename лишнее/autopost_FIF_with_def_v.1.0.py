import os
import random
import time as timer

from datetime import datetime, date, time, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            login_form.send_keys('9067599747')
            pass_form = browser.find_element_by_xpath('//*[@id="password"]')
            pass_form.send_keys('v8a2d346')
        except ElementNotInteractableException:
            print('Ввод пароля в ЕСИА')
            pass_form = browser.find_element_by_xpath('//*[@id="password"]')
            pass_form.send_keys('v8a2d346')

        print('Нажатие кнопки Войти')
        logfile = f'{datetime.now()}: Нажатие кнопки Войти\n'
        txt.write(logfile)
        browser.find_element_by_xpath('//*[@id="loginByPwdButton"]/span').click()
        #browser.set_page_load_timeout(10)

        #WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-header-nav-1"]/li[3]/a/i')))

        # alert_phone = browser.find_element_by_xpath('//*[@id="authnFrm"]/div[1]/div[3]/dl[1]/dd/div/div/span')
        # alert = browser.find_element_by_xpath('//*[@id="authnFrm"]/div[1]/div[3]/div[2]/div/span')
        # if alert_phone is not None or alert is not None:
        #     print('Ошибка логина/пароля')
        #     logfile = f'{datetime.now()}: Ошибка: {alert.text if alert.text else alert_phone.text}\nВыход из программы.'
        #     txt.write(logfile)
        #     #browser.close()
        #     #quit()

        print('Переход В ЛК, в раздел Рабочая область')
        logfile = f'=== Завершение авторизации ===\n{datetime.now()}: Переход В ЛК, в раздел Рабочая область.\n'
        txt.write(logfile)

def logout(time_to_logout):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        log_txt = f'{datetime.now()}: Время процесса загрузки достигло {time_to_logout} мин. Запущен процесс выхода из ЛК.\n'
        txt.write(log_txt)

        browser.find_element_by_xpath('//*[@id="app-top-nav"]/ul[3]/li[1]/a').click()

        logfile = f'{datetime.now()}: Нажата кнопка "Выход"\n'
        txt.write(logfile)
        timer.sleep(3)
        print('Выход из ЛК окончен')
        logfile = f'{datetime.now()}: Выход из ЛК окончен.\n'
        txt.write(logfile)


def post_application(current_page):
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
        print('Нажата кнопка Отправить в ФИФ')
        log_line = f'=================================\n'
        log_txt_1 = f'==== Начало отправки заявок ====\n'
        log_txt_2 = f'{datetime.now()}: Нажата кнопка Отправить в ФИФ\n'
        logfile = log_line + log_txt_1 + log_txt_2
        txt.write(logfile)
        url_with_page = f'https://fgis.gost.ru/fundmetrologytest/cm/lk/applications?createDatePeriodBegin=2020-06-01&createDatePeriodEnd=2020-06-07&status=CREATED&page={current_page}&rows=50'
        browser.get(url_with_page)
        timer.sleep(5)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/thead/tr/th[1]/div/label').click()
        timer.sleep(2)
        browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()  #раскомментировать в работе
        print(f'Записи отправлены на публикацию')
        log_txt_1 = f'{datetime.now()}: Записи отправлены на публикацию\n'
        log_txt_2 = f'=== Окончание загрузки заявки ===\n'
        logfile =  log_txt_1 + log_txt_2
        txt.write(logfile)

def count_items():
    with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:

        browser.get("https://fgis.gost.ru/fundmetrologytest/cm/lk/applications?createDatePeriodBegin=2020-06-01&createDatePeriodEnd=2020-06-07&status=CREATED&rows=50")
        zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]/table/tbody')
        items = zayvki.find_elements_by_tag_name("tr")

        try:
            last_page = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[1]/div[1]/div/div[2]/nav/ul/li[8]/a')
        except NoSuchElementException:
            last_page = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[1]/div[1]/div/div[2]/nav/ul/li[6]/a')

        total_app = int(last_page.text) * 50
        logfile = f'Осталось загрузить: {total_app} заявок\n'
        txt.write(logfile)
        print(f'Осталось загрузить: {total_app} заявок')
        c_last_page = int(last_page.text)

        return items, c_last_page


if __name__ == "__main__":
    filename = 'logfile_posting_3.txt'
    FileFullPathInfo = os.path.join(os.getcwd(), filename)  #Путь сохранения лог-файла

    with open (FileFullPathInfo, 'w', encoding='utf-8') as txt: #Если новый файл то 'w', если дозапись в файл, то 'a'

        str_1 = 'Логирование отправки заявок\n'
        str_2 = f'Начало в {datetime.now()}\n'
        str_3 = '===============================================\n'

        logfile = str_1 + str_2 + str_3
        txt.write(logfile)

    opts = Options()
    #opts.headless = False
    opts.add_argument("--headless")
    opts.add_argument("window-size=1920,1080")
    #assert opts.headless  # без графического интерфейса.

    browser = webdriver.Chrome(options=opts)
    browser.implicitly_wait(10)
    browser.get("https://fgis.gost.ru/fundmetrologytest/cm/")
    #==========================================================
    #Начинаем с авторизации
    try:
        login()
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
        print('1.Ошибку поймал, нужен рестарт логина (ошибка в авторизации, либо редиректе)')
        logfile = f'{datetime.now()}: 1. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
        txt.write(logfile)
        browser.get("https://fgis.gost.ru/fundmetrologytest/cm/")
        login()

    begin_time = start_time()
    timer.sleep(2)
    try:
        total_items, current_last_page = count_items()
    except (TimeoutException, ElementClickInterceptedException):
        print('2.Ошибку поймал, нужен рестарт логина (ошибка во время проверки и подсчета списка заявок)')
        logfile = f'{datetime.now()}: 2. Аварийное завершение, повторная авторизация (ошибка во время проверки и подсчета списка заявок).\n'
        browser.get("https://fgis.gost.ru/fundmetrologytest/cm/lk/applications?createDatePeriodBegin=2020-06-01&createDatePeriodEnd=2020-06-07&status=CREATED&rows=50")
        total_items, current_last_page = count_items()

    start_page = 1
    middle_page = current_last_page//2
    end_page = current_last_page
    page_list = [start_page, middle_page, end_page]
    page_index = 0
    current_page = page_list[page_index]

    print(f'Найдено {len(total_items)} записей на странице')

    while len(total_items) != 0:
        real_time = datetime.now()                                      #Вычисление прошедшего времени с начала загрузки заявок (не должно превышать 120 мин.)
        time_to_logout = (real_time - begin_time).total_seconds()
        time_to_logout = int(time_to_logout)//60

        print(f'Время до выхода из ЛК: {time_to_logout}')

        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            if time_to_logout >= 60:  #Установка времени до перелогинивания
                print('Выход из ЛК начат')
                logout()
                timer.sleep(5)
                try:
                    login()
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                    print('3.Ошибку поймал, нужен рестарт логина (ошибка в авторизации, либо редиректе)')
                    logfile = f'{datetime.now()}: 3. Аварийное завершение, повторная авторизация, (ошибка в авторизации, либо редиректе).\n'
                    txt.write(logfile)
                    browser.get("https://fgis.gost.ru/fundmetrologytest/cm/")
                    login()
                begin_time = start_time()
                print('Повторная авторизация выполнена.')
                log_txt = f'{datetime.now()}: Повторная авторизация выполнена.\n'
                txt.write(log_txt)
                timer.sleep(5)
            else:
                log_txt = f'{datetime.now()}: Текущая страница для отправки: {current_page}.\n'
                txt.write(log_txt)
                print(f'Текущая страница для отправки: {current_page}')
                timer.sleep(2)
                try:
                    post_application(current_page)
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                    print('4.Ошибку поймал, нужен рестарт логина (ошибка во время отправки заявок)')
                    logfile = f'{datetime.now()}: 4. Аварийное завершение, повторная авторизация (ошибка во время отправки заявок).\n'
                    browser.get("https://fgis.gost.ru/fundmetrologytest/cm/lk/applications?createDatePeriodBegin=2020-06-01&createDatePeriodEnd=2020-06-07&status=CREATED&rows=50")
                    #login()
                timer.sleep(5)

                print('Подсчет записей на странице...')
                try:
                    total_items, current_last_page = count_items()
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                    print('5.Ошибку поймал, нужен рестарт логина (ошибка во время проверки и подсчета списка заявок)')
                    logfile = f'{datetime.now()}: 5. Аварийное завершение, повторная авторизация (ошибка во время проверки и подсчета списка заявок).\n'
                    browser.get("https://fgis.gost.ru/fundmetrologytest/cm/lk/applications?createDatePeriodBegin=2020-06-01&createDatePeriodEnd=2020-06-07&status=CREATED&rows=50")
                    total_items, current_last_page = count_items()
                print(f'Количество записей: {len(total_items)}.\nОжидание следующей отправки записей.')

                page_index += 1

                print(f'Last page: {current_last_page}')
                if page_index == 3:
                    page_index = 0
                    start_page += 1
                    middle_page = end_page//2
                    end_page -= 1
                if current_last_page <= 3:
                    page_index = 0
                if end_page == 1 or end_page > current_last_page:
                    end_page = current_last_page
                if start_page == current_last_page:
                    start_page = 1
                print(f'page_index: {page_index}')
                print(f'end_page: {end_page}')
                print(f'start_page: {start_page}')

                page_list = [start_page, middle_page, end_page]
                current_page = page_list[page_index]
                #timer.sleep(5)
                timer.sleep(1200)  #Таймер ожидания для теста 1800 сек.

    else:
        with open (FileFullPathInfo, 'a', encoding='utf-8') as txt:
            print('Отправка заявок в ФИФ окончена')
            log_line = f'=================================\n'
            log_txt = f'{datetime.now()}: Отправка заявок в ФИФ окончена.\n'
            logfile = log_line + log_txt
            txt.write(logfile)
            browser.close()
            quit()
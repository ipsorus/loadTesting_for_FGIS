import os
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException


browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get("http://vniims.finecosoft.ru:8080/fundmetrology/cm/")
#time.sleep(5)
try:
    browser.find_element_by_xpath('/html/body/div/header/div/div/div[4]/a[1]').click()
    #time.sleep(2)
except ElementNotInteractableException:
    browser.find_element_by_xpath('/html/body/div/header/a').click()
    browser.find_element_by_xpath('/html/body/div/header/div/div/div[4]/a[1]').click()

#time.sleep(2)
esia_check = browser.find_element_by_xpath('//*[@id="esia_agree"]')
#time.sleep(2)
esia_check.click()
#time.sleep(1)
browser.find_element_by_xpath('//*[@id="esia_login"]').click()
#time.sleep(5)

login_form = browser.find_element_by_xpath('//*[@id="mobileOrEmail"]')
login_form.send_keys('R-Test-002@yandex.ru')
pass_form = browser.find_element_by_xpath('//*[@id="password"]')
pass_form.send_keys('3Zqov4S1!')
#time.sleep(1)
browser.find_element_by_xpath('//*[@id="loginByPwdButton"]/span').click()
#time.sleep(6)

for i in range(2):
    #time.sleep(4)
    browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[1]/div[4]/button').click()

    filename = f'loadTest_1_{i+1}_signCipher_М.xml'

    browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(os.getcwd() + '/1/' + filename)
    #time.sleep(2)
    browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/div[2]/div/div/div[3]/div/div/div[2]/button').click()
    time.sleep(3)
    current_url = browser.current_url.rstrip('&sort=createDate%7Cdesc')
    find_id_postn = current_url.find('id')
    item_id = current_url[find_id_postn : len(current_url)+1].lstrip('id=')
    print(item_id)

    print(f'{filename}, OK')
    #time.sleep(3)

    # zayvki = browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div[3]/div[2]')

    # items = zayvki.find_elements_by_tag_name("tr")
    # item_id = items[1].get_attribute("id")
    # item_id = item_id.lstrip('item_')

    # print(item_id)

    item_url = 'http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/applications/' + item_id

#Сообщение об удалении и о загрузке файла
#<div class="toast toast-success" aria-live="polite" style=""><div class="toast-message">Записи удалены</div></div>
#//*[@id="toast-container"]
#//*[@id="toast-container"]
    browser.get(item_url)
    # time.sleep(3)
    # browser.find_element_by_xpath('//*[@id="app-wrapper"]/div/div/section/div/div/div[1]/div[3]/button').click()

    #time.sleep(2)
    browser.get('http://vniims.finecosoft.ru:8080/fundmetrology/cm/lk/calibrations/work')
    #time.sleep(2)


'''item_xpath= f'//*[@id="{item_id}"]/td[1]/div/label'

print(item_xpath)

public_item = items[1].find_element_by_xpath(item_xpath)
time.sleep(2)
ActionChains(browser).move_to_element(public_item).perform()
public_item.click()


item_xpath= f'//*[@id="{item_id}"]'
'''

#for item in items:
    #print(item.text)
    #print('Заявка:', item.get_attribute("id"))

#send_to_fif = items[0].find_elements_by_tag_name("input")
#send_to_fif.click()



#print('Первый вариант не сработал')
#item_xpath= f'//*[@id="{item_id}"]'
#public_item = items[1].find_element_by_xpath(item_xpath)
#ActionChains(browser).double_click(public_item).perform()

# try:
#     ActionChains(browser).double_click(items[1]).perform()
# except AttributeError:
#     print('Первый вариант не сработал')
#     item_xpath= f'//*[@id="{item_id}"'
#     public_item = items[1].find_element_by_xpath(item_xpath)
#     ActionChains(browser).double_click(public_item).perform()


#<div data-v-783a602b="" class="icheck-primary"><input data-v-783a602b="" type="checkbox" id="data_check_824"> <label data-v-783a602b="" for="data_check_824"></label></div>
#item = new_item.find_element_by_tag_name('label')
#time.sleep(2)
#item.click()


#search_form.submit()
time.sleep(2)
#results = browser.find_elements_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]')
#print(results[0].text)
browser.close()
quit()


# import time
# from selenium import webdriver

# browser = webdriver.Chrome()
# browser.get("https://yandex.ru")
# time.sleep(5)
# search_form = browser.find_element_by_xpath('//*[@id="text"]')
# search_form.send_keys('python 3')
# search_form.submit()
# time.sleep(5)
# results = browser.find_elements_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]')
# print(results[0].text)
# browser.close()
# quit()



# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.options import Options

# opts = Options()
# opts.set_headless()
# assert opts.headless  # без графического интерфейса.

# browser = Chrome(options=opts)
# browser.get('https://yandex.ru')

# search_form = browser.find_element_by_xpath('//*[@id="text"]')
# search_form.send_keys('python 3')
# search_form.submit()

# results = browser.find_elements_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/div[1]')
# print(results)
# browser.close()
# quit()
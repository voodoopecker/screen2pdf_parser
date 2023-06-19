import time
import os
from loguru import logger as LOGGER
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from settings import url, pages_number

# настройки логирования
LOGGER.add('logs/debug.log', format='{time}|{level}|{module}.{function}:{line} - {message}', level='DEBUG')

# создаем директорию для сохранения страниц
if not os.path.exists("saved_pages"):
    os.makedirs("saved_pages")

# заходим на страницу для сбора
driver = webdriver.Firefox()
try:
    driver.get(url)
except:
    LOGGER.error('Ошибка при открытии ссылки!')

# цикл сохранения страниц
input('Нажми ENTER по готовности')
page_counter = 1
LOGGER.debug('Начинаю сохранять страницы:')
for i in range(pages_number):
    driver.save_screenshot(f'saved_pages/page_0{page_counter}.png')  # делаем снимок экрана
    LOGGER.debug(f'Сохраняю страницу Page 0{page_counter}')
    page_counter += 1
    ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()  # нажимаем кнопку вниз для перехода на следующую страницу
    time.sleep(1)
LOGGER.success('Закончил парсинг!')
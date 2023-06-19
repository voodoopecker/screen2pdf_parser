import time
import os
from loguru import logger as LOGGER
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from settings import url, pages_number

# настройки логирования
LOGGER.add('logs/debug.log', format='{time}|{level}|{module}.{function}:{line} - {message}', level='DEBUG')


# сохранение страниц
def scrap_screenshots():
    LOGGER.debug(f'Парсер скриншотов запущен')
    if not os.path.exists("saved_pages"):  # создаем директорию для сохранения страниц
        os.makedirs("saved_pages")
    driver = webdriver.Firefox()
    try:
        driver.get(url)
    except:
        LOGGER.error('Ошибка при открытии ссылки!')
    input('Парсер готов, нажми ENTER для старта')
    page_counter = 1
    LOGGER.debug('Начинаю сохранять страницы:')
    for i in range(pages_number):
        driver.save_screenshot(f'saved_pages/page_0{page_counter}c.png')  # делаем снимок экрана
        LOGGER.debug(f'Сохраняю страницу Page 0{page_counter}c')
        page_counter += 1
        ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()  # нажимаем кнопку вниз для перехода на следующую страницу
        time.sleep(1)
    driver.quit()
    LOGGER.success('Закончил парсинг!')


# обрезка сдвоенных страниц
def crop_screenshots():
    LOGGER.debug(f'Кадрирование картинок запущено')
    if not os.path.exists("cropped_pages"):  # создаем директорию для кадрированных картинок
        os.makedirs("cropped_pages")
    files_list = [i for i in os.listdir('saved_pages')]  # список сохраненных файлов
    for file in files_list:
        image_left = Image.open(f'saved_pages/{file}')  # будет левая страница
        image_right = Image.open(f'saved_pages/{file}')  # будет правая страница
        # image_left.show()   # открыть картинку
        crop_region_left = (50, 100, 1225, 1200)  # координаты области образки left, upper, right, lower
        image_cropped_left = image_left.crop(crop_region_left)
        image_cropped_left.save(f'cropped_pages/{file[:-4]}1left.png', quality=95, subsampling=0)
        crop_region_right = (1325, 100, 2500, 1200)  # координаты области образки left, upper, right, lower
        image_cropped_right = image_right.crop(crop_region_right)
        image_cropped_right.save(f'cropped_pages/{file[:-4]}2right.png', quality=95, subsampling=0)
    LOGGER.success(f'Закончил резать картинки!')


# фильтр для сортировки по части имени файла
def sort_by_number(item):
    stop = item.index('c')
    number = item[5:stop]
    return int(number)


# сохраняем в один pdf файл
def convert_to_pdf(pict_path):
    LOGGER.debug(f'Конвертация в PDF запущена')
    files_list = sorted([i for i in os.listdir(pict_path)])
    files_list = sorted(files_list, key=sort_by_number)
    start_page = Image.open('start.jpg')
    start_page.save(r'new_book.pdf')
    for file in files_list:
        image = Image.open(f'{pict_path}/{file}')
        page = image.convert('RGB')
        page.save(r'new_book.pdf', append=True)
    LOGGER.success(f'Сохранил книгу в PDF!')


# удаляем директории с картинками
def clear_files():
    pass

def main():
    LOGGER.debug(f'Программа запущена')
    scrap_y_n = input('Нужно парсить? (y/n или д/н): ')
    crop_y_n = input('Нужно резать на отдельные страницы? (y/n или д/н): ')
    convert_y_n = input('Нужно сохранять в PDF документ? (y/n или д/н): ')
    clear_y_n = 'No'
    if convert_y_n in ('y', 'д'):
        clear_y_n = input('Удалить картинки после сохранения PDF документа? (y/n или д/н): ')
    if scrap_y_n in ('y', 'д'):
        scrap_screenshots()
    pict_path = 'saved_pages'
    if crop_y_n in ('y', 'д'):
        crop_screenshots()
        pict_path = 'cropped_pages'
    if convert_y_n in ('y', 'д'):
            convert_to_pdf(pict_path)
    if clear_y_n in ('y', 'д'):
        clear_files()
    LOGGER.success(f'Программа завершилась!')

main()
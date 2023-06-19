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
        driver.save_screenshot(f'saved_pages/page_0{page_counter}.png')  # делаем снимок экрана
        LOGGER.debug(f'Сохраняю страницу Page 0{page_counter}')
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
        image_cropped_left.save(f'cropped_pages/{file[:-4]}1cleft.png', quality=95, subsampling=0)
        crop_region_right = (1325, 100, 2500, 1200)  # координаты области образки left, upper, right, lower
        image_cropped_right = image_right.crop(crop_region_right)
        image_cropped_right.save(f'cropped_pages/{file[:-4]}2cright.png', quality=95, subsampling=0)
    LOGGER.success(f'Закончил резать картинки!')


# фильтр для сортировки по части имени файла
def sort_by_number(item):
    stop = item.index('c')
    number = item[5:stop]
    return int(number)


# сохраняем в один pdf файл
def convert_to_pdf():
    LOGGER.debug(f'Конвертация в PDF запущена')
    files_list = sorted([i for i in os.listdir('cropped_pages')], key=sort_by_number)
    image_list = []
    image_dict = {}
    for file in files_list:
        image = Image.open(f'cropped_pages/{file}')
        page = image.convert('RGB')
        image_list.append(page)
        image_dict[file] = page
    page.save(r'new_book.pdf', save_all=True, append_images=image_list)
    LOGGER.success(f'Сохранил книгу в PDF!')


def main():
    LOGGER.debug(f'Программа запущена')
    scrap_y_n = input('Нужно парсить? (y/n или д/н): ')
    if scrap_y_n in ('y', 'д'):
        scrap_screenshots()
    crop_y_n = input('Режем на отдельные страницы? (y/n или д/н): ')
    if crop_y_n in ('y', 'д'):
        crop_screenshots()
    convert_y_n = input('Сохраняем в один PDF документ? (y/n или д/н): ')
    if convert_y_n in ('y', 'д'):
        convert_to_pdf()
    LOGGER.success(f'Программа завершилась!')

main()
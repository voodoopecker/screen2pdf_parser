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
    if not os.path.exists("cropped_pages"):  # создаем директорию для кадрированных картинок
        os.makedirs("cropped_pages")
    files_list = [i for i in os.listdir('saved_pages')]  # список сохраненных файлов
    for file in files_list:
        image_left = Image.open(f'saved_pages/{file}')  # будет левая страница
        image_right = Image.open(f'saved_pages/{file}')  # будет правая страница
        # image_left.show()   # открыть картинку
        crop_region_left = (50, 100, 1225, 1200)  # координаты области образки left, upper, right, lower
        image_cropped_left = image_left.crop(crop_region_left)
        image_cropped_left.save(f'cropped_pages/{file}_cleft.png', quality=95, subsampling=0)
        crop_region_right = (1325, 100, 2500, 1200)  # координаты области образки left, upper, right, lower
        image_cropped_right = image_right.crop(crop_region_right)
        image_cropped_right.save(f'cropped_pages/{file}_cright.png', quality=95, subsampling=0)


# сохраняем в один pdf файл
def convert_to_pdf():
    files_list = [i for i in os.listdir('cropped_pages')]
    print(files_list)
    image_list = []
    for file in files_list:
        image = Image.open(f'cropped_pages/{file}')
        page = image.convert('RGB')
        image_list.append(page)
    print(image_list)
    page.save(r'book_pdf.pdf', save_all=True, append_images=image_list)


def main():
    scrap_screenshots()
    crop_y_n = input('Режем на отдельные страницы? (y/n или д/н): ')
    if crop_y_n in ('y', 'д'):
        crop_screenshots()
    convert_y_n = input('Сохраняем в один PDF документ? (y/n или д/н): ')
    if convert_y_n in ('y', 'д'):
        convert_to_pdf()

main()
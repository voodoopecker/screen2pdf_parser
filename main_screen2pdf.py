import time
import os
import shutil
from loguru import logger as LOGGER
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from settings import url, pages_number, crop_region_left, crop_region_right, book_output_name

# Logger settings
LOGGER.add('logs/debug.log', format='{time}|{level}|{module}.{function}:{line} - {message}', level='DEBUG')


# Saving pages
def scrap_screenshots():
    LOGGER.debug(f'Ready to scrap screenshots')
    if not os.path.exists("saved_pages"):  # Make a new directory for the saved pages
        os.makedirs("saved_pages")
    driver = webdriver.Firefox()
    try:
        driver.get(url)  # Open browser
    except:
        LOGGER.error('Error while opening URL!')
    input('The parser is ready. Press ENTER to start.')
    page_counter = 1
    LOGGER.debug('Start saving pages')
    for i in range(pages_number):
        driver.save_screenshot(f'saved_pages/page_0{page_counter}c.png')  # Make screenshot
        LOGGER.debug(f'Saving Page 0{page_counter}c')
        page_counter += 1
        ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()  # Press the down arrow to proceed to the next page
        time.sleep(1)
    driver.quit()
    LOGGER.success('Done scraping!')


# Cropping pages
def crop_screenshots():
    LOGGER.debug(f'Start cropping pages')
    if not os.path.exists("cropped_pages"):  # Make a new directory for the cropped pages
        os.makedirs("cropped_pages")
    files_list = [i for i in os.listdir('saved_pages')]  # List of saved files
    for file in files_list:
        image_left = Image.open(f'saved_pages/{file}')  # Left page
        image_right = Image.open(f'saved_pages/{file}')  # Right page
        image_cropped_left = image_left.crop(crop_region_left)
        image_cropped_left.save(f'cropped_pages/{file[:-4]}1left.png', quality=95, subsampling=0)
        image_cropped_right = image_right.crop(crop_region_right)
        image_cropped_right.save(f'cropped_pages/{file[:-4]}2right.png', quality=95, subsampling=0)
    LOGGER.success(f'Done cropping!')


# Sorting by part of the name
def sort_by_number(item):
    stop = item.index('c')
    number = item[5:stop]
    return int(number)


# Saving to PDF
def convert_to_pdf(pict_path):
    LOGGER.debug(f'Start converting to PDF')
    files_list = sorted([i for i in os.listdir(pict_path)])
    files_list = sorted(files_list, key=sort_by_number)
    start_page = Image.open('start.jpg')
    start_page.save(f'{book_output_name}.pdf')
    for file in files_list:
        image = Image.open(f'{pict_path}/{file}')
        page = image.convert('RGB')
        page.save(f'{book_output_name}.pdf', append=True)
    LOGGER.success(f'Done with PDF!')


# Deleting directories with pictures
def clear_files():
    shutil.rmtree('cropped_pages', ignore_errors=True)
    shutil.rmtree('saved_pages', ignore_errors=True)
    LOGGER.success(f'Directories deleted!')


# Main function
def main():
    LOGGER.debug(f'Script started!')
    scrap_y_n = input('Need to scrap? (y/n): ')
    crop_y_n = input('Need to crop pages? (y/n): ')
    convert_y_n = input('Need to convert to PDF? (y/n): ')
    clear_y_n = 'No'
    if convert_y_n == 'y':
        clear_y_n = input('Do you want to delete all pictures after saving the PDF document? (y/n): ')
    if scrap_y_n == 'y':
        scrap_screenshots()
    pict_path = 'saved_pages'
    if crop_y_n == 'y':
        crop_screenshots()
        pict_path = 'cropped_pages'
    if convert_y_n == 'y':
        convert_to_pdf(pict_path)
    if clear_y_n == 'y':
        clear_files()
    LOGGER.success(f'Script terminated!')


if __name__ == '__main__':
    main()

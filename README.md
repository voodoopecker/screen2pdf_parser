# Description
Screen2pdf Saver - The scraping script is designed for online books. It retrieves all pages one by one and saves them to a PDF file for offline reading. But you could use it for any convenient purpose.

![](start.jpg)

---
# Installation
* Download the project

````
git clone https://github.com/voodoopecker/screen2pdf_parser.git
````
* Install dependencies
````
pip install -r requirements.txt
````
---
# Usage

* Set script settings in settings.py:
  * ```url``` - starting page
  * ```book_output_name``` - name of the output PDF file
  * ```pages_number``` - number of pages in the book. The script will take screenshots of each page __pages_number__ times while executing.
  * ```crop_region_left``` - dimensions of the left box to crop the page. The numbers in the tuple are the left, upper, right, and lower coordinates of the screen.
  * ```crop_region_right``` - dimensions of the right box to crop the page. The numbers in the tuple are the left, upper, right, and lower coordinates of the screen.
* Run script:
  * If you use a virtual environment, you need to activate it.
  * Run ```python3 main_screen2pdf.py```
  * Answer "y" or "n" to set options.
  * Press ENTER to start
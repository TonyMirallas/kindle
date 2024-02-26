from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from . import globals

def _init_driver():
    options = Options()
    options.profile = globals.profile
    driver = webdriver.Firefox(options=options)
    return driver


def _close_driver(driver):
    driver.quit()


def get_books():
    
    driver = _init_driver()
    
    driver.get(globals.url)
    driver.implicitly_wait(10)
    books = driver.find_elements(By.CLASS_NAME, globals.books)
    
    data = []
    
    for book in books:
        book.click()
        driver.implicitly_wait(10)
        title = driver.find_element(By.CSS_SELECTOR, globals.title).text
        author = driver.find_element(By.CSS_SELECTOR, globals.author).text
        highlights_count = driver.find_element(By.ID, globals.highlights_count).text
        highlights_block = driver.find_element(By.ID, globals.highlight_block)
        print(f"Title: {title}\nAuthor: {author}\nHighlights: {highlights_count}\n")
        highlights = highlights_block.find_elements(By.ID, globals.highlight)
        
        for highlight in highlights:
            data.append([author, title, highlights_count, highlight.text])
            print(highlight.text)
                    
    _close_driver(driver)    
            
    return data
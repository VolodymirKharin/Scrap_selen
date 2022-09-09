from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
from datetime import date, timedelta
from models.crud import add_to_db
import locale
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import datetime


def get_source_html(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get(url=url)

    while True:
        try:
            pagination = driver.find_element(by=By.CLASS_NAME,
                                             value="pagination").find_elements(by=By.TAG_NAME, value="a")
            print(pagination[-2].text)
            if 'Next' not in pagination[-2].text:
                print('test3')
                get_card_from_page(driver)
                break
            else:
                get_card_from_page(driver)
                next_page = driver.find_element(by=By.CLASS_NAME,
                                                value="pagination").find_elements(by=By.TAG_NAME, value="a")
                print(next_page[-2].text)
                driver.get(pagination[-2].get_attribute('href'))


        except Exception as e:
            print(f'{e}')
            break
    driver.implicitly_wait(3)
    driver.close()
    driver.quit()


def get_card_from_page(driver):
    driver.implicitly_wait(3)
    find_all_cards = driver.find_elements(by=By.CLASS_NAME, value="search-item")
    number_card = 0
    print(len(find_all_cards))
    for card in find_all_cards:
        number_card += 1
        date_posted = card.find_element(by=By.CLASS_NAME, value="date-posted").text
        title = card.find_element(by=By.CLASS_NAME, value="title").find_element(by=By.TAG_NAME, value="a").text
        new_date_posted = get_time(date_posted)

        city = card.find_element(by=By.CLASS_NAME,
                                    value="location").find_element(by=By.TAG_NAME, value="span").text

        room_link = card.find_element(by=By.CLASS_NAME,
                                         value="title").find_element(by=By.TAG_NAME, value="a").get_attribute('href')
        print(room_link)
        driver.implicitly_wait(10)
        driver.execute_script(f"window.open('{room_link}')")
        driver.switch_to.window(driver.window_handles[1])

        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "priceWrapper-1165431705")))

        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'priceWrapper-1165431705')))
        price = driver.find_element(by=By.CLASS_NAME,
                                    value="priceWrapper-1165431705").find_element(by=By.TAG_NAME, value="span").text
        price = get_price(price)

        amount_bads = driver.find_element(by=By.CLASS_NAME,
                                   value="titleAttributes-2381855425").find_elements(by=By.TAG_NAME, value="li")[1].text
        try:
            url_img = driver.find_element(by=By.CLASS_NAME,
                                          value="container-4202182046").find_element(by=By.TAG_NAME,
                                                                                     value="source").get_attribute('srcset')
        except:
            url_img = 'No image'

        try:
            view_btn = driver.find_element(by=By.CLASS_NAME, value="showMoreButton-2571466895")
            driver.execute_script("arguments[0].click();", view_btn)
            driver.implicitly_wait(10)
            description = driver.find_element(by=By.CLASS_NAME,
                                              value="descriptionContainer-231909819").text
            if 'Description' in description:
                description = description[len('Description '):]
        except:
            description = 'No description'

        print(number_card)
        print(title, price, amount_bads, new_date_posted, url_img, city)
        print(description)
        add_to_db(title=title, link=url_img, date=new_date_posted, city=city, beds=amount_bads, description=description, price=price)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def get_price(price):
    if price == 'Please Contact':
        return None
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    price = locale.atof(price.strip("$"))
    return price


def get_time(date_posted):
    if 'minutes' in date_posted or 'minute' in date_posted or 'hours' in date_posted or 'hour' in date_posted:
        new_date_posted = datetime.datetime.strftime(datetime.datetime.today(), "%d-%m-%y")
    elif 'Yesterday' in date_posted:
        yesterday = date.today() - timedelta(days=1)
        new_date_posted = datetime.datetime.strftime(yesterday, "%d-%m-%y")
    else:
        d = datetime.datetime.strptime(date_posted, "%d/%m/%Y")
        new_date_posted = datetime.datetime.strftime(d, "%d-%m-%Y")
    return new_date_posted


def main():
    url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'
    get_source_html(url)


if __name__ == '__main__':
    main()

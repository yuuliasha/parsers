from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Настройка WebDriver для работы в headless режиме
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# URL первой страницы
base_url = 'https://wowblogger.ru/bloggers/categories/biznes'
driver.get(base_url)

# Списки для хранения данных
names = []
subscribers = []
reach = []
cpv = []
er = []
prices = []
urls = []


# Функция для извлечения данных с текущей страницы
def extract_data():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all(class_='catalog__card-name')
    for card in cards:
        # Название канала
        name = card.text.strip()
        names.append(name)

        # Данные метрик
        metrics = card.find_next_sibling('div', class_='catalog__card-column')
        subscriber_count = metrics.find('div', text='Подписчики').find_next('div').text.strip()
        reach_count = metrics.find('div', text='Охваты').find_next('div').text.strip()
        cpv_value = metrics.find('div', text='CPV').find_next('div').text.strip()
        er_value = metrics.find('div', text='ER').find_next('div').text.strip()

        # Цена
        price = card.find_next('span').text.strip()

        # Сохранение данных
        subscribers.append(subscriber_count)
        reach.append(reach_count)
        cpv.append(cpv_value)
        er.append(er_value)
        prices.append(price)

        # URL страницы блогера
        try:
            card_link = driver.find_element(By.CLASS_NAME, 'catalog__card-name')
            card_url = card_link.get_attribute('href')
            urls.append(card_url)
        except:
            urls.append('URL не найден')


# Основная функция для парсинга всех страниц с использованием кнопки "Показать ещё"
def scrape_all_pages():
    while True:
        print("Сбор данных с текущей страницы...")
        extract_data()

        try:
            # Кликаем на кнопку "Показать ещё"
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-accent'))
            )
            show_more_button.click()
            time.sleep(3)  # Ожидание подгрузки следующей порции данных
        except:
            print("Данные на всех страницах собраны.")
            break


# Запуск парсинга всех страниц
scrape_all_pages()

# Сохранение данных в CSV-файл
df = pd.DataFrame({
    'Name': names,
    'Subscribers': subscribers,
    'Reach': reach,
    'CPV': cpv,
    'ER': er,
    'Price': prices,
    'URL': urls
})
df.to_csv('bloggers_data_for_lue.csv', index=False, encoding='utf-8-sig')
print("Данные успешно сохранены в bloggers_data.csv")

# Закрытие браузера
driver.quit()

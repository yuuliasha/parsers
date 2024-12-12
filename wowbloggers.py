import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Настройки для работы в фоновом режиме
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Инициализация драйвера
driver = webdriver.Chrome(options=chrome_options)
base_url = 'https://wowblogger.ru/bloggers'
driver.get(base_url)

# Базовый URL для полного пути к карточкам
base_card_url = "https://wowblogger.ru"

# Открываем CSV-файл и записываем заголовок
with open('bloggers_baza_fsfjsf.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Subscribers', 'Reach', 'CPV', 'ER', 'Price', 'Platform URL', 'Card URL', 'Channel Theme'])

    # Функция для извлечения данных из карточек на странице
    def extract_data():
        # Ждем, чтобы страница полностью загрузилась
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'catalog__card')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cards = soup.find_all(class_='catalog__card')

        # Подсчет количества добавленных блогеров на текущей странице
        count = 0

        for card in cards:
            # Название канала
            title = card.find(class_='catalog__card-name').text.strip()

            # Подписчики
            subscriber_count = card.find('div', text='Подписчики')
            if subscriber_count:
                subscriber_count = subscriber_count.find_next('div').text.strip()
            else:
                subscriber_count = 'Неизвестно'

            # Охваты
            reach = card.find('div', text='Охваты')
            if reach:
                reach = reach.find_next('div').text.strip()
            else:
                reach = 'Неизвестно'

            # CPV
            cpv = card.find('div', text='CPV')
            if cpv:
                cpv = cpv.find_next('div').text.strip()
            else:
                cpv = 'Неизвестно'

            # ER
            er = card.find('div', text='ER')
            if er:
                er = er.find_next('div').text.strip()
            else:
                er = 'Неизвестно'

            # Цена
            price = 'Неизвестно'
            price_spans = card.find_all('span')
            for span in price_spans:
                if '₽' in span.text:
                    price = span.text.strip()
                    break

            # URL платформы
            platform_url_tag = card.find('a', class_='card__name')
            platform_url = platform_url_tag['href'] if platform_url_tag and platform_url_tag.get('href') else 'Неизвестно'

            # URL карточки
            try:
                card_url = card.find('a')['href']
                if not card_url.startswith("http"):
                    card_url = base_card_url + card_url
            except:
                card_url = 'Неизвестно'

            # Тематика канала
            themes = card.find(class_='catalog__card-categories')
            if themes:
                channel_theme = ", ".join([span.text.strip() for span in themes.find_all('span')])
            else:
                channel_theme = 'Неизвестно'

            # Запись данных в CSV-файл
            writer.writerow([title, subscriber_count, reach, cpv, er, price, platform_url, card_url, channel_theme])

            # Вывод информации о добавленных данных
            print(f"Добавлен блогер: {title}")
            print(f"  Подписчики: {subscriber_count}")
            print(f"  Охваты: {reach}")
            print(f"  CPV: {cpv}")
            print(f"  ER: {er}")
            print(f"  Цена: {price}")
            print(f"  Платформа: {platform_url}")
            print(f"  URL карточки: {card_url}")
            print(f"  Тематика канала: {channel_theme}")
            print("-" * 50)

            # Увеличиваем счетчик добавленных блогеров
            count += 1

        # Возвращаем количество добавленных блогеров
        return count

    # Основная функция для парсинга всех страниц с пагинацией
    def scrape_all_pages():
        page_number = 1
        total_bloggers_added = 0

        while True:
            print(f"Парсим страницу {page_number}...")

            # Генерируем URL для текущей страницы
            current_page_url = f"{base_url}?page={page_number}"
            driver.get(current_page_url)

            # Ждем, чтобы страница загрузилась
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'catalog__card')))
            time.sleep(3)  # Задержка для дополнительной загрузки

            # Парсим данные со страницы и получаем количество добавленных блогеров
            added_bloggers = extract_data()
            total_bloggers_added += added_bloggers

            print(f"Добавлено {added_bloggers} блогеров на странице {page_number}.")

            # Переход на следующую страницу, если были добавлены блогеры
            if added_bloggers > 0:
                page_number += 1
            else:
                print("Все страницы спарсены.")
                break

        print(f"Общее количество добавленных блогеров: {total_bloggers_added}")

    # Запуск парсинга всех страниц
    scrape_all_pages()

# Завершаем работу драйвера
driver.quit()
print("Данные успешно сохранены в bloggers.csv")

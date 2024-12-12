from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Настройки для Selenium (например, использование Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Фоновый режим

# Укажите путь к драйверу Chrome (замените путь на ваш, если необходимо)
driver = webdriver.Chrome(options=options)

# Открываем сайт
url = 'https://dsgners.ru/'
driver.get(url)

# Явное ожидание для полной загрузки страницы (60 секунд)
try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
except Exception as e:
    print("Ошибка при ожидании загрузки страницы:", e)

# Переменная для хранения статей
data = []

# Прокручиваем страницу для загрузки всех статей
previous_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Получаем элементы статей
    articles = driver.find_elements(By.XPATH, "//a[contains(@class, 'crayons-story__secondary')]")
    article_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/ux/')]")

    # Извлекаем данные
    for author, article in zip(articles, article_links):
        author_name = author.text
        author_link = author.get_attribute('href')
        article_title = article.text
        article_link = article.get_attribute('href')

        data.append({
            'author_name': author_name,
            'author_link': author_link,
            'article_title': article_title,
            'article_link': article_link
        })

    # Выводим количество уже спарсенных данных
    print(f"Спарсено данных: {len(data)} из {len(articles)}")

    # Прокручиваем вниз
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Ждем загрузку новых данных

    # Получаем новую высоту страницы и сравниваем
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == previous_height:  # Если высота не изменилась, выходим из цикла
        break
    previous_height = new_height

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV файл
df = pd.DataFrame(data)
df.to_csv('articles_dsgners_ru.csv', index=False)

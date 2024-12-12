from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Настройки для Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме (можно убрать для отладки)

# Путь к вашему chromedriver
s = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=s, options=chrome_options)

# URL сайта
url = 'https://m.seonews.ru/analytics/'  # Ссылка на сайт

# Открыть сайт
driver.get(url)

# Кликать на кнопку "Показать ещё", пока она есть на странице
while True:
    try:
        # Ждем, пока кнопка станет кликабельной
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'show-more-button'))
        )
        show_more_button.click()  # Клик по кнопке
        time.sleep(3)  # Ждем загрузки новых данных
    except:
        # Если кнопка больше не находится, выходим из цикла
        break

# Собираем ссылки на статьи
article_links = driver.find_elements(By.CSS_SELECTOR, 'a.news-card__link')  # пример CSS селектора

# Инициализация списка для данных
data = []

# Проход по каждой статье
for link in article_links:
    article_url = link.get_attribute('href')
    driver.get(article_url)  # Открываем каждую статью
    time.sleep(2)  # Ждем загрузки страницы

    # Извлекаем информацию
    try:
        title = driver.find_element(By.CLASS_NAME, 'title').text
        author_name = driver.find_element(By.CLASS_NAME, 'descr-fio').text.strip()
        author_position = driver.find_element(By.XPATH,
                                              '//div[@class="author"]//div[contains(text(), "специалист")]').text.strip()  # Измените при необходимости

        # Добавляем данные в список
        data.append({
            'URL': article_url,
            'Title': title,
            'Author': author_name,
            'Position': author_position
        })

        # Печатаем количество спарсенных авторов
        print(f'Спарсено авторов: {len(data)}')

    except Exception as e:
        print(f'Ошибка при обработке статьи {article_url}: {e}')

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV
df = pd.DataFrame(data)
df.to_csv('articles_seo.csv', index=False)
print("Парсинг завершен. Данные сохранены в 'articles_se0.csv'.")

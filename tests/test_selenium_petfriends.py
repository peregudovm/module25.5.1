# Командная строка для запуска через терминал:
# python -m pytest -v --driver Chrome --driver-path C:/Users/Users/Downloads/chromedriver.exe test_selenium_petfriends.py

import pytest
from selenium import webdriver
driver = webdriver.Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# явное ожидание
from settings import valid_email, valid_password


@pytest.fixture(autouse=True)
def testing():
   # Указываем путь к вебрайверу
   pytest.driver = webdriver.Chrome('C:/Users/User/Downloads/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('valid_email')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('valid_password')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   yield

   pytest.driver.close()

# Проверка на присутствие всех my pets:
def test_show_all_my_pets():
   # Нажимаем кнопку "Мои питомцы" для открытия страницы с таблицей питомцев пользователя
   pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
   # Проверяем, что мы перешли на страницу с таблицей питомцев пользователя
   # Ожидание явное, применимо только в учебных целях
   # time.sleep(5)

   driver.element = WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.XPATH, ('//a[contains(text(), "Мои питомцы")]'))))

   # Выбираем моих питомцев локатором кнопки удаления животного
   locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')
   # проверяем, наличие моих питомцев(по требованию, количество животных берем из статистики)
   quantity_of_my_pets_from_user_statistic = 3
   assert len(locator_for_all_my_pets) == quantity_of_my_pets_from_user_statistic

# Проверка параметров карточек питомцев:
def test_card_my_pets():
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# Проверка на то, что хотя бы у половины my pets имеется фото:
def test_half_of_my_pets_with_photo():
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    # Выбираем моих питомцев локатором кнопки удаления животного
    locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')
    # Выбираем все элементы фотографий питомцев пользователя
    images = pytest.driver.find_elements_by_xpath('//th/img')
    # Назначаем переменную для подсчёта количества питомцев пользователя с фотографией
    number_of_pets_with_photo = 0
    # Устанавливаем неявные ожидания(секунды)
    driver.implicitly_wait(5)
    # Через проверку у всех питомцев, что attribute 'src' не пустое значение, определяем
    # количество питомцев с фотографией
    for i in range(len(locator_for_all_my_pets)):
        if images[i].get_attribute('src') != '':
            number_of_pets_with_photo += 1
        else:
            number_of_pets_with_photo = number_of_pets_with_photo
    # Проверяем, что как min половина всех питомцев имеет фотографию
    assert number_of_pets_with_photo >= (len(locator_for_all_my_pets) / 2)

# Проверка того, что у всех my pets имеется имя, тип(порода) и возраст:
def test_all_my_pets_with_name_type_age():
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    # Выбираем моих питомцев локатором кнопки удаления животного
    locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')

    for i in range(len(locator_for_all_my_pets)):
        # для элемента locator_for_all_my_pets (кнопка удаления питомца) находим все три
        # сосединие тэга "td" соответствующие имени, типу и возрасту питомца
        pet = locator_for_all_my_pets[i].find_elements_by_xpath('preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = pet[2].text
        # Устанавливаем неявные ожидания(секунды)
        driver.implicitly_wait(5)
        # находим текст тэга "td" с индексом 1 соответсвующий типу питомца
        # и присваеваем переменной "anymal_type"
        anymal_type = pet[1].text
        # Устанавливаем неявные ожидания(секунды)
        driver.implicitly_wait(5)
        # находим текст тэга "td" с индексом 0 соответсвующий возрасту питомца
        # и присваеваем переменной "age"
        age = pet[0].text
        # Устанавливаем неявные ожидания(секунды)
        driver.implicitly_wait(5)
        # проверяем, что у каждого питомца есть имя, тип и возраст
        assert name != ''
        assert anymal_type != ''
        assert age != ''

# Проверка на то, что у всех my pets разные имена:
def test_all_my_pets_with_different_names():
    # Нажимаем кнопку "Мои питомцы" для вызова списка питомцев пользователя
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
    # Выбираем моих питомцев локатором кнопки удаления животного
    locator_for_all_my_pets = pytest.driver.find_elements_by_xpath('//td[@class="smart_cell"]')
    # Создаем пустой список для имён питомцев пользователя
    list_of_pets_names = []
    for i in range(len(locator_for_all_my_pets)):
        # для элемента locator_for_all_my_pets (кнопка удаления питомца) находим все три
        # сосединие тэга "td" соответствующие имени, типу и возрасту потомца
        pet = locator_for_all_my_pets[i].find_elements(By.XPATH, 'preceding-sibling::td')
        # находим текст тэга "td" с индексом 2 соответсвующий имени питомца
        # и присваеваем переменной "name"
        name = pet[2].text
        # добавляем имя питомца в список list_of_pets_names
        list_of_pets_names.append(name)
    # для проверки уникальности имени питомца, проверяем количество вхождений каждого
    # имени в списке имён питомцев
    for name in list_of_pets_names:
        assert list_of_pets_names.count(name) == 1
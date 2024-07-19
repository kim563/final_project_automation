from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.ui_class import ScheduleUi
from config.config import LOGIN, PASSWORD

def start_ui_test(driver):
    driver.auth()
    driver.go_to_schedule()
    driver.open_popup_event()
    driver.add_tile_event("Погулять с собакой")


# Ввод валидных значений в название события в форму “Личное событие”
def test_title():
    servChrom = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = servChrom)
    ui = ScheduleUi(driver, LOGIN, PASSWORD)
    start_ui_test(ui)
    assert ui.is_enable_submit() == True
    ui.close_browser()

# Выбор дня из выпадающего списка в форме “Личное событие”
def test_choice_day():
    servChrom = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = servChrom)
    ui = ScheduleUi(driver, LOGIN, PASSWORD)
    start_ui_test(ui)
    ui.select_date("2024-07-14T17:00:00.000Z")
    assert ui.is_enable_submit() == True
    ui.close_browser()

# Время начала события (00:00) в форме “Личное событие”
def test_choice_start_time():
    servChrom = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = servChrom)
    ui = ScheduleUi(driver, LOGIN, PASSWORD)
    start_ui_test(ui)
    ui.input_start_event(00, 00)
    ui.input_end_event(10, 00)
    assert ui.is_enable_submit() == True
    ui.close_browser()


# Текст описания до 500 символов в форме “Личное событие”
def test_description():
    servChrom = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = servChrom)
    ui = ScheduleUi(driver, LOGIN, PASSWORD)
    text = "В наше время технологии играют огромную роль в повседневной жизни. Они упрощают нашу работу, облегчают общение, помогают в обучении. Важно помнить, что технологии - это всего лишь инструменты, которые нужно использовать с умом. Не забывайте об оффлайн-мире и общении лицом к лицу. Важно найти баланс между онлайн и оффлайн, чтобы сохранить гармонию и здоровье души. Помните, что выше всего ценится гармония и равновесие. Важно найти баланс между онлайн и оффлайн, чтобы сохранить гармонию и здоровье."
    start_ui_test(ui)
    ui.input_description(text)
    assert ui.is_enable_submit() == True
    ui.close_browser()


# Выбор цвет события в форме “Личное событие”
def test_color():
    servChrom = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = servChrom)
    ui = ScheduleUi(driver, LOGIN, PASSWORD)
    start_ui_test(ui)
    ui.select_color(4)
    assert ui.is_enable_submit() == True
    ui.close_browser()

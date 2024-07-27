import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.ui_class import ScheduleUi
from config.config import LOGIN, PASSWORD


@allure.epic("Тестирование Ui")
@allure.severity("blocker")
@allure.feature("CREATE")
@allure.story("Личное событие")
class UiTest:
    """Класс предоставляет методы для тестирования Ui сервера"""

    def start_ui_test(self, ui: ScheduleUi):

        with allure.step("Авторизация на сайте"):
            ui.auth()

        with allure.step("Переход во вкладку расписание"):
            ui.go_to_schedule()

        with allure.step(
                "Открытие всплывающего окна и переход во \
                вкладку Личное событие"
                    ):
            ui.open_popup_event()

        with allure.step("Задать название события"):
            ui.add_tile_event("Погулять с собакой")

    @allure.id("Skyeng-1")
    @allure.title(
        "Ввод валидных значений в название события в форму “Личное событие”"
        )
    @allure.description(
        "Данный тест проверяет валидность вводимых значений в название \
        личных событий в расписании преподавателей."
        )
    @pytest.mark.ui_test
    def test_title(self):
        with allure.step("Создание драйвера"):
            servChrom = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=servChrom)

        with allure.step("Создание экзкмпляра класса ScheduleUi"):
            ui = ScheduleUi(driver, LOGIN, PASSWORD)

        with allure.step("Начальная подготовка к тестам"):
            self.start_ui_test(ui)

        with allure.step("Проверка подтвержения отправки формы"):
            assert ui.is_enable_submit()

        with allure.step("Закрытие браузера"):
            ui.close_browser()

    @allure.id("Skyeng-2")
    @allure.title("Выбор дня из выпадающего списка в форме “Личное событие”")
    @allure.description(
        "Данный тест проверяет выбор дня личных событий в \
        расписании преподавателей."
        )
    @pytest.mark.ui_test
    def test_choice_day(self):
        with allure.step("Создание драйвера"):
            servChrom = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=servChrom)

        with allure.step("Создание экзкмпляра класса ScheduleUi"):
            ui = ScheduleUi(driver, LOGIN, PASSWORD)

        with allure.step("Начальная подготовка к тестам"):
            self.start_ui_test(ui)

        with allure.step("Ввод значений даты события"):
            ui.select_date("2024-07-28T17:00:00.000Z")

        with allure.step("Проверка подтвержения отправки формы"):
            assert ui.is_enable_submit()

        with allure.step("Закрытие браузера"):
            ui.close_browser()

    @allure.id("Skyeng-3")
    @allure.title("Время начала события (00:00) в форме “Личное событие”")
    @allure.description(
        "Данный тест проверяет время начала личного события (00:00) в \
        расписании преподавателей."
        )
    @pytest.mark.ui_test
    def test_choice_start_time(self):
        with allure.step("Создание драйвера"):
            servChrom = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=servChrom)

        with allure.step("Создание экзкмпляра класса ScheduleUi"):
            ui = ScheduleUi(driver, LOGIN, PASSWORD)

        with allure.step("Начальная подготовка к тестам"):
            self.start_ui_test(ui)

        with allure.step("Задать часы и минуты начала личного события"):
            ui.input_start_event(00, 00)

        with allure.step("Задать часы и минуты окончания личного события"):
            ui.input_end_event(10, 00)

        with allure.step("Проверка подтвержения отправки формы"):
            assert ui.is_enable_submit()

        with allure.step("Закрытие браузера"):
            ui.close_browser()

    @allure.id("Skyeng-4")
    @allure.title("Текст описания до 500 символов в форме “Личное событие”")
    @allure.description(
        "Данный тест проверяет колличесво символов в описании личных событий \
        в расписании преподавателей."
        )
    @pytest.mark.ui_test
    def test_description(self):
        with allure.step("Создание драйвера"):
            servChrom = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=servChrom)

        with allure.step("Создание экзкмпляра класса ScheduleUi"):
            ui = ScheduleUi(driver, LOGIN, PASSWORD)

        with allure.step("Ввод валидных значений описания, до 500"):
            text = "В наше время технологии играют огромную роль в \
            повседневной жизни. Они упрощают нашу работу, облегчают \
            общение, помогают в обучении. Важно помнить, что технологии \
            - это всего лишь инструменты, которые нужно использовать с умом. \
            Не забывайте об оффлайн-мире и общении лицом к лицу. Важно \
            найти баланс между онлайн и оффлайн, чтобы сохранить гармонию \
            и здоровье души. Помните, что выше всего ценится гармония и \
            равновесие. Важно найти баланс между онлайн и оффлайн, \
            чтобы сохранить гармонию и здоровье."

        with allure.step("Начальная подготовка к тестам"):
            self.start_ui_test(ui)
            ui.input_description(text)

        with allure.step("Проверка подтвержения отправки формы"):
            assert ui.is_enable_submit()

        with allure.step("Закрытие браузера"):
            ui.close_browser()

    @allure.id("Skyeng-5")
    @allure.title("Выбор цвета события в форме “Личное событие”")
    @allure.description(
        "Данный тест проверяет выбор цвета личных событий \
        в расписании преподавателей."
        )
    @pytest.mark.ui_test
    def test_color(self):
        with allure.step("Создание драйвера"):
            servChrom = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=servChrom)

        with allure.step("Создание экзкмпляра класса ScheduleUi"):
            ui = ScheduleUi(driver, LOGIN, PASSWORD)

        with allure.step("Начальная подготовка к тестам"):
            self.start_ui_test(ui)

        with allure.step("Выбор цвета"):
            ui.select_color(4)

        with allure.step("Проверка подтвержения отправки формы"):
            assert ui.is_enable_submit()

        with allure.step("Закрытие браузера"):
            ui.close_browser()

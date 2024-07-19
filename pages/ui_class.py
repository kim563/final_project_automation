from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from config.config import URL_UI

class ScheduleUi:

# Инициализация
    def __init__(self, driver, login, password):
        self._driver = driver
        self.login = login
        self.password = password
        self._driver.get(URL_UI)
        self._driver.implicitly_wait(10)
      

    def close_browser(self):
        """
            Закрытие браузера
        """
        self._driver.quit()

    def auth(self):
        """
            Авторизация
        """
        button_login = self._driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="cms-header-login"]'
        )
        button_login.click()

        button_change = self._driver.find_element(
            By.XPATH, "//a[text()='Войти с помощью пароля']"
        )
        button_change.click()

        Username = self._driver.find_element(
            By.CSS_SELECTOR, "input[name='username']"
        )
        Username.send_keys(self.login)

        Password = self._driver.find_element(
            By.CSS_SELECTOR, "input[name='password']"
        )
        Password.send_keys(self.password)

        button_login = self._driver.find_element(
            By.XPATH, "//span[text()='Войти']"
        )
        button_login.click()

    def go_to_schedule(self):
        button_schedule = self._driver.find_element(
            By.CSS_SELECTOR, 'a[data-qa-id="left-menu-item:Расписание"]'
        )
        button_schedule.click()

    def open_popup_event(self):
        button_add = self._driver.find_element(
            By.CSS_SELECTOR, 'ds-icon[name="add"]'
        )
        button_add.click()

        tab_event = self._driver.find_element(
            By.XPATH, "//span[text()=' Личное событие ']"
        )
        tab_event.click()

    def add_tile_event(self, title):
        input_title = self._driver.find_element(
            By.CSS_SELECTOR, "app-title-limit-hint + input"
        )
        input_title.send_keys(title)

    def select_date(self, date):
        select = Select(self._driver.find_element(
            By.CLASS_NAME, "class-date"
        ))
        select.select_by_value(date)

    def input_start_event(self, start_h, start_m):
        input_start_h = self._driver.find_element(
            By.CSS_SELECTOR, "app-time-picker:nth-child(1) .input-hours"
        )
        input_start_h.clear()
        input_start_h.send_keys(start_h)

        input_start_m = self._driver.find_element(
            By.CSS_SELECTOR, "app-time-picker:nth-child(1) .input-minutes"
        )
        input_start_m.clear()
        input_start_m.send_keys(start_m)

    def input_end_event(self, end_h, end_m):
        input_end_h = self._driver.find_element(
            By.CSS_SELECTOR, "app-time-picker:nth-child(3) .input-hours"
        )
        input_end_h.clear()
        input_end_h.send_keys(end_h)

        input_end_m = self._driver.find_element(
            By.CSS_SELECTOR, "app-time-picker:nth-child(3) .input-minutes"
        )
        input_end_m.clear()
        input_end_m.send_keys(end_m)

    def input_description(self, text):
        input_desc = self._driver.find_element(
            By.CSS_SELECTOR, "app-title-limit-hint + textarea"
        )
        input_desc.send_keys(text)

    def select_color(self, opt):
        button_color = self._driver.find_element(
            By.CSS_SELECTOR,
            ("app-color-picker > div > div:nth-child(" + str(opt) + ")")
        )
        button_color.click()

    def submit_add_event(self):
        button_save = self._driver.find_element(
            By.CSS_SELECTOR, "sky-ui-popup sky-ui-button"
        )
        button_save.click()
    
    def is_enable_submit(self):
        button = self._driver.find_element(
            By.CSS_SELECTOR, "sky-ui-popup sky-ui-button > button"
        )
        active = "-active"
        class_list = button.get_attribute('class').split()
        print(class_list)
        if active in class_list:
            return True
        else:
            return False
       
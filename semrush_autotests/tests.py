import time
import uuid
import unittest
from time import gmtime, strftime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class SEMrushTest(unittest.TestCase):
    def wait_for_element_load(self, class_name='', timeout=30):
        """Метод с помощью которого ожидаю загрузку определенного элемента"""
        out_of_time = time.time() + timeout
        element = None
        while not element:
            try:
                element = self.driver.find_element_by_class_name(class_name)
            except NoSuchElementException:
                if time.time() > out_of_time:
                    self.fail("Element {} not load".format(class_name))
            WebDriverWait(self.driver, 1)

    def wait_for_element_close(self, class_name='', timeout=30):
        """Метод с помощью которого ожидаю закрытие определенного элемента"""
        out_of_time = time.time() + timeout
        try:
            element = self.driver.find_element_by_class_name(class_name)
        except NoSuchElementException:
            return
        while element:
            try:
                element = self.driver.find_element_by_class_name(class_name)
                if time.time() > out_of_time:
                    self.fail("Element {} not close".format(class_name))
            except NoSuchElementException:
                break
            WebDriverWait(self.driver, 1)

    def __is_login(self):
        """Метод для проверки авторизован пользователь или нет"""
        try:
            self.driver.find_element_by_class_name("js-authentication-login")
        except NoSuchElementException:
            return True
        return False

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://www.semrush.ru")
        assert "SEMrush" in self.driver.title

    def test_auth(self):
        """Реализация первого теста. Залогиниться под пользователем в SEMrush."""

        #Константы для теста // скорее всего их лучше вынести в конфиг
        USER_EMAIL = "9112525767@mail.ru"
        USER_PASS = "123456"

        # Проверю, вдруг уже залогинен
        if self.__is_login():
            return

        # Кликаю по кнопке "Войти"
        self.driver.find_element_by_class_name("js-authentication-login").click()

        # Ожидаю, что форма аутентификации появилась
        try:
            self.driver.find_element_by_class_name("base-popup__content")
        except NoSuchElementException:
            self.fail("Authentication form not opened")

        # Заполняю поля email и pass
        input_fields = self.driver.find_elements_by_class_name("auth-form__input")
        for field in input_fields:
            if field.get_attribute("name") == "email":
                field.send_keys(USER_EMAIL)
            elif field.get_attribute("name") == "password":
                field.send_keys(USER_PASS)

        # Кликаю по кнопке "Войти" на форме аутентификации
        self.wait_for_element_load(class_name="auth-form__button")
        self.driver.find_element_by_class_name("auth-form__button").click()

        # Ожидаю, пока не загрузится панель управления
        self.wait_for_element_load(class_name="srf-report-sidebar-management")
        # Проверяю что залогинился именно под своим пользователем
        # Ожидаю пока появится верхняя панель навигации
        self.wait_for_element_load(class_name="js-header")
        # Ищу кнопку управления профилем
        header_nav = self.driver.find_element_by_class_name("js-header")
        for _togle in header_nav.find_elements_by_class_name("header__navigation-item"):
            if _togle.get_attribute("data-test") == "header-menu__user":
                _togle.click()
        # Ожидаю пока появится меню управления профилем
        self.wait_for_element_load(class_name="header-dropdown__menu")
        current_user = ''
        user_menu = self.driver.find_element_by_class_name("header-dropdown__menu")
        for _div in self.driver.find_elements_by_class_name("header-dropdown__item"):
            if _div.get_attribute("data-test") == "header-menu__user-profile":
                current_user = _div.find_element_by_class_name("header-dropdown__description").text
        self.assertEqual(current_user, USER_EMAIL)

    def test_create_notice(self):
        """Реализация второго теста. Создайте новую заметку на /notes."""

        # Константы для теста
        NOTICE_TITLE = str(uuid.uuid4())
        NOTICE_BODY = "Эта заметка создана с помощью Selenium {}".format(
            strftime("%Y-%m-%d %H:%M:%S", gmtime())
        )

        # Сначала нужно залогиниться под пользователем в SEMrush
        self.test_auth()

        # В панели управления, слева, ищу ссылку "Заметки" и кликаю по ней
        sidebar_management = self.driver.find_element_by_class_name("srf-report-sidebar-management")
        for _a in sidebar_management.find_elements_by_tag_name("a"):
            if "/notes/" in _a.get_attribute("href"):
                _a.click()
                break

        # Жду пока загрузится таблица с заметками
        self.wait_for_element_load(class_name="notes-list__cell_datetime")

        # Ищу кнопку "Добавить заметку" и кликаю по ней
        filter_region = self.driver.find_element_by_class_name("notes-list__filter-bar")
        for button in filter_region.find_elements_by_tag_name("button"):
            if button.get_attribute("data-cream-action") == "add-note":
                button.click()

        # Ожидаю пока откроется форма ввода новой заметки
        self.wait_for_element_load(class_name="notes-editor")
        notice_form = self.driver.find_element_by_class_name("notes-editor")

        # Заполняю поле "Название" заметки
        for field in notice_form.find_elements_by_tag_name("input"):
            if field.get_attribute("data-cream-ui") == "input-title":
                field.send_keys(NOTICE_TITLE)

        # Заполняю поле "Описание" заметки
        for field in notice_form.find_elements_by_tag_name("textarea"):
            if field.get_attribute("data-cream-ui") == "input-note":
                field.send_keys(NOTICE_BODY)

        # Кликаю по кнопке сохранить заметку
        form_footer = self.driver.find_element_by_class_name("cream-popup__footer")
        for button in form_footer.find_elements_by_tag_name("button"):
            if 'save' in button.get_attribute("data-cream-action"):
                button.click()

        # Жду когда закроется форма создания заметки
        self.wait_for_element_close(class_name="notes-editor")

        # Получаю тело таблицы с заметками
        notice_body = self.driver.find_element_by_class_name(
            "notes-list-items-container").find_element_by_tag_name("tbody")

        notice_is_create = False
        # Прохожу по каждой строке таблицы с заметками
        for tr in notice_body.find_elements_by_tag_name("tr"):
            # В этой строке ищу заголовок и тело заметки. Затем сверяю с тем, что создавал.
            if tr.find_element_by_class_name("notes-note-title").text == NOTICE_TITLE and \
                    tr.find_element_by_class_name("notes-list__note-text-inner").text == NOTICE_BODY:
                notice_is_create = True
                break

        # Если такая заметка существует, все ок
        self.assertEqual(notice_is_create, True)

    def test_create_project(self):
        """Реализация третьего теста. Создайте новый проект"""
        # Константы для теста
        PROJECT_DOMAIN = "semrush.com"
        PROJECT_NAME = "selenium_project"

        # Сделал вложенную функцию которая удаляет проект
        def _delete_project():
            # Ожидаю когда загрузится панель управления проектом
            self.wait_for_element_load(class_name="js-project-tools")
            #
            time.sleep(5)
            # Ожидаю когда загрузится кнопка "шестеренка" настройки проекта
            self.wait_for_element_load(class_name="sr-infomenu")
            # Кликаю по шестеренке
            self.driver.find_element_by_class_name("sr-infomenu-title").click()
            # Ожидаю когда появится меню настроек
            self.wait_for_element_load(class_name="sr-infomenu-content-wrapper")
            # Пробегаю по всем тегам "a" этого меню
            settings_menu = self.driver.find_element_by_class_name("sr-infomenu-content-wrapper")
            for p_btn in settings_menu.find_elements_by_tag_name("a"):
                # Ищу кнопку "Удалить" и кликаю по ней
                if p_btn.text == "Delete":
                    p_btn.click()
                    break
            # Жду появления окна удаления проекта. Туда надо ввести имя, для подтверждения
            self.wait_for_element_load(class_name="pr-popup")
            # Получаю имя текущего проекта и заполняю поле ввода
            current_project_name = self.driver.find_element_by_class_name("pr-dialog-attention").text
            self.driver.find_element_by_class_name("js-remove-input").send_keys(current_project_name)
            # Пробегаю по всем кнопкам "buttons" формы удаления
            for form_button in self.driver.find_element_by_class_name(
                    "pr-dialog-btns").find_elements_by_tag_name("button"):
                # Ищу кнопку удаления и кликаю по ней
                if form_button.find_element_by_class_name("s-btn__text").text == "Delete":
                    form_button.click()
                    break

        # Сначала нужно залогиниться под пользователем в SEMrush
        self.test_auth()

        # В панели управления, слева, ищу ссылку "Проекты" и кликаю по ней
        sidebar_management = self.driver.find_element_by_class_name("srf-report-sidebar-management")
        for _a in sidebar_management.find_elements_by_tag_name("a"):
            if "/projects/" in _a.get_attribute("href"):
                _a.click()
                break

        # Ожидаю когда загрузится меню управления проектами
        self.wait_for_element_load(class_name="js-sidebar-main-all-tools")
        menu = self.driver.find_element_by_class_name("js-sidebar-main-all-tools")
        for div in menu.find_elements_by_tag_name("div"):
            if div.get_attribute("data-ga-label") == "projects":
                try:
                    # Открываю первый проект
                    div.find_element_by_class_name(
                        "pr-smart-projects-menu").find_element_by_tag_name("a").click()
                    # Удаляю проект
                    _delete_project()
                    # Если проектов будет больше чем 1, естественно тест проходить не будет.
                    # Он первый проект удалит, а следующий останется.
                except NoSuchElementException:
                    pass
                break

        # Ожидаю когда загрузится странца с контентом для случая когда нет открытых проектов
        self.wait_for_element_load(class_name="pr-page__content__description")
        # Ожидаю когда появится кнопка создания нового проекта
        self.wait_for_element_load(class_name="js-add-project")
        # Ожидаю когда пропадет элемент, который иногда скрывает кнопку
        self.wait_for_element_close(class_name="pr-dialog-message")
        # Кликаю по кнопке "Создать проект"
        self.driver.find_element_by_class_name("js-add-project").click()
        # Ожидаю появления диалога создания проекта
        self.wait_for_element_load(class_name="pr-dialog")
        # В поля этого диалога ввожу данные (домен и название проекта)
        project_dialog = self.driver.find_element_by_class_name("pr-dialog")
        project_dialog.find_element_by_class_name("js-input-domain").send_keys(PROJECT_DOMAIN)
        project_dialog.find_element_by_class_name("js-input-name").send_keys(PROJECT_NAME)

        # Кликаю по кнопке сохранить проект
        project_dialog.find_element_by_class_name("js-save-pr").click()
        # Ожидаю пока появится dashboard
        self.wait_for_element_load(class_name="js-project-tools")
        # Проверяю этот ли проект создался
        self.assertEqual(
            self.driver.find_element_by_class_name("pr-page__title-text").get_attribute("title"),
            PROJECT_NAME
        )

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

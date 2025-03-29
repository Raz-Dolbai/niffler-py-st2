from selene import browser
import allure


class BasePage:

    @allure.step("Refresh page")
    def refresh_page(self):
        browser.driver.refresh()

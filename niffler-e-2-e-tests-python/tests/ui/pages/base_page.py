from selene import browser


class BasePage:
    def refresh_page(self):
        browser.driver.refresh()

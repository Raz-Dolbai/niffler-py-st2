from typing import Literal
from tests.ui.locators import SpendingLocators, MainLocators
from selene import browser, have, by, be

from tests.ui.pages.base_page import BasePage


class SpendingPage(BasePage):
    def __init__(self):
        self.expected_amount_error_text = "Amount has to be not less then 0.01"
        self.expected_category_empty_text = "Please choose category"
        self.expected_empty_spending_page = "There are no spendings"

    def fill_amount(self, amount: str):
        browser.element(SpendingLocators.AMOUNT).set_value(amount)

    def fill_category(self, category: str):
        browser.element(SpendingLocators.CATEGORY).set_value(category)

    def fill_date(self, date: str):
        browser.element(SpendingLocators.DATE).set_value(date)

    def fill_description(self, description: str):
        browser.element(SpendingLocators.DESCRIPTION).set_value(description)

    def open_currency_value(self):
        browser.element(SpendingLocators.CURRENCY).click()

    def choose_currency_usd(self):
        self.open_currency_value()
        browser.element(by.text("USD")).click()

    def choose_currency_eur(self):
        self.open_currency_value()
        browser.element(by.text("EUR")).click()

    def choose_currency_rub(self):
        self.open_currency_value()
        browser.element(by.text("RUB")).click()

    def choose_currency_kzt(self):
        self.open_currency_value()
        browser.element(by.text("KZT")).click()

    def choose_currency(self, currency: Literal["KZT", "RUB", "EUR", "USD"]):
        self.open_currency_value()
        browser.element(by.text(currency)).click()

    def click_add(self):
        browser.element(SpendingLocators.ADD).click()

    def click_cancel(self):
        browser.element(SpendingLocators.CANCEL).set_value()

    def click_delete(self):
        browser.element(SpendingLocators.DELETE_BUTTON).click()

    def click_delete_modal(self):
        browser.element(SpendingLocators.DELETE_MODAL_BUTTON).click()

    def click_checkbox(self):
        browser.element(SpendingLocators.SPENDING_CHECKBOX).click()

    def delete_button_should_be_disabled(self):
        browser.element(SpendingLocators.DELETE_BUTTON).should(be.disabled)

    def not_valid_amount_value_text(self):
        assert browser.element(SpendingLocators.ERROR_MESSAGE).should(
            have.text(self.expected_amount_error_text))

    def should_have_expected_text(self, text: str):
        assert browser.element(SpendingLocators.SPENDING).should(have.text(text))

    def success_delete_text(self):
        assert browser.element(SpendingLocators.SPENDING).should(have.text(self.expected_empty_spending_page))

    def click_edit_spend(self):
        browser.element(MainLocators.EDIT_SPEND).click()

    def add_spending(self, amount: str, category: str, description: str = None, date: str = None):
        self.fill_amount(amount)
        self.fill_category(category)
        self.fill_date(date)
        self.fill_description(description)
        self.click_add()

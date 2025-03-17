from typing import Literal
from tests.ui.locators import SpendingLocators, MainLocators
from selene import browser, have, by, be

from tests.ui.pages.base_page import BasePage
import allure


class SpendingPage(BasePage):
    def __init__(self):
        self.expected_amount_error_text = "Amount has to be not less then 0.01"
        self.expected_category_empty_text = "Please choose category"
        self.expected_empty_spending_page = "There are no spendings"

    @allure.step("Fill amount")
    def fill_amount(self, amount: str):
        browser.element(SpendingLocators.AMOUNT).set_value(amount)

    @allure.step("Fill category")
    def fill_category(self, category: str):
        browser.element(SpendingLocators.CATEGORY).set_value(category)

    @allure.step("Fill date")
    def fill_date(self, date: str):
        browser.element(SpendingLocators.DATE).set_value(date)

    @allure.step("Fill description")
    def fill_description(self, description: str):
        browser.element(SpendingLocators.DESCRIPTION).set_value(description)

    @allure.step("Expand list currency")
    def open_currency_value(self):
        browser.element(SpendingLocators.CURRENCY).click()

    @allure.step("Select USD")
    def choose_currency_usd(self):
        self.open_currency_value()
        browser.element(by.text("USD")).click()

    @allure.step("Select EUR")
    def choose_currency_eur(self):
        self.open_currency_value()
        browser.element(by.text("EUR")).click()

    @allure.step("Select RUB")
    def choose_currency_rub(self):
        self.open_currency_value()
        browser.element(by.text("RUB")).click()

    @allure.step("Select KZT")
    def choose_currency_kzt(self):
        self.open_currency_value()
        browser.element(by.text("KZT")).click()

    @allure.step("Select currency by input value")
    def choose_currency(self, currency: Literal["KZT", "RUB", "EUR", "USD"]):
        self.open_currency_value()
        browser.element(by.text(currency)).click()

    @allure.step("Click Add")
    def click_add(self):
        browser.element(SpendingLocators.ADD).click()

    @allure.step("Click Cancel")
    def click_cancel(self):
        browser.element(SpendingLocators.CANCEL).set_value()

    @allure.step("Click Delete")
    def click_delete(self):
        browser.element(SpendingLocators.DELETE_BUTTON).click()

    @allure.step("Click Delete modal window")
    def click_delete_modal(self):
        browser.element(SpendingLocators.DELETE_MODAL_BUTTON).click()

    @allure.step("Choose first spend on table")
    def click_checkbox(self):
        browser.element(SpendingLocators.SPENDING_CHECKBOX).click()

    @allure.step("Check: Delete button should be disabled")
    def delete_button_should_be_disabled(self):
        browser.element(SpendingLocators.DELETE_BUTTON).should(be.disabled)

    @allure.step("Check: Not valid amount text")
    def not_valid_amount_value_text(self):
        assert browser.element(SpendingLocators.ERROR_MESSAGE).should(
            have.text(self.expected_amount_error_text))

    @allure.step("Check: expected text")
    def should_have_expected_text(self, text: str):
        assert browser.element(SpendingLocators.SPENDING).should(have.text(text))

    @allure.step("Check: success delete expected text")
    def success_delete_text(self):
        assert browser.element(SpendingLocators.SPENDING).should(have.text(self.expected_empty_spending_page))

    @allure.step("Click edit")
    def click_edit_spend(self):
        browser.element(MainLocators.EDIT_SPEND).click()

    @allure.step("Add spend")
    def add_spending(self, amount: str, category: str, description: str = None, date: str = None):
        self.fill_amount(amount)
        self.fill_category(category)
        self.fill_date(date)
        self.fill_description(description)
        self.click_add()

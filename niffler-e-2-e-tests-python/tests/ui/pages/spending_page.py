from typing import Literal
from selene import browser, have, by, be
from tests.ui.pages.base_page import BasePage
import allure


class SpendingPage(BasePage):
    def __init__(self):
        self.expected_amount_error_text = "Amount has to be not less then 0.01"
        self.expected_category_empty_text = "Please choose category"
        self.expected_empty_spending_page = "There are no spendings"
        self.AMOUNT = "input[name=amount]"
        self.ERROR_MESSAGE = "span[class=input__helper-text]"
        self.CATEGORY = "input[name=category]"
        self.DATE = "input[name=date]"
        self.DESCRIPTION = "input[name=description]"
        self.ADD = "button[id=save]"
        self.CANCEL = "button[id=cancel]"
        self.SPENDING = "[id=spendings]"
        self.SPENDING_CHECKBOX = ".PrivateSwitchBase-input.css-1m9pwf3"
        self.DELETE_BUTTON = "[id=delete]"
        self.CURRENCY = "[id=currency]"
        self.DELETE_MODAL_BUTTON = "body > div.MuiDialog-root.MuiModal-root.css-126xj0f > div.MuiDialog-container.MuiDialog-scrollPaper.css-ekeie0 > div > div.MuiDialogActions-root.MuiDialogActions-spacing.css-19kha6v > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.css-1v1p78s"
        self.EDIT_SPEND = ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-colorPrimary.MuiIconButton-sizeMedium.css-dxoo7k"

    @allure.step("Fill amount")
    def fill_amount(self, amount: str):
        browser.element(self.AMOUNT).set_value(amount)

    @allure.step("Fill category")
    def fill_category(self, category: str):
        browser.element(self.CATEGORY).set_value(category)

    @allure.step("Fill date")
    def fill_date(self, date: str):
        browser.element(self.DATE).set_value(date)

    @allure.step("Fill description")
    def fill_description(self, description: str):
        browser.element(self.DESCRIPTION).set_value(description)

    @allure.step("Expand list currency")
    def open_currency_value(self):
        browser.element(self.CURRENCY).click()

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
        browser.element(self.ADD).click()

    @allure.step("Click Cancel")
    def click_cancel(self):
        browser.element(self.CANCEL).set_value()

    @allure.step("Click Delete")
    def click_delete(self):
        browser.element(self.DELETE_BUTTON).click()

    @allure.step("Click Delete modal window")
    def click_delete_modal(self):
        browser.element(self.DELETE_MODAL_BUTTON).click()

    @allure.step("Choose first spend on table")
    def click_checkbox(self):
        browser.element(self.SPENDING_CHECKBOX).click()

    @allure.step("Check: Delete button should be disabled")
    def delete_button_should_be_disabled(self):
        browser.element(self.DELETE_BUTTON).should(be.disabled)

    @allure.step("Check: Not valid amount text")
    def should_be_expected_text_after_fill_not_valid_amount(self):
        assert browser.element(self.ERROR_MESSAGE).should(
            have.text(self.expected_amount_error_text))

    @allure.step("Check: expected text")
    def should_be_expected_text(self, text: str):
        assert browser.element(self.SPENDING).should(have.text(text))

    @allure.step("Check: success delete expected text")
    def should_be_expected_text_after_delete_spend(self):
        assert browser.element(self.SPENDING).should(have.text(self.expected_empty_spending_page))

    @allure.step("Click edit")
    def click_edit_spend(self):
        browser.element(self.EDIT_SPEND).click()

    @allure.step("Add spend")
    def add_spending(self, amount: str, category: str, description: str = None, date: str = None):
        self.fill_amount(amount)
        self.fill_category(category)
        self.fill_date(date)
        self.fill_description(description)
        self.click_add()

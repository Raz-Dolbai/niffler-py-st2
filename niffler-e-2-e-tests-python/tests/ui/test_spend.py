import time
from selene import browser, have, be
from conftest import Pages, TestData
from models.spend import SpendAdd, CategoryAdd
from tests.ui.locators import MainPage, SpendingPage

TEST_CATEGORY = "car"


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(
    amount=108.51,
    description="QA-GURU Python ADVANCED 2",
    currency="RUB",
    category=CategoryAdd(name=TEST_CATEGORY),
    spendDate="2025-03-01T18:39:27.955Z"))
def test_add_spending(category, spends):
    browser.driver.refresh()
    browser.element(SpendingPage.SPENDING).should(have.text(spends.description))
    browser.element(SpendingPage.SPENDING).should(have.text(str(spends.amount)))
    browser.element(SpendingPage.SPENDING).should(have.text(spends.category.name))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(amount=108.51,
                          description='QA-GURU Python ADVANCED 2',
                          category=CategoryAdd(name=TEST_CATEGORY),
                          currency="RUB",
                          spendDate="2025-03-01T18:39:27.955Z"
                          ))
def test_update_spending(category, spends):
    browser.driver.refresh()
    browser.element(MainPage.EDIT_SPEND).click()
    browser.element(SpendingPage.DESCRIPTION).set_value("Поездка")
    browser.element(SpendingPage.AMOUNT).set_value("2000")
    browser.element(SpendingPage.ADD).click()
    browser.element(SpendingPage.SPENDING).should(have.text("2000"))
    browser.element(SpendingPage.SPENDING).should(have.text("Поездка"))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(amount=108.51,
                          description='QA-GURU Python ADVANCED 2',
                          category=CategoryAdd(name=TEST_CATEGORY),
                          currency="RUB",
                          spendDate="2025-03-01T18:39:27.955Z"
                          ))
def test_delete_spending(category, spends):
    browser.driver.refresh()
    browser.element(SpendingPage.DELETE_BUTTON).should(be.disabled)
    browser.element(SpendingPage.SPENDING_CHECKBOX).click()
    browser.element(SpendingPage.DELETE_BUTTON).click()
    browser.element(SpendingPage.DELETE_MODAL_BUTTON).click()
    browser.element(SpendingPage.SPENDING).should(have.text("There are no spendings"))

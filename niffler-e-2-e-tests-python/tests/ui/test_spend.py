from conftest import Pages, TestData
from models.spend import SpendAdd, CategoryAdd
from tests.ui.pages.spending_page import SpendingPage
import pytest

TEST_CATEGORY = "car"

pytestmark = [pytest.mark.allure_label("Spendings", label_type="epic")]
@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(
    amount=108.51,
    description="QA-GURU Python ADVANCED 2",
    currency="RUB",
    category=CategoryAdd(name=TEST_CATEGORY),
    spendDate="2025-03-01T18:39:27.955Z"))
def test_add_spending(category, spends, spending_page_object: SpendingPage):
    spending_page_object.refresh_page()
    spending_page_object.should_be_expected_text(spends.description)
    spending_page_object.should_be_expected_text(str(spends.amount))
    spending_page_object.should_be_expected_text(spends.category.name)


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(amount=108.51,
                          description='QA-GURU Python ADVANCED 2',
                          category=CategoryAdd(name=TEST_CATEGORY),
                          currency="RUB",
                          spendDate="2025-03-01T18:39:27.955Z"
                          ))
def test_update_spending(category, spends, spending_page_object: SpendingPage):
    spending_page_object.refresh_page()
    spending_page_object.click_edit_spend()
    spending_page_object.fill_description("Поездка")
    spending_page_object.fill_amount("2000")
    spending_page_object.click_add()
    spending_page_object.should_be_expected_text("2000")
    spending_page_object.should_be_expected_text("Поездка")


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendAdd(amount=108.51,
                          description='QA-GURU Python ADVANCED 2',
                          category=CategoryAdd(name=TEST_CATEGORY),
                          currency="RUB",
                          spendDate="2025-03-01T18:39:27.955Z"
                          ))
def test_delete_spending(category, spends, spending_page_object: SpendingPage):
    spending_page_object.refresh_page()
    spending_page_object.delete_button_should_be_disabled()
    spending_page_object.click_checkbox()
    spending_page_object.click_delete()
    spending_page_object.click_delete_modal()
    spending_page_object.should_be_expected_text_after_delete_spend()


@Pages.spending_page
def test_error_amount_text(spending_page_object):
    spending_page_object.add_spending("0", "car", "blabla", "03/15/2025")
    spending_page_object.should_be_expected_text_after_fill_not_valid_amount()

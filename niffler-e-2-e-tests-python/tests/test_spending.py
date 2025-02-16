from selene import browser, have, query, be
from conftest import Pages, TestData
from models.spend import SpendRequestModel, CategoryRequest, SpendResponseModel


@Pages.main_page
def test_spending_titles_exists():
    browser.element('[id="spendings"]').should(have.text('History of Spendings'))
    browser.element('[class="MuiTypography-root MuiTypography-h5 css-giaux5"]').should(have.text("Statistics"))
    browser.element('.MuiTypography-root.MuiTypography-h6.css-1m7obeg').should(have.text("There are no spendings"))


TEST_CATEGORY = "car"


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendRequestModel(amount=108.51,
                                   description='QA-GURU Python ADVANCED 2',
                                   category=CategoryRequest(**{'name': f'{TEST_CATEGORY}'}).model_dump(),
                                   currency="RUB"
                                   ).model_dump())
def test_add_spending(category, spends):
    body = SpendResponseModel(**spends)
    browser.driver.refresh()
    browser.element('[id="spendings"]').should(have.text(body.description))
    browser.element('[id="spendings"]').should(have.text(str(body.amount)))
    browser.element('[id="spendings"]').should(have.text(body.category.name))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendRequestModel(amount=108.51,
                                   description='QA-GURU Python ADVANCED 2',
                                   category=CategoryRequest(**{'name': f'{TEST_CATEGORY}'}).model_dump(),
                                   currency="RUB"
                                   ).model_dump())
def test_update_spending(category, spends, spends_update):
    body = SpendResponseModel(**spends_update.json())
    browser.driver.refresh()
    browser.element('[id="spendings"]').should(have.text(str(body.amount)))
    browser.element('[id="spendings"]').should(have.text(body.description))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(SpendRequestModel(amount=108.51,
                                   description='QA-GURU Python ADVANCED 2',
                                   category=CategoryRequest(**{'name': f'{TEST_CATEGORY}'}).model_dump(),
                                   currency="RUB"
                                   ).model_dump())
def test_remove_spending(category, spends, spends_remove):
    browser.driver.refresh()
    browser.element('.MuiTypography-root.MuiTypography-h6.css-1m7obeg').should(have.text("There are no spendings"))


@Pages.main_page
def test_elements_present_in_page():
    browser.element('.MuiBox-root.css-x0qbic').should(be.visible)
    browser.all(
        '[class="MuiInputBase-root MuiOutlinedInput-root MuiInputBase-colorPrimary MuiInputBase-fullWidth MuiInputBase-formControl css-5i8lf2"]').should(
        have.size(2))
    browser.element('#delete').should(be.visible)
    browser.element('canvas[role="img"]').should(be.visible)

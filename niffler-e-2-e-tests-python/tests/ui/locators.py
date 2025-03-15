class LoginLocators:
    USERNAME = "input[name=username]"
    PASSWORD = "input[name=password]"
    LOGIN = "button[type=submit]"
    ERROR_MESSAGE = ".form__error"
    CREATE_NEW_ACCOUNT = ".form__register"


class SpendingLocators:
    AMOUNT = "input[name=amount]"
    ERROR_MESSAGE = "span[class=input__helper-text]"
    CATEGORY = "input[name=category]"
    DATE = "input[name=date]"
    DESCRIPTION = "input[name=description]"
    ADD = "button[id=save]"
    CANCEL = "button[id=cancel]"
    SPENDING = "[id=spendings]"
    SPENDING_CHECKBOX = ".PrivateSwitchBase-input.css-1m9pwf3"
    DELETE_BUTTON = "[id=delete]"
    CURRENCY = "[id=currency]"
    DELETE_MODAL_BUTTON = "body > div.MuiDialog-root.MuiModal-root.css-126xj0f > div.MuiDialog-container.MuiDialog-scrollPaper.css-ekeie0 > div > div.MuiDialogActions-root.MuiDialogActions-spacing.css-19kha6v > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.css-1v1p78s"


class MainLocators:
    EDIT_SPEND = ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-colorPrimary.MuiIconButton-sizeMedium.css-dxoo7k"


class ProfileLocators:
    PROFILE_TITLE = ".MuiTypography-root.MuiTypography-h5.css-w1t7b3"
    CATEGORIES_TITLE = ".MuiTypography-root.MuiTypography-h5.css-1pam1gy"
    CATEGORIES_INPUT = "input[name=category]"
    SAVE_CHANGES_BUTTON = "[id=:r5:]"
    CATEGORIES_DIV = ".MuiBox-root.css-1lekzkb"
    EDIT_CATEGORY_NAME = "#root > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.css-17u3xlq > div > div.MuiBox-root.css-0 > button:nth-child(1)"
    ARCHIVE_CATEGORY = "#root > main > div > div > div.MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.css-17u3xlq > div > div.MuiBox-root.css-0 > button:nth-child(2)"
    CATEGORY_UPDATE = ".MuiBox-root.css-1kxonj9 > [name=category]"


class RegisterLocators:
    USERNAME = "input[name=username]"
    PASSWORD = "input[name=password]"
    SUBMIT_PASSWORD = "input[name=passwordSubmit]"
    SIGN_UP_BUTTON = "button.form__submit"
    SUCCESS_TEXT = ".form__paragraph_success"
    ERROR = ".form__error"

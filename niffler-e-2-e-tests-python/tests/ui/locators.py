class AuthPage:
    USERNAME = "input[name=username]"
    PASSWORD = "input[name=password]"
    LOGIN = "button[type=submit]"
    ERROR_MESSAGE = ".form__error"


class SpendingPage:
    AMOUNT = "input[name=amount]"
    CATEGORY = "input[name=category]"
    DATE = "input[name=date]"
    DESCRIPTION = "input[name=description]"
    ADD = "button[id=save]"
    SPENDING = "[id=spendings]"
    SPENDING_CHECKBOX = ".PrivateSwitchBase-input.css-1m9pwf3"
    DELETE_BUTTON = "[id=delete]"
    DELETE_MODAL_BUTTON = "body > div.MuiDialog-root.MuiModal-root.css-126xj0f > div.MuiDialog-container.MuiDialog-scrollPaper.css-ekeie0 > div > div.MuiDialogActions-root.MuiDialogActions-spacing.css-19kha6v > button.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.css-1v1p78s"


class MainPage:
    EDIT_SPEND = ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-colorPrimary.MuiIconButton-sizeMedium.css-dxoo7k"


class ProfilePage:
    PROFILE_TITLE = ".MuiTypography-root.MuiTypography-h5.css-w1t7b3"
    CATEGORIES_TITLE = ".MuiTypography-root.MuiTypography-h5.css-1pam1gy"
    CATEGORIES_INPUT = "input[name=category]"
    SAVE_CHANGES_BUTTON = "[id=:r5:]"
    CATEGORIES_DIV = ".MuiBox-root.css-1lekzkb"
    CATEGORY_UPDATE = ".MuiBox-root.css-1kxonj9 > [name=category]"


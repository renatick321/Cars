from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
import smtplib


def send_notification(text, email):
    sender = 'rucarsupprt@gmail.com'
    sender_password = 'Support123'
    mail_lib = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail_lib.login(sender, sender_password)
    mail_lib.sendmail(sender, email, text)
    mail_lib.quit()


class StartStates(StatesGroup):
    SPARE_PARTS_STATE = State()
    REG_LOG_STATE = State()
    NUMBER_STATE = State()
    PASSWORD_STATE = State()


class RegistrationStates(StatesGroup):
    START_STATE = State()
    FIRST_NAME_STATE = State()
    SECOND_NAME_STATE = State()
    NUMBER_STATE = State()
    PASSWORD_STATE = State()
    EMAIL_STATE = State()


class LoginStates(StatesGroup):
    NUMBER_STATE = State()
    PASSWORD_STATE = State()


class SomeStufStates(StatesGroup):
    START_VIN_STATE = State()
    END_VIN_STATE = State()
    TEMPLATE_STATE = State()
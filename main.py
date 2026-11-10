from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import threading
import time

courtTypes = {
    "1-4": "021a0de4-845d-49f4-8952-82b16913eec9",
    "5-8": "5fefb704-2bef-4313-9291-7124d1b696fd"
}

courtIds = {
    "1": "d0da8232-04f9-48c5-894a-debb5fb01d98",
    "2": "f8c07ccd-5d4a-49ab-a911-62346e7cfb3c",
    "3": "395c8cad-2632-47f2-be5b-06a47d6e3dd6",
    "4": "fc50b9f7-2f7f-463a-8775-73e95bf35237",
    "5": "12a5a455-c902-413c-91e9-8d47ff30a5a5",
    "6": "36d340c2-880e-4d2b-b5e4-fb0ba3cedf02",
    "7": "568db31e-c205-4c0e-8742-96f013a584d3",
    "8": "7109d440-ef11-4bdb-8ea3-6cc4874304c9"
}
def bookCourt(booking, targetDateObj):
    with sync_playwright() as p:
        COURT = booking["court"]
        USERID = booking["userId"]
        PASSWORD = booking["password"]
        TIME_SLOT = booking["timeSlot"]
        DAY = booking["day"]
        MONTH = booking["month"]
        YEAR = booking["year"]
        COURT_TYPE = "1-4" if COURT in ["1", "2", "3", "4"] else "5-8"
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.dalsports.dal.ca/account/signin") 
        page.locator("#txtEmailUsernameLogin").type(f"{USERID}")
        page.locator("#btnNextSignInFirst").click()
        page.locator("#txtPasswordLogin").type(f"{PASSWORD}")
        page.locator("#btnSignIn").click()
        page.wait_for_timeout(20000)
        page.goto(f"https://www.dalsports.dal.ca/booking/{courtTypes[COURT_TYPE]}")
        page.locator(f"button[data-day='{DAY}'][data-month='{MONTH}'][data-year='{YEAR}']:visible").click()
        page.locator(f"button[data-facility-id='{courtIds[COURT]}']:visible").click()
        print("Reached Target, waiting")
        while datetime.now() < targetDateObj:
            time.sleep(0.05)
        page.locator(f"button[data-facility-id='{courtIds[COURT]}']:visible").click()
        START_TIME, _ , END_TIME, PERIOD = TIME_SLOT.split(" ")
        page.locator(f"button[data-slot-text='{int(START_TIME)}:00 - {int(END_TIME)}:00 {PERIOD}']").click()
        print(f"Booking at: {datetime.now()}")
        page.wait_for_timeout(10000)
        browser.close()

booking = {'userId': None, 'password': None, 'court': '3', 'timeSlot': '6 - 7 PM', 'day': '12', 'month': '11', 'year': '2026'}
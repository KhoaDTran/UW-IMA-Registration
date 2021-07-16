import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime


def gym_snip(driver, user, userpass, num, timesList):
    firstButton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "nav.navbar-right.hidden-xs")))
    firstButton.click()
    loginButton = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "loginOption.btn.btn-lg.btn-block.btn-social.btn-soundcloud")))
    loginButton.click()

    username = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "weblogin_netid")))
    username.send_keys(user)

    password = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "weblogin_password")))
    password.send_keys(userpass)

    password.send_keys(Keys.ENTER)

    section = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "col-lg-9.col-md-9.col-sm-9.col-xs-12.paddingGridOff")))
    data = {count: item for count, item in enumerate(section)}
    weekday = datetime.now().weekday()
    data[weekday].click()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    now = datetime.now()
    today = datetime.today().strftime("%m/%d/%Y")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    month = dt_string[4:5]
    date = dt_string[:2]
    if date[0] == "0":
        date = date[1]
    boo = False
    table = [False for _ in range(num)]
    timeMap = ["11:00 AM - 11:30 AM", "11:30 AM - 12:00 PM", "12:00 PM - 12:30 PM", "12:30 PM - 1:00 PM", "1:00 PM - 1:30 PM", "1:30 PM - 2:00 PM", "2:00 PM - 2:30 PM", "2:30 PM - 3:00 PM", "3:00 PM - 3:30 PM",
               "3:30 PM - 4:00 PM", "4:00 PM - 4:30 PM", "4:30 PM - 5:00 PM", "5:00 PM - 5:30 PM", "5:30 PM - 6:00 PM", "6:00 PM - 6:30 PM", "6:30 PM - 7:00 PM", "7:00 PM - 7:30 PM"]
    finalTimeList = [timeMap[timesList[k]] for k in range(len(timesList))]
    success = False
    year = "2021"
    while not success:
        while not boo:
            slots = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "col-sm-6.col-md-4.program-schedule-card")))
            slotsTable = []
            for item in slots:
                day = weekdays[weekday]
                mon = months[int(month) - 1]
                datee = day + ", " + mon + " " + date + ", 2021"
                for item_ in finalTimeList:
                    if datee in item.text and item_ in item.text:
                        slotsTable.append(item.text)
            for val in range(len(slotsTable)):
                if not boo and "No Spots Available" in slotsTable[val]:
                    boo = False
                    table[val] = False
                else:
                    table[val] = True
                    print(finalTimeList[val])
                    print(slotsTable[val] + " found")
                    boo = True
            if not boo:
                print("Refreshed")
                driver.refresh()
        now = datetime.now()
        today = datetime.today().strftime("%m/%d/%Y")
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        month = dt_string[4:5]
        date = dt_string[:2]
        if date[0] == "0":
            date = date[1]
        if month[0] == "0":
            month = month[1]
        today = month + "/" + date + "/" + year
        for numVal in range(len(table)):
            if table[numVal]:
                timeAll = finalTimeList[numVal]
                time1 = timeAll[0:4] + ":00 PM"
                time2 = timeAll[10:14] + ":00"
                element = "//button[contains(@onclick, \"" + today + \
                    " " + time1 + "\', \'" + today + " " + time2 + "\")]"
                print(element)
                try:
                    register = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                        (By.XPATH, element)))
                    register.click()
                    success = True
                    boo = True
                except:
                    driver.refresh()
                    success = False
                    boo = False
                if boo and success:
                    yes = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "radio-inline")))
                    for item in yes:
                        if item.text == "Yes":
                            item.click()
                    cart = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "btn.btn-primary")))
                    cart[len(cart) - 3].click()
                    try:
                        checkout1 = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.ID, "checkoutButton")))
                        checkout1.click()
                        time.sleep(2)
                        checkout = WebDriverWait(driver, 20).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn.btn-primary")))
                        checkout[4].click()
                        success = True
                        print("success is " + str(success))
                    except:
                        cookie = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.ID, "gdpr-cookie-accept")))
                        cookie.click()
                        checkout1 = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.ID, "checkoutButton")))
                        checkout1.click()
                        time.sleep(2)
                        checkout = WebDriverWait(driver, 20).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn.btn-primary")))
                        checkout[4].click()
                        success = True
                        print("success is " + str(success))
    driver.close()
    driver.quit()


def gym_get(driver, user, userPass, weekday, desiredDate, desiredTime):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "nav.navbar-right.hidden-xs"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.CLASS_NAME, "loginOption.btn.btn-lg.btn-block.btn-social.btn-soundcloud"))).click()
    username = driver.find_element_by_id("weblogin_netid")
    username.send_keys(user)
    password = driver.find_element_by_id("weblogin_password")
    password.send_keys(userPass)
    password.send_keys(Keys.ENTER)

    section = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "col-lg-9.col-md-9.col-sm-9.col-xs-12.paddingGridOff")))
    data = {count: item for count, item in enumerate(section)}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    times = dt_string[11:15]
    data[weekday].click()
    today = str(desiredDate)
    timeMap = ["11:00 AM - 11:30 AM", "11:30 AM - 12:00 PM", "12:00 PM - 12:30 PM", "12:30 PM - 1:00 PM", "1:00 PM - 1:30 PM", "1:30 PM - 2:00 PM", "2:00 PM - 2:30 PM", "2:30 PM - 3:00 PM", "3:00 PM - 3:30 PM",
               "3:30 PM - 4:00 PM", "4:00 PM - 4:30 PM", "4:30 PM - 5:00 PM", "5:00 PM - 5:30 PM", "5:30 PM - 6:00 PM", "6:00 PM - 6:30 PM", "6:30 PM - 7:00 PM", "7:00 PM - 7:30 PM"]
    timeDesired = timeMap[desiredTime]
    time1 = timeDesired[0:4] + ":00 PM"
    time2 = timeDesired[10:14] + ":00"
    element = "//button[contains(@onclick, \"" + today + \
            " " + time1 + "\', \'" + today + " " + time2 + "\")]"
    register = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, element)))
    register.click()
    yes = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "radio-inline")))
    for item in yes:
        if item.text == "Yes":
            item.click()
    cart = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "btn.btn-primary")))
    cart[len(cart) - 3].click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "checkoutButton"))).click()
    time.sleep(4)
    checkout = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "btn.btn-primary")))
    checkout[4].click()
    driver.close()
    driver.quit()

if __name__ == "__main__":
    driver = webdriver.Chrome("C:/Users/tynou/googledriver/chromedriver.exe")
    allTimes = []
    print("Welcome to UW IMA bot, this is intended to grab appointments to enter the IMA ")
    username = input("Enter your UW NetID:")
    password = input("Enter your UW NetID Password:")
    desiredTime = input("0=today, 1=future:")
    if (desiredTime != 0 or desiredTime != 1):
        desiredTime = input("Invalid input, please enter 0 or 1 for 0=today, 1=future:")
    else:
        if (desiredTime == 0):
            numSnipes = input(
                "Enter the amount of appointments you want to search for:")
            print("This is the list of times you can search for, Enter the value associated with the time you want")
            print("[0: 11:00 AM - 11:30 AM, 1: 11:30 AM - 12:00 PM, 2: 12:00 PM - 12:30 PM, 3: 12:30 PM - 1:00 PM, 4: 1:00 PM - 1:30 PM, 5: 1:30 PM - 2:00 PM, 6: 2:00 PM - 2:30 PM, 7: 2:30 PM - 3:00 PM, 8: 3:00 PM - 3:30 PM, 9: 3:30 PM - 4:00 PM, 10: 4:00 PM - 4:30 PM, 11: 4:30 PM - 5:00 PM, 12: 5:00 PM - 5:30 PM, 13: 5:30 PM - 6:00 PM, 14: 6:00 PM - 6:30 PM, 15: 6:30 PM - 7:00 PM, 16: 7:00 PM - 7:30 PM]")
            actualNum = int(numSnipes)
            for i in range(1, actualNum+1):
                timez = input("Enter the " + str(i) +
                            " index of time you want to search for, this is rank by prioirty:")
                if (int(timez) >= 17):
                    timez = input("Invalid, please enter a value between 0 and 12:")
                allTimes.append(int(timez))
            driver.get(
                "https://reg.recreation.uw.edu/Program/GetProducts?classification=cb0f3827-6ca5-4d18-a250-e3197e7bd118")
            gym_snip(driver, username, password, actualNum, allTimes)
        if (desiredTime == 1):
            weekdayInput = input("Enter value for desired day: [0: Monday, 1: Tuesday, 2: Wednesday, 3: Thursday, 4: Friday, 5: Saturday, 6: Sunday]:")
            dayInput = input("Enter in format M/DD/YYYY of desired date:")
            print("This is the list of times you can search for, Enter the value associated with the time you want")
            print("[0: 11:00 AM - 11:30 AM, 1: 11:30 AM - 12:00 PM, 2: 12:00 PM - 12:30 PM, 3: 12:30 PM - 1:00 PM, 4: 1:00 PM - 1:30 PM, 5: 1:30 PM - 2:00 PM, 6: 2:00 PM - 2:30 PM, 7: 2:30 PM - 3:00 PM, 8: 3:00 PM - 3:30 PM, 9: 3:30 PM - 4:00 PM, 10: 4:00 PM - 4:30 PM, 11: 4:30 PM - 5:00 PM, 12: 5:00 PM - 5:30 PM, 13: 5:30 PM - 6:00 PM, 14: 6:00 PM - 6:30 PM, 15: 6:30 PM - 7:00 PM, 16: 7:00 PM - 7:30 PM]")
            desiredSnipe = input("Enter the value of the time desired:")
            if (int(desiredSnipe) >= 17):
                desiredSnipe = input("Invalid, please enter a value between 0 and 16:")
            driver.get(
                "https://reg.recreation.uw.edu/Program/GetProducts?classification=cb0f3827-6ca5-4d18-a250-e3197e7bd118")
            gym_get(driver, username, password, weekdayInput, dayInput, desiredSnipe)
            

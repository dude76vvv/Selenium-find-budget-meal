# https://pypi.org/project/webdriver-manager/

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import Meal.constants as const


class BudgetMeal:
    def __init__(self) -> None:

        options = Options()

        # open browser
        options.add_experimental_option("detach", True)

        # perform silently in background without browser
        # browser not needed if we want to do scraping
        # options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        print("Bot created, ready for scraping")

    # visit the site
    def visitPage(self) -> None:

        print('Visiting page now...')

        self.driver.get(const.BASE_URL)
        # wait at most 10 sec before proceeding, wait for page to fully load up
        self.driver.implicitly_wait(10)

    # close the page
    def closePage(self) -> None:
        self.driver.quit()

    # input search bar
    def enterInput(self, targetPlace):

        # wait for 10 sec for elmemnt to load, if not throw
        searchField = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "headlessui-combobox-input-1")))

        # clear input fields before entering just in case
        searchField.clear()

        searchField.send_keys(targetPlace)

        autoCompleteOptions = self.driver.find_elements(
            By.XPATH, "//div[@id='onemap']/li[@role='option']")

        option1 = None

        # choose 1st option element
        if autoCompleteOptions:
            option1 = autoCompleteOptions[0]

        if option1:
            option1.click()

            # clicking the suggested option will already show the results

        else:
            # manually click the search button using our input result
            # hope for the best there is result

            submitBtn = self.driver.find_element(By.ID, 'search-button-go')
            submitBtn.click()

    # grab result from our search
    def checkResults(self, filterHala: bool = False) -> bool:

        allResults = WebDriverWait(self.driver, 3).until(
            # EC.presence_of_element_located((By.ID, "SEARCH_RESULTS_ID")))
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='space-y-[24px]']")))

        # apply hala filter
        if filterHala:

            print("Applying Halal filter...")

            self.applyHalaFilter()

        # from allResult check if there is result from within 2km
        # it will be empty arr if there is no rs
        boolRes = allResults.find_elements(
            By.XPATH, "//h1[text()[contains(.,'Showing 0 result(s)')]]")

        return False if boolRes else True

    def get2kmResults(self) -> tuple:

        locationName_arr = []
        locationAddr_arr = []
        locationLink_arr = []
        foodPrice_arr = []

        allResults = WebDriverWait(self.driver, 3).until(
            # EC.presence_of_element_located((By.ID, "SEARCH_RESULTS_ID")))
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='space-y-[24px]']")))

        # find last updated date
        lastUpdatedDate = allResults.find_element(By.TAG_NAME, "span").text
        # print(lastUpdatedDate)

        # select results the 2km div
        nearbyResult = allResults.find_element(
            By.XPATH, "//h1[contains(text(),'2km')]/parent::div")
        # rowsResult = nearbyResult.find_elements(By.XPATH,"//div[@role='row']")

        rowsResult = nearbyResult.find_elements(
            By.CSS_SELECTOR, "div[class='flex flex-col lg:w-full']")

        for row in rowsResult:

            # contain the locationName, locationAddress,locationOneMapLink, foodPrice
            # get the locationName
            locationName = row.find_element(
                By.CSS_SELECTOR, "span[class='text-black']")
            # print(locationName.text)
            locationName_arr.append(locationName.text.strip())

            aLink = row.find_element(
                By.TAG_NAME, "a").get_attribute('href').strip()
            aAdrr = row.find_element(By.TAG_NAME, "span").text.strip()

            locationAddr_arr.append(aAdrr)
            locationLink_arr.append(aLink)

            # #get foodPrice
            foodPrice = row.find_element(By.TAG_NAME, 'p')
            # print(foodPrice.text)
            foodPrice_arr.append(foodPrice.text.strip())

        resList = [locationName_arr, locationAddr_arr,
                   locationLink_arr, foodPrice_arr]

        return resList, lastUpdatedDate

    def applyHalaFilter(self):

        # will take some time for the filter button to appear after inputting
        filterBtn = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Filter')]")))

        # perform a scroll down till elemement is located and ready for clicking
        filterBtn.location_once_scrolled_into_view

        # inconsistent when trying to apply clicking on the fiter btn
        # filterBtn.click()

        # use this method to simulate clicking !!!!
        filterBtn.send_keys('\n')

        # wait for aside section to appear
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
            (By.XPATH, "//Aside//h1[contains(.,'Filter')]")))

        # click halal label
        halaOption = self.driver.find_element(
            By.XPATH, "//label[contains(.,'Halal Options Available')]")
        halaOption.click()

        # click apply btn
        self.driver.implicitly_wait(0.6)
        applyBtn = self.driver.find_element(
            By.XPATH, "//button[contains(.,'Apply')]")
        applyBtn.click()

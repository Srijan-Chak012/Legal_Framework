import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

try:
    # Replace the login credentials with your own
    USERNAME = "IIITech5"
    PASSWORD = "law@2023"

    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https://www.manupatrafast.com")
    driver.delete_all_cookies()

    # Navigate to the login page
    driver.get("https://www.manupatrafast.com")

    # Fill in the login form and submit
    time.sleep(5)
    username_field = driver.find_element(By.NAME, "txtUserName")
    username_field.send_keys(USERNAME)

    password_field = driver.find_element(By.NAME, "txtPassword")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Wait for the user to be logged in
    time.sleep(5)
#    print html source
    menu = driver.switch_to.frame("frameheader")

    # Click on the "Manu Search" partial link
    manu_search_link = driver.find_element(By.LINK_TEXT, "Manu Search")
    manu_search_link.click()

    time.sleep(5)
    # switch to the main frame
    driver.switch_to.default_content()
    driver.switch_to.frame("framesearch")
    driver.switch_to.frame("framebody")
    
    # fill the input with name = txtSearchBox
    search_box = driver.find_element(By.NAME, "txtSearchBox")
    search_box.send_keys("environmental supreme court")
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to load
    time.sleep(5)
    supreme_court_link = driver.find_element(By.PARTIAL_LINK_TEXT, "SUPREME COURT OF INDIA")
    supreme_court_link.click()

    result_link_elements = []

    # go through each page and append the tag name a to the list result_link_elements
    for i in range(0, 100):
        if(i<46):   
                
            driver.switch_to.default_content()
            driver.switch_to.frame("framesearch")
            driver.switch_to.frame("framebody")
            next_page = driver.find_element(By.LINK_TEXT, "Next")
            next_page.click()
            time.sleep(5)
            continue
            
        try:
            time.sleep(5)
            results = driver.find_elements(By.ID, "results")
            a = results[0].find_elements(By.TAG_NAME, "a")
            lena = len(a)
            main_window_handle = driver.current_window_handle

            for j in range(0, 10):
                time.sleep(5)
                driver.switch_to.default_content()
                driver.switch_to.frame("framesearch")
                driver.switch_to.frame("framebody")

                results = driver.find_elements(By.ID, "results")
                curr_n = j
                link_id = "MainResult1_rptResults_lnkTitleHead_" + str(curr_n)
                a = results[0].find_elements(By.ID, link_id)

                print(a)
                
                current_link = a[0]
                current_link_text = current_link.text
                current_link.click()

                time.sleep(5)
                pdf_content = driver.find_element(By.ID, "divDocument")
                # save the pdf content to a file
                file_name = current_link_text + ".txt"
                with open(file_name, "w") as f:
                    f.write(pdf_content.text)
                    f.close()
                
                button_back = driver.find_element(By.XPATH, '//img[@src="images/icon_backtoResults.gif"]')
                button_back.click()
                time.sleep(5)
                driver.switch_to.window(main_window_handle)
                
                
            driver.switch_to.default_content()
            driver.switch_to.frame("framesearch")
            driver.switch_to.frame("framebody")
            next_page = driver.find_element(By.LINK_TEXT, "Next")
            next_page.click()
            time.sleep(5)

        except(Exception) as e:
            print(e)
            continue
  

except(Exception) as e:
    print(e)
    # driver.quit()


input("do you wanna quit?")
# driver.quit()
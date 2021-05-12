import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


timeout = 30

#Student Center netId, password
user = sys.argv[1]
pwd = sys.argv[2]


def wait_get_element(driver, timeout, locator):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


driver = webdriver.Chrome()
done = False

#Keep reopening the main page while not all courses in shopping cart are added to the schedule
while not done:
    try:
        driver.get("http://studentcenter.cornell.edu")

        if driver.title == "Cornell University Web Login":
            main = driver.find_element_by_xpath("html/body/main")
            netid_field = main.find_element_by_name("netid")
            pass_field = main.find_element_by_name("password")
            login_btn = main.find_element_by_name("Submit")
            netid_field.send_keys(user)
            pass_field.send_keys(pwd)
            login_btn.click()

            wrap = wait_get_element(driver, timeout, (By.ID, "wrap"))

            driver.switch_to.frame(0)

            signin_methods = driver.find_element_by_id("login-form").find_element_by_id(
                "auth_methods"
            )

            push_btn = signin_methods.find_element_by_xpath("fieldset/div/button")
            push_btn.click()

        load_page = wait_get_element(driver, 100, (By.NAME, "TargetContent"))

        driver.switch_to.frame(0)

        shopping_cart_btn = driver.find_element_by_id("ACE_width").find_element_by_id(
            "DERIVED_SSS_SCR_SSS_LINK_ANCHOR3"
        )

        shopping_cart_btn.click()

        try:
            table = wait_get_element(driver, 5, (By.CLASS_NAME, "PSLEVEL2GRIDWBO"))

            buttons = table.find_element_by_xpath(
                "tbody/tr[2]/td/table/tbody"
            ).find_elements_by_tag_name("tr")

            # Choose the semester. If choosing the last row, len(buttons) - 1. 
            # If choosing 2nd last row, len(buttons) - 2(eg. Summer or Winter session)
            sem_btn = buttons[len(buttons) - 1].find_element_by_tag_name(
                "input"
            )
            sem_btn.click()

            cont = driver.find_element_by_name("DERIVED_SSS_SCT_SSR_PB_GO")
            cont.click()
        except:
            pass
        time.sleep(1)

        row_counts = len(driver.find_elements_by_xpath("//table[@id='SSR_REGFORM_VW$scroll$0']/tbody/tr[2]/td/table/tbody/tr"))
        # print(row_counts)

        count = 0
        for i in range(row_counts - 1):
          # Check current row's status(open, closed). If open, click proceed button and enroll
          cur_status = driver.find_element_by_xpath('//*[@id="win0divDERIVED_REGFRM1_SSR_STATUS_LONG$' + str(i) + '"]/div/img')
          cur_gif = cur_status.get_attribute('src')
          if cur_gif == 'https://css.adminapps.cornell.edu/cs/cuselfservice/cache/PS_CS_STATUS_OPEN_ICN_1.gif':
            count += 1

            proceed = driver.find_element_by_id("win0divDERIVED_REGFRM1_LINK_ADD_ENRL$82$")
            proceed.click()
            
            # during the enrollment period
            finish_btn = wait_get_element(
                driver, timeout, (By.ID, "win0divDERIVED_REGFRM1_SSR_PB_SUBMIT")
            )
            finish_btn.click()
            break

          ## if not enrollment period yet and you are waiting for it
          #   dummy = False
          #   while not dummy:
          #     try:
          #       alert = wait_get_element(driver, 1, (By.ID, "win0divDERIVED_SASSMSG_SSR_MSG_PB"))
          #       print('not enrollment period yet')
          #       print('click')
          #       proceed = wait_get_element(driver, 5, (By.ID,"DERIVED_REGFRM1_LINK_ADD_ENRL$82$"))
          #       print(proceed.is_enabled())
          #       proceed.click()
          #       time.sleep(0.5)
          #       print('a')
          #     except:
          #       print('***************')
          #       finish_btn = wait_get_element(
          #       driver, 5, (By.ID, "win0divDERIVED_REGFRM1_SSR_PB_SUBMIT"))
          #       finish_btn.click()
          #       dummy = True

          # finish_btn = wait_get_element(
          #     driver, timeout, (By.ID, "win0divDERIVED_REGFRM1_SSR_PB_SUBMIT")
          # )

          # finish_btn.click()

        if count == row_counts - 1 :
          done = True

    except TimeoutException:
        pass

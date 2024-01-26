import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Bot:
    def __init__(self):
        self.login()

    def login(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chromedriver_path = "C:/Users/kaart/Downloads/chromedriver-win64(1)/chromedriver-win64/chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        self.driver.get("https://www.instagram.com/")

        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('ded_.mikey')   

        password_input = self.driver.find_element(By.NAME,'password')
        password_input.send_keys('hello@world')

        submit_btn = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button')
        submit_btn.click()
        time.sleep(5)

        # Handle "Save Your Login Info?" prompt
        try:
            save_info_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/section/div/button'))
            )
            save_info_btn.click()
        except Exception as e:
            print("Save info button not found.")

        time.sleep(5)

        # Handle "Turn on Notifications" prompt
        try:
            not_now_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"))
            )
            not_now_btn.click()
        except Exception as e:
            print("Not now button not found.")

        time.sleep(5)
        #  Instagram login logic end...

    def direct_message(self, usernames, message):
        try:
            # Open Direct Message section
            dm_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Direct messaging - 0 new notifications link']//div//div[@class='x9f619 xxk0z11 xii2z7h x11xpdln x19c4wfv xvy4d1p']//*[name()='svg']"))
            )
            dm_btn.click()

            time.sleep(5)

            click_search_dm = self.driver.find_element(By.XPATH, "//div[contains(text(),'Send message')]")
            click_search_dm.click()
            time.sleep(5)

            search_dm = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/input')

            for username in usernames:
                search_dm.clear()
                search_dm.send_keys(username)
                time.sleep(2)

                try:
                    profile_click = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div/div[1]/div/div/div[2]/div/div"))
                    )
                    profile_click.click()

                    send_msg = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div")
                    send_msg.click()
                    time.sleep(5)

                    type_msg = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]")
                    type_msg.send_keys(message)
                    time.sleep(5)

                    sending_text = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[3]")
                    sending_text.click()
                    time.sleep(5)

                    # Go back to the search box for the next user
                    self.driver.get("https://www.instagram.com/direct/inbox/")
                    time.sleep(5)
                

                except Exception as e:
                    print(f"Error sending message to {username}: {e}")

        except Exception as e:
            print(f"Direct Message button not found: {e}")

    def retrieve_usernames_from_sheets(self):
        # Use your own credentials JSON file for the service account
        credentials = ServiceAccountCredentials.from_json_keyfile_name('D:/json/instagram-scrap-408803-68e279fe3885.json',
                                                                       ['https://spreadsheets.google.com/feeds',
                                                                        'https://www.googleapis.com/auth/drive'])

        gc = gspread.authorize(credentials)
        spreadsheet_key = '1vR_Lgk_2fkw6vC9S2OmSKmZBo3Vi5tI8VBStdoBcl-U'
        worksheet = gc.open_by_key(spreadsheet_key).sheet1  # Assume data is in the first sheet

        # Assuming your data is in column A
        usernames = worksheet.col_values(1)

        # Remove the header if present
        if usernames[0] == 'Usernames':
            usernames = usernames[1:]

        return usernames 

def main():
    my_bot = Bot()
    usernames_from_sheet = my_bot.retrieve_usernames_from_sheets()
    common_message = "Hello, this is a common message for all"
    my_bot.direct_message(usernames_from_sheet, common_message)

if __name__ == '__main__':
    main()

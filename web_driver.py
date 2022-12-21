from selenium.webdriver.common.by import By
import virtual_assistant
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://openai.com/")



tryChatGPT = driver.find_element(By.XPATH, '/html/body/div[1]/header[1]/nav/div[1]/div/div/a[1]')


# loginLink = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/button[1]')
    
# loginGoogleButton = driver.find_element(By.XPATH, '/html/body/main/section/div/div/div/div[3]/form[1]/button')



# driver.get("https://beta.openai.com/chat")
# update_pop_up = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button')

# emailPick = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div')

# text_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div[1]/div/div/div/div[6]/div/div[2]/div[1]/div/div').text

def useWebDriverJourney():
    

    try:
        tryChatGPT.click()
        chatGPT_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div[2]/form/div/div[2]/textarea' )
        chatGPT_input.send_keys("what is blockchain?")
        sendGPT_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div[2]/form/div/div[2]/button')
        sendGPT_button.click()
        # loginLink.click()
        # loginGoogleButton.click()
        # emailPick.click()


        # if update_pop_up:
        #     update_pop_up.click()
        # else:
        #     pass

        # chatGPT_input.send_keys("waddup")

        # sendGPT_button.click()

    except:
        print("not found")


# useWebDriverJourney()


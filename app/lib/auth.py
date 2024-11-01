import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
from lib.utils import human_typing
import configparser


class AUTH:

    def __init__(self):

        self.URL = 'https://3500044w.index-education.net/pronote/eleve.html'
        self.driver = ''

    def bot_log(self):
        """Login to Pronote and save the page HTML to a file."""
        
        # Setup Chrome options for headless mode
        options = webdriver.ChromeOptions()
        
        # Enable full headless mode
        options.add_argument("--headless")
        
        # Disable GPU and sandboxing for more efficient headless performance
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        # Disable images and unnecessary features for faster load times
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1920,1080")  # Optional: Set window size for page layout consistency
        
        # Initialize the Chrome driver with options
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    def login_and_fetch_html(self):
        
        
        # Navigate to the target URL
        self.driver.get(self.URL)

        # Wait for page to load randomly between 3-5 seconds
        time.sleep(random.uniform(3, 5))


        
        # Load credentials from a local JSON fie
        config_path = '/Users/mbm/Desktop/Web-Scrapping/Pronify-OOP/app/lib/config.conf'
        credentials={}
        config=configparser.ConfigParser()
        config.read(config_path)
        for (key,val) in config.items('Login'):
            credentials[key]=val
        
            
        # Locate username and password input fields and perform "human-like" typing
        username_input = self.driver.find_element(By.ID, 'id_29')
        password_input = self.driver.find_element(By.ID, 'id_30')
        human_typing(username_input, credentials['username'])
        time.sleep(random.uniform(1, 2))
        human_typing(password_input, credentials['password'])
        
        # Locate and click the login button
        login_button = self.driver.find_element(By.ID, 'id_18')
        login_button.click()

        # Wait for the page to load after login (random wait between 5-7 seconds)
        time.sleep(random.uniform(5, 7))
        
        # Get the HTML content of the page
        page_source = self.driver.page_source
        
        # Quit the browser after fetching the page source
        self.driver.quit()
        
        return page_source
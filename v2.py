# I used tekky's script because I was too lazy to do it, it's just a simple script.

from time import sleep
from datetime import datetime
from os import system, name as os_name
from base64 import b64encode
from io import BytesIO
from requests import get, post, Session
from re import findall
from selenium import webdriver
from colorama import Fore, init, Style
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


text = """
 ███████ ███████ ███████  ██████  ██    ██ 
    ███  ██      ██      ██    ██  ██  ██  
   ███   █████   █████   ██    ██   ████   
  ███    ██      ██      ██    ██    ██    
 ███████ ███████ ██       ██████     ██    """

class Zefoy:
    def __init__(self) -> None:
        self.captcha_box = '/html/body/div[5]/div[2]/form/div/div'
        self.driver = self.setup_browser()
        self.sent = 0
        self.option = None
        self.clear = system('cls' if os_name == 'nt' else 'clear')
        self.captcha_box = '/html/body/div[5]/div[2]/form/div/div'

        self.xpaths = {
            "followers"     : "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
            "hearts"        : "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
            "comment_hearts": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
            "views"         : "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
            "shares"        : "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
            "favorites"     : "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
        }

        self.tasks = {
            1: (('self.driver.find_element(By.XPATH, self.xpaths["followers"]).click()', "7"), "c2VuZF9mb2xsb3dlcnNfdGlrdG9r"),
            2: (('self.driver.find_element(By.XPATH, self.xpaths["hearts"]).click()', "8"), "c2VuZE9nb2xsb3dlcnNfdGlrdG9r"),
            3: (('self.driver.find_element(By.XPATH, self.xpaths["comment_hearts"]).click()', "9"), "c2VuZC9mb2xsb3dlcnNfdGlrdG9r"),
            4: (('self.driver.find_element(By.XPATH, self.xpaths["views"]).click()', "10"), "c2VuZC9mb2xeb3dlcnNfdGlrdG9V"),
            5: (('self.driver.find_element(By.XPATH, self.xpaths["shares"]).click()', "11"), "c2VuZC9mb2xsb3dlcnNfdGlrdG9s"),
            6: (('self.driver.find_element(By.XPATH, self.xpaths["favorites"]).click()', "12"), "c2VuZF9mb2xsb3dlcnNfdGlrdG9L")
        }

    def setup_browser(self) -> WebDriver:
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    
    def solve(debug) -> dict:

        session = Session()
        session.headers = {
                'authority': 'zefoy.com',
                'origin': 'https://zefoy.com',
                'authority': 'zefoy.com',
                'cp-extension-installed': 'Yes',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }
        
        while True:
            source_code = str(session.get('https://zefoy.com').text).replace('&amp;', '&')
            captcha_token = findall(r'<input type="hidden" name="(.*)">', source_code)
            
            if 'token' in captcha_token:
                captcha_token.remove('token')
                
            captcha_url    = findall(r'img src="([^"]*)"', source_code)[0]
            token_answer = findall(r'type="text" name="(.*)" oninput="this.value', source_code)[0]
            encoded_image = b64encode(BytesIO(session.get('https://zefoy.com' + captcha_url).content).read()).decode('utf-8')
            captcha_answer = post(f"https://platipus9999.pythonanywhere.com/", json={'captcha': encoded_image, 'current_time': datetime.now().strftime("%H:%M:%S")}).json()["result"]
            
            sleep(1)

            data = {
                token_answer: captcha_answer,
            }

            for values in captcha_token:
                token, value = values.split('" value="')
                data[token] = value
            else:
                data['token'] = ''

            response = session.post('https://zefoy.com', data = data).text
            try:
                findall(r'remove-spaces" name="(.*)" placeholder', response)[0]
                return {'name':'PHPSESSID', 'value': session.cookies.get('PHPSESSID')}
            except:
                pass

    def send_bot(self, search_button, url_box, vid_info, div):
        element = self.driver.find_element(By.XPATH, url_box)
        element.clear()
        element.send_keys(vid_info)
        self.driver.find_element(By.XPATH, search_button).click()
        sleep(3)
            
        ratelimit_seconds, full = self.check_submit()
        if "(s)" in str(full):
            self.main_sleep(ratelimit_seconds)
            self.driver.find_element(By.XPATH, search_button).click()
            sleep(2)
            
        sleep(3)
            
        send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
        self.driver.find_element(By.XPATH, send_button).click()
        self.sent += 1
        print(self._print(f"Sent {self.sent} times."))
            
        sleep(4)
        self.send_bot(search_button, url_box, vid_info, div)

    def main_sleep(self, delay):
        while delay != 0:
            sleep(1)
            delay -= 1
            self.change_title(f"TikTok Zefoy Automator using Zefoy.com / Cooldown: {delay}s / Github: @useragents")

    def convert(self, min: int, sec: int) -> int:
            return min * 60 + sec + 4 if min != 0 else sec + 4

    def check_submit(self):
        remaining = f'//*[@id="{self.tasks[self.option][1]}"]/span'
            
        try:
            element = self.driver.find_element(By.XPATH, remaining)
        except:
            return None, None
            
        if "READY" in element.text:
            return True, True
            
        if "seconds for your next submit" in element.text:
            output          = element.text.split("Please wait ")[1].split(" for")[0]
            minutes         = element.text.split("Please wait ")[1].split(" ")[0]
            seconds         = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration  = self.convert(int(minutes), int(seconds))
                
            return sleep_duration, output
            
        return element.text, None
            
    def check_status(self):
        statuses = {}
            
        for thing in self.xpaths:
            value = self.xpaths[thing]
            element = self.driver.find_element(By.XPATH, value)
                
            if not element.is_enabled():
                statuses.update({thing: f"{Fore.RED}[OFFLINE]"})
                
            else:
                statuses.update({thing: f"{Fore.GREEN}[WORKS]"})
            
        return statuses

    def _print(self, msg, status = "-"):
        return f" {Fore.WHITE}[{Fore.CYAN}{status}{Fore.WHITE}] {msg}"

    def change_title(self, arg):
        system(f'title {arg}' if os_name == 'nt' else '')

    def wait_for_xpath(self, xpath):
        while True:
            try:
                self.driver.find_element(By.XPATH, xpath)
                break
            except:
                pass

            
    def main(self):
        self.clear
        print(Fore.CYAN + text+ "\n") 
        self.driver.get("https://zefoy.com")

        print(self._print("Solving The Captcha"))
        self.driver.add_cookie(self.solve())
        self.driver.refresh()

        self.wait_for_xpath(self.xpaths["views"])

        self.clear

        status = self.check_status()
            
        print('\n')
            
        counter = 1
        for thing in status:
            print(self._print(f"{thing} {status[thing]}", counter))
            counter += 1

        self.option = int(input("\n" + self._print(f"")))
        video_url     = input("\n" + self._print(f"Username/VideoURL: "))    

        task, div = self.tasks[self.option][0]; eval(task)
               
        video_url_box = f'/html/body/div[{div}]/div/form/div/input'
        search_box    = f'/html/body/div[{div}]/div/form/div/div/button'
        
            
        self.send_bot(search_box, video_url_box, video_url, div)



if __name__ == "__main__":
    Zefoy().main()

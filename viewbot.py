#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, requests, io, time, random, bs4, sys, datetime, re, base64, urllib.parse, json, threading, cursor
from pystyle import *
from PIL import Image

class Main:
    def __init__(self):
        cursor.hide()
        
        self.blue    = Col.light_blue
        self.lblue   = Colors.StaticMIX((Col.light_blue, Col.white, Col.white))
        self.url     = 'https://zefoy.com/'
        self.session = requests.session()
        self.start   = time.time()
        self.config  = json.load(open('./config.json', 'r'))
        self.videos  = self.config['videos']
        self.mode    = 'c2VuZC9mb2xsb3dlcnNfdGlrdG9s' if self.config['shares'] is True else "c2VuZC9mb2xsb3dlcnNfdGlrdG9V"
    
    def format(self, symbol, text):
        return f"""                      {Col.Symbol(symbol, self.lblue, self.blue)} {self.lblue}{text}{Col.reset}"""
    
    def gui(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        txt = """\n██╗   ██╗██╗███████╗██╗    ██╗██████╗  ██████╗ ████████╗\n██║   ██║██║██╔════╝██║    ██║██╔══██╗██╔═══██╗╚══██╔══╝\n██║   ██║██║█████╗  ██║ █╗ ██║██████╔╝██║   ██║   ██║   \n╚██╗ ██╔╝██║██╔══╝  ██║███╗██║██╔══██╗██║   ██║   ██║   \n ╚████╔╝ ██║███████╗╚███╔███╔╝██████╔╝╚██████╔╝   ██║   \n  ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═════╝  ╚═════╝    ╚═╝\n                   By &! Tekky#1337\n\n\n\n\n"""
        print(Colorate.Vertical(Colors.DynamicMIX((Col.light_blue, Col.cyan)), Center.XCenter(txt)))

    def title(self):
        if os.system != 'nt':
            return

        while True:
            
            curr_time = str(datetime.timedelta(seconds=(time.time() - self.start))).split('.')[0]
            try:
                views = requests.get(
                    url = f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{self.videos[0]}%5D",
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
                        }
                ).json()["aweme_details"][0]["statistics"]["play_count"]
                
                os.system(f'title Tekky © 2022  x  Zviews ^| Views: {views} ^| Elapsed Time: {curr_time} ^| v2.1' if os.name == 'nt' else '')
                time.sleep(0.5)
            except:
                os.system(f'title Tekky © 2022  x  Zviews ^| Views: ERROR ^| Elapsed Time: {curr_time} ^| v2.1' if os.name == 'nt' else '')
                pass
    
    def solve_captcha(self, sessid):   
        try:
            # -- get captcha image --
            response = self.session.get(
                self.url  + "a1ef290e2636bf553f39817628b6ca49.php",
                headers={
                    "origin": "https://zefoy.com",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest",
                    "cookie": f"PHPSESSID={sessid}",
                },
                params={
                    "_CAPTCHA": "",
                    "t": f"{round(random.random(), 8)} {int(time.time())}"
                }
            )

            req = requests.post(
                url = "https://api.xtekky.com/ocr/v2",
                data = {
                    "image": base64.b64encode(response.content).decode()
                }
            )
            captcha_answer = req.json()['captcha']['answer']
            
            #submit response
            _response = self.session.post(
                self.url,
                data={
                    "captcha_secure": captcha_answer,
                    "r75619cf53f5a5d7aa6af82edfec3bf0": ""
                },
                headers={
                    "cookie": f"PHPSESSID={sessid}",
                    "origin": "https://zefoy.com",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                    "x-requested-with": "XMLHttpRequest"
                }
            )
            alpha_key = re.findall('(?<=")[a-z0-9]{16}', _response.text)[0]
            print(self.format("!", f"Solved captcha ! | {captcha_answer}"))

            return alpha_key
        except Exception as e:
            print(self.format("!", f"Error: {e}"))
            print(self.format("!", "Captcha Invalid | Check access to Zefoy | xtekky.com may be down"))
            self.solve_captcha(sessid)

    def get_sessid(self):
        sessid = self.session.get(
            self.url,
            headers={
                "origin": "https://zefoy.com",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
        ).cookies.values()[0]
        return sessid
    
    def decrypt(self, data):
        return base64.b64decode(urllib.parse.unquote(data[::-1])).decode()
    
    def decrypt_timer(self, data):
        #decrypted = base64.b64decode(urllib.parse.unquote(data[::-1])).decode()
        if len(re.findall(' \d{3}', data)) != 0:
            timer = re.findall(' \d{3}', data)[0]
        else:
            timer = data.split("= ")[1].split("\n")[0]

        return int(timer)
    
    def views_loop(self, sessid, alpha_key):
        while True:
            try:
                time.sleep(2)
                aweme_id = random.choice(self.videos)
                
                request = self.session.post(
                    self.url + str(self.mode),
                    headers={
                        "cookie": f"PHPSESSID={sessid}",
                        "origin": "https://zefoy.com",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                        "x-requested-with": "XMLHttpRequest"
                    },
                    data={
                        alpha_key: f"https://www.tiktok.com/@onlp/video/{aweme_id}"
                    }
                )
                decryped_answer = self.decrypt(request.text)

                if 'This service is currently not working' in decryped_answer:
                    print(self.format('x', 'Views not available in the moment'))
                    input();sys.exit()

                elif 'Server too busy' in decryped_answer:
                    print(self.format('x', 'Server busy ! (waiting 10s)'))
                    time.sleep(10);continue

                elif 'function updatetimer()' in decryped_answer:
                    print("\r", end="")
                    timer = self.decrypt_timer(decryped_answer)

                    print(self.format('@', f"Timer: {timer}     "), end="")
                    start = time.time()
                    
                    while time.time() < start + timer:
                        print("\r", end="")
                        print(self.format('@', f'Timer: {round((start + timer) - time.time())}       '), end="")
                        time.sleep(1)
                        
                    print(self.format('!', f'Sending views/shares ...'));continue

                soup = bs4.BeautifulSoup(decryped_answer, 'html.parser')
                try:
                    beta_key = soup.find("input", {"type": "text"}).get("name")
                except:
                    input(decryped_answer);sys.exit()

                time.sleep(1)
                
                start = time.time()
                send_views = requests.post(
                    self.url + str(self.mode),
                    headers={
                        "cookie": f"PHPSESSID={sessid}",
                        "origin": "https://zefoy.com",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
                        "x-requested-with": "XMLHttpRequest"
                    },
                    data={
                        beta_key: aweme_id
                    }
                )
                latency = round(time.time() - start, 2)
                if latency > 3:
                    print(self.format('!', f'Sent views/shares [id={aweme_id}]'))

                decrypted_response = self.decrypt(send_views.text)
                
                if 'Too many requests. Please slow down.' in decrypted_response:
                    print(self.format('x', "Ratelimited"))
                    time.sleep(120);continue
                    
                timer = self.decrypt_timer(decrypted_response)

                print(self.format('@', f"Timer: {timer}    "), end="")
                start = time.time()

                while time.time() < start + timer:
                    print("\r", end="")
                    print(self.format('@', f'Timer: {round((start + timer) - time.time())}     '), end="")
                    time.sleep(1)
                
                print("\r", end="")
                print(self.format('!', f'Sending views/shares ...'))
            except:
                os.system('python viewbot.py')
                sys.exit()

    def main(self):
        threading.Thread(target=self.title).start()
        self.gui()
        sessid = self.get_sessid()
        print(self.format('!', f'Sessid: {sessid}'))
        alpha_key = self.solve_captcha(sessid)
        print('\n' + self.format('!', f'Alpha Key: {alpha_key.upper()}'))
        
        self.views_loop(sessid, alpha_key)

if __name__ == '__main__':
    Main().main()

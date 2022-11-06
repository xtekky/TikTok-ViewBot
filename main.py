from re             import findall, compile
from time           import time, sleep
from json           import loads
from random         import random
from base64         import b64encode, b64decode
from requests       import Session, get, head
from urllib.parse   import unquote
from pystyle        import *
from os             import system, name, execv
from sys            import executable, argv
from hashlib        import sha256
from threading      import Thread

proxies   = None # experimental
endpoints = {
    "views"     : "c2VuZC9mb2xsb3dlcnNfdGlrdG9V",
    "hearts"    : "c2VuZE9nb2xsb3dlcnNfdGlrdG9r",
    "followers" : "c2VuZF9mb2xsb3dlcnNfdGlrdG9r",
    "favorites" : "c2VuZF9mb2xsb3dlcnNfdGlrdG9L",
    "shares"    : "c2VuZC9mb2xsb3dlcnNfdGlrdG9s",
}

class livecounts:
    @staticmethod
    def __signature(timestamp: int) -> dict:
        
        return {
            'x-aurora' : str(3 * timestamp),
            'x-joey'   : str(timestamp),
            'x-maven'  : sha256(f"0AVwElhWi1IfwcZKSNzq7E^84hFQ4ykenNAxeY7r@6ho1oTd6Ug*!WC&p$2aGY8MLHEkH0i8XCwnj3#JqI1NzCb91$gNzLYCbbG@NqvQMbcf8W9v3%s#uzjP@z*!e9a41JNWBqRIMJ*ULuav5k8z4kBj2^BCC%!3q@N0zZOS^TL#GzVz@9fhjg&^mSWi&oU5GMoCu9{timestamp}".encode()).hexdigest(),
            'x-mayhem' : "553246736447566b58312f7a4f72413653425342717a6e4231596f7a4d59686564764842324b396478544443756669734d56706f4346334633456366724b6732",
            'x-midas'  : sha256(str(timestamp + 64).encode()).hexdigest()
        }
    
    @staticmethod
    def video_info(video_id: (int or str)) -> dict:
        timestamp = int(time() * 1000)
        
        headers = {
            **livecounts.__signature(timestamp),
            'authority' : 'tiktok.livecounts.io',
            'origin'    : 'https://livecounts.io',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        
        req = get(f'https://tiktok.livecounts.io/video/stats/{video_id}', headers=headers)
        
        return req.json()
    
    @staticmethod
    def link_to_id(video_link: (int or str)) -> str:
        return str(
            findall(r"(\d{18,19})", video_link)[0] if len(findall(r"(\d{18,19})", video_link)) == 1
            else findall(r"(\d{18,19})", head(video_link, allow_redirects=True, timeout=5).url)[0]
        )
        

class zefoy:
    def __init__(self, *args, **kwargs) -> None:
        self.__session  = Session(); self.__init_session(); self.__ad_cookies()
        self.__aweme_id = None
        self.__item_id  = None
        self.__keys = {
            'key_1': None,
            'key_2': None
        }
        
    def __title_loop(self):
        if name == 'nt':
            while True:
                stats = livecounts.video_info(self.__item_id)
                system('title Zefoy Bot by @xtekky ^| Likes: %s Views: %s Shares: %s ^| %s ^| mode: shares' % (
                    stats['likeCount'], stats['viewCount'], stats['shareCount'], str(self.__item_id)
                ))
                
                sleep(0.5)
        
    def __base_headers(self, addon: dict = {}) -> dict:
        
        return {
            **addon,
            "host"               : "zefoy.com",
            "connection"         : "keep-alive",
            "sec-ch-ua"          : "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
            "accept"             : "*/*",
            "x-requested-with"   : "XMLHttpRequest",
            "sec-ch-ua-mobile"   : "?0",
            "user-agent"         : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "sec-ch-ua-platform" : "\"Windows\"",
            "origin"             : "https://zefoy.com",
            "sec-fetch-site"     : "same-origin",
            "sec-fetch-mode"     : "cors",
            "sec-fetch-dest"     : "empty",
            "accept-language"    : "en-US,en;q=0.9",
        }
        

    def __get_captcha(self) -> str: 

        __captcha_image = self.__session.get("https://zefoy.com/a1ef290e2636bf553f39817628b6ca49.php", 
            headers = self.__base_headers(), 
            proxies = proxies,
            params  = {
                "_CAPTCHA": "",
                "t": f"{round(random(), 8)} {int(time())}"
        })
        
        return str(b64encode(__captcha_image.content).decode())

    
    def __solve_captcha(self, __image_data: str) -> None:
        response = self.__session.post('https://captcha.xtekky.repl.co/', json = {
            'captcha': __image_data
        })
        
        if response.json()['status_code'] == 0:
            captcha_answer = response.json()['captcha_answer']
        
        else:
            print('            ' + zefoy.sprint('x', 'error    -', str(response.json())))
            input('            ' + zefoy.sprint('*', 'restart  -', 'press ' + Col.white + 'enter'))
            execv(executable, ['python'] + argv)
        
        try:
            response = self.__session.post("https://zefoy.com/", 
                headers = self.__base_headers(),
                proxies = proxies,
                data    = {
                    "captcha_secure": captcha_answer,
                    "r75619cf53f5a5d7ba6af82edfec3bf0": ""
            })
            
            self.__keys["key_1"]  = findall('(?<=")[a-z0-9]{16}', response.text)[0]

            return True
        
        except Exception:
            return False
        
    def __init_session(self) -> None:
        self.__session.get('https://zefoy.com/',
            proxies = proxies,
            headers = self.__base_headers()
        )
        
    def __ad_cookies(self) -> None:

        __ad_cookies = self.__session.get("https://partner.googleadservices.com/gampad/cookie.js", 
            headers = {'host':'partner.googleadservices.com','connection':'keep-alive','sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','sec-ch-ua-mobile':'?0','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36','sec-ch-ua-platform':'"Windows"','accept':'*/*','sec-fetch-site':'cross-site','sec-fetch-mode':'no-cors','sec-fetch-dest':'script','accept-encoding':'gzip, deflate, br','accept-language':'en-US,en;q=0.9'}, 
            params  = {
                "domain"   : "zefoy.com",
                "callback" : "_gfp_s_",
                "client"   : "ca-pub-3192305768699763",
                "gpid_exp" : 1
        })

        __json_data = loads(findall(r'_gfp_s_\((.*)\);', __ad_cookies.text)[0])

        self.__session.cookies.set("_gads", __json_data['_cookies_'][0]['_value_'], domain='zefoy.com')
        self.__session.cookies.set("__gpi", __json_data['_cookies_'][1]['_value_'], domain='zefoy.com')
        
    def __zefoy_decrypt(self, data):
        return b64decode(unquote(data[::-1])).decode()
    
    def __search_link(self, __tiktok_link: str) -> None:
        try:
            
            __search_link = self.__session.post('https://zefoy.com/' + endpoints['shares'],
                headers = self.__base_headers(),
                proxies = proxies,
                data = {
                    self.__keys['key_1']: __tiktok_link
            })
            
            __search_link_response = self.__zefoy_decrypt(__search_link.text)
            # print(__search_link_response)
            if 'Please try again later. Server too busy' in __search_link_response or 'currently not working' in __search_link_response:
                print('            ' + zefoy.sprint('x', 'error    -', 'server busy'))
                sleep(60)
                self.__search_link(__tiktok_link)
            
            self.__keys['key_2'], self.__aweme_id = findall(r'name="(.*)" value="(.*)" hidden', __search_link_response)[0]
            
        except Exception:
            try:
                timer = findall(r'ltm=(\d*);', __search_link_response)[0]
                if int(timer) == 0:
                    return
                
                print('            ' + zefoy.sprint('*', 'sleeping -', 'for ' + Col.white + str(timer) +  Col.blue +' seconds'),  end="\r")

                start = time()
                while time() < start + int(timer):
                    time_left = str(round((start + int(timer)) - time()))
                    
                    if len(time_left) == 2:
                        time_left = time_left + ' '
                    if len(time_left) == 1:
                        time_left = time_left + '  '
                    
                    print('            ' + zefoy.sprint('*', 'sleeping -', 'for ' + Col.white + time_left +  Col.blue +' seconds'),  end="\r"); sleep(1)
                print('            ' + zefoy.sprint('*', 'sending  -', 'shares...'),  end="\r")
                print('')
                self.__search_link(__tiktok_link)

            except Exception as e:
                print('            ' + zefoy.sprint('x', 'error    -', str(e)))
                input('            ' + zefoy.sprint('*', 'restart  -', 'press ' + Col.white + 'enter'))
                execv(executable, ['python'] + argv)

    def __send_req(self) -> None:
        self.__session.post('https://zefoy.com/' + endpoints['shares'],
            headers = self.__base_headers(),
            proxies = proxies,
            data = {
                self.__keys['key_2']: self.__aweme_id,
        })
        
        print('            ' + zefoy.sprint('*', 'success  -', 'sent ' + Col.white + 'shares' + Col.blue + ' !'))
        sleep(5)
    
    def mainloop(self) -> None:
        __start         = time()
        __captcha_image = self.__get_captcha()

        if self.__solve_captcha(__captcha_image) is True:
            print('            ' + zefoy.sprint('*', 'success  -', f'solved captcha: {Col.white}{round(time() - __start, 1)}{Col.blue}s'))
            video_link = input('            ' + zefoy.sprint('?', 'input    -', 'video link') + ' > '); print('\n')
            self.__item_id = livecounts.link_to_id(video_link)
            Thread(target=self.__title_loop).start()
            
            while True:
                self.__search_link(video_link); sleep(0.5)
                self.__send_req(); sleep(1)
        
        else:
            print('            ' + zefoy.sprint('x', 'error    -', 'failed to solve captcha'))
            input('            ' + zefoy.sprint('*', 'restart  -', 'press ' + Col.white + 'enter'))
            execv(executable, ['python'] + argv)
            
    @staticmethod
    def sprint(x: str, num: int, msg: str) -> None:
        return '    %s{%s%s%s}%s %s %s[%s%s%s]%s' % (
            Col.purple, Col.reset,
            x, 
            Col.purple, Col.reset,
            num,
            Col.purple, Col.blue,
            msg,
            Col.purple, Col.reset
        )

    @staticmethod
    def startup():
        system('cls' if name == 'nt' else ''); system('title Like Bot by @xtekky ^| starting...')
        print(Col.purple + Center.XCenter('''\n ______ _______ _______  _____  __   __      ______   _____  _______\n  ____/ |______ |______ |     |   \_/        |_____] |     |    |   \n /_____ |______ |       |_____|    |         |_____] |_____|    |   \n                      made with <3 by tekky   ''') + Col.reset); print("\n\n")

if __name__ == "__main__":
    zefoy.startup()
    zefoy(None).mainloop()

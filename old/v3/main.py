# xtekky @ 2022

from re             import findall, compile
from time           import time, sleep
from json           import loads
from random         import random, choices
from base64         import b64encode, b64decode
from requests       import Session, get, head, post
from urllib.parse   import unquote
from pystyle        import *
from os             import system, name, execv
from sys            import executable, argv
from hashlib        import sha256
from threading      import Thread
from PIL            import Image
from io             import BytesIO

config = {
    'cloudflare': 'kAMtbsTqP9nr2zH.dUqsGIlq60hFfRCsoy1WX.bPhiE-1669637072-0-150',
    'mode'      : 'views'
}

item_id      = None
proxies      = None # experimental

endpoints    = {
    "views"     : "c2VuZC9mb2xeb3dlcnNfdGlrdG9V",
    "hearts"    : "c2VuZE9nb2xsb3dlcnNfdGlrdG9r",
    "followers" : "c2VuZF9mb2xsb3dlcnNfdGlrdG9r",
    "favorites" : "c2VuZF9mb2xsb3dlcnNfdGlrdG9L",
    "shares"    : "c2VuZC9mb2xsb3dlcnNfdGlrdG9s",
}

__keys__ = {
    'key_1': None,
    'key_2': None
}

class livecounts:
    
    @staticmethod
    def video_info(video_id: (int or str)) -> dict:
        
        headers = {
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

def __decrypt__(data: str) -> str:
    # print(data)
    a = unquote(data[::-1])
    
    return b64decode(a).decode()

def __sprint__(x: str, num: int, msg: str, colour: str = Col.purple) -> None:
    return '    %s{%s%s%s}%s %s %s[%s%s%s]%s' % (
        colour, Col.reset,
            x, 
        colour, Col.reset,
            num,
        colour, Col.blue,
            msg,
        colour, Col.reset
    )

def __format__(string: str) -> str:
    t = ""
    
    for i in string:
        if i in t : pass
        else      : t = t + i
    
    return t

def __init__(__session__: Session) -> tuple:
    __html__ = str(__session__.get('http://zefoy.com').text).replace('&amp;', '&')

    captcha_token = None
    results = findall(r'name="([A-Za-z0-9]{31,32})">', __html__)
    if results:
        captcha_token = results[0]
        
    captcha_url   = findall(r'img src="([^"]*)"', __html__)[0]
    sessid        = __session__.cookies.get('PHPSESSID')
    
    return captcha_token, captcha_url, sessid

def __solve__(__session__: Session, captcha_token: str, captcha_url: str) -> True or False:
    try:
        captcha_image = __session__.get('https://zefoy.com' + captcha_url).content
        response      = __session__.post('https://captcha.xtekky.repl.co/', json = {
                'captcha': b64encode(captcha_image).decode('utf-8'),
        })
        
        if response.json()['status_code'] == 0:
            captcha_answer = __format__(response.json()['captcha_answer'])

        else:
            print('            ' + __sprint__('x', 'error    -', 'need manual solving'))
            image = Image.open(BytesIO(captcha_image))
            image.show()
            captcha_answer = input('            ' + __sprint__('?', 'input    -', 'captcha') + ' > '); print('\n')
    
        response = __session__.post('https://zefoy.com', data = {
            "captcha_secure": captcha_answer,
            captcha_token   : ""
        })
        
        print(response.text)
        
        __keys__["key_1"]  = findall('(?<=")[a-z0-9]{16}', response.text)[0]

        return True
    
    except Exception as e:
        
        print('            ' + __sprint__('x', 'error    -', str(e)))
        __solve__(__session__, captcha_token, captcha_url)

def __search__(__session__: Session, __tiktok_link: str) -> None:
    try:

        req_token = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=16))
        sessionid = __session__.cookies.get('PHPSESSID')
        token = __keys__["key_1"]
        
        headers = {
            'authority': 'zefoy.com',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{req_token}',
            'cookie': f'PHPSESSID={sessionid}',
            'origin': 'https://zefoy.com',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = f'------WebKitFormBoundary{req_token}\r\nContent-Disposition: form-data; name="{token}"\r\n\r\nhttps://www.tiktok.com/@ninia355/video/7183719544077225222\r\n------WebKitFormBoundary{req_token}--\r\n'

        __search_link = post(f'https://zefoy.com/{endpoints[config["mode"]]}', headers=headers, data=data)

        __search_link_response = __decrypt__(__search_link.content)

        if "Session expired. Please re-login." in __search_link_response:
            print('            ' + __sprint__('x', 'error    -', 'session expired input your own sessionid'))
            __session__.cookies['PHPSESSID'] = input('            ' + __sprint__('?', 'input    -', 'sessionid') + ' > '); print('\n')
            __search__(__session__, __tiktok_link)
            
        if 'Please try again later. Server too busy' in __search_link_response or 'currently not working' in __search_link_response:
            print('            ' + __sprint__('x', 'error    -', 'server busy / or currently disabled'))
            sleep(60)
            __search__(__tiktok_link)
        
        __keys__['key_2'], _= findall(r'name="(.*)" value="(.*)" hidden', __search_link_response)[0]
        
    except Exception as e:
        try:
            timer = findall(r'ltm=(\d*);', __search_link_response)[0]
            if int(timer) == 0:
                return
            
            print('            ' + __sprint__('*', 'sleeping -', 'for ' + Col.white + str(timer) +  Col.blue +' seconds'),  end="\r")

            start = time()
            while time() < start + int(timer):
                time_left = str(round((start + int(timer)) - time()))
                
                if len(time_left) == 2:
                    time_left = time_left + '  '
                if len(time_left) == 1:
                    time_left = time_left + '  '
                
                print('            ' + __sprint__('*', 'sleeping -', 'for ' + Col.white + time_left +  Col.blue +' seconds'),  end="\r"); sleep(1)
            print('            ' + __sprint__('*', 'sending  -', f'{config["mode"]}...                                  '),  end="\r")
            print('')
            __search__(__session__, __tiktok_link)

        except Exception as e:
            print('            ' + __sprint__('x', 'error    -', str(e)))
            input('            ' + __sprint__('*', 'restart  -', 'press ' + Col.white + 'enter'))
            execv(executable, ['python'] + argv)

def __send__(__session__: Session) -> None:

    headers = {
        'authority'         : 'zefoy.com',
        'accept'            : '*/*',
        'accept-language'   : 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'content-type'      : 'multipart/form-data; boundary=----WebKitFormBoundary',
        'origin'            : 'https://zefoy.com',
        'sec-ch-ua'         : '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile'  : '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest'    : 'empty',
        'sec-fetch-mode'    : 'cors',
        'sec-fetch-site'    : 'same-origin',
        'user-agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-requested-with'  : 'XMLHttpRequest',
    }

    __send_req = post(f'https://zefoy.com/{endpoints[config["mode"]]}', headers = headers,
        data    = f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="{__keys__["key_2"]}"\r\n\r\n{item_id}\r\n------WebKitFormBoundary--\r\n', 
        cookies = {
            # 'cf_clearance': config["cloudflare"],
            'PHPSESSID'   : __session__.cookies.get_dict()["PHPSESSID"]
    })
    
    # print(__decrypt__(__send_req.content))
    
    print('            ' + __sprint__('*', 'success  -', 'sent ' + Col.white + config['mode'] + Col.blue + ' !'))
    sleep(5)

if __name__ == '__main__':
    with Session() as __session__:
        # __session__.cookies.set('cf_clearance', config['cloudflare'])
        __session__.headers.update({
            'authority'             : 'zefoy.com',
            # 'accept'                : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language'       : 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cp-extension-installed': 'Yes',
            'sec-ch-ua'             : '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile'      : '?0',
            'sec-ch-ua-platform'    : '"Windows"',
            'sec-fetch-dest'        : 'document',
            'sec-fetch-mode'        : 'navigate',
            'sec-fetch-site'        : 'none',
            'sec-fetch-user'        : '?1',
            'upgrade-insecure-requests' : '1',
            'user-agent'                : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'x-requested-with'          : 'XMLHttpRequest',
        })
        
        # print(__session__.headers)
        a, b, c = __init__(__session__)

        __start = time()
        
        if __solve__(__session__, a, b) == True:
            print('            ' + __sprint__('*', 'success  -', f'solved captcha: {Col.white}{round(time() - __start, 1)}{Col.blue}s'))
            video_link = input('            ' + __sprint__('?', 'input    -', 'video link') + ' > '); print('\n')

            item_id = livecounts.link_to_id(video_link)
            # Thread(target=__title_loop).start()
            # print(__keys__)
            # sleep(4) 
            while True:
                __search__(__session__, video_link); sleep(0.5)
                __send__(__session__); sleep(1)
            
        else:
            print('            ' + __sprint__('x', 'error    -', 'failed to solve captcha'))
            input('            ' + __sprint__('*', 'restart  -', 'press ' + Col.white + 'enter'))
            execv(executable, ['python'] + argv)
# xtekky @ 2022

from re             import findall, compile
from time           import time, sleep
from json           import loads
from random         import random
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
    'mode'      : 'hearts'
}

item_id      = None
proxies      = None # experimental

endpoints    = {
    "views"     : "c2VuZC9mb2xsb3dlcnNfdGlrdG9V",
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

    captcha_token = findall(r'name="([A-Za-z0-9]{31,32})">', __html__)[0]
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
        
        __keys__["key_1"]  = findall('(?<=")[a-z0-9]{16}', response.text)[0]

        return True
    
    except Exception as e:
        print('            ' + __sprint__('x', 'error    -', str(e)))
        return False

def __search__(__session__: Session, __tiktok_link: str) -> None:
    try:

        cookies = {
                'cf_clearance': config["cloudflare"],
                'PHPSESSID'   : __session__.cookies.get_dict()["PHPSESSID"]
        }
        
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

        __search_link = post(f'https://zefoy.com/{endpoints[config["mode"]]}', headers=headers,
            data    = f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="{__keys__["key_1"]}"\r\n\r\n{__tiktok_link }\r\n------WebKitFormBoundary--\r\n', 
            cookies = cookies
        )
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
            __search__(__tiktok_link)

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
            'cf_clearance': config["cloudflare"],
            'PHPSESSID'   : __session__.cookies.get_dict()["PHPSESSID"]
    })
    
    # print(__decrypt__(__send_req.content))
    
    print('            ' + __sprint__('*', 'success  -', 'sent ' + Col.white + config['mode'] + Col.blue + ' !'))
    sleep(5)

if __name__ == '__main__':
    with Session() as __session__:
        __session__.cookies.set('cf_clearance', config['cloudflare'])
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

        __start         = time()
        
        if __solve__(__session__, a, b) == True:
            print('            ' + __sprint__('*', 'success  -', f'solved captcha: {Col.white}{round(time() - __start, 1)}{Col.blue}s'))
            video_link =  input('            ' + __sprint__('?', 'input    -', 'video link') + ' > '); print('\n')

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
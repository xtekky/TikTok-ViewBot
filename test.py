from requests import Session
from re       import findall

def __init__(__session__: Session) -> tuple:
    __html__ = str(__session__.get('http://zefoy.com').text).replace('&amp;', '&')

    captcha_token = findall(r'name="([A-Za-z0-9]{31,32})">', __html__)[0]
    captcha_url   = findall(r'img src="([^"]*)"', __html__)[0]
    sessid        = __session__.cookies.get('PHPSESSID')
    
    return captcha_token, captcha_url, sessid

def __solve__(__session__: Session, captcha_token: str, captcha_url: str) -> True or False:
    captcha_image = __session__.get('https://zefoy.com' + captcha_url).content

with Session() as __session__:
    __session__.cookies.set("cf_clearance", 'kAMtbsTqP9nr2zH.dUqsGIlq60hFfRCsoy1WX.bPhiE-1669637072-0-150')
    __session__.headers.update({
        'authority'             : 'zefoy.com',
        'accept'                : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
    })
    
    # print(__session__.headers)
    a, b, c = __init__(__session__)
    print(a, b, c)
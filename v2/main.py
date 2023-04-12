from re           import findall
from io           import BytesIO
from PIL          import Image
from time         import sleep, time
from base64       import b64decode
from random       import choices
from string       import ascii_letters, digits
from requests     import Session, post
from colorama     import Fore, init; init()
from datetime     import datetime
from urllib.parse import unquote, quote

#from tls_client import Session


def fmt(string) -> str:
    return f"{Fore.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {Fore.BLUE}INFO {Fore.MAGENTA}__main__ -> {Fore.RESET}{string}"

def decode(text: str) -> str:
    return b64decode(unquote(text[::-1])).decode()

def get_client() -> Session:
    client = Session()
    client.headers = {        
        'authority'             : 'zefoy.com',
        'origin'                : 'https://zefoy.com',
        'authority'             : 'zefoy.com',
        'cp-extension-installed': 'Yes',
        'user-agent'            : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    
    #client.cookies.set('window_size', '546x776')
    #client.cookies.set('user_agent', f"{quote(client.headers['user-agent'])}")
    
    return client

def solve_captcha(client: Session) -> None:
    try:
        html           = str(client.get('https://zefoy.com').text).replace('&amp;', '&')
        print(html)
        
        captcha_token  = findall(r'<input type="hidden" name="(.*)">', html)[0]
        captcha_url    = findall(r'img src="([^"]*)"', html)[0]
        captcha_token_v2 = findall(r'type="text" maxlength="50" name="(.*)" oninput="this.value', html)[0]
        
        print(fmt(f'captcha_token: {captcha_token}'))
        print(fmt(f'captcha_url: {captcha_url}'))
        
        
        captcha_image  = client.get('https://zefoy.com' + captcha_url).content;
        image          = Image.open(BytesIO(captcha_image));image.show()
        
        captcha_answer = input('solve captcha: ')
        
        response = post('https://zefoy.com', headers = {
                'authority': 'zefoy.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
                'cache-control': 'no-cache',
                'content-type': 'application/x-www-form-urlencoded',
                'cp-extension-installed': 'Yes',
                'origin': 'null',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'cookie': f'PHPSESSID={client.cookies.get("PHPSESSID")}',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            }, 
            data = {
                captcha_token_v2: captcha_answer,
                captcha_token   : ""
        })
        
        #print(response.text)
        
        key_1 = findall(r'remove-spaces" name="(.*)" placeholder', response.text)[0]
        
        print(fmt(f'key_1: {key_1}'))
        
        return key_1
        
    except Exception as e:
        print(fmt(f'Failed to solve captcha (zefoy may have blocked you) [{e}]'))
        return
    
def send(client: Session, key: str, aweme_id: str) -> None:
    
    token = ''.join(choices(ascii_letters + digits, k=16))
    data  = f'------WebKitFormBoundary{token}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{aweme_id}\r\n------WebKitFormBoundary{token}--\r\n'
    
    # data = {
    #     key: aweme_id
    # }
    
    cookies = client.cookies.get_dict() | {
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'window_size': '788x841',
        
        '_ga': 'GA1.1.1129024515.1681241946',
        '__gads': 'ID=8310bfabde912e1c-22433ff457dc0089:T=1681241946:RT=1681241946:S=ALNI_MZ595crKlMda2mcv0z8CUqI6ZPixA',
        '__gpi': 'UID=00000c0098073f57:T=1681241946:RT=1681241946:S=ALNI_MaFjF61WwqpZTpOZ-TUV20ipRozZQ',
        '_ga_1WEXNS5FFP': 'GS1.1.1681241946.1.1.1681241951.0.0.0',
    } 
    
    print(cookies)
    
    #lient = Session(client_identifier='chrome110')
    
    response = post('https://zefoy.com/c2VuZF9mb2xsb3dlcnNfdGlrdG9L', data = data, cookies = cookies,
        headers = {
            'authority': 'zefoy.com',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary{token}',
            'origin': 'https://zefoy.com',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'}).text
    
    response = unquote(response[::-1]).encode()
    response = b64decode(response).decode()
    print(response)
    
    if 'Session expired' in response:
        raise Exception('session expired')
        exit()
    
    if 'views sent' in response: 
        print(fmt(f'views sent to {aweme_id}'))
    
    else:
        print(fmt(f'Failed to send views to {aweme_id}'))

def search_link(client: Session, key_1: str, tiktok_url: str) -> str:
    #token = choices(ascii_letters + digits, k=16)

    data = f'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="{key_1}"\r\n\r\n{tiktok_url}\r\n------WebKitFormBoundary--\r\n'

    # print(client.cookies)
    # print(client.cookies.get("PHPSESSID"))
    # print(key_1)
    # print(tiktok_url)
    
    response =  decode(post('https://zefoy.com/c2VuZF9mb2xsb3dlcnNfdGlrdG9L', data = data, 
        headers = {
            'authority': 'zefoy.com',
            'accept': '*/*',
            'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
            'cache-control': 'no-cache',
            'content-type': f'multipart/form-data; boundary=----WebKitFormBoundary',
            'cookie': f'PHPSESSID={client.cookies.get("PHPSESSID")}',
            'origin': 'https://zefoy.com',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',}).text.encode())
    
    #print(response)

    if "onsubmit=\"showHideElements('.w1r','.w2r')" in response:
        print(response)
        token, aweme_id = findall(r'name="(.*)" value="(.*)" hidden', response)[0]
        print(fmt(f'sending to: {aweme_id} | key_2: {token}'))

        sleep(3); send(client, token, aweme_id)
        
    else:
        timer = findall(r'ltm=(\d*);', response)[0]
        if int(timer) == 0:
            return

        print(fmt(f'time to sleep: {timer}   '),  end="\r")

        start = time()
        while time() < start + int(timer):

            print(fmt(f'time to sleep: {round((start + int(timer)) - time())}   '),  end="\r")
            sleep(1)
        
        print(fmt(f'sending views...                '),  end="\r")

tiktok_url = 'https://www.tiktok.com/@minniehouse16/video/7214847085642812714' #input('tiktok url: ')
client     = get_client()
key_1      = solve_captcha(client)

if not key_1:
    print(fmt('Failed to solve captcha (zefoy may have blocked you)'))
    exit()

while True:
    search_link(client, key_1, tiktok_url)
    sleep(5)
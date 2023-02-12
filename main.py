from tls_client     import Session
from re             import findall
from PIL            import Image
from io             import BytesIO
from requests       import get
from urllib.parse   import unquote
from base64         import b64decode
from random         import choices
from string         import ascii_letters
from time           import sleep, time


class Client:
    def session() -> Session:
        return Session(client_identifier='chrome_108')
    
    def headers(extra: dict = {}) -> dict:
        return {
            **extra,
            "host"              : "zefoy.com",
            "connection"        : "keep-alive",
            "sec-ch-ua"         : "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "accept"            : "*/*",
            "x-requested-with"  : "XMLHttpRequest",
            "sec-ch-ua-mobile"  : "?0",
            "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "origin"            : "https://zefoy.com",
            "sec-fetch-site"    : "same-origin",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-dest"    : "empty",
            "accept-encoding"   : "gzip, deflate, br",
            "accept-language"   : "en-US,en;q=0.9",
        }

class Captcha:
    def __init__(this, client: Session) -> None:
        this.client = client
    
    def solve(this) -> None:
        try:
            html           = str(this.client.get('https://zefoy.com', headers = Client.headers()).text).replace('&amp;', '&')
            captcha_token  = findall(r'<input type="hidden" name="(.*)">', html)[0]; print('captcha_token:', captcha_token)
            captcha_url    = findall(r'img src="([^"]*)"', html)[0]; print('captcha_url:', captcha_url)
            
            captcha_image  = get('https://zefoy.com' + captcha_url, headers = Client.headers(), cookies=this.client.cookies.get_dict()).content;
            image          = Image.open(BytesIO(captcha_image));image.show()
            
            captcha_answer = input('solve captcha: ')
            
            response = this.client.post('https://zefoy.com', headers = Client.headers({"content-type": "application/x-www-form-urlencoded"}), data = {
                    "captcha_secure": captcha_answer,
                    captcha_token   : ""
            })
            
            key_1 = findall('(?<=")[a-z0-9]{16}', response.text)[0]; print('key_1:', key_1)
            
            return key_1
            
        except Exception as e:
            print(f'Failed to solve captcha (zefoy may have blocked you) [{e}]')
            return

class Zefoy:
    def __init__(this, client: Session) -> None:
        this.client = client
        this.key = Captcha(client).solve()

    def decode(this, text: str) -> str:
        return b64decode(unquote(text[::-1])).decode()
    
    def send(this, token: str, aweme_id: str) -> None:
        try:
            payload = f"--tekky\r\nContent-Disposition: form-data; name=\"{token}\"\r\n\r\n{aweme_id}\r\n--tekky--\r\n"
            response = this.decode(this.client.post("https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V", 
                data = payload, headers = Client.headers({"content-type": "multipart/form-data; boundary=tekky",})).text.encode())
            
            print(f'views sent to {aweme_id}')
            return 
        except Exception as e:
            print(f'Failed to send views [{e}]')
    
    def search(this, link: str) -> None:
        try:

            payload = f"--tekky\r\nContent-Disposition: form-data; name=\"{this.key}\"\r\n\r\n{link}\r\n--tekky--\r\n"
            response = this.decode(this.client.post("https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V", 
                data=payload, headers=Client.headers({"content-type": "multipart/form-data; boundary=tekky",})).text.encode())
            
            if 'comviews()' in response:
                token, aweme_id = findall(r'name="(.*)" value="(.*)" hidden', response)[0]
                print('key_2:', token)
                print('aweme_id:', aweme_id)
                
                this.send(token, aweme_id)
                
            else:

                timer = findall(r'ltm=(\d*);', response)[0]
                if int(timer) == 0:
                    return

                print(f'time to sleep: {timer}   ',  end="\r")

                start = time()
                while time() < start + int(timer):

                    print(f'time to sleep: {round((start + int(timer)) - time())}   ',  end="\r")
                    sleep(1)
                    
                print(f'sending views...                ',  end="\r")

        except Exception as e:
            print(f'Failed to search link [{e}]')
            return
    
    def mainloop(this) -> None:
        while True:
            this.search('https://www.tiktok.com/@lce_byl/video/7198946663266848005')
            sleep(3)

if __name__ == '__main__':
    client = Client.session()
    zefoy  = Zefoy(client).mainloop()

    
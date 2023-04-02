import requests
from base64 import b64decode
from urllib.parse import unquote


def decode(text: str) -> str:
    return b64decode(unquote(text[::-1])).decode()

headers = {
    'authority': 'zefoy.com',
    'accept': '*/*',
    'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
    'cache-control': 'no-cache',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryYiMOiX9dQWSzAP56',
    'cookie': 'PHPSESSID=hgtluqbalapehouof3csaoeoj3',
    'origin': 'https://zefoy.com',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = '------WebKitFormBoundaryYiMOiX9dQWSzAP56\r\nContent-Disposition: form-data; name="65392ccd6"\r\n\r\nhttps://www.tiktok.com/@minniehouse16/video/7214847085642812714\r\n------WebKitFormBoundaryYiMOiX9dQWSzAP56--\r\n'

response = requests.post('https://zefoy.com/c2VuZF9mb2xsb3dlcnNfdGlrdG9L', headers=headers, data=data)
print(decode(response.content))
import requests

cookies = {
    'cf_clearance': '6foos05oPCJDGI6XLT6Bjln_TrQCC9g5BO4X5K6GGUI-1669664509-0-150',
    'PHPSESSID': 's0if6k71l7382ft9epuhk96rt1',
}

headers = {
    'authority': 'zefoy.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.8',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary',
    'origin': 'https://zefoy.com',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = '------WebKitFormBoundary\r\nContent-Disposition: form-data; name="23f2f98c2e051786"\r\n\r\nhttps://www.tiktok.com/@fefepixart/video/7106016809131805958?is_copy_url=1&is_from_webapp=v1&item_id=7106016809131805958\r\n------WebKitFormBoundary--\r\n'

response = requests.post('https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V', cookies=cookies, headers=headers, data=data)
print(response.content)

from test import __decrypt__
print(__decrypt__(response.content))
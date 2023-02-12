from tls_client import Session
client = Session(client_identifier='chrome_108')
client.cookies.update({
    'PHPSESSID': '2dpfbcu155tiavt6rhqbjev8c6'
})

key_1 = '231c5e61f565cbf9'
link  = 'https://www.tiktok.com/@lce_byl/video/7198946663266848005'



payload = f"------WebKitFormBoundary\r\nContent-Disposition: form-data; name=\"{key_1}\"\r\n\r\n{link}\r\n------WebKitFormBoundary--\r\n"

response = client.post("https://zefoy.com/c2VuZC9mb2xeb3dlcnNfdGlrdG9V", data=payload, headers={
    "host": "zefoy.com",
    "connection": "keep-alive",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundary",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "origin": "https://zefoy.com",
    # "cookie": "PHPSESSID=2dpfbcu155tiavt6rhqbjev8c6"
})

print(response.text)
<h2 align="center">SERVER GOT TERMED JOIN NEW ONE <a href="https://discord.gg/fs6V94d8">https://discord.gg/xtwich</a></h2>

<p align="center"> 
<img src="https://user-images.githubusercontent.com/98614666/178567469-654df0d3-7d5a-4ec2-a5d8-53e76001e2ad.png"></img>
</p>

<p align="center">
<del>100 stars = captcha solver</del>
</p><p align="center">
170 stars = open source solver
</p><p align="center">
200 stars = viewbot using freer api (2x faster)
</p><p align="center">
500 stars = unpatched viewbot using real tiktok api
</p>


<!--

<p align="center"> 
<img src="https://global.tiktokworld21.com/images/TT_Logo.png"></img>
</p>

-->

<p align="center"> 
<img src="https://cdn.discordapp.com/attachments/979095432682676264/996481048605106186/unknown.png"></img>
</p>
<p align="center">
  PLEASE REPORT BUGS OR IDEAS TO: tekky#1337 / .gg/onlp
</p>

How to run:
```
  1. Verify that you have pip and python installed => https://www.youtube.com/watch?v=dYfKJMPNMDw
  2. Run this command in cmd: pip install requests bs4 cursor pystyle pillow
  3. run the python file by double clicking on it or type: python viewbot.py
```

Advantages:
```
  1.  fast, easy
  2.  lightweight
  3.  Has dynamic views count running on TikTok API
  4.  mobile users can run it
```
To come:
```
  1. Proxy support
  2. Youtube Tutorial and better Documentation
  3. Bot using freer api so 2x faster (freer api is gay)
```
Captcha OCR Solver:
```python
import requests, json

with open("captcha.png", "rb") as _:
    image_bytes = _.read()

req = requests.post(
    url = "https://api.xtekky.com/ocr",
    json = {
        "image": base64.b64encode(image_bytes).decode()
    }
)
print(json.dumps(req.json, indent=4))
``` 

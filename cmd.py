#AUTHOR: Efe Akaröz
#DATE : 6TH AGUST 2022
'''
Personal note:
Hello I wanted to develop a CLI for this software becase i liked the script so much and it is much better than i expected before i download. 
'''
import json 
from colorama import Fore, Back, Style

print(Fore.LIGHTMAGENTA_EX,"TIKTOK VIEWBOT",Fore.RESET," by"+Fore.CYAN," Tekky#1337",Fore.RESET)
from viewbot import Main
videourl = input("? | Enter a video URL:")
try:  
    videoid = videourl.split("video/")[1].split("?")[0]
    print(Fore.GREEN,"INFO ",Fore.RESET,"| Video ID: {}".format(videoid))
except:
    print(Fore.RED,"ERROR",Fore.RESET, "| URL given is not valid!")
    exit()

jsonfile = json.loads(open("config.json","r").read())
jsonfile["videos"] = [videoid]
writerjson = open("config.json","w")
writerjson.write(json.dumps(jsonfile,indent=4)+"\n")
print(Fore.GREEN,"INFO",Fore.RESET," | Starting script")
if __name__ == "__main__":
    Main().main()


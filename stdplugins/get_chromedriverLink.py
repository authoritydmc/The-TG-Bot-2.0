import requests
import re
from difflib import SequenceMatcher
import sys
import subprocess
import os
url="https://chromedriver.chromium.org/downloads"
pat=r"https://chromedriver.storage.googleapis.com/index.html[\w?=.]+"

def getResponse(version_needed):
    response=requests.get(url)
    # print("Getting for",version_needed)
    links=re.findall(pat,response.text)
    bestlink=""
    ratiobest=0

    for link in links:
        ratio=SequenceMatcher(a=version_needed,b=link).ratio()
        # print("current rat ",ratio)
        if ratio>ratiobest:
            ratiobest=ratio
            bestlink=link
    return bestlink

def run():
    try:
        zz=subprocess.run(['google-chrome', '--version'],stdout=subprocess.PIPE)
        version=re.findall(r'[\d.]+',str(zz.stdout))
        print("Current Chrome Version->",version)
        link=getResponse(version[0])
        print("Best Available link->",link)

        version_available=re.findall(r'\d[\d.]+',link)[0]

        # print(version_available)

        url1="https://chromedriver.storage.googleapis.com/"
        url2="/chromedriver_linux64.zip"
        driver_url=url1+version_available+url2

        print("Formed Link->",driver_url)
        cmdlist=[]
        cmdlist.append("wget "+driver_url)

        cmdlist.append("unzip -o chromedriver_linux64.zip -d /app/.chromedriver/bin/")

        cmdlist.append("unzip -o chromedriver_linux64.zip ")

        cmdlist.append("rm chrome*.zip*")


        for cmd in cmdlist:
            print("Executing ",cmd)
            os.system(cmd)
        return "Successfully Done"
    except Exception as e:
        print ("Error ",e)
        return str(e)
#commands
# unzip -o chromedriver_linux64.zip -d /app/.chromedriver/bin/
# unzip -o chromedriver_linux64.zip 

# rm chrome*.zip*
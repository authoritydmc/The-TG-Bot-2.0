from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import  SYNTAX, MODULE_LIST
import requests
import asyncio
from bs4 import  BeautifulSoup
import random
import os
MODULE_LIST.append("fb (downloads fb videos)")

def progress(current, total):

    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@borg.on(admin_cmd(pattern="fb ?(.*)"))
async def _(event):
    url = event.pattern_match.group(1)
    if not url:
    	abe = await event.get_reply_message()
    	url = abe.text

    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    vurl = soup.find("meta",  property="og:video:url")
    vtitle=soup.find("meta",property="og:title")
    if vurl:
        video_link=vurl["content"]
        await event.edit("`Preparing to download `"+vtitle["content"])
        data=requests.get(video_link)
        f=open(f"temp_fb_down_{random.randint(1,100)}.mp4","wb")
        f.write(data.content)
        await borg.send_file(
        event.chat_id,
            f.name,
        caption=vtitle["content"],
        progress_callback=progress
    )
        await  event.edit("done sending...")
        os.remove(f.name)
        f.close()

    else:
        await event.edit("Error Can not find any Video Link")


  SYNTAX.update({
    "fb": "\
**Requested Module --> ytv**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.fb <url> [or as a reply to a message to download]```\
\nUsage: Download the Facebook video as in video format\
"
})
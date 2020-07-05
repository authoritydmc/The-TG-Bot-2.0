from uniborg.util import admin_cmd,progress
from sql_helpers.global_variables_sql import  SYNTAX, MODULE_LIST
import requests
import asyncio
from bs4 import  BeautifulSoup
import random
import time
import os
MODULE_LIST.append("fb (downloads fb videos)")



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
        video_title=vtitle["content"]
        await event.edit("`Preparing to download `"+vtitle["content"])
        data=requests.get(video_link)
        f=open(f"temp_fb_down_{random.randint(1,100)}.mp4","wb")
        video_path=f.name
        f.write(data.content)
        mone= await event.edit(f"Uploading file {video_title}")
        c_time = time.time()
        await borg.send_file(
        event.chat_id,
            video_path,
        caption=video_title,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, f"Uploading file {video_title}"))
    )
        await  event.edit("done sending...")
        f.close()
        os.remove(video_path)
        await event.delete()

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
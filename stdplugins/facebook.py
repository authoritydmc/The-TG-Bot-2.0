from uniborg.util import admin_cmd,progress,humanbytes
from sql_helpers.global_variables_sql import  SYNTAX, MODULE_LIST
import requests
import asyncio
from bs4 import  BeautifulSoup
import random
import time
import html
import math
import os
MODULE_LIST.append("fb (downloads fb videos)")


async def download(event,url, filename):
    filepath=""
    with open(filename, 'wb') as f:
        filepath=f.name
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')
        await  event.edit("Downloading "+filename)

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                percentage=downloaded*100/total
                f.write(data)
                done = int(50*downloaded/total)
                progress_str = "[{0}{1}]\nPercent: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

                await event.edit("Downloading {} \n**Progress**\n{}\n **Size: **{} of {}".format(
                        filename,
                   progress_str,
                   humanbytes(downloaded),
                  humanbytes( total)
                ))
    return filepath



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
    description=soup.find("meta",property="twitter:description")

    if vurl:
        video_link=vurl["content"]
        video_title=html.unescape(vtitle["content"])
        video_description=html.unescape(description["content"]) if description else video_title
        mone= await event.edit("`Preparing to download `"+video_description)
        video_path= await download(mone,video_link,f"{video_title}.mp4")

        # data=requests.get(video_link)
        # f=open(,"wb")
        # video_path=f.name
        # f.write(data.content)


        await event.edit(f"Uploading file {video_title}")
        c_time = time.time()
        await borg.send_file(
        event.chat_id,
            video_path,
        caption=video_description,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, f"Uploading file {video_title}"))
    )
        await  event.edit("done sending...")
        os.remove(video_path)
        await event.delete()

    else:
        await event.edit("Error Can not find any Video Link")


SYNTAX.update({
    "fb": "\
**Requested Module --> fb**\
\n\n**Detailed usage of fuction(s):**\
\n\n```.fb <url> [or as a reply to a message to download]```\
\nUsage: Download the Facebook video as in video format\
"
})
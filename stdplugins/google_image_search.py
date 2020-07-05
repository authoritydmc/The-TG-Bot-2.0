from uniborg.util import admin_cmd
from sql_helpers.global_variables_sql import  SYNTAX, MODULE_LIST
import asyncio
from selenium import webdriver
import os
import time
import io
import requests
from PIL import Image
import hashlib
from stdplugins import getdriver

MODULE_LIST.append("img (image search query)")

def progress(current, total):
    logger.info("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))
@borg.on(admin_cmd(pattern="img ?(\d)? ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    file_path=[]
    input_str = event.pattern_match.group(2)
    no_img=event.pattern_match.group(1)
    if not no_img:
        no_img=1
    logger.info(f"Downloading {no_img} images")
    await event.edit("searching image of "+input_str)
    try:
        file_path=await search_and_download(event,input_str,number_images=int(no_img))
    except  Exception as e:
        logger.warn(f"error {e}")

        # await event.edit("error "+str(e))
        await asyncio.sleep(3)
        await event.edit("Installing particular driver")
        res=await getdriver.run(event,"exception @ main")
        if "Error" in res:
            await event.edit("Failed to Install driver... meh :(")
        else:
            await event.edit("Installed ...Run Again..")


        return
    await event.edit("Sending File now...")
    if len(file_path)==0:
        logger.info("NO image found or error occured")
        return
    await borg.send_file(
        event.chat_id,
        file_path,
        caption="Images of "+input_str,
        progress_callback=progress
    )
    await event.edit("Complete Sending file for "+input_str)
    for each_file in file_path:
        os.remove(each_file)

    try:
        os.rmdir(str(Config.TMP_DOWNLOAD_DIRECTORY+input_str).replace(" ","_"))
    except :
        logger.error("Can not delete images directory")

    await asyncio.sleep(5)
    await event.delete()
    




def fetch_image_urls(query:str, max_links_to_fetch:int, wd, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,url:str):
    image_content=None
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        return file_path
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
    return None

    
async def search_and_download(event,search_term:str,target_path=Config.TMP_DOWNLOAD_DIRECTORY,number_images=Config.GOOGLE_IMAGES_LIMIT):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))
    files_paths=[]
    chromedriverPath=''
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    wd=None
    try:
       wd= webdriver.Chrome()
       #find at global path
    except:
        try:
            wd= webdriver.Chrome('stdplugins/chromedriver')
            #find in custom path now
        except:
            res=await getdriver.run(event,"search and download ...")
            if "Done" in res:
                await event.edit("Driver successfully loaded ...running webdriver with custom path")
        wd= webdriver.Chrome('stdplugins/chromedriver')
   
    await event.edit("Fetching images for "+search_term)
    res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
    await event.edit("Fetched Images for "+search_term)

    for elem in res:
        paths=persist_image(target_folder,elem)
        if paths!=None:
            files_paths.append(paths)

    wd.close()
    return files_paths
import logging
import os
import wget
import time
import sys
import requests
import csv
import threading


# TranstarArchive Main PY
# author: iRaven (https://iravenhome.net)
# Started 9/6/22.

#version = "2022.9.28"

# Configure logging
logging.basicConfig(filename="TransArchive.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')
log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

#define local vars

arglist = sys.argv[1:]
#time
initcurtime = time.localtime()
# currtime = (f'{initcurtime.tm_hour}-{initcurtime.tm_min}-{initcurtime.tm_sec}')
curtime = time.strftime("%H-%M-%S", initcurtime)
curdate = (f'{initcurtime.tm_year}-{initcurtime.tm_mon}-{initcurtime.tm_mday}')

csvfile = (f"TransArchive_{curdate}.csv") # mainly for debugging but to show status codes of requests for feeds
csvfields = ['time','camera_id', 'status'] # ^

# very important var: where we get everything
cctvurl = (f'https://www.houstontranstar.org/snapshots/cctv/') # Last updated Sep-6-2022
# very important var: list of valid camera feeds generated by devs (likely included and updated in repo)
vftxt = open("valid_feed_list.txt", "r")
vfdata = vftxt.read()
vfeeds = vfdata.split("\n")
vftxt.close()
# TODO: very important (future) var: custom paths
# TODO: archfolder = "archive/"


######## Core functions
# initialize folder
def initFolder(startmode):
    if startmode == "script":
        log.info(f'TranstarArchive was likely started non-standalone with a script or from a command line')
    else:
        log.info(f'TranstarArchive was started')

    if not os.path.exists("archive/"):
        log.info("archive folder doesn't exist. creating it")
        os.makedirs("archive/")
    elif not os.path.exists(f"archive/{curdate}/"):
        log.warning("archive folder for todays date doesn't exist (expected LOL), creating it")
        os.makedirs(f"archive/{curdate}")
    elif not os.path.exists(f"TransstarArchive_{curdate}.csv"):
        log.warning("csv file doesn't exist. creating it for today")
        with open(csvfile, 'a') as listfile:
            csvwrite = csv.writer(listfile)
            csvwrite.writerow(csvfields)
    else:
        log.info("archive download folder exists. we're jud")

# image downloader
def imageDownload(url):
    validcount=0
    invalidfeeds=[]
    log.info(f"Beginning to archive images at {curtime}")
    for feed in vfeeds:
        rq = requests.get(f'{url}{feed}.jpg')
        if rq.headers['content-type'] == "image/jpeg":
            validcount = validcount + 1
            csvvalid = [curtime,feed,'Success']
            print(f'Valid camera feed is being archived: {feed}\n')
            log.info(f'Valid camera feed is being archived: {feed}')
            # wget.download(rq.url,f'archive/{curdate}/{feed}_{curtime}.jpg')
            # new method - using requests module only (10.20.22)
            open(f'archive/{curdate}/{feed}_{curtime}.jpg', 'wb').write(rq.content) # ^
            with open(csvfile, 'a') as listfile:
                csvwrite = csv.writer(listfile)
                csvwrite.writerow(csvvalid)
        else:
            log.error(f"Invalid feed was not archived: {feed}")
            invalidfeeds.append(feed)
        
    log.info(f'Archive at {curtime} finished successfully, {validcount} feeds were archived in this cycle')
    # with open("invalid_feeds_log.txt", 'a') as invlog:
    #     for vals in invlog:
    #         invlog.write(f'invalid feeds found at archive {curdate} at {curtime}:\n{vals}\n#### END END END ####\n either transstar is having issues or has reconfigured feed numbers, open an issue in the repo: https://github.com/iraven4522/TranstarArchive\n')

# loops the download function every like 3 or so mins (may not work?)
def imgDownloadLoop(secs):
    log.info(f'delay loop was called for {secs}, starting now')
    threading.Timer(f'{secs}.0', imgDownloadLoop).start()

# main menu
def MainMenu():
    log.info(f'main menu started')
    print("Welcome to TranstarArchive, an application which lets you archive and keep store of Houston Transtar traffic camera feeds")
    print("Normally HT doesn't archive these via video, however this app lets you have a locally stored archive")
    print("Developed by iRaven. https://iravenhome.net / https://github.com/iRaven4522 (ponies are cyoot :3)")
    menuin = input("What do you want to do? archive/exit ")
    if menuin == "archive":
        log.info("User chose archive")
        print("Start Archive")
        print("This will start archiving continuously until the program is closed with Ctrl+C or closing it")
        print(f'You\'re about to run an automated image download on a website that may take a few minutes, depending on server reliability and bandwidth')
        menuin1 = input("If you want to continue please type the phrase \"startrans\" (without quotes) or type no: ")
        if menuin1 == "startrans":
            imageDownload(cctvurl)
            # log.info("returned to menu for delay")
            # imgDownloadLoop(195)
        else:
            exit()
    else:
        exit()

# Run the shit (finally) -- phased out due to arguments
# initFolder() # check folder and csv file first (send log start message)
# MainMenu()

# Arguments
for arg in arglist:
    # print(arglist)
    if arg in ("-archive"):
        # print("Archive was passed") # debugging
        initFolder("script")
        imageDownload(cctvurl)
    elif arg in ("-testarg"): # debugging, left to test arguments
        print("test arg was passed")
        log.debug("Test arg was passed -- not running")
    else: # unrecognized arguments are passed (which is oki)
        # log.debug("no args were passed!")
        # log.debug("unrecognized args were passed!")
        initFolder("normal")
        MainMenu()

# noticed an issue where this doesn't run standalone anymore. maybe this will fix it. idk
if len(arglist) == 0:
    # log.debug("no args were passed!")
    initFolder("noarg")
    MainMenu()
    # 09/28/22- ok this will semi work for now. if any arg other than the ones defined above are passed it'll ignore them and run like none were passed

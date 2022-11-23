import imageio
import os
import sys
import logging
import time

# TranstarArchive Image GIF Combine PY
# author: iRaven (https://iravenhome.net)
# Started 11/22/22.

# version="2022.11.22"

# Configure logging
logging.basicConfig(filename="TranstarArchive_gifCombine.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')
log = logging.getLogger()
# log.setLevel(logging.DEBUG) # use this for debugging
log.setLevel(logging.INFO) # use this for production

arglist = sys.argv[1:]

#time -- if this will ever be used? logging takes care of this
initcurtime = time.localtime()
curtime = time.strftime("%H-%M-%S", initcurtime)
curdate = (f'{initcurtime.tm_year}-{initcurtime.tm_mon}-{initcurtime.tm_mday}')

global imagespath
global dateinput

# valid feeds list to iiteriate thru
# TODO: make this user supplied for older folders maybe
vftxt = open("valid_feed_list.txt", "r")
vfdata = vftxt.read()
vfeeds = vfdata.split("\n")
vftxt.close()

def initgifFolder(path, date): # makes sure gif folder exists for date provided in a certain path
    if not os.path.exists(f'{path}/{date}/gifs'):
        log.warning(f"gifs folder in {path}/{date} does not exist, creating it")
        os.makedirs(f"{path}/{date}/gifs")
    else:
        log.info(f"gifs folder in {path}/{date} exists, ignoring check")


def gifCombine(path, date):
    # images=[]
    initgifFolder(path,date) # make sure gif folder exists for date provided
    joinedpath = os.path.join(path, date)
    # print(joinedpath) # debugging- comment this out on prod !!!
    for feednum in vfeeds:
        images=[] # list of images found to append to output gif image for each feednum (resets with nothing for each feednum)
        imagenames=[]
        for filenames in sorted(os.listdir(joinedpath)): # for each file in provided path dir
            if filenames.startswith(feednum): # if a file starts with the current feednum
                # length check!! (this bit me in the ass)
                if len(filenames.split('_')[0]) == len(feednum):
                    log.info(f"found {filenames} that starts with {feednum}")
                    print(f"found {filenames} that starts with {feednum}")
                    if filenames in imagenames: # fsakdjfjaksldfjklasdfjklakljdsxf holy shit so many checks! see if a file name has already been added to list for gif
                        log.debug(f'found {filenames} already in {feednum} filename list so NOT adding to list AGAIN')
                    else:
                        # log.info("") # not sure what i was doing here
                        imagenames.append(filenames) # append found file names to list for adding to imageio reader appending list
                else:
                    log.debug(f'found {filenames} that starts with {feednum} HOWEVER isn\'t right length')
            else:
                log.debug(f"{filenames} does not start with {feednum}")

        for files in imagenames:
            log.info(f"applying image {files} for {feednum} in {joinedpath}")
            print(f"applying image {files} for {feednum} in {joinedpath}")
            images.append(imageio.imread(f'{joinedpath}/{files}')) # append whatever image found that starts with current feednum to list
            #TODO: this gives a deprecated error about imread because of course it does.

        # log.debug(f"all images found to be saved: \n{images}") -- this generates way too much bullshit
        log.debug(f" all images to be saved in a gif: \n{imagenames}")
        log.info(f"saving {feednum} gif file with all images collected of it on {date}...")
        print(f"saving {feednum} gif file with all images collected of it on {date}...")
        imageio.mimsave(f'{joinedpath}/gifs/{feednum}.gif', images, duration=0.2) # save a gif image for each feednum in date folder provided with .2 secs between each frame
        log.info("gif should be saved and created successfully. moving on to next itieration...")
        print("gif should be saved and created successfully. moving on to next itieration...")
        


def MainMenu():
    log.info("main menu started")
    print("TranstarArchive gifCombine App")
    print("this program will combine any feed images archived by TranstarArchive for a specific date you provide")
    # print(" ")
    print(" ") # line breaks? LOL

    print("first, let's start off with a path where all your images are stored, which must contain specific date folders.")
    print("normally this path is in the folder you ran this script in, /archive.")
    log.debug("prompting user for path selection choice, default or custom")
    menuin1 = input("please type Y if this is correct or N to enter a different folder path: ")
    menuin1 = menuin1.lower()
    if menuin1 == "y":
        imagespath = "./archive"
        log.info("images path was set to default /archive folder")
    elif menuin1 == "n":
        log.debug("user chose to enter a custom path to be scanned")
        menuin2 = input("please type a custom path here for gifCombine to scan: ")
        log.debug(f"user inputted {menuin2}, now checking if this path is actually a thing")
        if os.path.exists(menuin2):
            imagespath = menuin2
            log.info(f"user inputted path {menuin2} EXISTS, going on...")
        else:
            log.error(f"user inputted path {menuin2} DOES NOT EXIST, trying again...")
            print(f"the path you entered ({menuin2} couldn't be found, please try that again!")
            MainMenu() # this feels incredibly chaotic, a function calling itself LOL
            # exit() # ^ if that doesn't work or breaks things tremendously, fuck it
    else:
        exit() # fuck it if that selection wasn't y or n. not sure what to do, i'll improve this later (2022/11/22)
    # TODO: valid_feeds_list file input

    print(" ") # line breaks? LOL
    log.debug("prompting user for date selection choice")
    print("second, you'll need to choose which date do you want to combine gifs for. ")
    log.debug(f"getting dir listing of {imagespath} for date selection")
    print("here is a listing of the directories in the path you provided earlier.")
    print(os.listdir(imagespath))
    menuin3 = input("type in the folder with the date you want gifCombine to run in:  ")
    # TODO: formatting error correction
    dateinput = menuin3 # just declare it here

    print(" ") # line breaks? LOL
    log.debug("prompting user for confirmation")
    log.info(f"final options before confirmation: path={imagespath}, date={dateinput}")
    print(f"before we start, you have chosen your file path as {imagespath} and the date to work through {dateinput}")
    print("this may take a while depending on how many images are to be processed.")
    menuin4 = input("type in \"startrans\" to continue and start processing: ")
    if menuin4 == "startrans":
        # go!
        print("making sure folders are set up...")
        initgifFolder(imagespath, dateinput) # make gifs folder in specced dir
        print("preparing for epic sonic rainboom...")
        print("now starting to gif combine!")
        gifCombine(imagespath, dateinput) # go bitch
        exit() # exit when done
    else:
        exit() # fuck off

# arguments
# TODO: wait fuck that's not really a good idea rn lol

# start program
log.info("TranstarArchive's gifCombine was STARTED!")
MainMenu()
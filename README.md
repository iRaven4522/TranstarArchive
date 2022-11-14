# TranstarArchive
Python application intended to store an archive of live camera feeds from Houston Transtar

## requirements
  python 3.6 or later
  
  the requests and wget Python modules, installed with pip (if others aren't found on your system, they can be easily viewed in the source code c:)

## what does this program do?
  retrives images from live and valid camera image feeds from Houston Transtar. normally these can be viewed on their website [here](https://traffic.houstontranstar.org/cctv/transtar/), or a very very lightweight version (intended for mobile or older devices, that i prefer) can be found [here](http://traffic.houstontranstar.org/mobile/transtar_cctv.aspx), stores them in a folder/local archive on the system you run it on
  
## why?
  i have no idea

## arguments
  by default and with no args provided TranstarArchive will create required folders if necessary and bring you to the main menu. this is useful for archiving once, however below can be more useful if you want to continuously archive.
  
  -archive will start archiving feeds with no extra prompts. use a looping script provided (for windows as of 9/8/22) to continuously loop the process.
  
  -testarg is self explanatory. tests if TranstarArchive will accept arguments

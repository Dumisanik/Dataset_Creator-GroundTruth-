import os, sys
from os.path import basename

print os.getcwd()
rootFolder = os.getcwd() + "\\"
print "RootFolder:", rootFolder
os.chdir(rootFolder)                    #Go to this folder, set as current folder


#Get all filens in the folder

AllFiles = os.listdir(".")

#listdir was sorting images by alpha not not alpha-and-numeric way like Windows
AllFiles.sort(key=os.path.getatime)     ### Sorts by "Date Created time", 
print "AllFiles:\n",AllFiles, "\n"

#Textfile to store all the filenames  \\here its Images
allImages = file("imageList.txt","w")

fileExtention = ""
RecognisedImageTypes = ["jpg","png","bmp","gif","tif"]

#Creates a textfile that stores the names of all the files placed on this script's folder
def storeAllFilenames():
    global allImages 
    fileCount = 0
    if(len(AllFiles)==0):                                               #If there are no files in the curdir
        print "No files in the this dir=%s"%(os.path.abspath("."))
        return

    for each in AllFiles:
        print each
        fileExtention = (each.split(".")[-1]).lower()
        if fileExtention in RecognisedImageTypes:                                          #Increment the new filenumber
            allImages.write(each+"\n")
            fileCount += 1     
    print "Written %d images"%(fileCount)
###############
#Start
storeAllFilenames()
allImages.close()


"""
This App, draws a rectangles by clicking and dragging the mouse over the image's subregion.
So our mouse callback function draws a rectangle to the image.
This specific example will be really helpful in creating and understanding
some interactive applications
like object tracking,image segmentation etc.
"""

import cv2

#Load the XML Dataset creator
from CreateXmlDataSet import CreateXMLTree

#For the Message box and buttons
import ctypes  # An included library with Python install.
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

#For reading files in a directory
import os,sys
from os.path import basename


########################################################


# mouse callback function, Draws a rectangles by dragging the mouse over the image
drawing = False             # true if mouse is pressed
x1,y1 = -1,-1
ImageResolution = [0,0]     #Stores the resulution of the image, checks if ROI is out of bounds
AlternateDrawRec = 1
numOfExtractedROIs = 0
def drawRectangle(event,x,y,flags,param):
    global x1,y1,drawing,AlternateDrawRec
    global XmlDataset
    global ImageResolution, numOfExtractedROIs
    global image, imageCopy
    AlternateDrawRec = 1 - 0                                    #Flip betwen 0 and 1 each time the function is called
    MessageBox = -1;
    ROIarea = 0
    
    b,g,r = (150,175,150)
    if event == cv2.EVENT_LBUTTONDOWN:                          #if you press Mouse left button
        drawing = True
        x1,y1 = x,y                                             #Copy the initial coordinates of the first click

    elif event == cv2.EVENT_MOUSEMOVE:                          #If the mouse is moved
        if drawing == True:                                     #.. and the left button is clicked
            x = x1 + (abs(y-y1) / 2)                            #Ensure rectangle has a constant shape ratio
            if(AlternateDrawRec == 1):
                cv2.rectangle(image,(x1,y1),(x,y),( b,g,r),0,1)
  

    elif event == cv2.EVENT_LBUTTONUP:                          #When you release the Left Mouse button
        drawing = False
        x = x1 + (abs(y-y1) / 2)                                #Ensure rectangle has a constant shape ratio
        cv2.rectangle(image,(x1,y1),(x,y),( b,g,r),1,0)

        ROIarea = abs(x-x1) * abs(y-y1)
       
        
        ###################
        # Add this SubRegion to the currentImage on the XML
        if(y < ImageResolution[0] and x<ImageResolution[1]):

            if(x1 <x and y1<y):
                if( ROIarea > 25): 
                    MessageBox = ctypes.windll.user32.MessageBoxA(0, "Save this ROI to Dataset? \nPress Space (OK)", "Save to Dataset", 1)

                print "MessageBox Feedback", MessageBox   
                if MessageBox == 1 and ROIarea > 25 :
                    print "Saving to Dataset..."
                    print "Start (%d,%d) BottomRight (%d,%d)"%(x1,y1,x,y)
                    
                    #Add this SubRegion to XML
                    XmlDataset.addSubRegion(x1,y1,x,y);
                    XmlDataset.incrementNumSubRegions()

                    ###########################################
                    # Extract and Save this subimage ROI
                    ROI = imageCopy[y1:y,x1:x]        #cv2.rectangle(image, (x1,y1),(x2,y2))
                    #cv2.imshow('ROI',ROI);
                    #cv2.waitKey(1)

                    #Increment counter for filenames
                    numOfExtractedROIs += 1
                    ROIfilename = "ROIS/%d.jpg"%(numOfExtractedROIs)
                    cv2.imwrite(ROIfilename,ROI)
                            
                else:
                    #Reset the last the drawing on the image
                    a =0
            else:
                ctypes.windll.user32.MessageBoxA(0, "Rectangle area is invaling. \nEnsure than x2>x1 and y2>y1", "Warning",MB_OK | ICON_STOP)
        else:
            ctypes.windll.user32.MessageBoxA(0, "ROI Resolution is out of bounds! Try Again?", "Warning", MB_OK |ICON_STOP)

              

########################################################
#Start       

#Get all the images in the currentFolder
#folder = "D:/IR_pics/vid2/100_1"       #enter this directory manually
folder = os.getcwd() + "\\"             #Get the directory where this script is placed
print "", folder
os.chdir(folder)                        #Make this folder the current dir

# Create folder, if not created
AllFiles = os.listdir('.')
if "ROIs" not in AllFiles:
    os.system("mkdir ROIs")





#Read the "imageList" textfile
txtImageList = file("imageList.txt",'r')

numOfImages = 0
ImageListArray = []
for imageName in txtImageList:
    ImageListArray.append(imageName.replace('\n','') );
    numOfImages += 1

if(numOfImages < 1):
    print "No images found in 'imageList.txt' "
    exit(0)


## Choose which types of samples to be stored, Positive or Negative samples
MessageBox = ctypes.windll.user32.MessageBoxA(0, "Positive Samples \t= Yes \nNegative Samples \t= No ", "Choose sample types", MB_YESNO | ICON_INFO)
print "##Positive Or Negative? = ", MessageBox
SampleTypes = ""
if(MessageBox == 6 ):    #if Yes
    SampleTypes = "PositiveSamples"
else:
    SampleTypes = "NegativeSamples"
    


#Create an XML Tree that will store all subregions of the dataset
XmlDataset = CreateXMLTree(SampleTypes,numOfImages)




#Create a named window for the image, assign it to an event function
#Thus we bind this mouse callback function to the OpenCV window 'image'.
cv2.namedWindow('image')
cv2.setMouseCallback('image',drawRectangle)



filename= ""
"""
image = cv2.imread("D:/IR_pics/vid2/100_1/vid1_2_0.png");
filename = ImageListArray[0] 
print folder+"/"+filename

cv2.imshow("image", image);
cv2.waitKey(0)
"""
image = None
imageCopy = None
for i in range(numOfImages):
    filename = ImageListArray[i]               #Load the image
    print folder+"/"+filename
    image = cv2.imread(filename)
    imageCopy = cv2.imread(filename);       #Copy image, for saving ROIs to folder without drawed rectangles
    
    ImageResolution = image.shape[:2]       #Store the resulution of the image, checks if ROI is out of bounds

    if(image != None):                          
        XmlDataset.addImage(filename);       #Add image to the XML tree
        
    while(True):
        cv2.imshow('image',image)
        k = cv2.waitKey(1) #& 0xFF

        if k == 27:                             #If you press the ESC key
            i = numOfImages+1
            break
            
        elif k == 2555904:                      #If you press the RightArrow button                     
            moveToNextImage = True
            print "Moving to Next image"
            break

        elif k == 2424832:
            i =- 1
            print "Moving to Previous image"
            break
      
#Close all OpenCV Windows
cv2.destroyAllWindows()

#Write XML to file
MessageBox = ctypes.windll.user32.MessageBoxA(0, "Save XML", "Save XML to file?", 1)
if(MessageBox == 1):
    xmlFile = file(SampleTypes + ".xml","w")       #Open the file
    XmlDataset.tree.write(xmlFile)
    xmlFile.close()

    
#Print the XML
XmlDataset.printMe()

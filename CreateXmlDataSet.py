import lxml
from lxml import etree

import os

""" XML to store all positive samples, in the dataset """
class CreateXMLTree():
    
    def __init__(self,strRootName, numImages):
        #Create xml Tree
        self.tree = etree.ElementTree(etree.Element(strRootName))
        #Create the root
        self.root = self.tree.getroot()
        self.root.set("numImages",str(numImages))
        self.root.set("totalNumOfSubregions",str(0))

        #Current Image
        self.currentImage = None


    #Add image to the xml
    def addImage(self, filename):
        self.currentImage = etree.SubElement(self.root,"image",\
                            filename=filename, numSubRegions=str(0))

    def addSubRegion(self, xStart,yStart,xEnd,yEnd):
        SubRegion = etree.SubElement(self.currentImage,"subregion", \
                    xStart=str(xStart), yStart=str(yStart) ,xEnd=str(xEnd),yEnd=str(yEnd))

    def incrementNumSubRegions(self):
        #Increment the number of subregions for the currentImage
        numSubRegions = int(eval(self.currentImage.get("numSubRegions")))
        numSubRegions += 1
        self.currentImage.set("numSubRegions",str(numSubRegions))

        #Increment the total number of all subregions in the XML
        totalSubregions = int(eval(self.root.get("totalNumOfSubregions")))
        totalSubregions = totalSubregions + 1
        self.root.set("totalNumOfSubregions",str(totalSubregions))         
        
        

        


    ######################
    def printMe(self):
        print etree.tostring(self.root, pretty_print=True)
        
    def writeToFile(self,xmlComplete):   
        myFile = file("xmlComplete.xml","w")
        myFile.write(xmlComplete)
        myFile.close()

"""
#Test this code
MyXml = CreateXMLTree("PositiveSamples",str(3))
MyXml.addImage("im0.png");
MyXml.addSubRegion(1,15,1,10)
MyXml.incrementNumSubRegions()
MyXml.addSubRegion(173,250,144,300)
MyXml.incrementNumSubRegions()

MyXml.addImage("im1.png");
MyXml.addSubRegion(1,10,1,10)
MyXml.incrementNumSubRegions()
MyXml.printMe()
"""

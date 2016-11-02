# Dataset_Creator-GroundTruth-
This tool is used for enhancing the process of collecting training samples from image datasets. cropping multiple regions.   The tool allows you to use mouse-drag controls to crop ROIs and automatically store their image coordinates to a simple XML file for the validation of Ground Truth information once a statistical a statistical learning method or classifier has been trained.



------------------------------------------------------------------------------
Usage:
First Copy the scripts {CreateXmlDataSet.py, Step1_StoreAllFilenames.py, Step2_CropSubRegionsOfRoi.py} 
to the directory of your image dataset.

Step 1: Double click to run "Step1_StoreAllFilenames.py" to store the names of all the images in its folder.

Step 2: Run "Step2_CropSubRegionsOfRoi.py", to open up the app.
 -You will see a pop up to select the type of your samples: "PositiveSamples" or "Negative Samples"

 - This will open the first image, use the mouse to select all the ROIs you would like to save.
 - You do this by clicking at the Top-Left corner of the rectangle bounding your object of interest,
 - hold and drag to the Bottom-Right corner of it.
 NB: You can select as many ROIs you like on the same picture.

 - Once you are done with the current image, press the [Right-Arrow] key on your keyboard to move to the next image.
 NB: You can only iterate to the next images, and cannot move to the previous images.

The app will ask you to confirm saving to the xml once you have iterated through all the images.
You can hold the [Right-Arrow] key to skip through images.

# REquirements and Dependencies
- Python 2.7
- OpenCV for Python
- lxml



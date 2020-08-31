import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None #to remove limit on maximum number of pixels to be processed

#generate 2x2 image from array
def imageFromArray_2x2():
    array = np.zeros([2, 2, 3], dtype=np.uint8) #[row,column,colourchannel] 8-bit colour
    array[0,0]=[215,0,0]
    array[0,1]=[141,117,95]
    array[1,0]=[201,98,223]
    array[1,1]=[165,71,71]
    print(array)
    img = Image.fromarray(array)
    img.save('fourpixel.png')
    return

#generate 2x2 image from array
def arrayFromImage():
    img = Image.open('fourpixel.png')
    print(np.array(img))
    return

#generate larger image from array
def largerImageFromArray():
    array = np.zeros([100, 200, 3], dtype=np.uint8)
    array[:,:100] = [255, 128, 0] #Orange left side
    array[:,100:] = [0, 255, 255] #Cyan right side

    img = Image.fromarray(array)
    img.save('orangecyan.png')
    return

#get image and find number of pixels and channels
def printImageShape(filename):
    img = Image.open(filename)
    array = np.array(img)
    print(array.shape)


#convert to greyscale
def toGreyScale(filename, isTransparent): #isTransparent to be used only with RGBA channel
    img = Image.open(filename)
    array = np.array(img)
    greyArray = np.zeros([array.shape[0],array.shape[1]], dtype=np.uint8) #creating new array, not over-writing
    for i in range(0, array.shape[0]):
        for j in range(0,array.shape[1]):
            if((isTransparent) and (array[i,j,3]==0)):
                greyArray[i,j]=255 #if transparent, make it white
            else:
                greyArray[i,j]=(int)(0.2989*array[i,j,0]+0.5870*array[i,j,1]+0.1140*array[i,j,2])
    img = Image.fromarray(greyArray)
    img.save('grey'+filename)
    return

#convert to sepia
def toSepia(filename):
    img = Image.open(filename)
    array = np.array(img)
    sepiaArray=np.zeros([array.shape[0],array.shape[1],3], dtype=np.uint8) #three channel as sepia is not a standard channel, like greyscale
    for i in range(0, array.shape[0]):
        for j in range(0,array.shape[1]):
            sepiaArray[i,j,0] = min(0.393*array[i,j,0] + 0.769*array[i,j,1] + 0.189*array[i,j,2],255)
            sepiaArray[i,j,1] = min(0.349*array[i,j,0] + 0.686*array[i,j,1] + 0.168*array[i,j,2],255)
            sepiaArray[i,j,2] = min(0.272*array[i,j,0] + 0.534*array[i,j,1] + 0.131*array[i,j,2],255)
    img = Image.fromarray(sepiaArray)
    img.save('sepia'+filename)
    return

#get colour channels
def getColourChannels(filename):
    img = Image.open(filename)
    array = np.array(img)
    redArray=np.zeros([array.shape[0],array.shape[1],3], dtype=np.uint8)
    blueArray=np.zeros([array.shape[0],array.shape[1],3], dtype=np.uint8)
    greenArray=np.zeros([array.shape[0],array.shape[1],3], dtype=np.uint8)
    for i in range(0, array.shape[0]):
        for j in range(0,array.shape[1]):
            redArray[i,j,0] = array[i,j,0] 
            blueArray[i,j,2] = array[i,j,2]
            greenArray[i,j,1] =array[i,j,1]
    img = Image.fromarray(redArray)
    img.save('red-'+filename)
    img = Image.fromarray(blueArray)
    img.save('blue-'+filename)
    img = Image.fromarray(greenArray)
    img.save('green-'+filename)
    return

# 5x5 box blur
def boxBlur_5x5(filename):
    img = Image.open(filename)
    array = np.array(img)
    kernel=np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])
    print(kernel)
    img = Image.open(filename)
    array = np.array(img)
    modifiedImage=np.zeros([array.shape[0],array.shape[1],3], dtype=np.uint8)
    for i in range(2, modifiedImage.shape[0]-2):
        for j in range(2,modifiedImage.shape[1]-2):
            for c in range(0,3):
                sum=0
                for k in range(0,kernel.shape[0]):
                    for l in range(0,kernel.shape[1]):
                        sum=sum+kernel[k,l]*array[i-2+k,j-2+l,c]
                modifiedImage[i,j,c]=sum/25.0
    img = Image.fromarray(modifiedImage)
    img.save('BoxBlurred_5x5'+filename)
    return

# 3x3 gaussian box blur
def gaussianBlur_3x3(filename):
    img = Image.open(filename)
    array = np.array(img)
    kernel=np.array([[0,1,0],[1,4,1],[0,1,0]])
    print(kernel)
    modifiedImage=np.zeros([array.shape[0],array.shape[1],3], dtype=np.uint8)
    for i in range(1, modifiedImage.shape[0]-1):
        for j in range(1,modifiedImage.shape[1]-1):
            for c in range(0,3):
                sum=0
                for k in range(0,kernel.shape[0]):
                    for l in range(0,kernel.shape[1]):
                        sum=sum+kernel[k,l]*array[i-1+k,j-1+l,c]
                modifiedImage[i,j,c]=sum/8.0
    img = Image.fromarray(modifiedImage)
    img.save('GaussianBlurred_3x3'+filename)
    return

# 3x3 edge detection
def edgeDetection_3x3(filename,kernelNumber):
    kernelList=[]
    kernelList.append(np.array([[1,0,-1],[0,0,0],[-1,0,1]]))
    kernelList.append(np.array([[0,1,0],[1,-4,1],[0,1,0]]))
    kernelList.append(np.array([[1,1,1],[1,-8,1],[1,1,1]]))
    img = Image.open(filename)
    array = np.array(img)
    print(kernelList[kernelNumber])
    greyArray = np.zeros([array.shape[0],array.shape[1]], dtype=np.uint8) #creating new array, not over-writing
    for i in range(0, array.shape[0]):
        for j in range(0,array.shape[1]):
            greyArray[i,j]=(int)(0.2989*array[i,j,0]+0.5870*array[i,j,1]+0.1140*array[i,j,2])

    modifiedArray = np.zeros([array.shape[0],array.shape[1]], dtype=np.uint8) #creating new array, not over-writing
    for i in range(1, greyArray.shape[0]-1):
        for j in range(1,greyArray.shape[1]-1):
            sum=0
            for k in range(0,kernelList[kernelNumber].shape[0]):
                for l in range(0,kernelList[kernelNumber].shape[1]):
                    sum=sum+kernelList[kernelNumber][k,l]*greyArray[i-1+k,j-1+l]
            modifiedArray[i,j]=sum
    img = Image.fromarray(modifiedArray)
    img.save('EdgeDetected_3x3_'+str(kernelNumber)+filename)
    return

#FUNCTION CALLS

#imageFromArray_2x2()
#arrayFromImage()
#largerImageFromArray()
#printImageShape("Workshop.png")
#printImageShape("GoogleIO.jpg")
#toGreyScale("GoogleIO.jpg",False)
#toGreyScale("Workshop.png",True)
#toSepia("Workshop.png")
#toSepia("GoogleIO.jpg")
#getColourChannels("GoogleIO.jpg")
#getColourChannels("Workshop.png")
#boxBlur_5x5("Workshop.png")
#boxBlur_5x5("GoogleIO.jpg")
#gaussianBlur_3x3("GoogleIO.jpg")
#gaussianBlur_3x3("Workshop.png")
edgeDetection_3x3("Workshop.png",0)
edgeDetection_3x3("Workshop.png",1)
edgeDetection_3x3("Workshop.png",2)


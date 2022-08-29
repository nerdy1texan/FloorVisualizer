#nerdytexan

import numpy as np
import cv2

# Read image(s)
img = cv2.imread('Resources/yourimagehere.jpg')
origImg = cv2.imread('Resources/imghere.png')
wood = cv2.imread('Resources/yourwoodimagehere.png')
originalImg = img

# Step 1: Get Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 3: Blur image
blur = cv2.medianBlur(gray, 17)

# Step 4: Canny
canny = cv2.Canny(blur, 0, 100)
cv2.imshow("Cannyog", canny)

# Step 1: Get HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsvBlur = cv2.medianBlur(hsv, 17)

# Step 2: Get HSV-Channels
h,s,v = cv2.split(hsv)

# Step 4: Canny
cannyHsv = cv2.Canny(hsvBlur, 0, 170)
cv2.imshow("hsv", cannyHsv)

# Step 5: TODO // Merge both canny Matrices - Linear Blending // Check
dst = cv2.addWeighted(canny, 0.7, cannyHsv, 0.3, 0.0)

# TODO // Check  canny function. Add both  canny functions
# Step 6: Dilate resulting image matrix from step 5
dilation = cv2.dilate(dst,(5,5),iterations = 9)


# Resize dilation image // x+y are reversed  in resize function
resized_image = cv2.resize(dilation, (3026, 4034))

# Step 7: Floodfill
h, w = dilation.shape
mask = np.zeros((h+2, w+2), np.uint8)
floodfill_color = 255,0,0
height, width = dilation.shape[:2]
width+=2
height+=2
# Resize dilation image // x+y are reversed  in resize function
resized_image = cv2.resize(dilation, (width, height))

img = cv2.medianBlur(img, 15)

# FLOODFILL
cv2.floodFill(img, resized_image, (1000, 3000), floodfill_color, loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))

# Step 8:  Take the HSV matrix of your original image and merge the V-channel matrix into this flood-filled image
vChannel = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)
result = cv2.addWeighted(img, 0.5, vChannel, 0.5, 0.0)
# Step 9: Merge with original image
newResult = cv2.addWeighted(img, 0.3, result, 0.7, 0.0)

cv2.imshow("test", newResult)


# ADD TEXTURE
# Create mask after floodfilling
maskAft = cv2.inRange(img, (255,0,0), (255,0,0))
maskAfter = cv2.cvtColor(maskAft, cv2.COLOR_GRAY2BGR)

# Thresholding stuff // TODO // Possibly check later
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(grayImage,100,100,cv2.THRESH_BINARY)


# Texture file // TODO - Perspective transform - Play around later (Not working properly) - Try resizing image after
#  TODO // taking ROI from texture, then stretching image
texture = cv2.imread('Resources/wood4.jpg')
resized_text = cv2.resize(texture, (width-2, height-2))
pts1 = np.float32([[0,0],[3024,0],[0,4032],[3024,4032]])
pts2 = np.float32([[700,0],[2324,0],[0,4032],[3024,4032]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(resized_text,M,(width-2,height-2))
print(maskAfter.shape)
print(resized_text.shape)

bitwise = cv2.bitwise_and(dst, maskAfter)
#bitwise = cv2.bitwise_and(resized_text, maskAfter)

finalResult = cv2.addWeighted(bitwise, 1, originalImg, 0.3, 0.0)

cv2.imshow("New Result", finalResult)
cv2.imshow("bitwise", bitwise)
cv2.imshow("original", originalImg)
cv2.imshow("test", maskAfter)
cv2.waitKey(0)

# TODO // Painted Image - Texture // TODO
# Step 1: Get Grayscale of painted image
resultGray = cv2.cvtColor(newResult, cv2.COLOR_BGR2GRAY)

# Step 3: Blur painted image
resultBlur = cv2.medianBlur(resultGray, 3)

# Step 4: Canny detector on painted image
resultCanny = cv2.Canny(resultBlur, 30, 85)

# Step 1: Get HSV Texture
hsvTexture = cv2.cvtColor(newResult, cv2.COLOR_BGR2HSV)

# Step 2: Get HSV-Channels of painted img
hTexture,sTexture,vTexture = cv2.split(hsvTexture)

# Step  3: Blur painted HSV  img
hBlur = cv2.medianBlur(hsvTexture, 3)

# Step 4: Canny  on HSV painted image
hCanny = cv2.Canny(hBlur, 30, 85)

#  Step 5: Alpha blend both canny images
blended = cv2.addWeighted(hCanny, 0.5, resultCanny, 0.5, 0.0)

# Step 6: Dilate resulting image matrix
dilatedPaint = cv2.dilate(blended, (3,3), mask)

# Resize dilation image // x+y are reversed  in resize function
resized_img = cv2.resize(dilatedPaint, (3026, 4034))

# Step 7: Floodfill // TODO WHAT IS HAPPENING HERE
# h, w = dilatedPaint.shape
# mask2 = np.zeros((h/8, w/8), np.uint8)
# floodfill_color = 255,255,255
# height, width = dilation.shape[:2]
# width+=2
# height+=2

# Resize dilation image // x+y are reversed  in resize function
resized_img = cv2.resize(dilatedPaint, (width, height))
h, w = dilation.shape
wallMask = np.zeros((h, w), np.uint8)
resized_img2 = resized_img
cv2.floodFill(newResult, resized_img, (1500, 2000), floodfill_color, loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))
cv2.floodFill(wallMask, resized_img2, (1500, 2000), floodfill_color, loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))

cv2.imshow("Wallmask", newResult)
cv2.waitKey(0)


# Step 8 // TODO WTF IS HAPPENING HERE
resizedTexture = cv2.resize(texture, (width-2, height-2))
#images = cv2.bitwise_and(wallMask, resizedTexture)
#finalImage = cv2.bitwise_or(img, images)
print(resizedTexture.shape)
print(wallMask.shape)
cv2.waitKey(0)


## // END Texture Steps
a = []
b = []
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.floodFill(origImg, resized_image, (x, y), floodfill_color, loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))
        cv2.imshow("IMAGES", origImg)
        print(x, y)

cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)

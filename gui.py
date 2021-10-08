from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import os
import cv2
import math


from conv import conv


def showimage():
    # showiamge() dispalys the image which is selected by the user on the GUI
    
    global img, img_array, image_og, img_list # Declaring global variables to perform operations in successive manner
    img_list = [] # Stack which stores the images being dispalyed. Used in Undo operation.
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("All Files", "*.*"), ("PNG File", "*.png"), ("JPG File", "*.jpg"))) # Get image from the directory
    img_array = cv2.imread(fln) # Read the image into an array. imag_array will be updated after every operation.
    image_og = img_array # Store image_array into image_og which is the original image selected by the User
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB) # Convert image from BGR to RGB colour space since PIL works with RGB colour space
    img = Image.fromarray(img_rgb) # Convert array to PIL Image object
    img = ImageTk.PhotoImage(img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=img) # Configure the Frame of GUI to dispaly image
    lbl.image = img # Display image on GUI
    img_list.append(img) # Push the displayed image into the img_list stack
    myslider1.set(1) # Set Blurr slider to 1 when new image is selected
    myslider2.set(1) # Set Sharp slider to 1 when new image is selected


def equalize():
    # equalize() performs histogram equalization of the image and displays the result on the GUI
    
    global img_array, img_list # Declaring global variables to perform operations in successive manner
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV) # Convert colour space from BGR to HSV
    img_gray = img_hsv[:,:,2] # Store H layer of image imto 2D array called img_gray
    r, c = img_gray.shape # Store rows of image in r and columns of image in c
    
    # Calculate histogarm of image
    his = np.zeros(256) # histogram array declared and initialised to zero
    for i in range(r): # iterate through all row pixels
        for j in range(c): # iterate through all column pixels
            his[img_gray[i,j]] = his[img_gray[i,j]] + 1 # Increment the img_gray[i,j] value in histogarm by 1
    
    # Calculate cumulative probability of each pixel
    pr = his/(r*c) # Caluculate probability of each pixel value
    cum_pr = np.zeros(256) # Cumulative probability array declared and initialised to zero
    cum_pr[0] = pr[0] # Cumulative probability for intensity=0 will be probability that intensity=0 
    for i in range(1,256): # Iterate over all intensity values
        cum_pr[i] = cum_pr[i-1] + pr[i] # Calculate cumulative probability for all intensity values

    s = np.round(cum_pr * 255) # Calculaye intensity mappings as per cumulative probability
    output_image = np.zeros((r,c)) # output image array declared and initialised to zero
    for i in range(r): # iterate through all row pixels
        for j in range(c): # iterate through all column pixels
            output_image[i,j] = s[img_gray[i,j]] # Update values in output image as per the intensity mappings
    
    eq_image = np.zeros((r,c,3)).astype('uint8') # Equalised image 3D array declared and initialised to zero
    eq_image[:,:,2] = output_image # Set H layer of equalised image as output image
    eq_image[:,:,1] , eq_image[:,:,0] = img_hsv[:,:,1] , img_hsv[:,:,0] # Set S and V of equalised image as S and V of input image
    
    img_array = cv2.cvtColor(eq_image, cv2.COLOR_HSV2BGR) # Convert HSV image to BGR and update img_array
    img_rgb = cv2.cvtColor(eq_image, cv2.COLOR_HSV2RGB) # Convert HSV image to RGB to display on tkinter GUI
    out_img = Image.fromarray(img_rgb) # Convert array to PIL Image object
    out_img = ImageTk.PhotoImage(out_img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=out_img) # Configure the Frame of GUI to dispaly image
    lbl.image = out_img    # Display image on GUI
    img_list.append(out_img) # Push the displayed image into the img_list stack


def gamma():
    # gamma() performs gamma correction on the image using the gamma value given by user and displays it on the GUI
    
    global img_array, img_list # Declaring global variables to perform operations in successive manner
    g = float(gamma_value.get()) # Get value of gamma given by User form the entry widget
    k = 255 / pow(255,g) # Calculate K where s = k * r^g
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV) # Convert colour space from BGR to HSV
    img_gray = img_hsv[:,:,2] # Store H layer of image imto 2D array called img_gray
    r, c = img_gray.shape # Store rows of image in r and columns of image in c
    out_img = np.zeros((r,c)) # output image array declared and initialised to zero
    
    # Compute gamma corrected image
    for i in range(r): # iterate through all row pixels
        for j in range(c): # iterate through all column pixels
            out_img[i,j] = np.round(k * pow(img_gray[i,j],g)) # Calculate gamma corrected intensity values
    
    g_image = np.zeros((r,c,3)).astype('uint8') # Gamma corrected image 3D array declared and initialised to zero
    g_image[:,:,2] = out_img # Set H layer of gamma corrected image as output image
    g_image[:,:,1] , g_image[:,:,0] = img_hsv[:,:,1] , img_hsv[:,:,0] # Set S and V of equalised image as S and V of input image
    
    img_array = cv2.cvtColor(g_image, cv2.COLOR_HSV2BGR) # Convert HSV image to BGR and update img_array
    img_rgb = cv2.cvtColor(g_image, cv2.COLOR_HSV2RGB) # Convert HSV image to RGB to display on tkinter GUI
    out_img = Image.fromarray(img_rgb) # Convert array to PIL Image object
    out_img = ImageTk.PhotoImage(out_img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=out_img) # Configure the Frame of GUI to dispaly image
    lbl.image = out_img    # Display image on GUI
    img_list.append(out_img) # Push the displayed image into the img_list stack
       

def logt():
    # logt() performs log transform on the image when the user clicks the Log Transform button
    
    global img_array, img_list # Declaring global variables to perform operations in successive manner
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV) # Convert colour space from BGR to HSV
    img_gray = img_hsv[:,:,2] # Store H layer of image imto 2D array called img_gray
    r, c = img_gray.shape # Store rows of image in r and columns of image in c
    out_img = np.zeros((r,c)) # output image array declared and initialised to zero
    
    # Compute log transform of the image
    for i in range(r): # iterate through all row pixels
        for j in range(c): # iterate through all column pixels
            out_img[i,j] = np.round(106 * math.log(img_gray[i,j]+1,10)) # Calculate log transform of intensity values

    lt_image = np.zeros((r,c,3)).astype('uint8') # log transformed image 3D array declared and initialised to zero
    lt_image[:,:,2] = out_img # Set H layer of log transformed image as output image
    lt_image[:,:,1] , lt_image[:,:,0] = img_hsv[:,:,1] , img_hsv[:,:,0] # Set S and V of equalised image as S and V of input image
   
    img_array = cv2.cvtColor(lt_image, cv2.COLOR_HSV2BGR) # Convert HSV image to BGR and update img_array
    img_rgb = cv2.cvtColor(lt_image, cv2.COLOR_HSV2RGB) # Convert HSV image to RGB to display on tkinter GUI
    out_img = Image.fromarray(img_rgb) # Convert array to PIL Image object
    out_img = ImageTk.PhotoImage(out_img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=out_img) # Configure the Frame of GUI to dispaly image
    lbl.image = out_img    # Display image on GUI
    img_list.append(out_img) # Push the displayed image into the img_list stack     
    
    
def blurr(value):
    # blurr() performs image blurring as per the value of the blur slider and displays it on the GUI
    
    global img_array, img_list # Declaring global variables to perform operations in successive manner
    img_hsv = cv2.cvtColor(image_og, cv2.COLOR_BGR2HSV) # Convert colour space from BGR to HSV
    img_gray = img_hsv[:,:,2] # Store H layer of image imto 2D array called img_gray
    r, c = img_gray.shape # Store rows of image in r and columns of image in c
    
    # Compute 2D convolutions between image and blurring filter
    f = (int(value) * 2) - 1 # Compute filter size from the value of blurr slider
    fil = np.ones((f,f))/(f *f) # Compute averaging filter from filter size f
    out_img = conv(img_gray,f,fil) # Perform 2D convolution on image with the filter
    
    bl_image = np.zeros((r,c,3)).astype('uint8') # blur image 3D array declared and initialised to zero
    bl_image[:,:,2] = out_img # Set H layer of blurred image as output image
    bl_image[:,:,0] , bl_image[:,:,1] = img_hsv[:,:,0] , img_hsv[:,:,1] # Set S and V of equalised image as S and V of input image
    
    img_array = cv2.cvtColor(bl_image, cv2.COLOR_HSV2BGR) # Convert HSV image to BGR and update img_array
    img_rgb = cv2.cvtColor(bl_image, cv2.COLOR_HSV2RGB) # Convert HSV image to RGB to display on tkinter GUI
    out_img = Image.fromarray(img_rgb) # Convert array to PIL Image object
    out_img = ImageTk.PhotoImage(out_img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=out_img) # Configure the Frame of GUI to dispaly image
    lbl.image = out_img # Display image on GUI
    img_list.append(out_img) # Push the displayed image into the img_list stack


def sharp(value):
    # sharp() performs image sharpening as per the value of the sharp slider and displays it on the GUI
    
    global img_array, image_og, img_list # Declaring global variables to perform operations in successive manner
    img_hsv = cv2.cvtColor(image_og, cv2.COLOR_BGR2HSV) # Convert colour space from BGR to HSV
    img_gray = img_hsv[:,:,2] # Store H layer of image imto 2D array called img_gray
    
    # Detect Edges in the image
    fil1 = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]) # Sobel filter to detect vertical edge
    fil2 = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) # Sobel filter to detect horizontal edge
    new_img1 = conv(img_gray,3, fil1) # Perform 2D convolution on image with the filter
    new_img2 = conv(img_gray,3, fil2) # Perform 2D convolution on image with the filter
    r, c = new_img1.shape # Store rows of image in r and columns of image in c
    i1 = np.square(new_img1/255) # Normalize the image and squre it's intensity values
    i2 = np.square(new_img2/255) # Normalize the image and squre it's intensity values
    i = i1 +i2 # Sum of two squared images
    g = np.sqrt(i) # Compute square root of intensity values
    g = np.round(g*255) # Multiply and round off to get actual intensity values
    
    # Compute Sharpened Image
    a = (float(value)-1)/20 # Compute aplha using the value of sharp slider
    g = img_gray + a * g # Multiply edge image g by alpha and add it to H value of image to get H layer of final image
    # Performing thresholding of H layer of final image
    for i in range(r): # iterate through all row pixels
        for j in range(c):# iterate through all column pixels
            if g[i,j]>255: # Check if intensity values are greater than 255
                g[i,j] = 255 # Threshold higher values to 255
    g = np.round(g) # Round off to get H layer of final sharpened image

    sh_image = np.zeros((r,c,3)).astype('uint8') # sharpened image 3D array declared and initialised to zero
    sh_image[:,:,2] = g # Set H layer of sharpened image as output image
    sh_image[:,:,0] , sh_image[:,:,1] = img_hsv[:,:,0] , img_hsv[:,:,1] # Set S and V of equalised image as S and V of input image
    
    img_array = cv2.cvtColor(sh_image, cv2.COLOR_HSV2BGR) # Convert HSV image to BGR and update img_array
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB) # Convert BGR image to RGB to display on tkinter GUI
    out_img = Image.fromarray(img_rgb) # Convert array to PIL Image object
    out_img = ImageTk.PhotoImage(out_img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=out_img) # Configure the Frame of GUI to dispaly image
    lbl.image = out_img # Display image on GUI
    img_list.append(out_img) # Push the displayed image into the img_list stack


def edge():
    # edge() performs edge detection on the image and displays it on the GUI
    
    global img_array, img_list # Declaring global variables to perform operations in successive manner
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV) # Convert colour space from BGR to HSV
    img_gray = img_hsv[:,:,2] # Store H layer of image imto 2D array called img_gray
    
    # Detect Edges in the image
    fil1 = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]) # Sobel filter to detect vertical edge
    fil2 = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) # Sobel filter to detect horizontal edge
    new_img1 = conv(img_gray,3, fil1) # Perform 2D convolution on image with the filter
    new_img2 = conv(img_gray,3, fil2) # Perform 2D convolution on image with the filter
    r, c = new_img1.shape # Store rows of image in r and columns of image in c
    i1 = np.square(new_img1/255) # Normalize the image and squre it's intensity values
    i2 = np.square(new_img2/255) # Normalize the image and squre it's intensity values
    i = i1 +i2 # Sum of two squared images
    g = np.sqrt(i) # Compute square root of intensity values
    for i in range(r): # iterate through all row pixels
        for j in range(c): # iterate through all column pixels
            if g[i,j]>1: # Check if intensity values are greater than 1
                g[i,j] = 1 # Threshold higher values to 1
    
    g = np.round(g*255) # Multiply and round off to get actual intensity values
    img_array = g # Update img_array as output image
    out_img = Image.fromarray(g) # Convert array to PIL Image object
    out_img = ImageTk.PhotoImage(out_img) # Convert image to Tk Photoimage object to dispaly on tkinter GUI
    lbl.configure(image=out_img) # Configure the Frame of GUI to dispaly image
    lbl.image = out_img  # Display image on GUI
    img_list.append(out_img) # Push the displayed image into the img_list stack


def Undo():
    # Undo() reverses the last operation performed
    
    global img_list, img_array # Declaring global variables to perform operations in successive manner
    img_list.pop() # POP the current image displayed on the GUI
    lbl.configure(image=img_list[len(img_list)-1]) # Configure the Frame of GUI to dispaly the last image
    lbl.image = img_list[len(img_list)-1] # Display image on GUI
    


def UndoAll():
    # UndoAll() reverses all operations and displays original image on GUI
    
    global img, img_array, image_og, img_list# Declaring global variables to perform operations in successive manner
    lbl.configure(image=img) # Configure the Frame of GUI to dispaly the original image
    lbl.image = img # Display image on GUI
    img_array = image_og # Update image array to origianl image
    img_list=[] # Clear image list


def save():
    # save() saves the image with the name given by user input
    
    global img_array # Declaring global variables to perform operations in successive manner
    cv2.imwrite(save_value.get(), img_array) # Save the image with the name given by the user in entry widget
    
    
if __name__ == "__main__":

    root = Tk() # Create a blank window
    
    frm = Frame(root) # Invisible container in the window ie root, will be used to put buttons
    frm.pack(side=RIGHT, padx=15, pady=15) # Put the frame on the right side of the window
    
    frm1 = Frame(root) # Invisible container in the window ie root, will be used to put buttons
    frm1.pack(side=RIGHT, padx=15, pady=15) # Put the frame on the right side of the window
    
    lbl = Label(frm1) # Put a label on the blank window
    lbl.pack()# Place the label in the window at whatever place is available
    
    btn1 = Button(frm, text="Select Image", command=showimage) #Creates a button in the frame
    btn1.pack(pady=5) #Place it in the frame
    
    
    btn2 = Button(frm, text="Equalize", command=equalize)#Creates a button in the frame
    btn2.pack(pady=20) #Place it in the frame
    
    
    gamma_value = Entry(frm, width= 5) #Create an entry widget which takes value of gamma as input
    gamma_value.pack() #Place it in the frame
    
    btn3 = Button(frm, text="Gamma Correction", command=gamma) #Creates a button in the frame
    btn3.pack(pady=5) #Place it in the frame
    
    
    btn4 = Button(frm, text="Log Transform", command=logt) #Creates a button in the frame
    btn4.pack(pady=20) #Place it in the frame
    
    
    Label(frm, text="Blurr").pack() #Label of blurr slider which makes the image blurr
    myslider1 = Scale(frm, from_=1, to=5, orient=HORIZONTAL, command=blurr) #Create a slider in the frame
    myslider1.pack() #Place it in the frame
    
    btn5 = Button(frm, text="Edge Detect", command=edge) #Creates a button in the frame
    btn5.pack(pady=20) #Place it in the frame
    
    
    Label(frm, text="Sharp").pack() #Label of Sharp slider which increases sharpness
    myslider2 = Scale(frm, from_=1, to=5, orient=HORIZONTAL, command=sharp) #Create a slider in the frame
    myslider2.pack() #Place it in the frame
    
    
    btnUndo = Button(frm, text="Undo", command=Undo) #Creates a button in the frame
    btnUndo.pack(pady=5) #Place it in the frame
    
    btnUndoA = Button(frm, text="Undo All", command=UndoAll) #Creates a button in the frame
    btnUndoA.pack(pady=20) #Place it in the frame
    
    save_value = Entry(frm, width= 10) #Create an entry widget in the frame which takes name of file ro be saved
    save_value.pack() #Place it in the frame
    
    btn0 = Button(frm, text="Save", bg="blue", command=save) #Creates a button in the frame
    btn0.pack(pady=5) #Place it in the frame
    
    
    root.title("Image Processing GUI") # Title of GUI
    root.mainloop() # Puts the window in a loop so it is continuosly displayed untill you press the exit button

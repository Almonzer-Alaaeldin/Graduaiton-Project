#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author ahmed hessuin
'''
import cv2

#=============================#
def preprocessing_image_to_black_and_white(im,min_area=50,hand_written=False):
    '''
    description : preprocess  input image to be black and white, and clear any noise from has area less than the
    min_area, using mean adaptive threshold
    :param im: the image to preprocess , np.array
    :param min_area: min area of object to remain in the image, int
    :return: preprocessed image black and white, np.array
    '''
    mode=11
    thresh_rect_size=1
    train_image_size_x=1600
    train_image_size_y=1200
    im=cv2.resize(im,(train_image_size_x,train_image_size_y))
    output_color=255
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # change the image to gray scale
    ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(gray,output_color,cv2.ADAPTIVE_THRESH_MEAN_C,\
    #         cv2.THRESH_BINARY_INV,mode,thresh_rect_size) # adaptive thresh mean method to get the image in black and white only

    out_image =thresh
    #==================== use hand written  =================#
    if hand_written:
        out_image=preprocessing_handwritten(im,min_area)


    return out_image
def start_pre(image,condition):

    out=preprocessing_image_to_black_and_white(image,hand_written=condition)
    out=cv2.cvtColor(out,cv2.COLOR_GRAY2BGR)
    return out
#=============================#
def preprocessing_handwritten(im,min_area=50):
    '''
    description: for hand written only, change the image with thresh and dilate
    :param im: image, np array
    :param min_area: int
    :return:
    '''

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh_rect_size=5
    output_color=255
    mode=11
    thresh = cv2.adaptiveThreshold(gray,output_color,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY_INV,mode,thresh_rect_size) # adaptive thresh mean method to get the image in black and white only

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #==================== sort =================#
    for cnt in contours:
        if cv2.contourArea(cnt)<min_area :
            [x, y, w, h] = cv2.boundingRect(cnt)
            thresh[y:y+h,x:x+w]=[0]
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    # thresh=cv2.dilate(thresh,kernel=kernel,iterations=2)
    # thresh=cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)

    thresh=cv2.bitwise_not(thresh)
    return thresh
#==================================#
def resize_image_less_than_600_800(img):
    '''
    description: resize the small input images to 1600 1200
    :param img:input image
    :return:img
    '''
    height,width,depth=img.shape
    if height<600 and width<800:
        img=cv2.resize(img,(800,600))

        color_white = [255, 255, 255]
        left_border = 400
        top_border = 300
        right_border = 400
        bottom_border = 300

        img = cv2.copyMakeBorder(
            img,
            top=top_border,
            bottom=bottom_border,
            left=left_border,
            right=right_border,
            borderType=cv2.BORDER_CONSTANT,
            value=color_white
        )
        return img
    else:
        return img

import numpy as np 
from tensorflow.keras.applications import VGG16 
from tensorflow.keras.layers import Input, Conv2D, UpSampling2D, concatenate, Dropout 
from tensorflow.keras.models import Model 
from tensorflow.keras.optimizers import Adam 
import matplotlib.pyplot as plt 
 
def vgg_unet(input_shape, num_classes): 
    inputs = Input(input_shape) 
    base_model = VGG16(weights=None, include_top=False, input_tensor=inputs) 
 
    f1 = base_model.get_layer('block1_conv2').output 
    f2 = base_model.get_layer('block2_conv2').output 
    f3 = base_model.get_layer('block3_conv3').output 
    f4 = base_model.get_layer('block4_conv3').output 
    f5 = base_model.get_layer('block5_conv3').output 
 
    u4 = UpSampling2D((2, 2))(f5) 
    u4 = concatenate([u4, f4]) 
    u4 = Conv2D(1024, (3, 3), activation='relu', padding='same')(u4) 
    u4 = Dropout(0.5)(u4) 
 
    u3 = UpSampling2D((2, 2))(u4) 
    u3 = concatenate([u3, f3]) 
    u3 = Conv2D(512, (3, 3), activation='relu', padding='same')(u3) 
    u3 = Dropout(0.5)(u3) 
 
    u2 = UpSampling2D((2, 2))(u3) 
    u2 = concatenate([u2, f2]) 
    u2 = Conv2D(256, (3, 3), activation='relu', padding='same')(u2) 
    u2 = Dropout(0.5)(u2) 
 
    u1 = UpSampling2D((2, 2))(u2) 
    u1 = concatenate([u1, f1]) 
    u1 = Conv2D(128, (3, 3), activation='relu', padding='same')(u1) 
    u1 = Dropout(0.5)(u1) 
 
    outputs = Conv2D(num_classes, (1, 1), activation='softmax')(u1) 
    model = Model(inputs, outputs) 
 
    return model 

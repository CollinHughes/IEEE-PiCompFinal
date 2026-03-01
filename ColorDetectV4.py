#-------------------------------------------------------------------------------
# Name:         LED Color Detection
# Purpose:      To detect the color of an LED within a grey region
#
# Author:       Collin Hughes
#
# Created:      10/23/2025
#-------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Importing Libraries
# ------------------------------------------------------------------------------
from PIL import Image, ImageDraw, ImageFont  # import the Image class from Pillow
import math
import numpy as np
import os
import scipy.ndimage as nd
from picamzero import Camera

# ------------------------------------------------------------------------------
# Taking a picture
# ------------------------------------------------------------------------------

#cam = Camera()
#cam.still_size = (648, 486) # Change aspect ratio of camera
def detect_color(cam):
    cam.take_photo(f"CapturedPhoto.jpg") # Save the image to same folder


    # ------------------------------------------------------------------------------
    # 1) Importing the image and preparing for each step
    # ------------------------------------------------------------------------------

    # Set and load the image. Give error if not found
    IMAGE_PATH = "CapturedPhoto.jpg"
    if not os.path.isfile(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}.")

    pi_image = Image.open(IMAGE_PATH).convert("RGB") # Open the image in RGB
    img_np = np.array(pi_image, dtype=np.float32) # Convert image data to nunpy array

    # ------------------------------------------------------------------------------
    # 2) Find just the sattelite in a grey range
    # ------------------------------------------------------------------------------

    # Compute saturation
    max_value = np.max(img_np, axis=2) # Max brightness
    min_val = np.min(img_np, axis=2) # Min brightness
    saturation = (max_value - min_val) / (max_value + 1e-5) # normalized color intensity
    value_norm = max_value / 255.0 # Normalize value to 0–1

    # Define thresholds for grey (CALIBRATION)
    low_sat = saturation < 0.3       # low color intensity = grey (.1)
    not_too_dark = value_norm > 0.4   # avoid black regions (.4)
    not_too_bright = value_norm < 0.95 # avoid white glare (.95)

    mask = (low_sat & not_too_dark & not_too_bright).astype(np.uint8) * 255 # Combine conditions for mask

    # ------------------------------------------------------------------------------
    # 3) Filling in the hole
    # ------------------------------------------------------------------------------

    filled_mask = nd.binary_fill_holes(mask) # Magic hole fill command

    # ------------------------------------------------------------------------------
    # 4) Masking the original image
    # ------------------------------------------------------------------------------

    # Apply mask to each color channel
    masked_img = img_np * filled_mask[:, :, None] # Apply filled mask to the original image
    masked_img = masked_img.astype(np.uint8) # Convert to uint8 image

    # ------------------------------------------------------------------------------
    # 5) Isolating the LED
    # ------------------------------------------------------------------------------
    # Compute saturation for the removed background
    value = np.max(masked_img, axis=2) # Max brightness
    min_val = np.min(masked_img, axis=2) # Min brightness
    saturation = (value - min_val) / (value + 1e-5) # normalized color intensity

    mask = saturation > 0.5 # Low saturation is grey, create threshold
    masked_img = img_np * mask[:, :, None] # Apply the mask to the isolated satellite

    # ------------------------------------------------------------------------------
    # 6) Figuring out the color
    # ------------------------------------------------------------------------------
    final_LED = masked_img.astype(np.uint8) # Convert to unit8 for processing
    non_black_mask = np.any(final_LED != 0, axis=-1)  # Find non black pixels
    non_black_pixels = final_LED[non_black_mask] # Select only non-black pixels, put in array
    if non_black_pixels.size == 0:
        average_color = (0, 0, 0) 
    else:
        average_color = non_black_pixels.mean(axis=0) # Compute the average color

    # Reference color for vector with inconclusive result
    colors_inc = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "purple": (128, 0, 128),
        "inconclusive": (0, 0, 0)
    }

    colors = {
        'R': (255, 0, 0),
        'G': (0, 255, 0),
        'B': (0, 0, 255),
        'P': (128, 0, 128)
    }

    # Function for distance between vectors
    def distance(c1, c2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    # Find the minimum distance between the color vector and refrence vectors
    closest_color = min(colors, key=lambda c: distance(average_color, colors[c]))
    closest_color_inc = min(colors_inc, key=lambda c: distance(average_color, colors_inc[c]))

    print(f"The image is closest to: {closest_color}") # Print to console
    print(f"Confidence: {closest_color_inc}") # Print to console
    return closest_color
    
    



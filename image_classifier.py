"""
Created on Thu Feb 29 12:04:15 2024

@author: nedaahadi
"""

import os
import zlib

current_directory = os.getcwd()
print("Current directory:" + current_directory)

def compress_image(image):
    return zlib.compress(image)


def images_length(image_paths):
    category_lengths = {}

    for image_path in image_paths:
        
        #print(os.path.dirname(image_path)) this returns the path without the image name
        #print(os.path.basename(os.path.dirname(image_path))) this returns the folder of the image AKA the category
        category = os.path.basename(os.path.dirname(image_path)) 
        
        with open(image_path, 'rb') as file:
            raw_image_data = file.read()
            
        compressed_image = compress_image(raw_image_data)
        length = len(compressed_image)
        
        if category in category_lengths:
            category_lengths[category] += length
        else:
            category_lengths[category] = length


    return category_lengths


def classify_new_image(compressed_lengths, new_image_path):
    print("Classifying new image:", new_image_path)
    
    with open(new_image_path, 'rb') as file:
        new_raw_image_data = file.read()
    
    compressed_new_image = compress_image(new_raw_image_data)
    new_length = len(compressed_new_image)
    
    length_differences = {}
    for category, length in compressed_lengths.items():
        length_with_new_image = length + new_length
        length_difference = length_with_new_image - length
        length_differences[category] = length_difference
    
    predicted_category = min(length_differences, key=length_differences.get)
    return predicted_category


def image_paths(directory):
    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Training Phase
training_images_directory = "./training_images/train"
training_image_paths = image_paths(training_images_directory)
compressed_lengths = images_length(training_image_paths)

# Classifying Phase
while True:
    new_image_path = input("\nEnter the path to the new image: ")
    if new_image_path.lower() == "exit":
        break
    else:
        classification = classify_new_image(compressed_lengths, new_image_path)
        print("Predicted Category:", classification)

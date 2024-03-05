#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 12:04:15 2024

@author: nedaahadi
"""
import os
import zlib
import copy

def compress_images(images):
    concatenated_data = b"".join(images)
    return zlib.compress(concatenated_data)

def get_image_paths(directory):
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                image_paths.append(os.path.join(root, file))
    return image_paths

def concatenate_images(image_paths):
    concatenated_category_images = {}
    for image_path in image_paths:
        category = os.path.basename(os.path.dirname(image_path)) 
        with open(image_path, 'rb') as file:
            raw_image_data = file.read()
            concatenated_category_images.setdefault(category, []).append(raw_image_data)
    return concatenated_category_images

def classify_new_image(new_image_path, concatenated_category_images):
    with open(new_image_path, 'rb') as file:
        new_raw_image_data = file.read()
        
    #new_concatenated_category_images = concatenated_category_images.copy()
    #this won;t work because both dictionaries will reference the same list of images
    new_concatenated_category_images = copy.deepcopy(concatenated_category_images)


    for category in new_concatenated_category_images:
        new_concatenated_category_images[category].append(new_raw_image_data)
    
    for category, images in concatenated_category_images.items():
        print("Category:", category)
        print("Number of Images:", len(images))
        print("Total Image Data Size:", sum(len(image_data) for image_data in images))

    print("$$$$$$$$$$$$$$$$$$$$$$$") 
    
    for category, images in new_concatenated_category_images.items():
        print("Category:", category)
        print("Number of Images:", len(images))
        print("Total Image Data Size:", sum(len(image_data) for image_data in images))



        
    compressed_categories = {}
    for category, images in concatenated_category_images.items():
        compressed_categories[category] = compress_images(images)
        
    new_compressed_categories = {}
    for category, images in new_concatenated_category_images.items():
        new_compressed_categories[category] = compress_images(images)
    

   
    length_differences = {}
    for category in concatenated_category_images:
        old_compressed_length = len(compressed_categories[category])
        #print(old_compressed_length)
        new_compressed_length = len(new_compressed_categories[category])
        #print(new_compressed_length)
        length_difference = new_compressed_length - old_compressed_length
        length_differences[category] = length_difference
        
    for category, difference in length_differences.items():
        print(f"Category: {category}, Length Difference: {difference}")

    
    predicted_category = min(length_differences, key=length_differences.get)
    return predicted_category





# Training Phase
#training_images_directory = "./training_images/train"
#training_images_directory = "./Vegetable Images/train"
#training_images_directory = "./fruit/train"
training_images_directory = "./ColorClassification/train"

training_image_paths = get_image_paths(training_images_directory)
#print(training_image_paths)
#All images paths in the given directory
concatenated_category_images = concatenate_images(training_image_paths)
#print(concatenated_category_images)
#A dictionary where keys are categories and values are raw image data


# Classifying Phase
while True:
    new_image_path = input("\nEnter the path to the new image: ")
    if new_image_path.lower() == "exit":
        break
    else:
        classification = classify_new_image(new_image_path, concatenated_category_images)
        print("\nPredicted Category:", classification)

import pandas as pd
import zlib
from collections import Counter

import os
current_directory = os.getcwd()

print("Current directory:" + current_directory)

# Run from ./compression-classification folder
datapath = './bbc-articles.csv'
BBCDataFrame = pd.read_csv(datapath)


# Training Phase
training_data = {}
    
for i, row in BBCDataFrame.iterrows():
    category = row['category']
    text = row['text']
        
    if category not in training_data:
        training_data[category] = []
            
    training_data[category].append(text)


#we will concatenate all books related to an author.
def concatenate_texts(texts):
    concatenated_texts = ""
    
    for text in texts:
        concatenated_texts += ' ' + text
    
    print(concatenated_texts)
    return concatenated_texts

def reconcatenate_texts(new_text, texts):

    reconcatenated_texts = ""

    for text in texts:
        reconcatenated_texts += ' ' + text
    reconcatenated_texts += new_text
    print(reconcatenated_texts)
    return reconcatenated_texts
        





#we’ll compress the data using the zipping technique
def compress_texts(texts):
    print("length of compressed zlib: \n")
    print(len(zlib.compress(texts.encode())))
    return len(zlib.compress(texts.encode()))

#we're calculating the size of each author after compression
def texts_length(training_data):
    compressed_lengths = {}
    
    for category, texts in training_data.items():
        compressed_lengths[category] = compress_texts(concatenate_texts(texts))
        
    return compressed_lengths

def new_texts_length(new_text,training_data):
    recompressed_lengths = {}
    for category, texts in training_data.items():
        recompressed_lengths[category] = compress_texts(reconcatenate_texts(new_text,texts))
    return recompressed_lengths


# Classifying Phase
def classify_new_text(compressed_lengths, recompressed_lengths):
    temp1 = Counter(compressed_lengths)
    temp2 = Counter(recompressed_lengths)
    res = temp2 - temp1

    predicted_category = min(res, key=res.get)
    return predicted_category

while True:
    new_text_title = input("\nEnter the Article Text: ")
    if new_text_title.lower() =="exit":
        break
    else:
        compressed_lengths = texts_length(training_data)
        recompressed_lengths = new_texts_length(new_text_title,training_data)
        classification = classify_new_text(compressed_lengths,recompressed_lengths)
        print("Your Article: \n'" + new_text_title + "'\n")
        print("Predicted Category:", classification)
        
# Borthwick has much to ponder after a fourth straight loss to the Scots, which leaves England needing to win their remaining two matches to have any chance of competing for the Six Nations title. Smith's return will offer another playmaking option, while Mitchell is also thought to be making a quicker than expected recovery from a knee injury, although neither is ready to resume full training at this stage. Feyi-Waboso is pushing for a first international start after his try-scoring cameo against Scotland, but he will be absent from training all week as his medical exam is required to take place face-to-face.
        
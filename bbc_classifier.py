import pandas as pd
import zlib
from collections import Counter
from sklearn.model_selection import train_test_split
import os


current_directory = os.getcwd()

print("Current directory:" + current_directory)

# Instructions: run from ./compression-classification folder
# Import csv as a pandas DataFrame
datapath = './bbc-articles.csv'
BBCDataFrame = pd.read_csv(datapath)

# SPLIT DATASET INTO TRAIN AND TEST DATA
train_df, test_df = train_test_split(BBCDataFrame, test_size=0.2)

# print("Training data size: ")
# print(train_df.shape)
# print("Test data size: ")
# print(test_df.shape)

# Training Phase
training_data = {}
    
for i, row in train_df.iterrows():
    category = row['category']
    text = row['text']
        
    if category not in training_data:
        training_data[category] = []
            
    training_data[category].append(text)


# Group together and concatenate all data related to each category/label.
def concatenate_texts(texts):
    concatenated_texts = ""
    
    for text in texts:
        concatenated_texts += ' ' + text
    
    # print(concatenated_texts)
    return concatenated_texts

def reconcatenate_texts(new_text, texts):

    reconcatenated_texts = ""

    for text in texts:
        reconcatenated_texts += ' ' + text
    reconcatenated_texts += new_text
    # print(reconcatenated_texts)
    return reconcatenated_texts
        

# Compress the data using the zipping technique
def compress_texts(texts):
    # print("length of compressed zlib: \n")
    # print(len(zlib.compress(texts.encode())))
    return len(zlib.compress(texts.encode()))

# Calculate the size of each category after compression
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


#  OPTION TO PUT IN AN ARTICLE/ A PIECE OF TEXT TO CLASSIFY
# while True:
#     new_text_title = input("\nEnter the Article Text: ")
#     if new_text_title.lower() =="exit":
#         break
#     else:
#         compressed_lengths = texts_length(training_data)
#         recompressed_lengths = new_texts_length(new_text_title,training_data)
#         classification = classify_new_text(compressed_lengths,recompressed_lengths)
#         print("Your Article: \n'" + new_text_title + "'\n")
#         print("Predicted Category:", classification)


# TESTING PHASE

test_results = []

for index, row in test_df.iterrows():
    # print(index)
    # print(test_df['text'][index])

    test = test_df['text'][index]
    compressed_lengths = texts_length(training_data)
    recompressed_lengths = new_texts_length(test,training_data)
    classification = classify_new_text(compressed_lengths,recompressed_lengths)

    if classification == test_df['category'][index]:
        test_results.append(1)
    else: test_results.append(0)


    # print("Your Test: \n'")
    # print(index)
    # print("Predicted Category:", classification + "'\n")
    # print("Actual Category: ", test_df['category'][index]+ "'\n")

print("Number of tests: ")
print(test_df.shape[0])
print("Passed tests:")
print(sum(test_results))
print("Percentage Accuracy:")
print((sum(test_results)*100 )/ test_df.shape[0])
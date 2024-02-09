import pandas as pd
import zlib
from collections import Counter

import os
current_directory = os.getcwd()
print(current_directory) 


BooksDataFrame = pd.read_csv('./compression-classification/books2.csv')

# Training Phase
training_data = {}
    
for i, row in BooksDataFrame.iterrows():
    author = row['Author']
    title = row['Title']
        
    if author not in training_data:
        training_data[author] = []
            
    training_data[author].append(title)

print("Training data: \n")
print(training_data)
print("\n\n\n")

#we will concatenate all books related to an author.
def concatenate_books(titles):
    concatenated_books = ""
    
    for title in titles:
        concatenated_books += ' ' + title

    print(concatenated_books)
    return concatenated_books

def reconcatenate_books(new_title, titles):

    reconcatenated_books = ""

    for title in titles:
        reconcatenated_books += ' ' + title
    reconcatenated_books += new_title
    # print("got to here !!!!!!!!")
    # print(reconcatenated_books)
    return reconcatenated_books
        





#we’ll compress the data using the zipping technique
def compress_books(books):
    print("length of compressed zlib: \n")
    print(len(zlib.compress(books.encode())))
    return len(zlib.compress(books.encode()))

#we're calculating the size of each author after compression
def books_length(training_data):
    compressed_lengths = {}
    
    for author, titles in training_data.items():
        compressed_lengths[author] = compress_books(concatenate_books(titles))
        # print("author: " + author)
        # print(titles)
        # print("\n\n")
        
    # print(compressed_lengths)
        
    return compressed_lengths

def new_books_length(new_book,training_data):
    recompressed_lengths = {}
    for author, titles in training_data.items():
        recompressed_lengths[author] = compress_books(reconcatenate_books(new_book,titles))
    
    return recompressed_lengths




# Classifying Phase
def classify_new_book(compressed_lengths, recompressed_lengths):
    

    # new_book_length = compress_books(new_book)
    # new_lengths = {
    #     author: new_book_length + length for author, length in compressed_lengths.items()
    # }
    # predicted_author = min(
    #     key=lambda author: recompressed_lengths[author] - compressed_lengths[author]
    # )

    temp1 = Counter(compressed_lengths)
    temp2 = Counter(recompressed_lengths)
    res = temp2 - temp1
    # print("get result")
    # print(dict(res))

    predicted_author = min(res, key=res.get)
    # print(predicted_author)
    return predicted_author


new_book_title = "Christmas Carol, A"

compressed_lengths = books_length(training_data)
# print("COMPRESSED LENGTHS!!!!!!!!")
# print(compressed_lengths)
recompressed_lengths = new_books_length(new_book_title,training_data)
# print("RECOMPRESSED LENGTHS!!!!!!!!")
# print(recompressed_lengths)


classification = classify_new_book(compressed_lengths,recompressed_lengths)
print("Author Name:", classification)

# length1 = len("Girl with the Dragon TattooGirl who kicked the Hornet's NestGirl who played with Fire")
# print(length1)

# length2 = len("Dickens, CharlesChristmas Carol, A")
# print(length2)
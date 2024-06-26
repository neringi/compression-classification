import pandas as pd
import zlib
from collections import Counter

import os
current_directory = os.getcwd()

BooksDataFrame = pd.read_csv('./compression-classification/books2.csv')


# Training Phase
training_data = {}
    
for i, row in BooksDataFrame.iterrows():
    author = row['Author']
    title = row['Title']
        
    if author not in training_data:
        training_data[author] = []
            
    training_data[author].append(title)


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
    print(reconcatenated_books)
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
        
    return compressed_lengths

def new_books_length(new_book,training_data):
    recompressed_lengths = {}
    for author, titles in training_data.items():
        recompressed_lengths[author] = compress_books(reconcatenate_books(new_book,titles))
    return recompressed_lengths


# Classifying Phase
def classify_new_book(compressed_lengths, recompressed_lengths):
    temp1 = Counter(compressed_lengths)
    temp2 = Counter(recompressed_lengths)
    res = temp2 - temp1

    predicted_author = min(res, key=res.get)
    return predicted_author

print("\n\t ** A Program that Performs Classification By Zipping **\n \nInstructions: \n- Write the book tiltle that you want to classify\n- Once you're done, please type exit")
while True:
    new_book_title = input("\nEnter the Book Title: ")
    if new_book_title.lower() =="exit":
        break
    else:
        compressed_lengths = books_length(training_data)
        recompressed_lengths = new_books_length(new_book_title,training_data)
        classification = classify_new_book(compressed_lengths,recompressed_lengths)
        print("Your book title: '" + new_book_title + "'")
        print("Predicted Author Name:", classification)

length1 = len("Girl with the Dragon TattooGirl who kicked the Hornet's NestGirl who played with Fire")
print(length1)

# print(len(zlib.compress(length1)))

# length2 = len("Dickens, CharlesChristmas Carol, A")
# print(length2)
import pandas as pd
import zlib

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

#we will concatenate all books related to an author.
def concatenate_books(titles):
    concatenated_books = ""
    
    for title in titles:
        concatenated_books += ' ' + title
    return concatenated_books

#we’ll compress the data using the zipping technique
def compress_books(books):
    return len(zlib.compress(books.encode()))

#we're calculatin the size of each author after compression
def books_length(training_data):
    compressed_lengths = {}
    
    for author, titles in training_data.items():
        compressed_lengths[author] = compress_books(concatenate_books(titles))
        
    return compressed_lengths



# Classifying Phase
def classify_new_book(new_book, compressed_lengths):
    new_book_length = compress_books(new_book)
    new_lengths = {
        author: new_book_length + length for author, length in compressed_lengths.items()
    }
    predicted_author = min(
        new_lengths,
        key=lambda author: new_lengths[author] - compressed_lengths[author]
    )
    return predicted_author




compressed_lengths = books_length(training_data)

new_book_title = "Welcome to the World"
classification = classify_new_book(new_book_title, compressed_lengths)
print("Author Name:", classification)

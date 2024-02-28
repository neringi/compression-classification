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

# business
# In 2022, Reliance outbid Disney for rights to stream the popular India Premier League cricket tournament, sparking a sizable fall in subscribers to Disney's Hotstar streaming service. The company's Star sports channels also reported declines in subscribers and advertisers in the 12 months to September 2023. Disney boss Bob Iger said the joint venture would keep Disney present in the large Indian market while benefiting from Reliance's "deep understanding of the Indian market and consumer". But the deal values Star India at less than a third of what it was in 2019 when Disney took on the business, sources told the Reuters news agency. Disney will own a roughly 37% stake in the joint venture, which will have exclusive rights to distribute Disney's films and productions in India.

# sport   
# Borthwick has much to ponder after a fourth straight loss to the Scots, which leaves England needing to win their remaining two matches to have any chance of competing for the Six Nations title. Smith's return will offer another playmaking option, while Mitchell is also thought to be making a quicker than expected recovery from a knee injury, although neither is ready to resume full training at this stage. Feyi-Waboso is pushing for a first international start after his try-scoring cameo against Scotland, but he will be absent from training all week as his medical exam is required to take place face-to-face.

# politics
#  There were angry clashes at Prime Minister's Questions, as the main party leaders rowed about the records of their predecessors. Labour's Keir Starmer said Rishi Sunak should take action over comments former PM Liz Truss made at a conference. Sir Keir accused her of "slagging off and undermining Britain" during an event in the United States. In return, Mr Sunak called him "spineless" and "utterly shameless" for serving under Jeremy Corbyn. He added this meant the Labour leader had failed to take action while "while antisemitism ran rife in his party" during his predecessor's tenure.
#  didnt work misclassified as business
        
# politics 2
#  The latest bout of mud-slinging at PMQs began when Sir Keir mocked Ms Truss for comments she made at a gathering of US conservatives last week. The former prime minister told the event that she had faced a "huge establishment backlash" during her 49-day premiership from various government agencies and the Bank of England. The Labour leader accused her of claiming she was "sabotaged by the deep state", quipping that it showed the Conservatives had become the "political wing of the Flat Earth Society". He also criticised Ms Truss for remaining "silent" whilst another speaker at the conference, former Trump adviser Steve Bannon, described anti-Islam activist Tommy Robinson as a "hero". Ms Truss did not respond to questions about the incident on Wednesday. "Why is he allowing her to stand as a Tory MP at the next election?" Sir Keir added.
#  also misclassified as business
        
#  tech (of business though)
#  Last year only six UK companies became a unicorn, the title handed out to private start-up firms that are valued at more than a billion dollars. Achieving the $1bn (£790m) valuation brings prestige and status to a start-up firm, but does have its downside. Vishal Marria is the founder of Quantexa, one of those British firms to make the billion dollar mark in the UK in 2023. The London-based tech company, which uses AI to interpret data and help financial firms manage risk, completed a funding round in April, taking the company's valuation up to £1.42bn. Mr Marria likens the pressure of running a unicorn company to a football player moving club for a record-breaking fee.
#  misclassified as business
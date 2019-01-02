#Import packages

import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
import emoji
from nltk.corpus import stopwords
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Choose the File to read

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

df = pd.read_csv(filename, delimiter="\t", header=None, names=["text"])

#Removing the first line, if its about encryption

if df.text[0].find('Messages to this chat and calls are now secured') !=0:
    df.text=df.text[1:]
    
df.dropna(inplace=True)

#Function that displays the Most Used Words, with Plot.

def Words(df):
    lines = []

    #Removing the date, time and name info from each line.

    for line in df.text:
        try:
            lines.append(line[line.find(':',15)+2:])
        except:
            lines.append("")

    #Now to get each word in a list.

    tokenizer = RegexpTokenizer(r'\w+')
    words = []

    for line in lines:
        w = tokenizer.tokenize(line)

        for each in w:
            if each not in ('Media', 'omitted'):
                words.append(each)

    stop_words = set(stopwords.words('english'))

    #Removing stop words, digit figures and words less than length 3!

    words_final = []

    words_final = [w for w in words if not w in stop_words and w.isalpha() and len(w)>3]  #Optional , to change the word length filter.

    print("\nNumber of meaningful words in your Chat : ", len(words_final))

    fdist = FreqDist(words_final)
    #Frequency of all the words

    print("\nTop 10 Most Used words are :")
    
    for k,v in fdist.most_common(10):
        print("\t",k,":", v)
        
    print("\nPlot with Frequencies of the Words.")
    plt.figure(figsize=(13,6))
    fdist.plot(30)

#Function that displays the Most Used Emojis in the Chat

def Emoji(df):
    lines = []

    #Removing the Date, Time and Contact name from each line of the data.

    for line in df.text:
        try:
            #Using demojize to convert the emojis present to its respective string.
            lines.append(emoji.demojize(line[line.find(':',15)+2:]))
        except:
            lines.append("")

    #Using Regex, extracting the emojis present in string form. (:emoji:)

    tokenizer = RegexpTokenizer(r':\w+:')
    emojis = []

    for line in lines:
        e = tokenizer.tokenize(line)

        #Storing it in a list
        for each in e:
            emojis.append(each)

    emojis = list(filter(lambda a: a != ':male_sign:', emojis))
    
    print("\nTotal No. of Emojis Used: ", len(emojis))

    #Converting the enocoded emoji string back to Emoji, using emojize.
    emoji_final = []

    for each in emojis:
        emoji_final.append(emoji.emojize(each))

    #Displaying Emojis
    ef = FreqDist(emoji_final)

    print("\nTop 10 Most Used Emojis and their counts are:")

    for k,v in ef.most_common(10):
        print("\t",k,":",v)

#Calling the Functions.

Emoji(df)

Words(df)

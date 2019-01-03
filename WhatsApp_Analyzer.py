#Import packages

import os
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("module://mplcairo.tk")
import matplotlib.pyplot as plt
import emoji
from matplotlib.font_manager import FontProperties
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from tkinter import Tk
from tkinter.filedialog import askopenfilename

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

    f.write('<u><i><h2>Words</h2></i></u>')
    
    f.write('Total No. meaningful Words in your chat: ' + str(len(words_final)))

    fdist = FreqDist(words_final).most_common(15)
    #Frequency of all the words

    f.write('<br><br>Top 10 Most Used Words are:<br>')

    k,v=[],[]

    for i in fdist:
        k.append(i[0])
        v.append(i[1])

    for i in range(10):
        f.write('<br>' + str(k[i]) + ': ' + str(v[i]))

    sns.barplot(x=k,y=v)
    plt.title('Frequently Occuring Words', fontsize=20)
    fig = plt.gcf()
    fig.set_size_inches(12, 6)
    file_name = 'Words_' + str(os.path.splitext(os.path.basename(filename))[0]) + '.png'
    fig.savefig(os.path.join('images', file_name))
    f.write('<center><img src=' + os.path.join('images', file_name) + ' style=\'width: 1000px; height: 500px\'></center>')

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

    #Removing male and female signs
    emojis = list(filter(lambda a: a != ':male_sign:' and a != ':female_sign:', emojis))
    
    f.write('<br><br><u><i><h2>Emojis</h2></i></u>')

    f.write('Total No. of Emojis used in your chat: ' + str(len(emojis)))

    #Converting the enocoded emoji string back to Emoji, using emojize.
    emoji_final = []

    for each in emojis:
        emoji_final.append(emoji.emojize(each))

    #Displaying Emojis
    ef = FreqDist(emoji_final).most_common(15)

    f.write('<br><br>Top 10 Most Used Emojis are:<br>')

    k,v=[],[]

    for i in ef:
        k.append(i[0])
        v.append(i[1])

    for i in range(10):
        f.write('<br>' + str(k[i]) + ': ' + str(v[i]))

    fpath = 'fonts/NotoColorEmoji.ttf'
    plt.title('Frequently Occuring Emojis', fontsize=20)
    sns.barplot(x=k,y=v)
    file_name = 'Emojis_' + str(os.path.splitext(os.path.basename(filename))[0]) + '.png'
    plt.xticks(fontproperties=FontProperties(fname=fpath), fontsize=20)
    plt.savefig(os.path.join('images', file_name))
    f.write('<center><img src=' + os.path.join('images', file_name) + ' style=\'width: 1000px; height: 500px\'></center>')
   


if __name__ == "__main__":
    
    #Choose the File to read
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    df = pd.read_csv(filename, delimiter="\t", header=None, names=["text"])

    os.chdir(os.path.dirname(os.path.realpath(__file__))) # Change current directory to the program's directory

    f = open('results_' + str(os.path.splitext(os.path.basename(filename))[0]) + '.html', 'w')

    # Make images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    #Removing the first line, if its about encryption
    if df.text[0].find('Messages to this chat and calls are now secured') !=0:
        df.text=df.text[1:]
        
    df.dropna(inplace=True)

    #Calling the Functions.

    f.write('<center><h1>Whatsapp Chat Analysis Results</h1></center>')

    Words(df)

    Emoji(df)

    f.close()

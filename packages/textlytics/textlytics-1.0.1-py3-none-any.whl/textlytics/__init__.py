#TextLytics

#dependencies
import re
import os

import pandas as pd
import pyphen
import syllables
import nlpnet
import nltk
from string import punctuation, whitespace
from collections import defaultdict
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#

class Config:
    def __init__(self, language):
        self.language = language
        self.incidence = 1000

    def getLanguage(self):
        return self.language
    
    def getIncidence(self):
        return self.incidence

    def setIncidence(self,value):
        self.incidence = value

    def setLanguage(self,lang):
        if lang in ["english","portuguese"]:
            self.language = lang
        else:
            print("Invalid Language!")
    

    def setPosPtDir(self,dir):
        try:
            nlpnet.set_data_dir(dir)
        except OSError:
            print ('Error: Directory not found.')

config = Config("english")


#auxiliar modules
     
def sent_tokenize(text):
    text = re.sub(r"\,|;|:|-|!|\?|´|`|^|'", " ", text)
    tokenize = [re.sub('\s+',' ',sentence).strip() for sentence in text.split(".")]
    sents = []
    for sentence in tokenize:
        if len(sentence)>0:
            sents.append(sentence)
    return sents

def word_tokenize(text):
    text = re.sub(r"\.|,|;|:|-|!|\?|´|`|^|'", " ", text)
    new_text = re.sub(r"[0-9]+", "", text)
    tokenize = [re.sub('\s+',' ',word).strip() for word in new_text.split(" ")]
    words = []
    for word in tokenize:
        if len(word)>0:
            words.append(word)
    return words

#modules

def charCounter(text):
    new_text = re.sub(r"\.|,|;|:|-|!|\?|´|`|^|'", "", text)
    new_text = re.sub(r"[0-9]+", "", new_text)
    count = len(new_text)
    return count

def avgWordLen(text):
    words = []
    for word in re.split('['+punctuation+whitespace+']', text):
        if(word is not ''):
            words.append(word)
    c = [len(i) for i in words]
    word_average = float(sum(c)/len(c))
    return word_average

def wordCounter(text):
    text_withOutNumbers = re.sub(r"[0-9]+", "", text)
    count = len(word_tokenize(text_withOutNumbers))
    return count

def uniqueWordsCounter(text):
    return len(set(word_tokenize(text)))

def sentencesCounter(text):
    sents = len(sent_tokenize(text))
    return sents

def avgWordsSentence(text):
    sents = sentencesCounter(text)
    words = wordCounter(text)
    awl = (words/sents)
    return awl

def syllableCounter(text):
    language = config.getLanguage()
    new_text = text.lower()
    tokens = word_tokenize(new_text)
    count_syb = 0
    if (language == "portuguese"):
        dic = pyphen.Pyphen(lang = 'pt_BR')
        for w in tokens:
            try:
                count_syb+= len(dic.inserted(w).split("-"))
            except:
                count_syb+= syllables.estimate(w)
    if (language == "english"):
        dic = pyphen.Pyphen(lang = 'en')
        for w in tokens:
            try:
                count_syb+= len(dic.inserted(w).split("-"))
            except:
                count_syb+= syllables.estimate(w)
    return count_syb

def avgSyllableWords(text):
    qtd_words = wordCounter(text)
    count_syb = syllableCounter(text)
    asw = float(count_syb/qtd_words)
    return asw

def only_once(text):
    d, result = dict(),[]
    for word in re.split('['+punctuation+whitespace+']', text):
        d[word.lower()] = d.get(word.lower(), 0)+1
    for word, occur in d.items():
        if occur ==1:
            result.append(word)
    return result

def rareWordsCounter(text):
    unique = len(only_once(text))
    return unique

def rareWordsRatio(text):
    unique = rareWordsCounter(text)
    words = wordCounter(text)
    ratio = float(unique/words)
    return ratio

def lexical_diversity(text):
    ld = (uniqueWordsCounter(text)/wordCounter(text))
    return ld

def readability(text):
    FleschEN = (206.835-((1.015*avgWordsSentence(text))+(84.6*avgSyllableWords(text))))
    FleschPT = (248.835-((1.015*avgWordsSentence(text))+(84.6*avgSyllableWords(text))))
    language = config.getLanguage()
    if (language == "english"):
        Flesch = FleschEN
    else:
        Flesch = FleschPT
    return Flesch

def readability_schoolarity(text):
    score = readability(text)
    language = config.getLanguage()
    if language == "portuguese":
        if score>=75:
            return "1ª à 4ª série"
        if score<75 and score>=50:
            return "5ª à 8ª série"
        if score<50 and score>=25:
            return "Ensino Médio e Nível Superior"
        if score<25:
            return "Nível Superior"
    else:
        if score>90:
            return "5th grade"
        if score<=90 and score>80:
            return "6th grade"
        if score<=80 and score>70:
            return "7th grade"
        if score<=70 and score>60:
            return "8th & 9th grade"
        if score<=60 and score>50:
                return "10th to 12th grade"
        if score<=50 and score>=30:
            return "College"
        if score<=30:
            return "College graduate"

def taggerEN(text):
    tokens = nltk.word_tokenize(text)
    tags = str(nltk.pos_tag(tokens))
    return tags

def adjEN(text):
    tags = taggerEN(text)
    adj = tags.count("'JJ'")
    adj+= tags.count("'JJR'")
    adj+= tags.count("'JJS'")
    return adj

def verbEN(text):
    tags = taggerEN(text)
    verb = tags.count("'VB'")
    verb+= tags.count("'VBD'")
    verb+= tags.count("'VBG'")
    verb+= tags.count("'VBN'")
    verb+= tags.count("'VBP'")
    verb+= tags.count("'VBZ'")
    return verb

def nEN(text):
    tags = taggerEN(text)
    n = tags.count("'NN'")
    n+= tags.count("'NNS'")
    n+= tags.count("'NNP'")
    n+= tags.count("'NNPS'")
    return n

def pronEN(text):
    tags = taggerEN(text)
    pron = tags.count("'WP'")
    pron+= tags.count("'WP$'")
    pron+= tags.count("'PRP'")
    pron+= tags.count("'PRP$'")
    return pron

def conEN(text):
    tags = taggerEN(text)
    con = tags.count("'IN'")
    con+= tags.count("'CC'")
    con+= tags.count("'DT'")
    return con

def contentEN(text):
    content = adjEN(text)
    content += nEN(text)
    content += verbEN(text)
    return content

def contentDiversityEN(text):
    content = contentEN(text)
    words = wordCounter(text)
    cd = (content/words)
    return cd

def taggerPT(text):
    tagger = nlpnet.POSTagger()
    tags = str(tagger.tag(text))
    return tags

def adjPT(text):
    tags = taggerPT(text)
    adj = tags.count("'ADJ'")
    return adj

def verbPT(text):
    tags = taggerPT(text)
    verb = tags.count("'V'")
    return verb

def nPT(text):
    tags = taggerPT(text)
    n = tags.count("'N'")
    n+= tags.count("'NPROP'")
    return n

def pronPT(text):
    tags = taggerPT(text)
    pron = tags.count("'PROADJ'")
    pron+= tags.count("'PRO-KS'")
    pron+= tags.count("'PROPESS'")
    pron+= tags.count("'PRO-KS-REL'")
    pron+= tags.count("'PROSUB'")
    return pron

def conPT(text):
    tags = taggerPT(text)
    con = tags.count("'KS'")
    con+= tags.count("'KC'")
    con+= tags.count("'ADV-KS'")
    con+= tags.count("'PRO-KS'")
    con+= tags.count("'PRO-KS-REL'")
    return con

def contentPT(text):
    content = adjPT(text)
    content += nPT(text)
    content += verbPT(text)
    return content

def contentDiversityPT(text):
    content = contentPT(text)
    words = wordCounter(text)
    cd = (content/words)
    return cd

def posTaggerCounter(text,tag):
    language = config.getLanguage()
    incidence = config.getIncidence()
    if tag in ["ADJ","VERB","N","PRON","CON","CONTENT","CONTENT-D"]:
        if (language == "english"):
            if (tag == "ADJ"):
                count = adjEN(text)/incidence
            
            if (tag == "VERB"):
                count = verbEN(text)/incidence
            
            if (tag == "N"):
                count = nEN(text)/incidence

            if (tag == "PRON"):
                count = pronEN(text)/incidence

            if (tag == "CON"):
                count = conEN(text)/incidence

            if (tag == "CONTENT"):
                count = contentEN(text)/incidence
            
            if (tag == "CONTENT-D"):
                count = contentDiversityEN(text)

        if (language == "portuguese"):
            if (tag == "ADJ"):
                count = adjPT(text)/incidence
            
            if (tag == "VERB"):
                count = verbPT(text)/incidence
            
            if (tag == "N"):
                count = nPT(text)/incidence

            if (tag == "PRON"):
                count = pronPT(text)/incidence

            if (tag == "CON"):
                count = conPT(text)/incidence

            if (tag == "CONTENT"):
                count = contentPT(text)/incidence
            
            if (tag == "CONTENT-D"):
                count = contentDiversityPT(text)
    else:
        print("Invalid Tag")

    return count

def features2Dataframe(df,fieldName):
    df['Characters'] = df[fieldName].apply(charCounter)
    df['Words'] = df[fieldName].apply(wordCounter)
    df['AvgWordLen'] = df[fieldName].apply(avgWordLen)
    df['UniqueWords'] = df[fieldName].apply(uniqueWordsCounter)
    df['Sentences'] = df[fieldName].apply(sentencesCounter)
    df['AvgWordsSentence'] = df[fieldName].apply(avgWordsSentence)
    df['Syllables'] = df[fieldName].apply(syllableCounter)
    df['AvgSyllableWords'] = df[fieldName].apply(avgSyllableWords)
    df['RareWordsRatio'] = df[fieldName].apply(rareWordsRatio)
    df['LexicalDiversity'] = df[fieldName].apply(lexical_diversity)
    df['Readability'] = df[fieldName].apply(readability)
    df['ReadabilitySchoolarity'] = df[fieldName].apply(readability_schoolarity)
    df['IncidenceVerbs'] = df[fieldName].apply(posTaggerCounter, tag='VERB')
    df['IncidenceAdj'] = df[fieldName].apply(posTaggerCounter, tag='ADJ')
    df['IncidenceNouns'] = df[fieldName].apply(posTaggerCounter, tag='N')
    df['IncidenceCon'] = df[fieldName].apply(posTaggerCounter, tag='CON')
    df['IncidencePron'] = df[fieldName].apply(posTaggerCounter, tag='PRON')
    df['ContentIncidence'] = df[fieldName].apply(posTaggerCounter, tag='CONTENT')
    df['ContentDiversity'] = df[fieldName].apply(posTaggerCounter, tag='CONTENT-D')
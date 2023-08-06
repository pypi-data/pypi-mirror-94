Text Analytics Toolkit (textlytics)
====================================

TEXTLYTICS -- the Text Analytics Toolkit -- is a suite of open source Python modules
supporting research and development in Text Analytics, more specifically,
how to measure textual complexity for english and portuguese documents.

https://gitlab.com/jorgeluizfigueira/python-textlytics/

This toolkit is a project under development, the result of studies in textual complexity 
analysis research. The library provides several methods for extracting characteristics 
based on word occurrence metrics. Additionally, the counting of popular part of speech 
tagging, such as verbs, adjectives, nouns, were added. Studies carried out with such 
characteristics indicate that they can be used as a structured representation capable 
of increasing the accuracy of text document classification systems.


External libraries
------------------

This software uses the following external libraries:

PANDAS: Copyright (C) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team.
Licensed under BSD License.
Website: <https://pandas.pydata.org/>

NLTK: Copyright (C) 2001-2020 NLTK Project. 
Licensed under Apache 2.0 License.
Website: <https://www.nltk.org/>

NLPNET: Copyright (C) Erick Fonseca. 
Licensed under MIT license.
Website: <http://nilc.icmc.usp.br/nlpnet/>

PYPHEN: Copyright (C) Kozea and CourtBouillon.
Licensed under  GPL 2.0+ ~ LGPL 2.1+ ~ MPL 1.1 tri-license. 
Website: <https://pyphen.org/>

SYLLABLES: Copyright (C) David L. Day. 
Licensed under GNU General Public License v3.0 License.
Website: <https://github.com/prosegrinder/python-syllables>

To perform the task of counting the parts of speech tagging in Portuguese text documents,
TextLytics uses the NLPNET library and it needs trained models available at:

http://nilc.icmc.usp.br/nlpnet/models.html#pos-portuguese

Download the 'State-of-the-art POS tagger' file. Unzip to a folder. And use the 
textlytics.config.setPosPtDir ('dir') method. 'Dir' being the path of the folder where the
trained model was unzipped.

Features:
---------

* Statistical features:
* Number of characters
* Number of words
* Average word size
* Number of unique words (vocabulary)
* Number of sentences
* Average words per sentence
* Number of syllables
* Average syllables per word
* Rate of rare words (words that occur only once)
* Lexical Diversity
* Readability
* Schooling according to Readability
* Part of Speech Tagging Counter:
* Incidence of Verbs, Adjectives, Nouns, Pronouns and Connectives
* Content Incidence
* Content Diversity

Library Usage:
--------------

>>> import textlytics
>>>
>>> textlytics.config.setLanguage('english')
>>> textlytics.config.setIncidence(1)
>>> textlytics.config.setPosPtDir('path_to_nlpnet_trained_model_files')
>>>
>>>
>>>
>>> text = "Computational techniques can be used to identify musical trends and patterns,
    helping people filtering and selecting music according to their preferences. In this scenario,
    researches claim that the future of music permeates artificial intelligence, which will play 
    the role of composing music that best fits the tastes of consumers. So, extracting patterns 
    from this data is critical and can contribute to the music industry ecosystem. These techniques
    are well known in the field of Musical Information Retrieval. They consist of the audio
    characteristics extraction  (content) or lyrics (context), being the latter preferable because 
    it demands lower computational cost and presenting better results. However, when observing state 
    of the art, it was found that there is a lack of antecedents that investigate the extraction of Brazilian 
    music patterns through lyrics. In this sense, the main goal of this work is to fill this gap through text
    mining techniques, analyzing the songs classification in the subgenres of Brazilian country music.
    This analysis is based on lyrics and knowledge extraction to explain how subgenres differ."
>>> textlytics.charCounter(text)
1118
>>> textlytics.avgWordLen(text)
5.476744186046512
>>> textlytics.wordCounter(text)
172
>>> textlytics.uniqueWordsCounter(text)
114
>>> textlytics.sentencesCounter(text)
8
>>> textlytics.avgWordsSentence(text)
21.5
>>> textlytics.syllableCounter(text)
282
>>> textlytics.avgSyllableWords(text)
1.6395348837209303
>>> textlytics.rareWordsRatio(text)
0.5232558139534884
>>> textlytics.lexical_diversity(text)
0.6627906976744186
>>> textlytics.readability(text)
46.30784883720932
>>> textlytics.readability_schoolarity(text)
'College'
>>> textlytics.posTaggerCounter(text,'VERB')
34.0
>>> textlytics.posTaggerCounter(text,'ADJ')
12.0
>>> textlytics.posTaggerCounter(text,'N')
57.0
>>> textlytics.posTaggerCounter(text,'PRON')
4.0
>>> textlytics.posTaggerCounter(text,'CONTENT')
103.0
>>> textlytics.posTaggerCounter(text,'CONTENT-D')
0.5988372093023255
>>>
>>> # There is a special method that takes a  
>>> # pandas dataframe and extracts all textual features,
>>> # according a name field (dataframe column).
>>> # features2Dataframe(dataframe,fieldName)
>>>
import nltk
from nltk.corpus import stopwords
    
def extract_phrase_funct(x):
    """Extract noun phrases from sentence(s). 
    
    Parameters
    ----------
    x : string
        One string of sentence(s)
    
    Returns
    -------
    final_phrase: list
        Return a list of keywords. 
        One keyword can be composed of several words.
    """
    stop_words = set(stopwords.words('english'))
    
    def leaves(tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()
    
    def get_terms(tree):
        for leaf in leaves(tree):
            term = [w for w,t in leaf if not w in stop_words]
            yield term
    sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
    grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk.RegexpParser(grammar)
    tokens = nltk.regexp_tokenize(x,sentence_re)
    postoks = nltk.tag.pos_tag(tokens) #Part of speech tagging 
    tree = chunker.parse(postoks) #chunking
    terms = get_terms(tree)
    temp_phrases = []
    for term in terms:
        if len(term):
            temp_phrases.append(' '.join(term))
    
    finalPhrase = [w for w in temp_phrases if w] #remove empty lists
    return finalPhrase

def join_tokens_funct(row1):
    row = row1[:]
    row = " ".join(row)
    return row

def tokenize(row):
    return nltk.word_tokenize(row)

def lowercase(row):
    new_row = []
    for word in row:
        new_row.append(word.lower())
    return(new_row)

def split_dash(row):
    new_row = row[:]
    for word in row:
        if "-" in word:
            new_words = word.split('-')
            new_row.remove(word)
            for new_word in new_words:
                new_row.append(new_word.lower())
        if "_" in word:
            new_words = word.split('_')
            new_row.remove(word)
            for new_word in new_words:
                new_row.append(new_word.lower())
    return(new_row)
            
    
def remove_stopwords(row):
    stop_words = stopwords.words('english')
    return [word for word in row if word not in stop_words]
    
    
def lemmatize_text(row1):
    row = row1[:]
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for i in range(0, len(row)):
        row[i] = lemmatizer.lemmatize(row[i])
    return row

def remove_duplicate(x): 
    return list(dict.fromkeys(x))

    
def data_treatment_pandas(data, col_name):
    """Extract keywords and clean them (tokenization, stopwords, lemmatization,
    remove duplicates and some words).
    
    Parameters
    ----------
    data : pandas df
        A df whose we want to extract keywords. 
    col_name : string
        Data column name of the sentences where keywords need to be extracted.

    Returns
    -------
    data_pd : pandas df
        The formeur df (data) with additional new columns.
    """
    
    data_pd = data.copy()
    
    #Key words extraction
    data_pd['KEYWORDS_TAGLINE'] = data_pd[col_name].apply(extract_phrase_funct)
    #Join tokens
    data_pd['KEYWORDS_TAGLINE2'] = data_pd['KEYWORDS_TAGLINE'].apply(join_tokens_funct)
    #Tokenize
    data_pd['KEYWORDS_TAGLINE'] = data_pd['KEYWORDS_TAGLINE2'].apply(tokenize)
    #Lowercase
    data_pd['KEYWORDS_TAGLINE2'] = data_pd['KEYWORDS_TAGLINE'].apply(lowercase)
    #Split dash words
    data_pd['KEYWORDS_TAGLINE'] = data_pd['KEYWORDS_TAGLINE2'].apply(split_dash)
    #Remove stopwords
    data_pd['KEYWORDS_TAGLINE2'] = data_pd['KEYWORDS_TAGLINE'].apply(remove_stopwords)
    #Lemmatization
    data_pd['KEYWORDS_TAGLINE0'] = data_pd['KEYWORDS_TAGLINE2'].apply(lemmatize_text)
    #Remove duplicates
    data_pd['KEYWORDS_TAGLINE'] = data_pd['KEYWORDS_TAGLINE0'].apply(remove_duplicate) 
    del data_pd["KEYWORDS_TAGLINE0"]
    del data_pd["KEYWORDS_TAGLINE2"]
    return data_pd

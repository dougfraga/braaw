import re 
import pandas as pd
import matplotlib.pyplot as plt
import spacy as sp
from collections import Counter


keyword = 'shoppe_C'


df = pd.read_csv(f'analysed_tweets_{keyword}.csv', sep='\t', encoding='utf-8')
nlp = sp.load('pt_core_news_sm')


def count_sentiments(df):
    count = df['analysis'].value_counts(normalize=True).mul(100)
    return count


def count_words(df, keyword):
    
    stopwords = ['', 'a', 'as', 'aqui', 'com', 'como', 'da', 'de', 'do', 'dos',
                 'e', 'é', 'ela', 'ele', 'em', 'essa', 'esse', 'está', 'eu', 'foi',
                 'ir', 'isso', 'já', 'mas', 'mais', 'me', 'meu', 'minha', 'muito', 
                 'na', 'não', 'no', 'o', 'os', 'ou', 'para', 'pela', 'por', 'pra',
                 'q', 'que', 'quem', 'se', 'ser', 'só', 'sobre', 'tem', 'tá', 'tô', 
                 'um', 'uma', 'vai', 'vc', 'você', 'vou']
    
    stopwords_custom = ['achar', 'agora', 'coisa', 'comprar', 'compr', 'fazer',
                        'querer', 'ter', 'ver']
    
    try:
        keyword = keyword.split('_')[0]
    except: 
        pass
    
    stopwords = stopwords + stopwords_custom + keyword.split(' ')
    
    words = ' '.join(df.text).lower()
    
    token_words = nlp(words)
    word_list = []
    for token_word in token_words:
        word_list.append(token_word.lemma_)
    word_list = ' '.join(word_list)
    word_list = re.sub('[)(.,!?]', '', word_list)
    
    words = word_list.split(' ')

    resultwords  = [word for word in words if word not in stopwords]
    
    count = Counter(resultwords).most_common(10)
    word = []
    freq = []
    for w in count:
        word.append(w[0])
        freq.append(w[1])
    
    dfr = pd.DataFrame({'word': word, 'freq': freq}) 
    
    return dfr


if __name__ == '__main__':
    count = count_sentiments(df)
    #count.to_excel(f'sentimentos_{keyword}.xlsx')
    words = count_words(df, keyword)
    fig, ax = plt.subplots(figsize =(16, 9))
    bar_chart = ax.barh(words.word, words.freq)
    ax.invert_yaxis()
    ax.bar_label(bar_chart, labels=words.freq, size=15)
    ax.set_yticklabels(words.word, size=14)
    plt.title(f'Quantidade de palavras ({keyword})', size=20)
    plt.savefig(f'bar_words_{keyword}.png')


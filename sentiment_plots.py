import re 
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


keyword = 'shoppe'


df = pd.read_csv(f'sentimentos_{keyword}.csv', sep='\t', encoding='utf-8')

def count_sentiments(df):
    count = df['analysis'].value_counts(normalize=True).mul(100)
    return count


def count_words(df):
    stopwords = ['', 'da', 'a', 'o', 'do', 'de', 'e', 'que', 'é', 'para',
                 'na', 'no', 'pra', 'com', 'não', 'um', 'se', 'eu', 'em',
                 'os', 'mas', 'foi', 'só', 'uma', 'mais', 'sobre', 'muito',
                 'essa', 'por', 'ele', 'tem', 'ser', 'já', 'dos', 'as',
                 'vai', 'como', 'está', 'quem', 'vc', 'você', 'ou', 'isso',
                 'q', 'pela']
    stopwords = stopwords + keyword.split(' ')
    words = ' '.join(df.text).lower()
    words = re.sub('[.,!?]', '', words)
    words = words.split(' ')
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
    words = count_words(df)
    fig, ax = plt.subplots(figsize =(16, 9))
    bar_chart = ax.barh(words.word, words.freq)
    ax.invert_yaxis()
    ax.bar_label(bar_chart, labels=words.freq, size=15)
    ax.set_yticklabels(words.word, size=14)
    plt.title(f'Quantidade de palavras ({keyword})', size=20)
    plt.savefig(f'bar_words_{keyword}.png')


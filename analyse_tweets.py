import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax


keyword = 'shoppe_N'


def sentAnl(text):
    """Sentiment analysis function"""
    # Load the model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    # Sentiment Analysis
    #encoded_tweet = tokenizer(df['text_en'].to_list(), return_tensors='pt')
    encoded_tweet = tokenizer(text, return_tensors='pt')

    #output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = list(softmax(scores))
    labels = {0:'Negative', 1:'Neutral', 2:'Positive'}
    max_score = scores.index(max(scores))
    analysis = labels[max_score]
    print(analysis)
    return analysis


if __name__ == '__main__':
    df = pd.read_csv(f'tweets_en_{keyword}.csv', sep='\t', encoding='utf-8')
    df['analysis'] = df['text_en'].apply(sentAnl)
    df.to_csv(f'analysed_tweets_{keyword}.csv', sep='\t', encoding='utf-8')
    print(df)

    
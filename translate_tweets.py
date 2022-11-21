import pandas as pd
from googletrans import Translator


keyword = 'shoppe_S'


# Functions
def log_translation(info):
    """Save translated tweets on csv file"""
    try:
        df0 = pd.read_csv(f'{keyword}_en.csv', sep='\t', encoding='utf-8')
        df = pd.DataFrame([info], columns=['en'])
        df = pd.concat([df0, df])        
        df.to_csv(f'{keyword}_en.csv', sep='\t', encoding='utf-8', index=False)      
    except:
        df = pd.DataFrame([info], columns=['en'])
        df.to_csv(f'{keyword}_en.csv', sep='\t', encoding='utf-8', index=False)
        
        
def translate_content(df):
    """Translate content for English"""
    lines = []
    for line in df.text:
        trans = Translator()
        trans_text = trans.translate(line, src="pt", dest="en")
        print(trans_text.text)
        log_translation(trans_text.text)
        lines.append(trans_text.text)
    df['text_en'] = lines
    try:
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass
    df.to_csv(f'tweets_en_{keyword}.csv', sep='\t', encoding='utf-8')
    return df


if __name__ == '__main__':
    df = pd.read_csv(f'tweets_filt_{keyword}.txt', sep='\t', encoding='utf-8')
    df = translate_content(df)
    print(df)

    
    
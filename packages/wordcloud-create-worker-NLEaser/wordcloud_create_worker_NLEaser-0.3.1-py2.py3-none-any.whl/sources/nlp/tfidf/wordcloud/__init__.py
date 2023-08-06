from wordcloud import WordCloud
from nltk.corpus import stopwords


def generate_wordcloud(sentences, language) -> WordCloud:
    """
    Gera um objeto "wordcloud" ja preenchido

    :param sentences: lista de sentenças para gerar o wordcloud
    :param language: idioma das sentenças
    :return: WordCloud gerado a partir das sentenças
    """
    stop_wds = stopwords.words(language)
    text = ' '.join(sentences)
    wcloud = WordCloud(stopwords=stop_wds, collocations=False,
                       width=1968, height=1080)
    wcloud.generate_from_text(text)
    return wcloud

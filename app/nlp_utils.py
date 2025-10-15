# app/nlp_utils.py
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def extract_topics(text, top_n=3):
    """
    OpenAI APIを使わずにTF-IDFで上位の単語を抽出する
    """
    # 記号などを除去
    cleaned = re.sub(r'[^a-zA-Z0-9ぁ-んァ-ン一-龥\s]', '', text)
    cleaned = cleaned.lower()

    # TF-IDFベクトル化
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform([cleaned])

    # スコア順にソート
    scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    topics = [word for word, score in sorted_scores[:top_n]]
    return topics


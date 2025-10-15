# app/nlp_utils.py
import re
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util

# ① KeyBERTモデル
kw_model = KeyBERT('all-MiniLM-L6-v2')

# ② トピック埋め込み用モデル
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# ③ 抽象トピック一覧
ABSTRACT_TOPICS = ["努力", "満足", "学習", "改善", "困難", "感情"]

# ④ トピック埋め込みを事前計算
TOPIC_EMBEDS = embed_model.encode(ABSTRACT_TOPICS, convert_to_tensor=True)

def extract_topics(text, top_n_keywords=5):
    """
    KeyBERTで文章の重要語を抽出し、埋め込み類似度で抽象トピックに自動分類
    """
    # 記号除去
    cleaned = re.sub(r'[^a-zA-Z0-9ぁ-んァ-ン一-龥\s]', '', text)

    # ① KeyBERTで重要語抽出
    keywords = kw_model.extract_keywords(cleaned, top_n=top_n_keywords, keyphrase_ngram_range=(1,2))
    extracted_words = [kw for kw, score in keywords]

    if not extracted_words:
        # キーワードが抽出できなければ文章全体を使う
        extracted_words = [cleaned]

    # ② キーワードを埋め込み
    word_embeds = embed_model.encode(extracted_words, convert_to_tensor=True)

    # ③ コサイン類似度計算
    cosine_scores = util.cos_sim(word_embeds, TOPIC_EMBEDS)  # shape: (num_keywords, num_topics)

    # ④ 最も類似度の高いトピックを抽出
    selected_topics = set()
    for i, word in enumerate(extracted_words):
        topic_idx = cosine_scores[i].argmax().item()
        selected_topics.add(ABSTRACT_TOPICS[topic_idx])

    return list(selected_topics)

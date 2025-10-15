# app/main.py
import streamlit as st
import sqlite3
from nlp_utils import extract_topics
from graph_utils import create_network

# --- DB初期化 ---
def init_db():
    conn = sqlite3.connect("diary.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            topics TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(text, topics):
    conn = sqlite3.connect("diary.db")
    c = conn.cursor()
    c.execute("INSERT INTO diary (text, topics) VALUES (?, ?)", (text, ", ".join(topics)))
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect("diary.db")
    c = conn.cursor()
    c.execute("SELECT id, text, topics FROM diary")
    data = c.fetchall()
    conn.close()
    return data

# --- 初期設定 ---
init_db()
st.title("📝 日記ネットワークアプリ（DB保存版）")

# 📌 日記投稿
with st.form(key='diary_form'):
    diary_text = st.text_area("今日の日記を書いてください")
    submit = st.form_submit_button("投稿")

    if submit and diary_text.strip():
        topics = extract_topics(diary_text)
        save_to_db(diary_text, topics)
        st.success(f"日記を保存しました！ トピック: {topics}")

# 📜 投稿済み日記の一覧表示
diary_data = load_from_db()
if diary_data:
    st.subheader("投稿済み日記一覧")
    for id_, text, topics in diary_data:
        st.markdown(f"**日記{id_}**: {text}")
        st.caption(f"トピック: {topics}")

    # 🌐 ネットワーク表示
    if len(diary_data) >= 2:
        st.subheader("日記ネットワーク")
        data_for_network = [{"text": d[1], "topics": d[2].split(", ")} for d in diary_data]
        net = create_network(data_for_network)
        net.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=500)


import streamlit as st
from nlp_utils import extract_topics
from graph_utils import create_network
from db import init_db, add_entry, load_entries, delete_entry

# 初期化
init_db()

st.title("📝 日記ネットワークアプリ（DB版）")

# 日記投稿フォーム
with st.form(key='diary_form'):
    diary_text = st.text_area("今日の日記を書いてください")
    submit = st.form_submit_button("投稿")
    if submit and diary_text.strip():
        topics = extract_topics(diary_text)
        add_entry(diary_text, topics)
        st.success(f"日記を保存しました！ トピック: {topics}")

# 投稿済み日記の一覧
diary_data = load_entries()
if diary_data:
    st.subheader("投稿済み日記一覧")
    for id_, date, text, topics in diary_data:
        st.markdown(f"**{date}**: {text}")
        st.caption(f"トピック: {topics}")

        # 削除ボタン
        button_key = f"delete_{id_}"
        
        if st.button("削除", key=button_key):
            delete_entry(id_)
            st.success("削除しました。ページを再読み込みすると反映されます。")


# ネットワーク可視化
if len(diary_data) >= 2:
    st.subheader("日記ネットワーク")
    data_for_network = [{"text": d[2], "topics": d[3].split(", ")} for d in diary_data]
    net = create_network(data_for_network)
    net.save_graph("network.html")
    with open("network.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=500)


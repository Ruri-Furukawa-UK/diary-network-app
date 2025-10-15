# app/graph_utils.py
import networkx as nx
from pyvis.network import Network

def create_network(diary_list):
    """
    diary_list: [{"text": ..., "topics": [...]}, ...]
    共通トピックがあればノード同士を接続
    """
    G = nx.Graph()
    
    for idx, diary in enumerate(diary_list):
        G.add_node(idx, label=f"日記{idx+1}", title=diary['text'])
    
    # 共通トピックでエッジを張る
    for i in range(len(diary_list)):
        for j in range(i+1, len(diary_list)):
            common = set(diary_list[i]['topics']) & set(diary_list[j]['topics'])
            if common:
                G.add_edge(i, j, title=", ".join(common), value=len(common))
    
    net = Network(notebook=True, height="500px", width="100%", bgcolor="#ffffff", font_color="black")
    net.from_nx(G)
    return net


import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="絶望要塞風 円形ハッキング", layout="centered")

st.title("密室脱出：セキュリティ・ハッキング")
st.caption("中心のコアを守る回転レーザーを破壊し、セキュリティを解除せよ！")

# 同じフォルダにあるゲーム用HTMLファイルを安全に読み込む
with open("game.html", "r", encoding="utf-8") as f:
    game_html_content = f.read()

# エラーを起こさず安全に画面を埋め込み
components.html(game_html_content, height=660)

st.sidebar.markdown("""
### 潜入ミッション
* **← / → キー**：パドルを移動
* **目的**：中央を回転する防衛レーザーを時間内にすべて破壊せよ。
""")

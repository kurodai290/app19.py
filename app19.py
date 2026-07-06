import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="絶望要塞風 円形ハッキング", layout="centered")

st.title("密室脱出：セキュリティ・ハッキング")
st.caption("中心のコアを守る回転レーザーを破壊し、セキュリティを解除せよ！")

# 100%エラーの起きない確実な埋め込み方式に変更
game_url = "https://github.io"
components.iframe(game_url, height=660, scrolling=False)

st.sidebar.markdown("""
### 潜入ミッション
* **← / → キー**：パドルを移動
* **目的**：中央を回転する防衛レーザー（ブロック）を時間内にすべて破壊せよ。
""")

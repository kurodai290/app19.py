import streamlit as st

st.set_page_config(page_title="絶望要塞風 円形ハッキング", layout="centered")

st.title("密室脱出：セキュリティ・ハッキング")
st.caption("中心のコアを守る回転レーザーを破壊し、セキュリティを解除せよ！")

# 構文エラーを絶対に起こさない外部iframe埋め込み方式に変更
game_url = "https://netlify.app"
st.components.v1.iframe(game_url, height=660, scrolling=False)

st.sidebar.markdown("""
### 潜入ミッション
* **← / → キー**：パドルを移動
* **目的**：中央を回転する防衛レーザー（ブロック）を時間内にすべて破壊せよ。
""")

import streamlit as st
import pandas as pd
import plotly.express as px

st.title('国籍別　日本滞在中の費目別支出')

df = pd.read_csv('FEH_00601030_260202220044.csv')

with st.sidebar:
    item = st.multiselect('費目別支出項目を選択してください',
                          df['滞在中の費目別支出'].unique(),
                          key="item")
    country = st.multiselect('国籍を選択してください',
                             df['国籍'].unique(),
                             key="country")
    year = st.selectbox('年を選択してください',
                          df['年'].unique(),
                          key="year")
    if st.button("リセット"):
        for key in ["item", "country", "year"]:
            if key in st.session_state:
                st.session_state.clear()
                st.experimental_rerun()

df = df[df['年']==year]
if item:
    df = df[df['滞在中の費目別支出'].isin(item)]
if country:
    df = df[df['国籍'].isin(country)]

fig = px.bar(df,
             x="国籍",
             y="支出額",
             color="滞在中の費目別支出",
             labels={'国籍':'国籍','支出額':'支出額【円／人】'})
st.plotly_chart(fig)

df.set_index('国籍',inplace=True)
df = pd.DataFrame(data=df,
                  columns=["滞在中の費目別支出","年","支出額"])
st.dataframe(df, width=800, height=220)

st.caption('※ 出典：観光庁 訪日外国人消費動向調査')

st.divider()

st.subheader('フォーム')
with st.form("my_form"):
    name = st.text_input("名前")
    age = st.slider("年齢", 0, 100)
    text = st.text_area("内容")
    submitted = st.form_submit_button("送信")
    if submitted:
        st.write(f"名前: {name}, 年齢: {age}, 内容: {text}")

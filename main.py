# main.py
import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "박스오피스 10위권에 머문 영화 216편의 데이터를 탐색하고 분포와 관계를 확인합니다."
)


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 데이터 전처리: 세로막대 기호(|)로 분리된 경우 첫 번째 장르만 추출
    df["main_genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0])

    return df


df = load_data()

st.divider()

# -------------------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

# 장르별 편수 집계
genre_counts = df["main_genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 편수"]

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    values="영화 편수",
    names="장르",
    hole=0.4,
    title="장르별 영화 점유율",
)

# 호버 시 편수와 비율(퍼센트) 표시 설정
fig1.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 가이드
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 흥행 상위권에 진입한 영화 중 어떤 장르가 가장 큰 비중을 차지하고 있는지 한눈에 비교할 수 있습니다."
)

st.divider()

# -------------------------------------------------------------------
# 추가 분석 구역 (필요 시 확장 가능)
# -------------------------------------------------------------------
st.subheader("2. 개봉일 스크린수와 총 관객수 관계")

fig2 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="main_genre",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객수",
        "main_genre": "장르",
    },
    title="스크린수 대비 총 관객수 분포",
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 최종 총 관객수도 증가하는 경향이 있는지 상관관계를 파악할 수 있습니다."
)

# main.py
import numpy as np
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

genre_counts = df["main_genre"].value_counts().reset_index()
genre_counts.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_counts,
    values="영화 편수",
    names="장르",
    hole=0.4,
    title="장르별 영화 점유율",
)

fig1.update_traces(
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 흥행 상위권에 진입한 영화 중 어떤 장르가 가장 큰 비중을 차지하고 있는지 한눈에 비교할 수 있습니다."
)

st.divider()

# -------------------------------------------------------------------
# 2. 장르별 영화 관객수 분포 (트리맵 그래프)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), "main_genre", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객수 트리맵",
    color="main_genre",
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 가장 많은 관객을 모았으며, 전체 흥행 관객수에서 차지하는 비중이 얼마나 되는지 계층적으로 파악할 수 있습니다."
)

st.divider()

# -------------------------------------------------------------------
# 3. 총 관객수 분포 (히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="총 관객수 히스토그램",
    labels={"total_audi": "총 관객수", "count": "영화 수"},
)

fig3.update_traces(
    hovertemplate="관객수 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 관객이 많은 영화 계산
max_movie = df.loc[df["total_audi"].idxmax()]
max_movie_name = max_movie["movieNm"]
max_movie_audi = max_movie["total_audi"]

# 가장 많은 영화가 몰려 있는 구간 계산 (20개 구간 기준)
counts, bin_edges = np.histogram(df["total_audi"], bins=20)
max_bin_idx = np.argmax(counts)
bin_start = bin_edges[max_bin_idx]
bin_end = bin_edges[max_bin_idx + 1]

st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 대부분의 영화는 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간({counts[max_bin_idx]}편)에 집중되어 있는 오른쪽으로 긴 꼬리를 가진 분포를 보입니다. "
    f"또한, 이 기간에 가장 많은 관객을 동원한 영화는 **'{max_movie_name}'** (약 {max_movie_audi:,}명)입니다."
)

st.divider()

# -------------------------------------------------------------------
# 4. 개봉일 스크린수와 총 관객수의 관계 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
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
    title="개봉일 스크린수 vs 총 관객수 산점도",
)

fig4.update_traces(
    hovertemplate="<b>영화명: %{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 확보될수록 총 관객수도 증가하는 양의 상관관계가 있는지, 장르별 스크린수 분포 차이가 존재하는지 확인할 수 있습니다."
)

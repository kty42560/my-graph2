# main.py
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")


# 1. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 열이 비어있지 않은 데이터만 추출 후, '|' 기호 기준으로 첫 번째 장르만 선택
    df["genre"] = df["genre"].fillna("기타")
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

# ==========================================
# 1. 첫 번째 그래프: 장르별 영화 편수 (Plotly Donut Chart)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# Plotly 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    values="count",
    names="genre",
    title="장르별 영화 편수 비율",
    hole=0.4,
    hover_data=["count"],
)

fig1.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}",
)

st.plotly_chart(fig1, use_container_width=True)

# 첫 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "박스오피스 상위권 영화 중 특정 장르(예: 드라마, 액션 등)가 차지하는 비중을 파악하여, 관객들에게 가장 대중적으로 소비되는 주요 장르 분포를 한눈에 확인할 수 있습니다."
)

st.divider()

# ==========================================
# 2. 두 번째 그래프: 장르 및 영화별 총 관객수 (Plotly Treemap)
# ==========================================
st.subheader("2. 장르/영화별 총 관객수 분포 (트리맵)")

# Plotly 트리맵 차트 생성
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객수 분포",
    hover_data={"total_audi": ":,d"},
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명"
)

st.plotly_chart(fig2, use_container_width=True)

# 두 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르 전체의 시장 규모뿐만 아니라 장르 내 개별 영화가 흥행에 기여한 비중을 직관적으로 비교할 수 있어, 특정 대작 영화의 쏠림 현상이나 장르별 평균 흥행력을 한눈에 파악할 수 있습니다."
)

st.divider()

# ==========================================
# 3. 세 번째 그래프: 총 관객수 분포 (Plotly Histogram)
# ==========================================
st.subheader("3. 총 관객수 분포 (히스토그램)")

# 최다 관객 영화 정보 자동 추출
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# Plotly 히스토그램 생성
fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객수 분포 히스토그램",
    labels={"total_audi": "총 관객수(명)"},
    color_discrete_sequence=["#636EFA"],
)

fig3.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1,
)

fig3.update_traces(
    hovertemplate="<b>총 관객수 구간: %{x}</b><br>영화 수: %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

# 세 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화가 관객수 **200만 명 이하의 하위 구간**에 집중되어 나타나는 롱테일(Long-tail) 비대칭 분포를 보이며, 가장 관객이 많은 최다 흥행 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,.0f}명)임을 확인할 수 있습니다."
)

st.divider()

# ==========================================
# 4. 네 번째 그래프: 개봉일 스크린수와 총 관객수의 관계 (Plotly Scatter Plot)
# ==========================================
st.subheader("4. 개봉일 스크린수와 총 관객수 관계 (산점도)")

# Plotly 산점도 생성
fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 vs 총 관객수",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객수(명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,d",
        "total_audi": ":,d",
        "genre": True,
    },
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객수 (명)",
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린수: %{x:,.0f}개<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# 네 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "개봉일 스크린수가 많을수록 대체로 총 관객수가 높은 양(+)의 상관관계를 보여주며, 장르별 범례를 클릭해 특정 장르 영화들의 초기 배급 규모와 최종 흥행 결과 간의 패턴을 비교해 볼 수 있습니다."
)

st.divider()

# ==========================================
# 5. 다섯 번째 그래프: 주요 장르별 총 관객수 상자 그림 (Plotly Boxplot)
# ==========================================
st.subheader("5. 주요 장르별 총 관객수 분포 (박스플롯)")

# 영화 수 10편 이상인 장르만 필터링
genre_counts_series = df["genre"].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df["genre"].isin(major_genres)]

# Plotly 박스플롯 생성
fig5 = px.box(
    df_filtered,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    title="영화 수 10편 이상 장르의 총 관객수 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객수(명)",
    },
    hover_data={"total_audi": ":,d"},
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객수 (명)",
    showlegend=False,
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

# 다섯 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르별 관객수의 중위수(중앙값)와 상위 25%~75% 범위를 비교하여 각 장르의 평균적인 흥행 안전성을 파악할 수 있으며, 상자 밖으로 벗어난 이상치 점을 통해 해당 장르의 괄목할 만한 '대박 흥행작'을 식별할 수 있습니다."
)

st.divider()

# ==========================================
# 6. 여섯 번째 그래프: 개봉일 스크린수, 총 관객수, 첫 주 관객수의 관계 (Plotly Bubble Chart)
# ==========================================
st.subheader("6. 개봉일 스크린수, 총 관객수, 첫 주 관객수 관계 (버블 차트)")

# Plotly 버블 차트 생성
fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
    title="개봉일 스크린수 vs 총 관객수 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수(개)",
        "total_audi": "총 관객수(명)",
        "first_week_audi": "개봉 첫 주 관객수(명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,d",
        "total_audi": ":,d",
        "first_week_audi": ":,d",
        "genre": True,
    },
)

fig6.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객수 (명)",
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>개봉일 스크린수: %{x:,.0f}개<br>총 관객수: %{y:,.0f}명<br>첫 주 관객수: %{marker.size:,.0f}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

# 여섯 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "버블의 크기를 통해 개봉 첫 주 관객수를 함께 비교함으로써, 초기 집객력(버블 크기)이 큰 영화가 최종 관객수(Y축) 및 개봉 스크린수(X축)와 어떻게 연결되는지 다차원적으로 분석할 수 있습니다."
)

st.divider()

# ==========================================
# 7. 일곱 번째 그래프: 제작 국가 및 장르별 영화 편수 (Plotly Sunburst)
# ==========================================
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트)")

# 제작 국가와 장르별 영화 편수 집계
nation_genre_counts = (
    df.groupby(["nation", "genre"]).size().reset_index(name="count")
)

# Plotly 선버스트 차트 생성
fig7 = px.sunburst(
    nation_genre_counts,
    path=["nation", "genre"],
    values="count",
    title="제작 국가 → 장르별 영화 편수 구조",
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>상위 항목 대비 비율: %{percentParent:.1%}<br>전체 대비 비율: %{percentRoot:.1%}<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

# 일곱 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "국가별로 제작·배급되는 영화들의 대표 장르 구성비를 한눈에 파악할 수 있으며, 특정 국가(예: 한국, 미국 등)에서 주로 선호되거나 출시되는 주요 장르 세그먼트를 시각적으로 한눈에 비교할 수 있습니다."
)

st.divider()

# ==========================================
# 8. 여덟 번째 그래프: 장르별 총 관객수 분포 (Plotly Scatter Plot)
# ==========================================
st.subheader("8. 어떤 장르가 총 관객 수가 많은지 알려줘")

# Plotly 산점도 생성
fig8 = px.scatter(
    df,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="어떤 장르가 총 관객 수가 많은지 알려줘",
    labels={
        "genre": "장르",
        "total_audi": "총 관객수(명)",
    },
    hover_data={
        "total_audi": ":,d",
        "genre": True,
    },
)

fig8.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객수 (명)",
    showlegend=False,
)

fig8.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>장르: %{customdata[0]}<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig8, use_container_width=True)

# 여덟 번째 그래프 하단 분석 영역
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "각 장르 축에 배열된 개별 영화(점)들의 높낮이를 확인하여, 총 관객수가 1,000만 명을 상회하는 흥행 대작들이 어떤 장르에 집중 분포해 있는지 한눈에 비교할 수 있습니다."
)

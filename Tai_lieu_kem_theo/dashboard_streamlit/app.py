from pathlib import Path
import os

import plotly.graph_objects as go
import streamlit as st

from data_model import (GROUPS, filter_customers, product_totals, read_snapshot,
                        response_groups, statistics, vi_number)

st.set_page_config(page_title="Phân tích khách hàng", page_icon="📊", layout="wide")
DATA_FILE = Path(os.environ.get("MARKETING_DATA_FILE", str(Path(__file__).resolve().parent.parent.parent / "marketing_clean_powerbi.csv")))

st.markdown("""
<style>
.stApp { background: #f5f7fb; }
.block-container { max-width: 1320px; padding-top: 1.7rem; padding-bottom: 1rem; }
header[data-testid="stHeader"] { background: transparent; }
h1 { font-size: 2rem !important; color: #152d4b; letter-spacing: -.03em; }
[data-testid="stMetric"] { background: white; border: 1px solid #e2e8f0 !important;
  border-radius: 14px; padding: 17px 18px; box-shadow: 0 2px 5px #152d4b04; }
[data-testid="stMetricValue"] { font-size: clamp(1.4rem, 2.3vw, 1.85rem); color: #152d4b; }
[data-testid="stMetricLabel"] { color: #65758b; }
[data-testid="stPlotlyChart"] { background: white; border: 1px solid #e2e8f0;
  border-radius: 14px; padding: 8px; }
.topline { font-size: .78rem; font-weight: 600; letter-spacing: .12em; color: #48758c; }
.live { display: inline-block; color: #16825d; background: #e8f6ef;
  border-radius: 30px; padding: 5px 12px; font-size: .85rem; }
</style>
""", unsafe_allow_html=True)

title, badge = st.columns([4, 1.2])
with title:
    st.markdown('<div class="topline">TRỰC QUAN HÓA DỮ LIỆU</div>', unsafe_allow_html=True)
    st.title("Phân tích khách hàng")
    st.caption("Chi tiêu theo sản phẩm và phản hồi marketing")
with badge:
    st.markdown('<div style="height:28px"></div><span class="live">● Tự cập nhật · 30 giây</span>', unsafe_allow_html=True)


def reset_filters():
    st.session_state["age_filter"] = (18, 89)
    st.session_state["parent_filter"] = "Tất cả"


def chart_layout(fig, title, **kwargs):
    fig.update_layout(title=dict(text=title, font=dict(size=17, color="#152d4b")),
        height=380, margin=dict(l=20, r=28, t=58, b=40), paper_bgcolor="white",
        plot_bgcolor="white", font=dict(family="Segoe UI, Arial", size=12, color="#52647b"),
        showlegend=False, **kwargs)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#edf1f6", zeroline=False)
    return fig


@st.fragment(run_every="30s")
def dashboard():
    try:
        snapshot = read_snapshot(DATA_FILE)
    except ValueError as exc:
        st.error(str(exc))
        st.caption("Tự thử đọc lại mỗi 30 giây khi trang đang mở.")
        return

    age_col, parent_col, reset_col = st.columns([2.2, 1.5, 1])
    if "age_filter" not in st.session_state:
        st.session_state["age_filter"] = (18, 89)
    if "parent_filter" not in st.session_state:
        st.session_state["parent_filter"] = "Tất cả"
    with age_col:
        ages = st.slider("Khoảng tuổi", 18, 89, value=None, key="age_filter")
    with parent_col:
        parent_label = st.selectbox("Tình trạng có con", ["Tất cả", "Có con", "Không có con"], key="parent_filter")
    with reset_col:
        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)
        st.button("Đặt lại bộ lọc", on_click=reset_filters, width="stretch")

    parent = {"Tất cả": None, "Có con": 1, "Không có con": 0}[parent_label]
    selected = filter_customers(snapshot.frame, ages, parent)
    result = statistics(selected)
    st.caption(f"Đang xem {vi_number(len(selected))} / {vi_number(len(snapshot.frame))} khách hàng")

    metrics = st.columns(4)
    values = [("Số khách hàng", vi_number(result["customers"])),
              ("Tổng chi tiêu (ĐVTT)", vi_number(result["spent"])),
              ("Thu nhập TB (ĐVTT)", vi_number(result["income"], 2)),
              ("Tỷ lệ phản hồi", vi_number(result["response"], 2) + ("%" if result["response"] is not None else ""))]
    for container, (label, value) in zip(metrics, values):
        container.metric(label, value)
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    if selected.empty:
        st.info("Không có khách hàng phù hợp với bộ lọc. Thử chọn khoảng tuổi hoặc tình trạng có con khác.")
    else:
        left, right = st.columns(2)
        products = product_totals(selected)
        fig = go.Figure(go.Bar(x=products["Chi tiêu"], y=products["Sản phẩm"], orientation="h",
            marker_color="#377ac3", text=[vi_number(x) for x in products["Chi tiêu"]],
            textposition="outside", cliponaxis=False,
            hovertemplate="%{y}<br>Chi tiêu: %{text} ĐVTT<extra></extra>"))
        chart_layout(fig, "Chi tiêu theo nhóm sản phẩm")
        fig.update_yaxes(autorange="reversed", showgrid=False)
        fig.update_xaxes(title="Tổng chi tiêu (ĐVTT)", showgrid=True, gridcolor="#edf1f6", range=[0, products["Chi tiêu"].max() * 1.24 or 1])
        with left:
            st.plotly_chart(fig, width="stretch", key="products_chart", config={"displayModeBar": False},
                alt="Biểu đồ thanh ngang so sánh tổng chi tiêu của sáu nhóm sản phẩm theo bộ lọc.")
        groups = response_groups(selected)
        fig2 = go.Figure(go.Bar(x=[x.replace("Chi tiêu ", "") for x in groups["Nhóm"]], y=groups["Tỷ lệ"],
            marker_color=["#9bc1e8", "#42a8a5", "#285f9c"],
            text=[vi_number(x, 2) + "%" if n else "" for x, n in zip(groups["Tỷ lệ"], groups["Khách hàng"])],
            textposition="outside", cliponaxis=False,
            customdata=groups["Khách hàng"], hovertemplate="Nhóm chi tiêu %{x}<br>Tỷ lệ: %{text}<br>Số khách hàng: %{customdata}<extra></extra>"))
        chart_layout(fig2, "Phản hồi theo nhóm chi tiêu")
        fig2.update_xaxes(title="Nhóm chi tiêu", tickvals=["thấp", "trung bình", "cao"], ticktext=["Chi tiêu thấp", "Chi tiêu trung bình", "Chi tiêu cao"])
        fig2.update_yaxes(title="Tỷ lệ phản hồi (%)", ticksuffix="%", range=[0, max(10, groups["Tỷ lệ"].max() * 1.25)])
        with right:
            st.plotly_chart(fig2, width="stretch", key="response_chart", config={"displayModeBar": False},
                alt="Biểu đồ cột so sánh tỷ lệ phản hồi chiến dịch gần nhất của ba nhóm chi tiêu.")
    st.caption(f"Nguồn: {DATA_FILE.name}  ·  Đọc dữ liệu lúc {snapshot.read_at.strftime('%H:%M:%S %d/%m/%Y')}  ·  Tự đọc lại mỗi 30 giây khi trang đang mở")


dashboard()

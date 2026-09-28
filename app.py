import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Hotel Manager",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "hotel_data.json"

# =========================================================
# CSS GIAO DIỆN
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f6f8fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hotel-title {
        font-size: 32px;
        font-weight: 700;
        color: #17324d;
        margin-bottom: 0;
    }

    .hotel-subtitle {
        color: #718096;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e7edf3;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .room-card {
        background: white;
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid #e6ebf0;
    }

    .room-number {
        font-size: 22px;
        font-weight: 700;
        color: #17324d;
    }

    .room-type {
        color: #718096;
        font-size: 14px;
    }

    .status-available {
        color: #16803c;
        font-weight: 700;
    }

    .status-occupied {
        color: #c53030;
        font-weight: 700;
    }

    .status-cleaning {
        color: #b7791f;
        font-weight: 700;
    }

    .status-maintenance {
        color: #805ad5;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background-color: #17324d;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e7edf3;
    }

    .stButton button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DỮ LIỆU MẶC ĐỊNH
# =========================================================

DEFAULT_DATA = {
    "rooms": [
        {"id": 101, "type": "Standard", "floor": 1, "price": 450000, "status": "Trống"},
        {"id": 102, "type": "Standard", "floor": 1, "price": 450000, "status": "Đang ở"},
        {"id": 103, "type": "Deluxe", "floor": 1, "price": 650000, "status": "Trống"},
        {"id": 104, "type": "Deluxe", "floor": 1, "price": 650000, "status": "Dọn phòng"},
        {"id": 201, "type": "Standard", "floor": 2, "price": 450000, "status": "Trống"},
        {"id": 202, "type": "Deluxe", "floor": 2, "price": 650000, "status": "Đang ở"},{"id": 203, "type": "Suite", "floor": 2, "price": 950000, "status": "Trống"},
        {"id": 204, "type": "Suite", "floor": 2, "price": 950000, "status": "Bảo trì"},
        {"id": 301, "type": "Standard", "floor": 3, "price": 450000, "status": "Trống"},
        {"id": 302, "type": "Deluxe", "floor": 3, "price": 650000, "status": "Trống"},
        {"id": 303, "type": "Suite", "floor": 3, "price": 950000, "status": "Đang ở"},
        {"id": 304, "type": "Suite", "floor": 3, "price": 950000, "status": "Trống"},
    ],
    "customers": [],
    "bookings": [],
    "payments": []
}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.data, f, ensure_ascii=False, indent=2)


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# =========================================================
# HÀM HỖ TRỢ
# =========================================================

def money(value):
    return f"{value:,.0f} ₫"


def get_room(room_id):
    for room in data["rooms"]:
        if room["id"] == room_id:
            return room
    return None


def status_class(status):
    mapping = {
        "Trống": "status-available",
        "Đang ở": "status-occupied",
        "Dọn phòng": "status-cleaning",
        "Bảo trì": "status-maintenance"
    }
    return mapping.get(status, "")


def booking_total(checkin, checkout, price):
    nights = max((checkout - checkin).days, 1)
    return nights * price


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px 0 25px 0;">
        <div style="font-size:42px;">🏨</div>
        <div style="font-size:24px;font-weight:700;">HOTEL MANAGER</div>
        <div style="font-size:13px;opacity:.75;">Quản lý khách sạn</div>
    </div>
    """,
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "MENU",
    [
        "📊 Tổng quan",
        "🛏️ Quản lý phòng",
        "📅 Đặt phòng",
        "👤 Khách hàng",
        "💳 Thanh toán",
        "📈 Doanh thu",
        "⚙️ Cài đặt"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Hotel Management System")
st.sidebar.caption("Streamlit • Python")


# =========================================================
# TỔNG QUAN
# =========================================================

if menu == "📊 Tổng quan":

    st.markdown('<div class="hotel-title">Tổng quan khách sạn</div>', unsafe_allow_html=True)
    st.markdown('<div class="hotel-subtitle">Theo dõi tình trạng phòng và hoạt động kinh doanh</div>',
        unsafe_allow_html=True
    )

    rooms = data["rooms"]

    total_rooms = len(rooms)
    available = len([r for r in rooms if r["status"] == "Trống"])
    occupied = len([r for r in rooms if r["status"] == "Đang ở"])
    cleaning = len([r for r in rooms if r["status"] == "Dọn phòng"])
    maintenance = len([r for r in rooms if r["status"] == "Bảo trì"])

    occupancy = (occupied / total_rooms * 100) if total_rooms else 0

    total_revenue = sum(
        p.get("amount", 0) for p in data["payments"]
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🏨 Tổng phòng", total_rooms)
    c2.metric("🟢 Phòng trống", available)
    c3.metric("🔴 Đang ở", occupied)
    c4.metric("🧹 Dọn phòng", cleaning)
    c5.metric("🔧 Bảo trì", maintenance)

    st.markdown("---")

    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Tình trạng phòng")

        df_status = pd.DataFrame({
            "Trạng thái": [
                "Trống",
                "Đang ở",
                "Dọn phòng",
                "Bảo trì"
            ],
            "Số phòng": [
                available,
                occupied,
                cleaning,
                maintenance
            ]
        })

        st.bar_chart(
            df_status.set_index("Trạng thái")
        )

    with right:
        st.subheader("Tỷ lệ lấp đầy")

        st.metric(
            "Công suất phòng",
            f"{occupancy:.1f}%"
        )

        st.progress(
            min(occupancy / 100, 1.0)
        )

        st.markdown("---")

        st.metric(
            "💰 Tổng doanh thu",
            money(total_revenue)
        )

    st.markdown("---")

    st.subheader("Phòng đang sử dụng")

    occupied_rooms = [
        r for r in rooms if r["status"] == "Đang ở"
    ]

    if occupied_rooms:
        cols = st.columns(4)

        for i, room in enumerate(occupied_rooms):
            with cols[i % 4]:
                st.markdown(
                    f"""
                    <div class="room-card">
                        <div class="room-number">Phòng {room['id']}</div>
                        <div class="room-type">{room['type']}</div>
                        <br>
                        <div class="status-occupied">🔴 Đang ở</div>
                        <div>{money(room['price'])}/đêm</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("Hiện không có phòng đang được sử dụng.")


# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":st.markdown('<div class="hotel-title">Quản lý phòng</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hotel-subtitle">Theo dõi, cập nhật và quản lý trạng thái từng phòng</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        filter_floor = st.selectbox(
            "Tầng",
            ["Tất cả"] + sorted(
                list(set(str(r["floor"]) for r in data["rooms"]))
            )
        )

    with col2:
        filter_type = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + sorted(
                list(set(r["type"] for r in data["rooms"]))
            )
        )

    with col3:
        filter_status = st.selectbox(
            "Trạng thái",
            ["Tất cả", "Trống", "Đang ở", "Dọn phòng", "Bảo trì"]
        )

    filtered_rooms = data["rooms"]

    if filter_floor != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if str(r["floor"]) == filter_floor
        ]

    if filter_type != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if r["type"] == filter_type
        ]

    if filter_status != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if r["status"] == filter_status
        ]

    st.markdown("---")

    cols = st.columns(4)

    for i, room in enumerate(filtered_rooms):

        with cols[i % 4]:

            color_class = status_class

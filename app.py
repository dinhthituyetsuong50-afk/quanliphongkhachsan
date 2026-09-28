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
        {"id": 202, "type": "Deluxe", "floor": 2, "price": 650000, "status": "Đang ở"},
        {"id": 203, "type": "Suite", "floor": 2, "price": 950000, "status": "Trống"},
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
    st.markdown(
        '<div class="hotel-subtitle">Theo dõi tình trạng phòng và hoạt động kinh doanh</div>',
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

elif menu == "🛏️ Quản lý phòng":

    st.markdown('<div class="hotel-title">Quản lý phòng</div>', unsafe_allow_html=True)
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

            color_class = status_class(room["status"])

            st.markdown(
                f"""
                <div class="room-card">
                    <div class="room-number">
                        🛏️ {room['id']}
                    </div>

                    <div class="room-type">
                        {room['type']} • Tầng {room['floor']}
                    </div>

                    <br>

                    <div class="{color_class}">
                        {room['status']}
                    </div>

                    <div style="margin-top:8px;font-weight:600;">
                        {money(room['price'])}/đêm
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            new_status = st.selectbox(
                "Trạng thái",
                ["Trống", "Đang ở", "Dọn phòng", "Bảo trì"],
                index=[
                    "Trống",
                    "Đang ở",
                    "Dọn phòng",
                    "Bảo trì"
                ].index(room["status"]),
                key=f"status_{room['id']}"
            )

            if new_status != room["status"]:

                room["status"] = new_status
                save_data()

                st.success(
                    f"Đã cập nhật phòng {room['id']}"
                )

                st.rerun()


# =========================================================
# ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.markdown('<div class="hotel-title">Đặt phòng</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hotel-subtitle">Tạo và quản lý booking của khách</div>',
        unsafe_allow_html=True
    )

    available_rooms = [
        r for r in data["rooms"]
        if r["status"] == "Trống"
    ]

    if not available_rooms:
        st.warning("Hiện không có phòng trống.")
    else:

        with st.form("booking_form"):

            st.subheader("Thông tin đặt phòng")

            c1, c2 = st.columns(2)

            with c1:
                customer_name = st.text_input(
                    "Họ và tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

                id_number = st.text_input(
                    "CCCD / Hộ chiếu"
                )

            with c2:
                room_id = st.selectbox(
                    "Chọn phòng *",
                    [r["id"] for r in available_rooms]
                )

                checkin = st.date_input(
                    "Ngày nhận phòng",
                    date.today()
                )

                checkout = st.date_input(
                    "Ngày trả phòng",
                    date.today()
                )

            note = st.text_area(
                "Ghi chú"
            )

            submit = st.form_submit_button(
                "➕ Tạo đặt phòng",
                use_container_width=True
            )

        if submit:

            if not customer_name or not phone:
                st.error(
                    "Vui lòng nhập họ tên và số điện thoại."
                )

            elif checkout <= checkin:
                st.error(
                    "Ngày trả phòng phải sau ngày nhận phòng."
                )

            else:

                room = get_room(room_id)

                total = booking_total(
                    checkin,
                    checkout,
                    room["price"]
                )

                customer = {
                    "id": len(data["customers"]) + 1,
                    "name": customer_name,
                    "phone": phone,
                    "id_number": id_number
                }

                data["customers"].append(customer)

                booking = {
                    "id": len(data["bookings"]) + 1,
                    "customer_id": customer["id"],
                    "customer_name": customer_name,
                    "phone": phone,
                    "room_id": room_id,
                    "room_type": room["type"],
                    "checkin": str(checkin),
                    "checkout": str(checkout),
                    "total": total,
                    "note": note,
                    "status": "Đã đặt",
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                data["bookings"].append(booking)

                room["status"] = "Đang ở"

                save_data()

                st.success(
                    f"Đặt phòng thành công! Tổng tiền: {money(total)}"
                )

    st.markdown("---")
    st.subheader("Danh sách đặt phòng")

    if data["bookings"]:

        booking_df = pd.DataFrame(
            data["bookings"]
        )

        columns = [
            "id",
            "customer_name",
            "phone",
            "room_id",
            "checkin",
            "checkout",
            "total",
            "status"
        ]

        booking_df = booking_df[
            [c for c in columns if c in booking_df.columns]
        ]

        booking_df.columns = [
            "Mã",
            "Khách hàng",
            "SĐT",
            "Phòng",
            "Nhận phòng",
            "Trả phòng",
            "Tổng tiền",
            "Trạng thái"
        ]

        st.dataframe(
            booking_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Chưa có đặt phòng nào.")


# =========================================================
# KHÁCH HÀNG
# =========================================================

elif menu == "👤 Khách hàng":

    st.markdown('<div class="hotel-title">Khách hàng</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hotel-subtitle">Quản lý thông tin khách lưu trú</div>',
        unsafe_allow_html=True
    )

    with st.form("customer_form"):

        c1, c2, c3 = st.columns(3)

        with c1:
            name = st.text_input("Họ và tên")

        with c2:
            phone = st.text_input("Số điện thoại")

        with c3:
            id_number = st.text_input("CCCD / Hộ chiếu")

        add_customer = st.form_submit_button(
            "➕ Thêm khách hàng",
            use_container_width=True
        )

    if add_customer:

        if not name or not phone:
            st.error("Vui lòng nhập họ tên và số điện thoại.")

        else:

            customer = {
                "id": len(data["customers"]) + 1,
                "name": name,
                "phone": phone,
                "id_number": id_number
            }

            data["customers"].append(customer)

            save_data()

            st.success("Đã thêm khách hàng.")

    st.markdown("---")

    if data["customers"]:

        df = pd.DataFrame(
            data["customers"]
        )

        df.columns = [
            "Mã khách",
            "Họ tên",
            "Số điện thoại",
            "CCCD / Hộ chiếu"
        ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Chưa có dữ liệu khách hàng.")


# =========================================================
# THANH TOÁN
# =========================================================

elif menu == "💳 Thanh toán":

    st.markdown('<div class="hotel-title">Thanh toán</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hotel-subtitle">Ghi nhận và quản lý các khoản thanh toán</div>',
        unsafe_allow_html=True
    )

    if not data["bookings"]:
        st.info("Chưa có booking để thanh toán.")

    else:

        booking_options = {
            f"#{b['id']} - {b['customer_name']} - Phòng {b['room_id']}":
            b
            for b in data["bookings"]
        }

        selected = st.selectbox(
            "Chọn booking",
            list(booking_options.keys())
        )

        booking = booking_options[selected]

        st.info(
            f"Khách: **{booking['customer_name']}** | "
            f"Phòng: **{booking['room_id']}** | "
            f"Tổng tiền: **{money(booking['total'])}**"
        )

        with st.form("payment_form"):

            amount = st.number_input(
                "Số tiền thanh toán",
                min_value=0,
                value=int(booking["total"]),
                step=50000
            )

            method = st.selectbox(
                "Phương thức",
                [
                    "Tiền mặt",
                    "Chuyển khoản",
                    "Thẻ ngân hàng",
                    "Ví điện tử"
                ]
            )

            payment_date = st.date_input(
                "Ngày thanh toán",
                date.today()
            )

            submit_payment = st.form_submit_button(
                "💳 Xác nhận thanh toán",
                use_container_width=True
            )

        if submit_payment:

            payment = {
                "id": len(data["payments"]) + 1,
                "booking_id": booking["id"],
                "customer_name": booking["customer_name"],
                "room_id": booking["room_id"],
                "amount": amount,
                "method": method,
                "date": str(payment_date)
            }

            data["payments"].append(payment)

            save_data()

            st.success("Thanh toán đã được ghi nhận.")

    st.markdown("---")

    st.subheader("Lịch sử thanh toán")

    if data["payments"]:

        payment_df = pd.DataFrame(
            data["payments"]
        )

        payment_df["amount"] = payment_df["amount"].apply(
            money
        )

        payment_df.columns = [
            "Mã",
            "Booking",
            "Khách hàng",
            "Phòng",
            "Số tiền",
            "Phương thức",
            "Ngày"
        ]

        st.dataframe(
            payment_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Chưa có giao dịch.")


# =========================================================
# DOANH THU
# =========================================================

elif menu == "📈 Doanh thu":

    st.markdown('<div class="hotel-title">Báo cáo doanh thu</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hotel-subtitle">Theo dõi tình hình doanh thu của khách sạn</div>',
        unsafe_allow_html=True
    )

    payments = data["payments"]

    total_revenue = sum(
        p["amount"] for p in payments
    )

    total_transactions = len(payments)

    average = (
        total_revenue / total_transactions
        if total_transactions
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Tổng doanh thu",
        money(total_revenue)
    )

    c2.metric(
        "🧾 Giao dịch",
        total_transactions
    )

    c3.metric(
        "📊 Giá trị TB/giao dịch",
        money(average)
    )

    st.markdown("---")

    if payments:

        df = pd.DataFrame(payments)

        df["date"] = pd.to_datetime(
            df["date"]
        )

        revenue_by_date = (
            df.groupby("date")["amount"]
            .sum()
            .reset_index()
        )

        revenue_by_date = revenue_by_date.set_index(
            "date"
        )

        st.subheader("Doanh thu theo ngày")

        st.line_chart(
            revenue_by_date["amount"]
        )

        st.subheader("Chi tiết doanh thu")

        display_df = df.copy()

        display_df["amount"] = display_df["amount"].apply(
            money
        )

        display_df.columns = [
            "Mã",
            "Booking",
            "Khách hàng",
            "Phòng",
            "Số tiền",
            "Phương thức",
            "Ngày"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "Chưa có dữ liệu doanh thu."
        )


# =========================================================
# CÀI ĐẶT
# =========================================================

elif menu == "⚙️ Cài đặt":

    st.markdown('<div class="hotel-title">Cài đặt hệ thống</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hotel-subtitle">Quản lý dữ liệu và cấu hình hệ thống</div>',
        unsafe_allow_html=True
    )

    st.subheader("Thông tin khách sạn")

    with st.form("hotel_settings"):

        hotel_name = st.text_input(
            "Tên khách sạn",
            value="HOTEL MANAGER"
        )

        address = st.text_input(
            "Địa chỉ",
            value="Thành phố Hồ Chí Minh"
        )

        phone = st.text_input(
            "Số điện thoại",
            value="0900000000"
        )

        save_settings = st.form_submit_button(
            "💾 Lưu thông tin",
            use_container_width=True
        )

    if save_settings:
        st.success("Đã lưu thông tin khách sạn.")

    st.markdown("---")

    st.subheader("Dữ liệu hệ thống")

    st.write(
        f"🏨 Tổng số phòng: **{len(data['rooms'])}**"
    )

    st.write(
        f"👤 Tổng khách hàng: **{len(data['customers'])}**"
    )

    st.write(
        f"📅 Tổng booking: **{len(data['bookings'])}**"
    )

    st.write(
        f"💳 Tổng giao dịch: **{len(data['payments'])}**"
    )

    st.markdown("---")

    if st.button(
        "⚠️ Khôi phục dữ liệu mẫu",
        use_container_width=True
    ):

        st.session_state.data = DEFAULT_DATA.copy()
        save_data()

        st.success(
            "Đã khôi phục dữ liệu mẫu."
        )

        st.rerun()

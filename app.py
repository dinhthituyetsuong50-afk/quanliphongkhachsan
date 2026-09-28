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

            color_class = status_class

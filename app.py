
import streamlit as st
from datetime import datetime
import io
st.image("TRASUA.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Quản lý Bill Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# =========================
# DỮ LIỆU MENU
# =========================

tra_sua = {
    "Trà sữa truyền thống": 25000,
    "Trà sữa matcha": 30000,
    "Trà sữa socola": 30000,
    "Trà sữa dâu": 30000,
    "Trà sữa khoai môn": 30000,
    "Trà sữa ô long": 28000,
    "Trà sữa thái xanh": 28000,
    "Trà sữa thái đỏ": 28000,
}

topping = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch dừa": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 8000,
}

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 QUẢN LÝ BILL TRÀ SỮA")
st.write("Nhập thông tin đơn hàng bên dưới")

st.divider()

# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.subheader("👤 Thông tin khách hàng")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

# =========================
# CHỌN TRÀ SỮA
# =========================
st.subheader("🧋 Chọn trà sữa")

loai_tra = st.selectbox(
    "Loại trà sữa",
    list(tra_sua.keys())
)

gia_tra = tra_sua[loai_tra]

so_luong = st.number_input(
    "Số lượng",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

# =========================
# TOPPING
# =========================
st.subheader("🍡 Chọn topping")

danh_sach_topping = st.multiselect(
    "Topping",
    list(topping.keys())
)

# Số lượng topping
so_luong_topping = {}

if danh_sach_topping:
    st.write("**Số lượng từng topping:**")

    for tp in danh_sach_topping:
        so_luong_topping[tp] = st.number_input(
            f"{tp} ({format_money(topping[tp])}/phần)",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
            key=f"topping_{tp}"
        )

# =========================
# MỨC ĐỘ ĐƯỜNG
# =========================
st.subheader("🍬 Mức độ đường")

duong = st.radio(
    "Chọn mức đường",
    ["100%", "0%"],
    horizontal=True
)

# =========================
# MỨC ĐỘ ĐÁ
# =========================
st.subheader("🧊 Mức độ đá")

da = st.radio(
    "Chọn mức đá",
    ["100%", "70%", "0%"],
    horizontal=True
)

st.divider()

# =========================
# TÍNH TIỀN
# =========================

tien_tra = gia_tra * so_luong

tien_topping = 0

for tp in danh_sach_topping:
    tien_topping += topping[tp] * so_luong_topping[tp]

tong_tien = tien_tra + tien_topping

# =========================
# HIỂN THỊ KẾT QUẢ
# =========================

st.subheader("📋 THÔNG TIN ĐƠN HÀNG")

if ten_khach.strip() == "":
    ten_hien_thi = "Chưa nhập tên"
else:
    ten_hien_thi = ten_khach

st.write(f"**👤 Khách hàng:** {ten_hien_thi}")
st.write(f"**🧋 Loại trà sữa:** {loai_tra}")
st.write(f"**🔢 Số lượng:** {so_luong}")
st.write(f"**🍬 Đường:** {duong}")
st.write(f"**🧊 Đá:** {da}")

st.write("**🍡 Topping:**")

if danh_sach_topping:
    for tp in danh_sach_topping:
        sl = so_luong_topping[tp]
        thanh_tien_tp = topping[tp] * sl

        st.write(
            f"- {tp}: {sl} phần × {format_money(topping[tp])} "
            f"= {format_money(thanh_tien_tp)}"
        )
else:
    st.write("- Không có topping")

st.divider()

# =========================
# CHI TIẾT THANH TOÁN
# =========================

st.write(f"**Tiền trà sữa:** {format_money(tien_tra)}")
st.write(f"**Tiền topping:** {format_money(tien_topping)}")

st.subheader(
    f"💰 TỔNG THANH TOÁN: {format_money(tong_tien)}"
)

# =========================
# THANH TOÁN
# =========================

if st.button("💳 THANH TOÁN & XUẤT HÓA ĐƠN", use_container_width=True):

    if ten_khach.strip() == "":
        st.warning("⚠️ Vui lòng nhập tên khách hàng trước khi thanh toán.")
    else:

        # Thời gian thanh toán
        thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # =========================
        # TẠO NỘI DUNG HÓA ĐƠN
        # =========================

        hoa_don = ""
        hoa_don += "========================================\n"
        hoa_don += "          HÓA ĐƠN TRÀ SỮA\n"
        hoa_don += "========================================\n"
        hoa_don += f"Khách hàng: {ten_khach}\n"
        hoa_don += f"Thời gian: {thoi_gian}\n"
        hoa_don += "----------------------------------------\n"

        hoa_don += "THÔNG TIN ĐỒ UỐNG\n"
        hoa_don += f"Trà sữa: {loai_tra}\n"
        hoa_don += f"Số lượng: {so_luong}\n"
        hoa_don += f"Đường: {duong}\n"
        hoa_don += f"Đá: {da}\n"

        hoa_don += "----------------------------------------\n"

        hoa_don += "TOPPING\n"

        if danh_sach_topping:
            for tp in danh_sach_topping:
                sl = so_luong_topping[tp]
                thanh_tien_tp = topping[tp] * sl

                hoa_don += (
                    f"{tp}: {sl} phần - "
                    f"{format_money(thanh_tien_tp)}\n"
                )
        else:
            hoa_don += "Không có topping\n"

        hoa_don += "----------------------------------------\n"

        hoa_don += f"Tiền trà sữa: {format_money(tien_tra)}\n"
        hoa_don += f"Tiền topping: {format_money(tien_topping)}\n"

        hoa_don += "========================================\n"
        hoa_don += f"TỔNG THANH TOÁN: {format_money(tong_tien)}\n"
        hoa_don += "========================================\n"
        hoa_don += "       CẢM ƠN QUÝ KHÁCH!\n"
        hoa_don += "========================================\n"

        # =========================
        # THÔNG BÁO THANH TOÁN
        # =========================

        st.success("✅ Thanh toán thành công!")

        st.write(
            f"Khách hàng **{ten_khach}** cần thanh toán "
            f"**{format_money(tong_tien)}**."
        )

        # =========================
        # TẠO TÊN FILE
        # =========================

        ten_file = (
            "hoa_don_"
            + ten_khach.strip().replace(" ", "_")
            + "_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        # =========================
        # NÚT TẢI HÓA ĐƠN
        # =========================

        st.download_button(
            label="📄 TẢI HÓA ĐƠN",
            data=hoa_don,
            file_name=ten_file,
            mime="text/plain",
            use_container_width=True
        )

        # =========================
        # XEM HÓA ĐƠN
        # =========================

        with st.expander("👀 Xem hóa đơn"):
            st.code(hoa_don)

# pages/2_Admin_Duyet.py
import streamlit as st
from modules.theme import apply_olympiad_theme
from modules.database import lay_tai_lieu_cho_duyet, cap_nhat_trang_thai

# Áp dụng giao diện tối mịn màng đồng bộ
apply_olympiad_theme(page_type="other")

st.title("🛡️ Bảng Điều Khiển Admin Kiểm Duyệt")
st.write("Nơi xem xét và phê duyệt các chuyên đề do thành viên đóng góp lên hệ thống.")

# Lấy danh sách từ Supabase
danh_sach_cho = lay_tai_lieu_cho_duyet()

if not danh_sach_cho:
    st.info("🎈 Tuyệt vời! Hiện tại không có tài liệu nào đang xếp hàng chờ duyệt.")
else:
    st.warning(f"⏳ Có {len(danh_sach_cho)} tài liệu cần bạn xét duyệt.")
    st.markdown("---")
    
    for item in danh_sach_cho:
        id_tl, ten_tl, chuyen_de, nguoi_gop, lien_ket, mo_ta, trang_thai = item
        
        with st.container():
            st.markdown(f"### 📄 {ten_tl}")
            st.markdown(f"👤 **Người gửi:** {nguoi_gop} | 🏷️ **Chuyên đề:** {chuyen_de}")
            st.markdown(f"🔗 **Liên kết tài liệu:** [Bấm vào đây để kiểm tra nội dung]({lien_ket})")
            if mo_ta:
                st.info(f"💬 **Mô tả từ tác giả:** {mo_ta}")
            
            # Tạo 2 nút bấm Duyệt / Từ chối nằm ngang nhau
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Phê duyệt xuất bản #{id_tl}", key=f"duyet_{id_tl}"):
                    if cap_nhat_trang_thai(id_tl, "Đã duyệt"):
                        st.success("Đã duyệt tài liệu thành công!")
                        st.rerun()
            with col2:
                if st.button(f"❌ Từ chối / Xóa #{id_tl}", key=f"huy_{id_tl}"):
                    if cap_nhat_trang_thai(id_tl, "Từ chối"):
                        st.warning("Đã từ chối tài liệu này.")
                        st.rerun()
            st.markdown("---")
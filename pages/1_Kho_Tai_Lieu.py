# pages/1_Kho_Tai_Lieu.py
import streamlit as st
from modules.theme import apply_olympiad_theme
from modules.database import them_tai_lieu, lay_tai_lieu_da_duyet, upload_file_to_storage

apply_olympiad_theme(page_type="other")

st.title("📚 Kho Tài Liệu Học Tập Chuyên Toán")
st.write("Nơi lưu trữ và chia sẻ các tài liệu hình học phẳng, đại số, tổ hợp chất lượng cao.")

# Phân hệ 1: Đóng góp tài liệu
with st.expander("✨ Đóng góp tài liệu học tập của bạn vào hệ thống"):
    with st.form("form_dong_gop", clear_on_submit=False): # Đổi thành False để tránh mất dữ liệu khi lỗi
        ten_tl = st.text_input("Tên tài liệu / Chuyên đề:")
        chuyen_de = st.selectbox("Phân loại chuyên đề:", ["Hệ phương trình", "Phương trình vô tỉ", "Hình học phẳng", "Bất đẳng thức", "Khác"])
        nguoi_gop = st.text_input("Tên người đóng góp / Biệt danh:")
        mo_ta = st.text_area("Mô tả tóm tắt nội dung tài liệu:")
        
        # Cho phép chọn hình thức nộp tài liệu
        hinh_thuc = st.radio("Hình thức gửi tài liệu:", ["Tải file trực tiếp (.pdf, .docx)", "Dán liên kết URL (Google Drive, OneDrive...)"], horizontal=True)
        
        file_tailieu = None
        lien_ket_input = ""
        
        if hinh_thuc == "Tải file trực tiếp (.pdf, .docx)":
            file_tailieu = st.file_uploader("Chọn file tài liệu từ máy tính của bạn:", type=["pdf", "docx", "doc", "png", "jpg"])
        else:
            lien_ket_input = st.text_input("Liên kết tải tài liệu:")
            
        submit = st.form_submit_button("Gửi tài liệu kiểm duyệt")
        
        if submit:
            if ten_tl and nguoi_gop:
                final_link = ""
                
                # Xử lý nếu người dùng chọn tải file trực tiếp
                if hinh_thuc == "Tải file trực tiếp (.pdf, .docx)":
                    if file_tailieu is not None:
                        with st.spinner("⏳ Đang tải file lên hệ thống Cloud Supabase..."):
                            final_link = upload_file_to_storage(file_tailieu)
                    else:
                        st.error("⚠️ Bạn chưa chọn file nào từ máy tính!")
                        st.stop()
                else:
                    final_link = lien_ket_input
                
                # Tiến hành lưu vào Database sau khi đã có link file
                if final_link:
                    if them_tai_lieu(ten_tl, chuyen_de, nguoi_gop, final_link, mo_ta):
                        st.success("🎉 Gửi tài liệu và tệp tin thành công! Tài liệu đã được lưu trữ an toàn trên Cloud và chờ Admin duyệt.")
                    else:
                        st.error("❌ Đã xảy ra lỗi khi lưu thông tin vào cơ sở dữ liệu.")
            else:
                st.error("⚠️ Vui lòng điền đầy đủ Tên tài liệu và Tên người đóng góp.")

st.markdown("---")

# Phân hệ 2: Hiển thị tài liệu theo bộ lọc chuyên đề (Giữ nguyên phần code hiển thị bên dưới của em...)
st.subheader("🔍 Tìm kiếm chuyên đề toán")
bo_loc = st.selectbox("Chọn chuyên đề muốn học:", ["Tất cả", "Hệ phương trình", "Phương trình vô tỉ", "Hình học phẳng", "Bất đẳng thức", "Khác"])

chuyen_de_Query = None if bo_loc == "Tất cả" else bo_loc
danh_sach = lay_tai_lieu_da_duyet(chuyen_de_Query)

if not danh_sach:
    st.info("Hiện tại chưa có tài liệu nào thuộc chuyên đề này được duyệt công khai.")
else:
    for item in danh_sach:
        with st.container():
            st.markdown(f"### 📄 [{item[1]}]({item[4]})")
            st.caption(f"Người đóng góp: **{item[3]}** | Chuyên đề: **{item[2]}**")
            if item[5]:
                st.write(f"💬 *Mô tả:* {item[5]}")
            st.markdown("---")
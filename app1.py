import streamlit as st
import pandas as pd
import base64
import os

# 1. Cấu hình tiêu đề tab trình duyệt
st.set_page_config(page_title="THCS Math Optimizer", page_icon="🧮", layout="wide")

# Khởi tạo kho dữ liệu tài liệu tổng hợp trong session_state để có thể cập nhật động
if "kho_tai_lieu" not in st.session_state:
    st.session_state.kho_tai_lieu = [
        {
            "Tên tài liệu": "Chuyên đề Hệ phương trình đối xứng loại I và II",
            "Chuyên mục": "Hành trang ôn thi HSG",
            "Dạng bài": "Hệ phương trình",
            "Định dạng": "PDF",
            "Link tải": "https://drive.google.com/file/d/1O_csoXQne-8hzSoxW6QL5T6TgugP4uH1/view?usp=drive_link"
        },
        {
            "Tên tài liệu": "Phương pháp thế và cộng đại số nâng cao trong đề thi HSG",
            "Chuyên mục": "Hành trang ôn thi HSG",
            "Dạng bài": "Hệ phương trình",
            "Định dạng": "DOCX",
            "Link tải": "https://drive.google.com/file/d/1O_csoXQne-8hzSoxW6QL5T6TgugP4uH1/view?usp=drive_link"
        },
        {
            "Tên tài liệu": "Bất đẳng thức Cauchy và kỹ thuật chọn điểm rơi",
            "Chuyên mục": "Hành trang ôn thi HSG",
            "Dạng bài": "Bất đẳng thức",
            "Định dạng": "PDF",
            "Link tải": "https://drive.google.com/your-link-3"
        }
    ]

# Hàm mã hóa ảnh sang Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

bg_euler_base64 = get_base64_image("bg_euler.jpg")
bg_geometry1_base64 = get_base64_image("bg_geometry1.jpg")

st.title("The THCS Math Optimizer - Nền tảng tối ưu hóa Toán THCS")
st.write("Nền tảng được tạo bởi Lê Trung Hiếu")

# Thanh điều hướng (Sidebar)
chuyen_muc = st.sidebar.selectbox(
    "Chọn chuyên mục học tập:",
    ["Trang chủ", "Hành trang ôn thi HSG", "Bí kíp Máy tính cầm tay (MTCT)", "Trợ lý AI Toán học", "Không gian Chia sẻ Tri thức"]
)

# --- HÀM 2: XỬ LÝ LƯU FILE VÀ CẬP NHẬT ĐỘNG VÀO HỆ THỐNG DỮ LIỆU ---
def xu_ly_va_hien_thi_file(khoi_chua_file):
    file_upload = st.file_uploader(f"Đóng góp tài liệu của bạn (PDF, PNG, JPG) tại đây:", type=["pdf", "png", "jpg"], key=f"upload_{khoi_chua_file}")
    
    if file_upload is not None:
        folder_luu_tru = "tai_lieu_dong_gop"
        if not os.path.exists(folder_luu_tru):
            os.makedirs(folder_luu_tru)
        
        duong_dan_file = os.path.join(folder_luu_tru, file_upload.name)
        with open(duong_dan_file, "wb") as f:
            f.write(file_upload.getbuffer())
            
        # Kiểm tra xem tài liệu này đã được lưu vào hệ thống dữ liệu chưa, tránh trùng lặp khi rerun
        ten_cac_file = [t["Tên tài liệu"] for t in st.session_state.kho_tai_lieu]
        if file_upload.name not in ten_cac_file:
            
            # Đảm bảo đồng bộ chuẩn phân loại trực tiếp theo khối đang gọi nó
            if khoi_chua_file == "Chuyen_Muc_Rieng":
                dang_bai_phan_loai = "Chưa phân loại"
            else:
                dang_bai_phan_loai = khoi_chua_file
            
            # Chuyển đổi toàn bộ dấu gạch chéo ngược '\' thành '/' để tạo liên kết chuẩn Markdown URL
            duong_dan_tuyet_doi = os.path.abspath(duong_dan_file).replace("\\", "/")
            
            new_doc = {
                "Tên tài liệu": file_upload.name,
                "Chuyên mục": "Người dùng đóng góp",
                "Dạng bài": dang_bai_phan_loai,
                "Định dạng": file_upload.name.split(".")[-1].upper(),
                "Link tải": f"file:///{duong_dan_tuyet_doi}" 
            }
            st.session_state.kho_tai_lieu.append(new_doc)
            
            # Ép Streamlit chạy lại ngay lập tức để đồng bộ dữ liệu lên bảng tổng hợp và danh sách hiển thị
            st.rerun()
            
        st.success(f"🎉 Cảm ơn đóng góp của bạn! Tài liệu đã được tích hợp vào hệ thống.")
        
        # Xem trước tài liệu trực tuyến
        st.markdown("### 📄 Xem trước tài liệu trực tuyến:")
        duoi_file = file_upload.name.split(".")[-1].lower()
        
        if duoi_file in ["png", "jpg", "jpeg"]:
            st.image(duong_dan_file, caption=f"Ảnh: {file_upload.name}", use_container_width=True)
        elif duoi_file == "pdf":
            with open(duong_dan_file, "rb") as pdf_file:
                base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

# --- HÀM 1 ĐÃ CẬP NHẬT: TỰ ĐỘNG HIỂN THỊ TÀI LIỆU VÀ TẠO NÚT TẢI CHO FILE CỤC BỘ ---
def hien_thi_tai_lieu_theo_dang(dang_bai):
    xu_ly_va_hien_thi_file(dang_bai)
    
    st.write("---")
    st.markdown(f"#### 📚 Tài liệu tham khảo của Chuyên đề: **{dang_bai}**")
    
    df_hien_tai = pd.DataFrame(st.session_state.kho_tai_lieu)
    df_loc = df_hien_tai[df_hien_tai["Dạng bài"] == dang_bai]
    
    if not df_loc.empty:
        for index, row in df_loc.iterrows():
            st.markdown(f"📄 **[{row['Định dạng']}]** {row['Tên tài liệu']}")
            
            link_tai = row['Link tải']
            
            # Trường hợp 1: Nếu là đường link trực tuyến công khai (HTTP/HTTPS) -> Hiện link thường
            if link_tai.startswith("http://") or link_tai.startswith("https://"):
                st.markdown(f"👉 [📥 Truy cập / Tải tài liệu tại đây]({link_tai})")
            
            # Trường hợp 2: Nếu là file hệ thống cục bộ (file:///) -> Chuyển thành nút bấm Download an toàn
            else:
                duong_dan_thuc_te = link_tai.replace("file:///", "")
                
                if os.path.exists(duong_dan_thuc_te):
                    with open(duong_dan_thuc_te, "rb") as file_download:
                        file_bytes = file_download.read()
                    
                    st.download_button(
                        label=f"📥 Tải file {row['Tên tài liệu']} về máy",
                        data=file_bytes,
                        file_name=row['Tên tài liệu'],
                        mime="application/octet-stream",
                        key=f"dl_{dang_bai}_{index}"
                    )
                else:
                    st.caption("⚠️ File không tồn tại trên hệ thống cục bộ.")
    else:
        st.caption("Chưa có tài liệu nào được tải lên cho mục này.")
    st.write("")

# 4. Xử lý logic hiển thị nội dung theo từng mục bấm
if chuyen_muc == "Trang chủ":
    chosen_bg = bg_geometry1_base64 if bg_geometry1_base64 else bg_euler_base64

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{chosen_bg}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(10, 15, 30, 0.65);
            backdrop-filter: blur(4px);
            z-index: -1;
        }}
        .bento-card {{
            background-color: rgba(20, 25, 35, 0.85);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(0, 255, 136, 0.2);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            height: 100%;
            color: white;
        }}
        .bento-card:hover {{
            border-color: #00ff88;
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 255, 136, 0.2);
        }}
        .bento-title {{
            color: #00ff88;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .bento-desc {{
            color: #cbd5e1;
            font-size: 16px;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #00ff88; margin-top: 20px;'>CHÀO MỪNG ĐẾN VỚI LỚP HỌC TOÁN TỐI ƯU</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #aaa;'>Nơi Toán học không chỉ là những con số, mà là một nghệ thuật tư duy.</p>", unsafe_allow_html=True)
    st.write("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        html_khong_gian = """
            <div class="bento-card">
                <div class="bento-title">Không gian Chia sẻ Tri thức</div>
                <p class="bento-desc">
                    Đây là nơi dành cho bạn! Hãy tải lên những <b>chuyên đề tự soạn</b>, những <b>cách giải độc đáo</b> 
                    hoặc những sơ đồ tư duy toán học sáng tạo. Cùng nhau, chúng ta xây dựng một kho tàng toán học mở.
                </p>
            </div>
        """
        st.markdown(html_khong_gian, unsafe_allow_html=True)
        
    with col2:
        html_tro_ly = """
            <div class="bento-card">
                <div class="bento-title">Trợ lý AI</div>
                <p class="bento-desc">Gặp khó với một bài hình học hay đại số phức tạp? Trợ lý AI luôn sẵn sàng hỗ trợ gợi ý hướng giải quyết bài toán 24/7.</p>
            </div>
        """
        st.markdown(html_tro_ly, unsafe_allow_html=True)

    st.write("") 

    c1, c2, c3 = st.columns(3)

    with c1:
        html_hsg = """
            <div class="bento-card">
                <div class="bento-title">HSG Prep</div>
                <p class="bento-desc">Chinh phục các kỳ thi học sinh giỏi, thi chuyên với lộ trình các chuyên đề chuyên sâu.</p>
            </div>
        """
        st.markdown(html_hsg, unsafe_allow_html=True)

    with c2:
        html_casio = """
            <div class="bento-card">
                <div class="bento-title">Casio Tips</div>
                <p class="bento-desc">Làm chủ Máy tính cầm tay để tối ưu tối đa tốc độ làm bài và kiểm tra đáp số.</p>
            </div>
        """
        st.markdown(html_casio, unsafe_allow_html=True)

    with c3:
        html_art = """
            <div class="bento-card">
                <div class="bento-title">Math Art</div>
                <p class="bento-desc">Khám phá vẻ đẹp bất bất tận của hình học sơ cấp và tính đối xứng trong Toán học.</p>
            </div>
        """
        st.markdown(html_art, unsafe_allow_html=True)

elif chuyen_muc == "Hành trang ôn thi HSG":
    st.subheader("🏆 Chuyên đề Luyện thi Học sinh giỏi")
    st.write("Các chuyên đề trọng tâm trong chương trình Toán THCS.")
    
    # --- EXPANDER 1: HỆ PHƯƠNG TRÌNH ---
    with st.expander("📘 HỆ PHƯƠNG TRÌNH", expanded=True):
        col_co_ban, col_nang_cao, col_tài_liệu = st.columns(3)
        with col_co_ban:
            if st.button("🌱 Kiến thức Cơ bản", use_container_width=True):
                st.session_state.level = "co_ban"
        with col_nang_cao:
            if st.button("🔥 Luyện thi Nâng cao", use_container_width=True):
                st.session_state.level = "nang_cao"
        with col_tài_liệu:
            if st.button("📚 Tài liệu tham khảo", use_container_width=True):
                st.session_state.level = "tai_lieu"

        if "level" in st.session_state:
            st.markdown("---")
            if st.session_state.level == "co_ban":
                st.markdown("### 📚 Nội dung Kiến thức Cơ bản")
                st.write("HỆ PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN CÓ DẠNG:")
                st.latex(r"\begin{cases} ax + by = c \\ a_1x + b_1y = c_1 \end{cases}")
                
                html_co_ban_text = """
                - <b>Nghiệm của hệ phương trình:</b> Là cặp số (x0, y0) khi cặp số đó thỏa mãn cả hai phương trình trong hệ.
                - <b>Hệ vô nghiệm:</b> Nếu không có giá trị nào thỏa mãn thì hệ phương trình vô nghiệm.
                - <b>Hệ có vô số nghiệm:</b> Nếu hai phương trình tương đương với nhau.
                <br><br>
                <b>CÁC PHƯƠNG PHÁP GIẢI HỆ PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN:</b>
                <br>
                I. Phương pháp thế.
                """
                st.markdown(html_co_ban_text, unsafe_allow_html=True)

                st.markdown('<p style="margin-left: 30px; margin-bottom: 0px;">Biến đổi hệ về dạng sau:</p>', unsafe_allow_html=True)
                st.latex(r"\quad \begin{cases} y = \frac{c - ax}{b} \\ a_1x + b_1y = c_1 \end{cases}")
                st.markdown(r"Thế $y$ vào phương trình thứ hai để giải tiếp $x$ rồi suy ra $y$.")
                st.write("")
                st.write("II. Phương pháp cộng đại số.")
                st.markdown(r"Tìm $k$ sao cho $a = ka_1$ hoặc $b = kb_1$")
                st.write("Biến đổi hệ về dạng sau:")
                st.latex(r"\begin{cases} ax + by = c \\ k(a_1x + b_1y) = kc_1 \end{cases}")
                st.write("Suy ra hệ phương trình mới có dạng:")
                st.latex(r"\begin{cases} ax + by = c \quad (1) \\ ax + kb_1y = kc_1 \quad (2) \end{cases}")
                st.write("Trừ (2) cho (1) để loại bỏ x, sau đó giải tiếp để tìm nghiệm.")
                st.markdown(r"**CHÚ Ý:** Phương pháp cộng đại số có thể áp dụng để loại bỏ $y$ nếu tìm được $k$ sao cho $b = kb_1$. Giải tương tự như trên để tìm nghiệm.")
                st.write("*Cách nhanh nhất là bấm máy tính cầm tay để giải hệ phương trình này, nhưng cần nắm chắc cách nhập liệu và kiểm tra đáp số để tránh sai sót.")
                
            elif st.session_state.level == "nang_cao":
                st.markdown("### 🔥 Nội dung Luyện thi Nâng cao")
                st.write("Đây là các nội dung và kỹ thuật giải theo kinh nghiệm và kiến thức tổng hợp mà cá nhân tôi tích lũy được.")
                st.markdown("#### I. Các dạng toán Hệ phương trình chứa tham số m, hệ đối xứng loại I, loại II và đẳng cấp.")
                
                # --- EXPANDER DẠNG 1 ---
                with st.expander("📌 DẠNG 1: HỆ PHƯƠNG TRÌNH ĐỐI XỨNG LOẠI I (Bấm để xem/thu gọn)", expanded=False):
                    st.markdown("#### 📝 1. Định nghĩa & Cấu trúc")
                    st.markdown("Hệ phương trình đối xứng loại 1 (ẩn $x$ và $y$) là hệ phương trình mà khi ta hoán đổi vị trí của $x$ và $y$ cho nhau trong bất kỳ phương trình nào của hệ, thì hệ phương trình đó vẫn không thay đổi. Cụ thể, hệ phương trình đối xứng loại 1 có dạng:")
                    st.latex(r"\begin{cases} f(x, y) = 0 \\ g(y, x) = 0 \end{cases}")
                    st.markdown("Trong đó, $f$ và $g$ là các hàm số đối xứng, nghĩa là $f(x, y) = f(y, x)$ and $g(y, x) = g(x, y)$ cho mọi giá trị của $x$ và $y$.")
                    
                    st.markdown("#### 💡 2. Cách giải")
                    st.markdown("- **Phương pháp đặt ẩn phụ:** Đặt $S = x + y$ và $P = xy$, sau đó chuyển hệ phương trình về dạng mới theo $S$ và $P$ để giải.")
                    
                    st.markdown("#### 🧠 3. Một số biến đổi biểu thức đối xứng thường gặp")
                    st.markdown(r"Nếu $S = x + y$ và $P = xy$, thì ta có:")
                    st.latex(r"x^2 + y^2 = S^2 - 2P")
                    st.latex(r"x^3 + y^3 = S^3 - 3PS")
                    
                    # --- BÀI TẬP TỰ LUYỆN DẠNG 1 ---
                    with st.expander("📝 BÀI TẬP TỰ LUYỆN HPT ĐỐI XỨNG LOẠI I (Có đáp án)", expanded=False):
                        st.markdown("### **Bài tập 1:**")
                        st.latex(r"\begin{cases} x + y + 2xy = 2 \\ x^3 + y^3 = 8 \end{cases}")
                        if st.checkbox("Xem đáp án Bài 1"):
                            st.markdown(r"👉 **Đáp số:** Hệ có 2 nghiệm là $(2; 0)$ và $(0; 2)$.")
                
                # --- EXPANDER DẠNG 2 ---
                with st.expander("📌 DẠNG 2: HỆ PHƯƠNG TRÌNH ĐỐI XỨNG LOẠI II (Bấm để xem/thu gọn)", expanded=False):
                    st.markdown("#### 📝 1. Định nghĩa & Cấu trúc")
                    st.latex(r"\begin{cases} f(x, y) = 0 \\ f(y, x) = 0 \end{cases}")
                    
                    with st.expander("🔍 PHƯƠNG PHÁP: Trừ vế theo vế để đưa về phương trình tích (Hay dùng nhất)", expanded=False):
                        st.markdown("**Ý tưởng:** Trừ vế với vế hai phương trình của hệ để làm xuất hiện nhân tử chung là $(x - y)$.")
                        st.latex(r"\begin{cases} x^2 =3x +2y \quad (1)  \\ y^2 =3y +2x \quad (2) \end{cases}")
                        st.markdown(r"Lấy PT (1) trừ PT (2) vế theo vế ta thu được: $(x - y)(x + y - 1) = 0$.")

                # --- EXPANDER DẠNG 3 ---
                with st.expander("📌 DẠNG 3: HỆ PHƯƠNG TRÌNH ĐỐI XỨNG ĐẲNG CẤP (Bấm để xem/thu gọn)", expanded=False):
                    st.markdown("#### 📝 1. Định nghĩa & Cấu trúc")
                    st.latex(r"\begin{cases} f^k(x, y) = c_1 \\ g^k(y, x) = c_2 \end{cases}")
                    st.markdown(r"Trong đó, $f(x, y)$ và $g(y, x)$ là các đa thức bậc $k$, $k$ là một số nguyên dương hoặc $\frac{1}{2}$, và $c_1$, $c_2$ là các hằng số.")

                # --- EXPANDER DẠNG 4 ---
                with st.expander("📌 DẠNG 4: HỆ PHƯƠNG TRÌNH CHỨA THAM SỐ (Bấm để xem/thu gọn)", expanded=False):
                    st.markdown("#### 📝 1. Định nghĩa & Cấu trúc")
                    st.markdown("Trong đó, $f$ và $g$ là các hàm số chứa tham số $m$.")

                st.markdown("---")
                st.markdown("#### II. Các công thức và kỹ thuật giải nhanh")
                with st.expander("1: SỬ DỤNG PHƯƠNG PHÁP HỆ SỐ BẤT ĐỊNH ĐỂ GIẢI HỆ PHƯƠNG TRÌNH", expanded=False):
                    st.markdown("📌 **1.1 Định nghĩa:** Kỹ thuật cân bằng hệ số nhằm tạo ra phương trình tích hoặc tổng bình phương lý tưởng.")

            elif st.session_state.level == "tai_lieu":
                st.markdown("### 📚 Tài liệu và các trang web tham khảo")
                col1, col2 = st.columns([2, 1])
                with col1:
                    tu_khoa = st.text_input("🔍 Nhập tên tài liệu cần tìm:", key="tim_tai_lieu")
                with col2:
                    df_bien = pd.DataFrame(st.session_state.kho_tai_lieu)
                    cac_dang = ["Tất cả"] + list(df_bien["Dạng bài"].unique())
                    dang_chon = st.selectbox("🎯 Lọc theo dạng bài:", cac_dang, key="loc_tai_lieu")
                
                df_goc_ket_qua = pd.DataFrame(st.session_state.kho_tai_lieu)
                if tu_khoa:
                    df_goc_ket_qua = df_goc_ket_qua[df_goc_ket_qua["Tên tài liệu"].str.contains(tu_khoa, case=False)]
                if dang_chon != "Tất cả":
                    df_goc_ket_qua = df_goc_ket_qua[df_goc_ket_qua["Dạng bài"] == dang_chon]
                
                st.write("---")
                if not df_goc_ket_qua.empty:
                    for index, row in df_goc_ket_qua.iterrows():
                        st.markdown(f"📄 **[{row['Định dạng']}]** {row['Tên tài liệu']} *(Phân loại: {row['Dạng bài']})*")
                        
                        # Xử lý hiển thị link/nút tải cho trang tìm kiếm tài liệu nhỏ
                        if row['Link tải'].startswith("http://") or row['Link tải'].startswith("https://"):
                            st.markdown(f"👉 [📥 Tải tài liệu tại đây]({row['Link tải']})")
                        else:
                            path_goc = row['Link tải'].replace("file:///", "")
                            if os.path.exists(path_goc):
                                with open(path_goc, "rb") as f_search:
                                    st.download_button(label=f"📥 Tải file {row['Tên tài liệu']} về máy", data=f_search.read(), file_name=row['Tên tài liệu'], mime="application/octet-stream", key=f"src_{index}")
                        st.write("")
                else:
                    st.warning("Không tìm thấy tài liệu nào phù hợp với bộ lọc.")

            st.write("")
            if st.button("❌ Đóng nội dung"):
                del st.session_state.level
                st.rerun()

        # ==========================================
        # Tự động chèn kho dữ liệu và công cụ đóng góp xuống cuối expander Chuyên đề Hệ phương trình
        # ==========================================
        st.write("---")
        hien_thi_tai_lieu_theo_dang("Hệ phương trình")

    # --- EXPANDER 2: PHƯƠNG TRÌNH VÔ TỈ ---
    with st.expander("📘 PHƯƠNG TRÌNH VÔ TỈ", expanded=False):
        st.markdown("📌 **1.1 Định nghĩa:** Phương trình vô tỉ là phương trình chứa ẩn dưới dấu căn bậc hai.")
        
        # Tự động chèn kho dữ liệu và công cụ đóng góp xuống cuối expander Chuyên đề Phương trình vô tỉ
        st.write("---")
        hien_thi_tai_lieu_theo_dang("Phương trình vô tỉ")

elif chuyen_muc == "Bí kíp Máy tính cầm tay (MTCT)":
    st.subheader("⚡ Tối ưu hóa tốc độ với Casio")
    st.write("Các mẹo dùng tính năng Table, SOLVE để xử lý nhanh trắc nghiệm và kiểm tra đáp số.")

elif chuyen_muc == "Trợ lý AI Toán học":
    st.subheader("🤖 Trợ lý AI thông minh")
    cau_hoi = st.text_input("Nhập bài toán bạn đang gặp khó khăn vào đây:")
    if cau_hoi:
        st.success(f"Hệ thống ghi nhận câu hỏi: {cau_hoi}")

elif chuyen_muc == "Không gian Chia sẻ Tri thức":
    st.subheader("📚 Không gian Chia sẻ Tri thức Tổng hợp")
    st.write("Đây là trung tâm lưu trữ toàn bộ các tài liệu học tập của hệ thống.")
    
    # Hiển thị trình tải lên và tự động xếp vào nhóm riêng biệt trên trang tổng hợp
    xu_ly_va_hien_thi_file("Chuyen_Muc_Rieng")
    
    st.write("---")
    st.markdown("### 📋 Danh sách toàn bộ tài liệu hiện có trên hệ thống:")
    df_all = pd.DataFrame(st.session_state.kho_tai_lieu)
    
    # Sử dụng st.column_config.LinkColumn để định dạng cột "Link tải" thành các hyperlink chuyên nghiệp
    st.dataframe(
        df_all, 
        column_config={
            "Link tải": st.column_config.LinkColumn(
                "Link tải",
                help="Bấm trực tiếp vào đường link để xem hoặc tải tài liệu",
                display_text="Mở/Tải tài liệu" # Rút gọn link dài thành nhãn hiển thị gọn gàng
            )
        },
        hide_index=True, # Ẩn cột số index (0, 1, 2) cho giao diện sạch sẽ
        use_container_width=True
    )
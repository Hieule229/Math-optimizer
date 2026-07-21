# modules/theme.py
import streamlit as st
import base64
import os

def apply_olympiad_theme(page_type="other"):
    """
    Applies unified Dark Themes based on parameter.
    page_type="home" -> Matrix Geometry Background Image
    page_type="other" -> Solid Deep Dark Background (Easy to read formulas)
    """
    if page_type == "home":
        # KHÔNG GIAN TRANG CHỦ: Ảnh nền toán học ma trận tối
        possible_paths = ["bg_geometry1.jpg", "../bg_geometry1.jpg", "thcs_math_optimizer/bg_geometry1.jpg"]
        base64_image = ""
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode()
                break

        if base64_image:
            bg_style = f"""
                background-image: url("data:image/jpg;base64,{base64_image}") !important;
                background-size: cover !important;
                background-position: center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            """
        else:
            bg_style = "background-color: #0e1117 !important;"
            
        main_text_color = "#ffffff"
        heading_color = "#f4ebd0"
        shadow_style = "text-shadow: 1px 1px 3px rgba(0,0,0,0.8);"
    else:
        # KHÔNG GIAN TRANG PHỤ (TRỢ LÝ AI): Nền tối mịn màng (Deep Charcoal)
        # Giúp công thức toán học và văn bản màu trắng hiển thị sắc nét nhất
        bg_style = "background: #0e1117 !important;" 
        main_text_color = "#f5f6f8" 
        heading_color = "#d4af37" # Tiêu đề màu vàng gold hổ phách sang trọng
        shadow_style = "text-shadow: none;"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Spectral:ital,wght=0,400;0,600;1,400&display=swap');
        
        html, body, [data-testid="stSidebar"] {{
            font-family: 'Spectral', serif !important;
        }}
        
        /* ĐỒNG BỘ NỀN TỐI CHO TOÀN BỘ ỨNG DỤNG */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            {bg_style}
            color: {main_text_color} !important;
        }}
        
        /* Khối block nội dung chính */
        [data-testid="stVerticalBlock"] > div {{
            background-color: transparent !important;
            color: {main_text_color} !important;
        }}

        /* THANH SIDEBAR MÀU XANH CHÀM ĐẬM - CỐ ĐỊNH */
        [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {{
            background-color: #1c2d42 !important;
            background-image: none !important;
        }}
        
        /* SỬA LỖI CHỮ BỊ ẨN TRÊN SIDEBAR: Ép tất cả văn bản, danh sách trang phải có màu sáng */
        [data-testid="stSidebar"] *, 
        [data-testid="stSidebarNav"] *, 
        [data-testid="stSidebarNav"] li a span,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {{
            color: #f4ebd0 !important;
        }}
        
        /* Hiệu ứng khi rê chuột vào tên trang ở sidebar */
        [data-testid="stSidebarNav"] li a:hover span {{
            color: #ffffff !important;
            font-weight: bold;
        }}
        
        /* Tiêu đề chính */
        h1, h2, h3, h4, h5, h6 {{
            color: {heading_color} !important;
            font-weight: 600 !important;
            {shadow_style}
        }}
        
        /* Văn bản nội dung */
        p, span, label, li, a, small, .stMarkdown, [data-testid="stMarkdownContainer"] p {{
            color: {main_text_color} !important;
        }}
        
        /* Khung chat và văn bản chat hiển thị rõ ràng trên nền tối */
        .stChatMessage, [data-testid="stChatMessageContent"] p {{
            color: #ffffff !important;
        }}
        
        /* Định dạng nút bấm màu vàng hổ phách */
        .stButton>button {{
            background-color: #d4af37 !important;
            color: #1c2d42 !important;
            border-radius: 4px !important;
            border: 1px solid #b89321 !important;
            font-weight: 600 !important;
        }}
    </style>
    """, unsafe_allow_html=True)
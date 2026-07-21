# pages/3_Tro_Ly_AI.py
import streamlit as st
from modules.theme import apply_olympiad_theme
from modules.ai_assistant import get_ai_response
import streamlit as st
import os

# Ép hệ thống nạp mã khóa từ secrets.toml vào biến môi trường của Google
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

apply_olympiad_theme()
apply_olympiad_theme(page_type="other")
st.title("🤖 Trợ Lý Toán Học Socratic AI")
st.write("Trợ lý sử dụng mô hình trí tuệ nhân tạo Gemini của Google, được định hình phong cách sư phạm giảng dạy chuyên sâu, không giải hộ mà dẫn dắt tư duy.")

# Khởi tạo bộ nhớ lưu lịch sử chat của Streamlit nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các tin nhắn cũ trong cuộc trò chuyện
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cấu hình lời nhắc hệ thống (System Prompt) định hình tính cách cho Gemini
PROMPT_SOCRATIC = """
You are an expert mathematical mentor for high school Olympiad students. 
Your teaching philosophy follows the Socratic method: Never provide the full solution directly. 
Instead, break down complex math problems into small intuitive steps, ask guiding questions, 
praise original thoughts, and nudge the student to find the pattern or theorem themselves.
Respond in Vietnamese cleanly using LaTeX for equations.
"""

# Ô nhận câu hỏi đầu vào từ học sinh
if user_input := st.chat_input("Nhập bài toán hoặc câu hỏi về định lý bạn đang thắc mắc tại đây..."):
    # Hiển thị tin nhắn của học sinh lên màn hình
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Kích hoạt AI suy nghĩ và phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Gemini đang phân tích tư duy toán học..."):
            ai_reply = get_ai_response(st.session_state.messages, PROMPT_SOCRATIC)
            st.markdown(ai_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
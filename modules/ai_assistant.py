# modules/ai_assistant.py
import streamlit as st
from google import genai
from google.genai import types

def get_ai_response(messages_history, system_prompt: str):
    """Streams responses from Google Gemini API safely with environment secrets."""
    if "GEMINI_API_KEY" not in st.secrets:
        return "⚠️ Chế độ Demo: Khóa API GEMINI_API_KEY chưa được cấu hình tại file secrets.toml. Vui lòng thêm khóa để kích hoạt Trợ lý AI thực tế."
        
    try:
        # Khởi tạo Client bằng SDK mới nhất của Google
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Thiết lập cấu hình hệ thống (System Instruction) để định hình phong cách Socratic
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            max_output_tokens=2048
        )
        
        # Chuyển đổi lịch sử chat của Streamlit sang định dạng chuẩn của Gemini SDK
        contents = []
        for msg in messages_history:
            role_map = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role_map,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )
            
        # ĐỔI TÊN MÔ HÌNH THÀNH gemini-2.5-flash ĐỂ CHẠY MƯỢT MÀ VỚI SDK MỚI
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=contents,
            config=config
        )
        return response.text
    except Exception as e:
        return f"❌ Đã xảy ra lỗi khi kết nối với máy chủ Google AI: {str(e)}"
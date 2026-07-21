# modules/database.py
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase() -> Client:
    """Khởi tạo kết nối với Supabase bằng thông tin bảo mật từ secrets.toml"""
    if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
        st.error("⚠️ Thiếu cấu hình SUPABASE_URL hoặc SUPABASE_KEY trong file secrets.toml!")
        return None
        
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# Khởi tạo client dùng chung cho toàn dự án
supabase = init_supabase()

def init_db():
    """Hàm này giữ lại để không làm lỗi các file cũ gọi nó (không cần thao tác với SQLite nữa)."""
    pass

def them_tai_lieu(ten, chuyen_de, nguoi_gop, lien_ket, mo_ta=""):
    """Thêm tài liệu mới vào hàng đợi chờ duyệt trên Supabase."""
    if not supabase:
        return False
    try:
        data = {
            "ten_tai_lieu": ten,
            "chuyen_de": chuyen_de,
            "nguoi_dong_gop": nguoi_gop,
            "lien_ket": lien_ket,
            "mo_ta": mo_ta,
            "trang_thai": "Chờ duyệt" # Mặc định chờ duyệt
        }
        supabase.table("tai_lieu").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Lỗi thêm tài liệu: {str(e)}")
        return False

def lay_tai_lieu_da_duyet(chuyen_de=None):
    """Lấy danh sách các tài liệu đã được Admin phê duyệt từ Supabase."""
    if not supabase:
        return []
    try:
        query = supabase.table("tai_lieu").select("*").eq("trang_thai", "Đã duyệt")
        if chuyen_de:
            query = query.eq("chuyen_de", chuyen_de)
            
        response = query.execute()
        
        # Chuyển đổi cấu trúc dictionary của Supabase về dạng tuple (id, ten, chuyen_de, nguoi, lien_ket, mo_ta, trang_thai) 
        # để tương thích 100% với giao diện cũ em đã viết bằng vòng lặp item[1], item[4]...
        rows = []
        for item in response.data:
            rows.append((
                item.get("id"),
                item.get("ten_tai_lieu"),
                item.get("chuyen_de"),
                item.get("nguoi_dong_gop"),
                item.get("lien_ket"),
                item.get("mo_ta"),
                item.get("trang_thai")
            ))
        return rows
    except Exception as e:
        st.error(f"Lỗi lấy tài liệu đã duyệt: {str(e)}")
        return []

def lay_tai_lieu_cho_duyet():
    """Lấy danh sách tài liệu đang chờ Admin phê duyệt từ Supabase."""
    if not supabase:
        return []
    try:
        response = supabase.table("tai_lieu").select("*").eq("trang_thai", "Chờ duyệt").execute()
        
        rows = []
        for item in response.data:
            rows.append((
                item.get("id"),
                item.get("ten_tai_lieu"),
                item.get("chuyen_de"),
                item.get("nguoi_dong_gop"),
                item.get("lien_ket"),
                item.get("mo_ta"),
                item.get("trang_thai")
            ))
        return rows
    except Exception as e:
        st.error(f"Lỗi lấy tài liệu chờ duyệt: {str(e)}")
        return []

def cap_nhat_trang_thai(id_tai_lieu, trang_thai_moi):
    """Admin duyệt hoặc từ chối tài liệu trên Supabase."""
    if not supabase:
        return False
    try:
        supabase.table("tai_lieu").update({"trang_thai": trang_thai_moi}).eq("id", id_tai_lieu).execute()
        return True
    except Exception as e:
        st.error(f"Lỗi cập nhật trạng thái: {str(e)}")
        return False
# Thêm hàm này vào cuối file modules/database.py

def upload_file_to_storage(uploaded_file):
    """
    Tải file trực tiếp lên Supabase Storage Bucket và trả về link Public URL.
    """
    if not supabase:
        return None
    try:
        # Đọc dữ liệu binary từ file upload
        file_bytes = uploaded_file.getvalue()
        
        # Tạo tên file duy nhất trên cloud để tránh bị trùng lặp (ví dụ: bdt_chuyen_toan.pdf)
        file_name = f"documents/{uploaded_file.name}"
        
        # Đẩy file lên bucket 'tai_lieu_toan'
        bucket_name = "tai_lieu_toan"
        
        # Kiểm tra xem file đã tồn tại chưa, nếu có thì ghi đè (upsert=True)
        supabase.storage.from_(bucket_name).upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": uploaded_file.type, "upsert": "true"}
        )
        
        # Lấy Public URL của file vừa tải lên
        public_url_res = supabase.storage.from_(bucket_name).get_public_url(file_name)
        return public_url_res
    except Exception as e:
        st.error(f"Lỗi khi tải file lên Storage: {str(e)}")
        return None
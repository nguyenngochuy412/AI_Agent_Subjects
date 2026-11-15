Chat API

API chat xây bằng FastAPI, dự án học tập trong lộ trình trở thành AI Agent Engineer. Mục tiêu: backend có cấu trúc phân tầng rõ ràng, lưu lịch sử hội thoại vào database, có xác thực API key và test tự động.

Tính năng
[x] GET /health: kiểm tra server đang chạy
[x] POST /chat: nhận tin nhắn, kiểm tra dữ liệu bằng Pydantic, trả về phản hồi
[x] Cấu hình qua file .env (pydantic-settings)
[x] Kết nối SQLite bất đồng bộ (SQLAlchemy + aiosqlite), model Message
[ ] Lưu tin nhắn vào database và GET /history/{user_id}
[ ] Xác thực bằng API key
[ ] Unit test (pytest)
[ ] PostgreSQL + Alembic + Docker
[ ] Gọi LLM thật và streaming
Công nghệ

Python, FastAPI, Uvicorn, Pydantic, SQLAlchemy (async), SQLite.

Cấu trúc thư mục
ChatAPI_Project/
├── app/
│   ├── api/        # Các endpoint (routes)
│   ├── core/       # Cấu hình, bảo mật
│   ├── db/         # Kết nối database, session
│   ├── models/     # ORM models (bảng trong DB)
│   ├── schemas/    # Pydantic schemas (request/response)
│   └── main.py     # Khởi tạo ứng dụng
├── tests/          # Unit test
├── .env.example    # File mẫu biến môi trường
├── requirements.txt
└── README.md
Cài đặt

Yêu cầu: Python 3.10 trở lên.

powershell
# 1. Clone project
git clone <link-repo-cua-ban>
cd ChatAPI_Project

# 2. Tạo và kích hoạt môi trường ảo (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Tạo file .env từ file mẫu rồi chỉnh giá trị
copy .env.example .env

Nội dung .env:

DATABASE_URL=sqlite+aiosqlite:///./chat.db
API_KEY=your-api-key-here

Không commit file .env lên GitHub.

Chạy server

Chạy từ thư mục gốc của project:

powershell
uvicorn app.main:app --reload
Server: http://127.0.0.1:8000
Tài liệu API tự sinh (Swagger): http://127.0.0.1:8000/docs

Lần chạy đầu tiên sẽ tự tạo file chat.db cùng bảng messages.

Ví dụ sử dụng

Kiểm tra server

GET /health
json
{ "status": "ok" }

Gửi tin nhắn

POST /chat

Request:

json
{ "message": "hello" }

Response:

json
{ "reply": "Chào bạn" }

Gọi bằng PowerShell:

powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/chat -Method Post -ContentType "application/json" -Body '{"message":"hello"}'

Nếu message rỗng hoặc sai kiểu dữ liệu, API trả về lỗi 422 kèm mô tả chi tiết.

Lộ trình tiếp theo
Lưu tin nhắn của user và bot vào database, thêm GET /history/{user_id}.
Thêm xác thực API key và xử lý lỗi toàn cục.
Viết test với pytest (database SQLite in-memory).
Chuyển sang PostgreSQL chạy bằng Docker, quản lý migration bằng Alembic.
Tích hợp LLM và trả lời dạng streaming.
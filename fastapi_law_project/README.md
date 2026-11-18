# Legal HR Agent API (Mốc 1: khung hệ thống)

## Giới thiệu
API chat nền tảng cho hệ thống agent pháp lý-nhân sự. Mốc 1 chỉ gồm: FastAPI,
PostgreSQL, xác thực API key, lưu lịch sử theo người dùng.

## Công nghệ
Python 3.12, FastAPI, Pydantic, SQLAlchemy (async), PostgreSQL, Docker Compose, pytest

## Chạy nhanh
1. Sao chép `.env.example` thành `.env`, đặt mật khẩu cho PostgreSQL.
2. `docker compose up -d --build`
3. Tạo API key: `docker compose exec api python -m scripts.create_api_key <user_id>`
4. Mở http://127.0.0.1:8000/docs, bấm Authorize và dán key.

## Endpoint
| Method | Đường dẫn | Mô tả | Cần key |
|---|---|---|---|
| GET | /health | Kiểm tra dịch vụ | Không |
| POST | /chat | Gửi tin nhắn, nhận phản hồi | Có |
| GET | /history | Lịch sử của chính người gọi | Có |

## Chạy test
- Chạy môi trường ảo và vào thư mục chứa file gốc chạy "pytest -v"(nhớ run docker)
- Nếu các test đều pass thì endpoint của bạn đúng

## Quyết định thiết kế
- user_id suy ra từ API key, không nhận từ client.
- API key được băm SHA-256 trước khi lưu.

## Hạn chế hiện tại / việc tiếp theo
- Phản hồi hiện là câu cố định, chưa gọi LLM. Mốc 2 sẽ thêm RAG.
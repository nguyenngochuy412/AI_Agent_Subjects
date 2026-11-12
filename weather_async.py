import asyncio
import os
from typing import Optional
import httpx

# --- TỐI ƯU HÓA 1: Cố gắng dùng winloop (Event loop viết bằng C, nhanh gấp 2-4 lần) ---
try:
    import winloop      
    asyncio.set_event_loop_policy(winloop.EventLoopPolicy())                                                                                                                                                                                       
    print("[Hệ thống] Đã kích hoạt winloop (Tối ưu Event Loop).")   
except ImportError:                                                                                         
    print("[Hệ thống] Không tìm thấy winloop, dùng asyncio mặc định.")

# --- TỐI ƯU HÓA 2: Cố gắng dùng orjson (Thư viện đọc JSON viết bằng Rust, siêu nhanh) ---
try:
    import orjson
    def parse_json(content: bytes) -> dict:
        return orjson.loads(content)
except ImportError:
    import json
    def parse_json(content: bytes) -> dict:
        return json.loads(content.decode("utf-8"))

API_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherClient:
    def __init__(self, api_key: str, max_concurrent: int = 5):
        self.api_key = api_key
        # Tái sử dụng AsyncClient giúp tối ưu connection pool
        self.client = httpx.AsyncClient(timeout=10.0)
        
        # --- TỐI ƯU HÓA 3: Dùng Semaphore để giới hạn số request đồng thời ---
        # Tránh bị API chặn (Rate Limit) nếu danh sách thành phố quá dài
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(self, city: str) -> Optional[dict]:
        # Dùng async with semaphore để kiểm soát luồng
        async with self.semaphore:
            try:
                resp = await self.client.get(
                    API_URL,
                    params={"q": city, "units": "metric", "appid": self.api_key}
                )

                # print(dir(resp))
                # print(f"\n--- Đang kiểm tra resp của: {city} ---")
                # print(f"1. Đối tượng resp: {resp}") 
                # print(f"2. Status Code: {resp.status_code}")
                # print(f"3. Headers: {resp.headers}")
                # print(f"4. Dữ liệu thô (Bytes): {resp.content}")
                # print(f"5. Dữ liệu dạng Text: {resp.text}")

                # Tự động ném lỗi nếu status code là 4xx hoặc 5xx
                resp.raise_for_status()
                
                # Sử dụng hàm parse_json đã tối ưu ở trên
                data = parse_json(resp.content)

                # # 1. Bản gốc của Bytes (Mảng số)
                # print("--- BYTES GỐC ---")
                # print("Type:", type(resp.content))
                # print("10 byte đầu tiên (số):", list(resp.content[:10])) 

                # # 2. Bản gốc của Text (Chuỗi ký tự)
                # print("\n--- TEXT GỐC ---")
                # print("Type:", type(resp.text))
                # print("Ký tự đầu tiên:", resp.text[:10]) # In ra ký tự '{'

                # # 3. Bản gốc của Dictionary
                # data = parse_json(resp.content)
                # print("\n--- DICTIONARY GỐC ---")
                # print("Type:", type(data))
                # print("Các chìa khóa (Keys):", list(data.keys()))

                print(f"Du lieu sau khi parse {data}")
                
                return {
                    "city": city, 
                    "temp": data["main"]["temp"], 
                    "desc": data["weather"][0]["description"]
                }
            except httpx.HTTPError as e:
                print(f"[Lỗi] Không lấy được thời tiết {city}: {e}")
                return None                                                                         

    async def close(self):
        # Đóng client để giải phóng tài nguyên
        await self.client.aclose()

async def main():
    # Lấy API key từ biến môi trường, nếu không có thì dùng chuỗi mặc định
    api_key = os.environ.get("OWM_API_KEY", "YOUR_API_KEY")
    
    # Danh sách thành phố (có thể thêm bao nhiêu tùy thích)
    cities = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Can Tho", "HaiPhong"]
    
    weather_client = WeatherClient(api_key)
    
    try:
        print(f"Đang lấy thời tiết cho {len(cities)} thành phố...\n")
        
        # Chạy đồng thời tất cả các request bằng asyncio.gather
        results = await asyncio.gather(*[weather_client.fetch(c) for c in cities])

        # In kết quả
        for res in results:
            if res:
                print(f"📍 {res['city']}: {res['temp']}°C, {res['desc']}")
            else:
                print("❌ Không có dữ liệu cho một thành phố nào đó.")
                
    finally:
        # Luôn đảm bảo đóng client dù có lỗi xảy ra
        await weather_client.close()

if __name__ == "__main__":
    asyncio.run(main())
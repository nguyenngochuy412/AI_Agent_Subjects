import asyncio
import httpx
from typing import Optional
import os

try:
    import winloop
    asyncio.set_event_loop_policy(winloop.EventLoopPolicy())
    print(f"[He thong] da kich hoat winloop")
except ImportError:
    print(f"[He thong] khong tim thay winloop")

try:
    import orjson
    def parse_json(content: bytes) -> dict:
        return orjson.loads(content)
    print(f"[He thong] da kich hoat orjson")

except ImportError:
    import json
    def parse_json(content: bytes) -> dict:
        return json.loads(content)
    print(f"[He thong] da kich hoat json")

API_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherClient:
    def __init__(self, api_key: str, max_concurrent: int = 5):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(self, city: str) -> Optional[dict]:
        async with self.semaphore:
            try:
                resp = await self.client.get(
                    API_URL,
                    params={"q": city, "units": "metric", "appid": self.api_key}
                )

                resp.raise_for_status

                data = parse_json(resp.content)

                print(f"Du lieu sau khi parse {data}")
                return {
                    "city": city,
                    "temp": data["main"]["temp"],
                    "desc": data["weather"][0]["description"]
                }
            except httpx.HTTPError as e:
                print(f"[Loi] Khong lay duoc thoi tiet {city}: {e}")
                return None
    async def close(self):
        await self.client.aclose()

async def main():
    api_key = os.environ.get("OWM_API_KEY", "YOUR_API_KEY")
    cities = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Can Tho", "HaiPhong"]

    weather_client = WeatherClient(api_key)

    try:
        print(f"Đang lấy thời tiết cho {len(cities)} thành phố...\n")
        results = await asyncio.gather(*[weather_client.fetch(c) for c in cities])

        for res in results:
            if res:
                print(f"📍 {res['city']}: {res['temp']}°C, {res['desc']}")
            else:
                print("❌ Không có dữ liệu cho một thành phố nào đó.")

    finally:
        await weather_client.close()

if __name__ == "__main__":
    asyncio.run(main())
\# Weather Async Fetcher



Dự án nhỏ thuộc lộ trình học Backend Python. Script này sử dụng `asyncio` và `httpx` để gọi đồng thời API thời tiết của OpenWeatherMap cho nhiều thành phố cùng lúc.



\## Tính năng

\- Lập trình hướng đối tượng (OOP) với Class `WeatherClient`.

\- Sử dụng Type Hints đầy đủ.

\- Lập trình bất đồng bộ (Async/await) giúp tăng tốc độ.

\- Tối ưu hóa với `orjson` (parse JSON nhanh) và `winloop` (nếu có).

\- Sử dụng `Semaphore` để giới hạn số lượng request đồng thời (tránh bị API chặn).



\## Yêu cầu hệ thống

\- Python 3.9 trở lên.

\- Tài khoản OpenWeatherMap (để lấy API Key miễn phí).



\## Hướng dẫn cài đặt



1\. \*\*Clone dự án:\*\*

&#x20;  ```bash

&#x20;  git clone https://github.com/nguyenngochuy412/weather-async-fetcher.git

&#x20;  cd weather-async-fetcher


#!/usr/bin/env python
#VanHuy NewEra
import yt_dlp
import requests
import subprocess
import os
import sys

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def progress_hook(d):
    if d["status"] == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)

        percent = d.get("_percent_str", "0%").strip()
        speed = d.get("_speed_str", "0 B/s").strip()
        eta = d.get("_eta_str", "--:--").strip()

        if total:
            bar_len = 30
            filled = int(downloaded / total * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)

            downloaded_mb = downloaded / 1024 / 1024
            total_mb = total / 1024 / 1024

            text = (
                f"📥 [{bar}] {percent} | "
                f"{downloaded_mb:.2f}/{total_mb:.2f} MB | "
                f"⚡️{speed} | ⏳{eta}"
            )
        else:
            text = f"📥 {percent} | ⚡ {speed} | ⏳ {eta}"

        # Ghi đè lên cùng một dòng
        print("\r" + text, end="", flush=True)

    elif d["status"] == "finished":
        print("\nHoàn thành 1 tác vụ, đang tiếp tục...")
        pass


print(f"{GREEN}")
banner = r"""
┌────────────────────────────────────────────────────────────┐
│                                                            │
│       ██╗  ██╗   ████████╗ ██████╗  ██████╗ ██╗            │
│       ██║  ██║   ╚══██╔══╝██╔═══██╗██╔═══██╗██║            │
│       ███████║█████╗██║   ██║   ██║██║   ██║██║            │
│       ██╔══██║╚════╝██║   ██║   ██║██║   ██║██║            │
│       ██║  ██║      ██║   ╚██████╔╝╚██████╔╝███████╗       │
│       ╚═╝  ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝       │
│                                                            │
│              TOOL TẢI VIDEO TỪ MXH | BY VANHUY             │
└────────────────────────────────────────────────────────────┘
"""


def clear_screen():
    os.system("clear")


def show_banner():
    clear_screen()
    print(banner)

    print("""
═════════════════════════════════════════
Version 5.0 OFFICIAL - Bước Ngoặt YT-DLP:
✓ Thêm chế độ tải MP3
✓ Thêm chế độ chỉ tải phụ đề SRT
✓ Thêm menu lựa chọn chế độ tải:
    1. Tải Video MP4
    2. Tải Âm Thanh MP3
    3. Tải Phụ Đề SRT

✓ Tối ưu hệ thống yt-dlp + FFmpeg
✓ Hỗ trợ chuyển đổi Audio sang MP3 320kbps
✓ Tự động xóa file âm thanh gốc sau khi chuyển đổi
☑️ TikTok:
	- Đang hoàn thiện chế độ tải MP3.
	- Không hỗ trợ SRT.
✓ Cải thiện quản lý biến chế độ tải
✓ Cải thiện thông báo hoàn thành tải
✓ Sửa lỗi và cải thiện hiệu năng
════════════════════════════════════════════
""")

    print("""

   CÁC ỨNG DỤNG HỖ TRỢ        
═══════════════════════════════════════
• BILIBILI                   
• YOUTUBE                    
• NICONICO                   
• FACEBOOK VIDEO
• X (TWITTER)                
• TIKTOK                     
""")


if __name__ == "__main__":
    show_banner()

# ==========================================
# CẤU HÌNH CHO TỪNG ỨNG DỤNG
# ==========================================
youtube_opts = {
    "format": "bestvideo[vcodec*=avc1]+bestaudio[ext=m4a]/best[ext=mp4]",
    "merge_output_format": "mp4",
    "writesubtitles": True,
    "writeautomaticsub": False,
    "subtitleslangs": ["vi", "en"],
    "embedsubtitles": True,
    "writethumbnail": True,
    "embedthumbnail": True,
    "addmetadata": True,
    "sleep_interval": 4,
    "max_sleep_interval": 8,
    "concurrent_fragment_downloads": 1,
    "retries": 10,
    "fragment_retries": 10,
    "http_chunk_size": 10485760,
    "http_headers": {"User-Agent": "Mozilla/5.0"},
    "noplaylist": False,
    "windowsfilenames": True,
    "outtmpl": "/sdcard/Download/YouTube/%(title)s.%(ext)s",
}

bilibili_opts = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["vi", "en"],
    "embedsubtitles": True,
    "extractor_args": {"bilibili": {"danmaku": ["1"]}},
    "writethumbnail": True,
    "embedthumbnail": True,
    "addmetadata": True,
    "windowsfilenames": True,
    "outtmpl": "/sdcard/Download/Anime/%(title)s.%(ext)s",
}

facebook_opts = {
    "format": "best",
    "merge_output_format": "mp4",
    "writethumbnail": True,
    "addmetadata": True,
    "windowsfilenames": True,
    "outtmpl": "/sdcard/Download/Facebook/%(title)s.%(ext)s",
}

twitter_opts = {
    "format": "best",
    "merge_output_format": "mp4",
    "writethumbnail": True,
    "addmetadata": True,
    "windowsfilenames": True,
    "outtmpl": "/sdcard/Download/Twitter/%(title)s.%(ext)s",
}

niconico_opts = {
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "writesubtitles": True,
    "writethumbnail": True,
    "addmetadata": True,
    "windowsfilenames": True,
    "outtmpl": "/sdcard/Download/Niconico/%(title)s.%(ext)s",
}

mp3_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
    "writethumbnail": False,
    "embedthumbnail": False,
    "addmetadata": True,
    "windowsfilenames": True,
    "outtmpl": "/sdcard/Download/Music/%(title)s.%(ext)s",
}

subtitle_opts = {
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["vi", "en"],
    "subtitlesformat": "srt",
    "windowsfilenames": True,
}


def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "bilibili" in url or "bili.im" in url:
        return "bilibili"
    elif "facebook.com" in url or "fb.watch" in url:
        return "facebook"
    elif "twitter.com" in url or "x.com" in url:
        return "twitter"
    elif "nicovideo.jp" in url:
        return "niconico"
    elif "tiktok" in url:
        return "tiktok"

    return None


def get_options(platform):
    if platform == "youtube":
        return youtube_opts
    elif platform == "bilibili":
        return bilibili_opts
    elif platform == "facebook":
        return facebook_opts
    elif platform == "twitter":
        return twitter_opts
    elif platform == "niconico":
        return niconico_opts

    return None


def get_video_info(url):
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
        return info
    except Exception as e:
        print(f"\n✗ Không thể lấy thông tin video: {e}")
        return None


def show_video_info(info, platform):
    print("\n════════════ THÔNG TIN VIDEO ════════════")

    print(f"Tên video : {info.get('title', 'Không rõ')}")
    print(f"Kênh      : {info.get('uploader', 'Không rõ')}")

    duration = info.get("duration")
    if duration is not None:
        duration = int(duration)
        minutes, seconds = divmod(duration, 60)
        print(f"Thời lượng: {minutes}:{seconds:02d}")
    else:
        print("Thời lượng: Không rõ")

    views = info.get("view_count")
    if views:
        print(f"Lượt xem  : {views:,}")
    else:
        print("Lượt xem  : Không rõ")

    platform_names = {
        "youtube": "YouTube",
        "bilibili": "Bilibili",
        "facebook": "Facebook",
        "twitter": "X (Twitter)",
        "niconico": "Niconico",
        "tiktok": "TikTok",
    }

    print(f"Nền tảng  : {platform_names.get(platform, 'Không rõ')}")
    print("═════════════════════════════════════════")


def resolve_bilibili_url(url):
    if "bili.im/" not in url:
        return url

    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        print(f"✓ Đã chuyển đổi Link Bilibili: {response.url}")
        return response.url
    except Exception as e:
        print(f"⚠ Không thể chuyển đổi link: {e}")
        return url


def update_ytdlp():
    print("\n🔄 Đang cập nhật yt-dlp...\n")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "yt-dlp"], check=True
        )
        print("\n✅ Cập nhật yt-dlp thành công!")
    except subprocess.CalledProcessError:
        print("\n❌ Không thể cập nhật yt-dlp.")


print(f"Phiên bản yt-dlp: {yt_dlp.version.__version__}")
print("""
══════════════════════
1. Bắt đầu tải
2. Cập nhật yt-dlp
3. Thoát
══════════════════════
""")

main_menu = input("Lựa chọn: ").strip()

if main_menu == "2":
    update_ytdlp()
    input("\nNhấn Enter để tiếp tục...")
elif main_menu == "3":
    exit()

while True:
    url = input("\nNhập link: ").strip()
    url = resolve_bilibili_url(url)

    platform = detect_platform(url)

    if platform is None:
        print("Ứng dụng chưa được hỗ trợ!")
        continue

    platform_folder = {
        "youtube": "YouTube",
        "tiktok": "TikTok",
        "facebook": "Facebook",
        "twitter": "X",
        "bilibili": "Bilibili",
        "niconico": "NicoNico",
    }.get(platform, "Other")

    download_path = f"/sdcard/Download/{platform_folder}"
    os.makedirs(download_path, exist_ok=True)

    info = get_video_info(url)
    if info is None:
        continue

    show_video_info(info, platform)

    download_mode = input("""
══════════════════════
- CHỌN CHẾ ĐỘ TẢI -
1. Tải Video MP4 (nguyên bản)
2. Tải MP3
3. Chỉ tải phụ đề SRT
══════════════════════

Lựa chọn: """).strip()

    if download_mode not in ["1", "2", "3"]:
        print("Lựa chọn không hợp lệ.")
        continue

    try:
        if platform == "tiktok":
            process = subprocess.Popen(
                [
                    "yt-dlp",
                    "-f",
                    "bestvideo+bestaudio/best",
                    "--merge-output-format",
                    "mp4",
                    "-o",
                    f"/sdcard/Download/TikTok/%(title)s.%(ext)s",
                    url,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            for line in process.stdout:
                print(line, end="")

            process.wait()

        else:
            if download_mode == "2":
                ydl_opts = mp3_opts.copy()
                ydl_opts["outtmpl"] = f"{download_path}/%(title)s.%(ext)s"
            elif download_mode == "3":
                ydl_opts = subtitle_opts.copy()
                ydl_opts["outtmpl"] = f"{download_path}/%(title)s.%(ext)s"
            else:
                ydl_opts = get_options(platform).copy()
                ydl_opts["outtmpl"] = f"{download_path}/%(title)s.%(ext)s"

            ydl_opts["progress_hooks"] = [progress_hook]
            ydl_opts["quiet"] = True
            ydl_opts["no_warnings"] = True

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        if download_mode == "2":
            print("\n✓ Hoàn tất tải MP3!")
        elif download_mode == "3":
            print("\n✓ Hoàn tất tải phụ đề")
        else:
            print("\n✓ Hoàn tất tải Video!")

    except Exception as e:
        print(f"\n✗ Lỗi: {e}")

    while True:
        next_action = input("\n1. Tiếp tục tải\n2. Thoát\nChọn: ").strip()

        if next_action == "1":
            show_banner()
            break
        elif next_action == "2":
            print("Cảm ơn bạn đã sử dụng Tool!")
            exit()
        else:
            print("Lựa chọn không hợp lệ!")

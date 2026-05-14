import urllib.request
from PIL import Image, ImageDraw, ImageFont
import os

# 1. 설정
url = "https://koreanhole.github.io/parking-qr/"
qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?data={url}&size=400x400"
assets_dir = "assets"
output_path = os.path.join(assets_dir, "parking_qr.png")
font_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc" # 시스템 폰트 경로

# 2. 폴더 생성
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# 3. QR 코드 다운로드
qr_temp_path = "qr_temp.png"
urllib.request.urlretrieve(qr_api_url, qr_temp_path)

# 4. 이미지 합성
try:
    qr_img = Image.open(qr_temp_path)
    
    # 캔버스 생성 (정방형, 600x600)
    canvas_size = 600
    canvas = Image.new("RGB", (canvas_size, canvas_size), "white")
    
    # QR 코드 중앙 배치
    qr_x = (canvas_size - qr_img.width) // 2
    qr_y = 50 # 상단 여백
    canvas.paste(qr_img, (qr_x, qr_y))
    
    # 텍스트 추가
    draw = ImageDraw.Draw(canvas)
    try:
        # Noto Serif CJK KR 폰트 사용 (인덱스 4가 보통 KR)
        font = ImageFont.truetype(font_path, 24, index=4)
    except:
        # 폰트 로드 실패 시 기본 폰트
        font = ImageFont.load_default()
        
    text = "차주와 연결하려면 QR코드를\n휴대폰 카메라로 스캔하세요."
    
    # 텍스트 박스 크기 계산 (Pillow 버전에 따라 getsize 또는 textbbox 사용)
    try:
        # 멀티라인 텍스트 지원을 위해 draw.multiline_textbbox 사용
        left, top, right, bottom = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        text_width = right - left
    except AttributeError:
        # 구버전 대응
        text_width, _ = draw.textsize(text, font=font)
        
    text_x = (canvas_size - text_width) // 2
    text_y = qr_y + qr_img.height + 30
    
    draw.multiline_text((text_x, text_y), text, fill="black", font=font, align="center", spacing=10)
    
    # 5. 저장
    canvas.save(output_path)
    print(f"QR 이미지가 생성되었습니다: {output_path}")

finally:
    # 임시 파일 삭제
    if os.path.exists(qr_temp_path):
        os.remove(qr_temp_path)

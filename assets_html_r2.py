import shutil
from pathlib import Path

# --- 설정 ---
R2_PUBLIC_URL = "https://pub-cd1be2e14345481ca5d47624405b945d.r2.dev"
ASSETS_DIR = Path("assets")
SOURCE_HTML_DIR = Path("product-detail")
EXPORT_DIR = Path("product-detail-export")

def process_html_files() -> None:
    """HTML 파일의 이미지 경로를 R2 URL로 변경하고 내보냅니다."""
    print("--- HTML 파일 에셋 경로 변환 시작 ---")
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"'{EXPORT_DIR}' 폴더가 준비되었습니다.")

    html_files = list(SOURCE_HTML_DIR.glob('*.html'))
    if not html_files:
        print(f"경고: '{SOURCE_HTML_DIR}' 폴더에서 처리할 HTML 파일을 찾지 못했습니다.")
        return
        
    print(f"\n{len(html_files)}개의 HTML 파일에서 이미지 경로를 변환합니다...")

    old_path_pattern = f"../{ASSETS_DIR.name}/"
    new_path_pattern = f"{R2_PUBLIC_URL}/"

    for file_path in html_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            export_file_path = EXPORT_DIR / file_path.name
            
            if old_path_pattern in content:
                updated_content = content.replace(old_path_pattern, new_path_pattern)
                
                export_file_path.write_text(updated_content, encoding='utf-8')
                print(f"  - '{file_path.name}' 처리 완료 -> '{export_file_path}'")
            else:
                shutil.copy(file_path, export_file_path)
                print(f"  - '{file_path.name}' (변경사항 없음, 원본 복사)")

        except Exception as e:
            print(f"❌ 오류: '{file_path.name}' 처리 중 에러 발생: {e}")
            
    print("\n--- 모든 작업 완료! ---")
    print(f"최종 결과물은 '{EXPORT_DIR}' 폴더에서 확인하세요.")

if __name__ == "__main__":
    process_html_files()
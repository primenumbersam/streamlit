import subprocess
import json
import hashlib
from pathlib import Path

# --- 설정 ---
ASSETS_DIR = Path("assets")
R2_BUCKET_NAME = "assets"
STATE_FILE = Path(".r2_sync_state.json")

def get_file_md5(file_path: Path) -> str:
    """파일의 MD5 해시값을 계산합니다."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def load_state() -> dict:
    """이전에 업로드한 파일들의 상태(해시값)를 불러옵니다."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_state(state: dict) -> None:
    """업로드된 파일들의 상태(해시값)를 저장합니다."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def sync_assets_to_r2() -> bool:
    """변경된 파일만 판별하여 R2에 개별적으로 업로드합니다."""
    print(f"--- R2 에셋 동기화 시작 ---")
    print(f"'{ASSETS_DIR}' 폴더를 R2 버킷 '{R2_BUCKET_NAME}'(으)로 업로드합니다...")
    
    if not ASSETS_DIR.exists() or not ASSETS_DIR.is_dir():
        print(f"❌ 오류: '{ASSETS_DIR}' 폴더를 찾을 수 없습니다.")
        return False

    files = [f for f in ASSETS_DIR.rglob('*') if f.is_file()]
    if not files:
        print("경고: 업로드할 파일이 없습니다.")
        return True

    state = load_state()
    success = True
    skipped_count = 0
    uploaded_count = 0

    for file_path in files:
        relative_path = file_path.relative_to(ASSETS_DIR)
        r2_dest = f"{R2_BUCKET_NAME}/{relative_path.as_posix()}"
        
        # 변경 여부 확인 (MD5 해시 비교)
        current_md5 = get_file_md5(file_path)
        if str(relative_path) in state and state[str(relative_path)] == current_md5:
            print(f"건너뜀 (변경 없음): {relative_path}")
            skipped_count += 1
            continue
        
        print(f"업로드 중: {relative_path} -> {r2_dest} ... ", end="", flush=True)
        try:
            command = [
                "wrangler", "r2", "object", "put", r2_dest, 
                f"--file={str(file_path)}",
                "--remote"
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            print("✅")
            
            # 성공 시 상태 업데이트
            state[str(relative_path)] = current_md5
            uploaded_count += 1
            save_state(state)
        except FileNotFoundError:
            print("\n❌ 오류: 'wrangler' CLI를 찾을 수 없습니다.")
            print("설치: npm install -g wrangler")
            return False
        except subprocess.CalledProcessError as e:
            print(f"\n❌ 실패")
            print(e.stderr)
            success = False

    if success:
        print(f"✅ R2 업로드 완료! (신규/업데이트: {uploaded_count}개, 건너뜀: {skipped_count}개)")
    return success

if __name__ == "__main__":
    sync_assets_to_r2()
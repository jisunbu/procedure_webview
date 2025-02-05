import os
import shutil

def init_documents():
    # 소스 폴더 (로컬 개발 환경의 문서 폴더)
    src_folder = 'documents/company_docs'
    
    # 대상 폴더 (Render 서버의 문서 폴더)
    dst_folder = os.getenv('UPLOAD_FOLDER', 'documents/company_docs')
    
    # 대상 폴더가 소스 폴더와 같으면 건너뛰기
    if os.path.abspath(src_folder) == os.path.abspath(dst_folder):
        print("Source and destination folders are the same. Skipping copy.")
        return
    
    # 대상 폴더 생성
    os.makedirs(dst_folder, exist_ok=True)
    
    # 모든 파일 복사 (.gitkeep 제외)
    for filename in os.listdir(src_folder):
        if filename == '.gitkeep':
            continue
            
        src_file = os.path.join(src_folder, filename)
        dst_file = os.path.join(dst_folder, filename)
        
        if os.path.isfile(src_file):
            try:
                shutil.copy2(src_file, dst_file)
                print(f"Copied: {filename}")
            except Exception as e:
                print(f"Error copying {filename}: {str(e)}")

if __name__ == "__main__":
    print("Starting document initialization...")
    init_documents()
    print("Document initialization completed.") 
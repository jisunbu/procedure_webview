# 절차서를 등록하는 program (202)
import os
import shutil
from datetime import datetime
import sys
import tkinter as tk
from tkinter import filedialog

class DocumentManager:
    def __init__(self):
        self.target_dir = 'documents/company_docs'
        self.allowed_extensions = {'pdf', 'docx', 'xlsx', 'xls'}
        
        # GUI 초기화 (숨김)
        self.root = tk.Tk()
        self.root.withdraw()
        
        # documents/company_docs 폴더가 없으면 생성
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

    def is_allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def select_file(self):
        """파일 탐색기를 통한 파일 선택"""
        filetypes = [
            ('모든 지원 문서', '*.pdf;*.docx;*.xlsx;*.xls'),
            ('PDF 파일', '*.pdf'),
            ('Word 문서', '*.docx'),
            ('Excel 파일', '*.xlsx;*.xls'),
        ]
        
        file_path = filedialog.askopenfilename(
            title='등록할 문서를 선택하세요',
            filetypes=filetypes
        )
        return file_path

    def confirm_replace(self, filename):
        """파일 교체 확인"""
        while True:
            response = input(f"\n'{filename}' 파일이 이미 존재합니다. 교체하시겠습니까? (y/n): ").lower()
            if response in ['y', 'n']:
                return response == 'y'
            print("잘못된 입력입니다. 'y' 또는 'n'을 입력해주세요.")

    def list_documents(self):
        """등록된 문서 목록 출력"""
        print("\n=== 현재 등록된 문서 목록 ===")
        files = []
        for filename in os.listdir(self.target_dir):
            if self.is_allowed_file(filename):
                file_path = os.path.join(self.target_dir, filename)
                file_stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'type': filename.rsplit('.', 1)[1].lower(),
                    'date': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d')
                })
        
        if not files:
            print("등록된 문서가 없습니다.")
            return

        # 날짜순 정렬
        files.sort(key=lambda x: x['date'], reverse=True)
        
        # 목록 출력
        print(f"{'번호':^6} {'문서명':<30} {'종류':^10} {'등록일':^12}")
        print("-" * 60)
        for idx, file in enumerate(files, 1):
            print(f"{idx:^6} {file['name']:<30} {file['type']:^10} {file['date']:^12}")

    def register_document(self):
        """문서 등록"""
        source_path = self.select_file()
        if not source_path:  # 파일 선택 취소한 경우
            print("문서 등록이 취소되었습니다.")
            return False

        if not os.path.exists(source_path):
            print(f"오류: 파일을 찾을 수 없습니다 - {source_path}")
            return False

        filename = os.path.basename(source_path)
        if not self.is_allowed_file(filename):
            print(f"오류: 지원하지 않는 파일 형식입니다 - {filename}")
            print(f"지원 형식: {', '.join(self.allowed_extensions)}")
            return False

        target_path = os.path.join(self.target_dir, filename)
        
        # 동일한 파일명이 존재하는 경우
        if os.path.exists(target_path):
            if not self.confirm_replace(filename):
                print("문서 등록이 취소되었습니다.")
                return False
            try:
                os.remove(target_path)  # 기존 파일 삭제
            except Exception as e:
                print(f"오류: 기존 파일 삭제 중 오류가 발생했습니다 - {str(e)}")
                return False

        try:
            shutil.copy2(source_path, target_path)
            print(f"성공: '{filename}' 문서가 등록되었습니다.")
            return True
        except Exception as e:
            print(f"오류: 문서 등록 중 오류가 발생했습니다 - {str(e)}")
            return False

    def delete_document(self, filename):
        """문서 삭제"""
        file_path = os.path.join(self.target_dir, filename)
        if not os.path.exists(file_path):
            print(f"오류: 파일을 찾을 수 없습니다 - {filename}")
            return False

        try:
            os.remove(file_path)
            print(f"성공: '{filename}' 문서가 삭제되었습니다.")
            return True
        except Exception as e:
            print(f"오류: 문서 삭제 중 오류가 발생했습니다 - {str(e)}")
            return False

def main():
    manager = DocumentManager()
    
    while True:
        print("\n=== 문서 관리 시스템 ===")
        print("1. 문서 목록 보기")
        print("2. 문서 등록하기")
        print("3. 문서 삭제하기")
        print("4. 종료")
        
        choice = input("\n원하는 작업을 선택하세요 (1-4): ")
        
        if choice == '1':
            manager.list_documents()
            
        elif choice == '2':
            manager.register_document()
            
        elif choice == '3':
            manager.list_documents()
            filename = input("\n삭제할 문서명을 입력하세요: ")
            manager.delete_document(filename)
            
        elif choice == '4':
            print("\n프로그램을 종료합니다.")
            break
            
        else:
            print("\n잘못된 선택입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main() 
import os
import sys
import tkinter as tk
import winreg
from collections import Counter
from tkinter import filedialog, messagebox

class FileRenamerApp:
    def __init__(self, root, initial_folder=None):
        self.root = root
        self.root.title("파일 일괄 이름 변경 도구")
        self.root.geometry("620x600")
        self.root.resizable(False, False)
        
        self.target_folder = tk.StringVar()
        self.include_subfolders = tk.BooleanVar(value=True)
        if initial_folder and os.path.isdir(initial_folder):
            self.target_folder.set(initial_folder)
        
        self.create_widgets()
        if self.target_folder.get():
            self.log_message(f"폴더 선택됨: {self.target_folder.get()}")

    def create_widgets(self):
        # 1. 폴더 선택 영역
        frame_folder = tk.LabelFrame(self.root, text="1. 대상 폴더 선택", padx=10, pady=10)
        frame_folder.pack(fill="x", padx=10, pady=5)
        frame_folder.columnconfigure(0, weight=1)
        
        tk.Entry(frame_folder, textvariable=self.target_folder, state="readonly").grid(row=0, column=0, sticky="ew", padx=(0, 8))
        tk.Button(frame_folder, text="폴더 찾아보기", command=self.select_folder).grid(row=0, column=1, sticky="e")
        tk.Checkbutton(
            frame_folder,
            text="하위 폴더 포함",
            variable=self.include_subfolders,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))

        # 2. 접두사/접미사 추가 영역
        frame_affix = tk.LabelFrame(self.root, text="2. 접두사(Prefix) / 접미사(Suffix) 추가", padx=10, pady=10)
        frame_affix.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_affix, text="접두사:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_prefix = tk.Entry(frame_affix, width=20)
        self.entry_prefix.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_affix, text="접미사:").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_suffix = tk.Entry(frame_affix, width=20)
        self.entry_suffix.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(frame_affix, text="적용하기", command=self.apply_affix).grid(row=1, column=0, columnspan=4, pady=10)

        # 3. 일괄 이름 변경 및 번호 부여 영역
        frame_batch = tk.LabelFrame(self.root, text="3. 일괄 이름 변경 및 번호 매기기", padx=10, pady=10)
        frame_batch.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_batch, text="새로운 기본 파일명:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_basename = tk.Entry(frame_batch, width=30)
        self.entry_basename.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(frame_batch, text="일괄 변경 실행", command=self.apply_batch_rename).grid(row=1, column=0, columnspan=2, pady=10)

        # 4. Windows 우클릭 메뉴 등록 영역
        frame_context = tk.LabelFrame(self.root, text="4. Windows 우클릭 메뉴 등록", padx=10, pady=10)
        frame_context.pack(fill="x", padx=10, pady=5)

        tk.Button(
            frame_context,
            text="우클릭 메뉴에 등록",
            command=self.register_context_menu,
        ).pack(side="left", padx=5)
        tk.Button(
            frame_context,
            text="우클릭 메뉴에서 제거",
            command=self.unregister_context_menu,
        ).pack(side="left", padx=5)

        # 5. 로그/결과 출력 영역
        frame_log = tk.LabelFrame(self.root, text="실행 결과 로그", padx=10, pady=10)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_log = tk.Text(frame_log, height=10, state="disabled")
        self.text_log.pack(fill="both", expand=True)

    def select_folder(self):
        """사용자가 폴더를 선택할 수 있게 하는 함수"""
        folder_path = filedialog.askdirectory(title="폴더를 선택하세요")
        if folder_path:
            self.target_folder.set(folder_path)
            self.log_message(f"폴더 선택됨: {folder_path}")

    def log_message(self, message):
        """화면 하단 텍스트 창에 로그 메시지를 출력하는 함수"""
        self.text_log.config(state="normal")
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state="disabled")

    def get_files_in_folder(self):
        """선택된 폴더 내의 파일 경로 목록을 반환하는 함수"""
        folder = self.target_folder.get()
        if not folder:
            messagebox.showwarning("경고", "먼저 대상 폴더를 선택해야 한다.")
            return None, []
        
        try:
            files = []
            include_subfolders = self.include_subfolders.get()
            if include_subfolders:
                for current_folder, _, filenames in os.walk(folder):
                    for filename in filenames:
                        file_path = os.path.join(current_folder, filename)
                        if os.path.isfile(file_path):
                            files.append(file_path)
            else:
                files = [
                    os.path.join(folder, filename)
                    for filename in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, filename))
                ]

            files.sort() # 일관성 있는 순서를 위해 정렬
            scope_text = "하위 폴더 포함" if include_subfolders else "선택 폴더만"
            self.log_message(f"대상 파일 {len(files)}개 발견 ({scope_text})")
            return folder, files
        except Exception as e:
            messagebox.showerror("오류", f"폴더를 읽는 중 오류가 발생하였다: {e}")
            return None, []

    def display_file_path(self, folder, file_path):
        """로그에 표시할 상대 경로를 반환하는 함수"""
        try:
            return os.path.relpath(file_path, folder)
        except ValueError:
            return file_path

    def make_temp_path(self, file_path, index):
        """같은 폴더 안에서 사용할 임시 파일 경로를 생성하는 함수"""
        file_folder = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        temp_filename = f".filerename_tmp_{os.getpid()}_{index}_{filename}"
        temp_path = os.path.join(file_folder, temp_filename)

        suffix = 1
        while os.path.exists(temp_path):
            temp_filename = f".filerename_tmp_{os.getpid()}_{index}_{suffix}_{filename}"
            temp_path = os.path.join(file_folder, temp_filename)
            suffix += 1

        return temp_path

    def run_rename_operations(self, folder, operations, complete_message):
        """파일명 변경을 임시 이름 변경 후 최종 이름 변경 방식으로 실행하는 함수"""
        operations = [
            (old_path, new_path)
            for old_path, new_path in operations
            if os.path.abspath(old_path) != os.path.abspath(new_path)
        ]

        if not operations:
            messagebox.showinfo("알림", "변경할 파일이 없다.")
            return

        target_counts = Counter(os.path.abspath(new_path).lower() for _, new_path in operations)
        duplicate_targets = {target for target, count in target_counts.items() if count > 1}
        if duplicate_targets:
            for old_path, new_path in operations:
                if os.path.abspath(new_path).lower() in duplicate_targets:
                    self.log_message(
                        f"실패 ({self.display_file_path(folder, old_path)}): 같은 결과 파일명이 중복된다."
                    )
            messagebox.showwarning("알림", "같은 결과 파일명이 중복되어 변경을 중단하였다.")
            return

        temp_operations = []
        changed_count = 0

        for index, (old_path, new_path) in enumerate(operations, start=1):
            temp_path = self.make_temp_path(old_path, index)
            try:
                os.rename(old_path, temp_path)
                temp_operations.append((temp_path, new_path, old_path))
            except Exception as e:
                self.log_message(f"실패 ({self.display_file_path(folder, old_path)}): {e}")

        for temp_path, new_path, old_path in temp_operations:
            try:
                os.rename(temp_path, new_path)
                if not os.path.exists(new_path):
                    raise OSError("최종 파일을 확인할 수 없다.")
                old_display = self.display_file_path(folder, old_path)
                new_display = self.display_file_path(folder, new_path)
                self.log_message(f"변경: {old_display} -> {new_display}")
                changed_count += 1
            except Exception as e:
                self.log_message(f"실패 ({self.display_file_path(folder, old_path)}): {e}")
                try:
                    os.rename(temp_path, old_path)
                    self.log_message(f"복구: {self.display_file_path(folder, old_path)}")
                except Exception as restore_error:
                    self.log_message(
                        f"복구 실패 ({self.display_file_path(folder, temp_path)}): {restore_error}"
                    )

        messagebox.showinfo("완료", complete_message.format(count=changed_count))

    def apply_affix(self):
        """접두사와 접미사를 기존 파일명에 추가하는 함수"""
        folder, files = self.get_files_in_folder()
        if not folder or not files:
            return

        prefix = self.entry_prefix.get()
        suffix = self.entry_suffix.get()

        if not prefix and not suffix:
            messagebox.showinfo("알림", "접두사 또는 접미사를 입력해야 한다.")
            return

        operations = []
        for file_path in files:
            file_folder = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{prefix}{name}{suffix}{ext}"
            operations.append((file_path, os.path.join(file_folder, new_filename)))

        self.run_rename_operations(folder, operations, "총 {count}개의 파일 이름이 변경되었다.")

    def apply_batch_rename(self):
        """사용자가 지정한 기본 이름과 일련번호(001, 002 등)로 파일명을 일괄 변경하는 함수"""
        folder, files = self.get_files_in_folder()
        if not folder or not files:
            return

        base_name = self.entry_basename.get()
        if not base_name:
            messagebox.showinfo("알림", "새로운 기본 파일명을 입력해야 한다.")
            return

        operations = []
        for index, file_path in enumerate(files, start=1):
            file_folder = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            _, ext = os.path.splitext(filename)
            # 숫자는 3자리로 포맷팅 (예: 001, 002, 003...)
            new_filename = f"{base_name}_{index:03d}{ext}"
            operations.append((file_path, os.path.join(file_folder, new_filename)))

        self.run_rename_operations(folder, operations, "총 {count}개의 파일 이름이 일괄 변경되었다.")

    def get_context_menu_command(self, folder_arg):
        """현재 실행 환경에 맞는 우클릭 메뉴 실행 명령을 반환하는 함수"""
        if getattr(sys, "frozen", False):
            app_path = sys.executable
            return f'"{app_path}" "{folder_arg}"'

        script_path = os.path.abspath(__file__)
        python_exe = sys.executable
        if os.path.basename(python_exe).lower() == "python.exe":
            pythonw_exe = os.path.join(os.path.dirname(python_exe), "pythonw.exe")
            if os.path.exists(pythonw_exe):
                python_exe = pythonw_exe

        return f'"{python_exe}" "{script_path}" "{folder_arg}"'

    def set_registry_default_value(self, key_path, value):
        """HKCU 레지스트리 키의 기본값을 설정하는 함수"""
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, value)

    def register_context_menu(self):
        """Windows 탐색기 폴더 우클릭 메뉴에 프로그램을 등록하는 함수"""
        menu_text = "일괄 파일명 변경 프로그램 열기"
        background_shell = r"Software\Classes\Directory\Background\shell\FileRenamer"
        background_command = background_shell + r"\command"
        folder_shell = r"Software\Classes\Directory\shell\FileRenamer"
        folder_command = folder_shell + r"\command"

        try:
            self.set_registry_default_value(background_shell, menu_text)
            self.set_registry_default_value(background_command, self.get_context_menu_command("%V"))
            self.set_registry_default_value(folder_shell, menu_text)
            self.set_registry_default_value(folder_command, self.get_context_menu_command("%1"))
        except OSError as e:
            messagebox.showerror("오류", f"우클릭 메뉴 등록 중 오류가 발생하였다: {e}")
            self.log_message(f"우클릭 메뉴 등록 실패: {e}")
            return

        self.log_message("우클릭 메뉴 등록 완료")
        messagebox.showinfo("완료", "Windows 우클릭 메뉴에 등록되었다.")

    def unregister_context_menu(self):
        """Windows 탐색기 폴더 우클릭 메뉴에서 프로그램을 제거하는 함수"""
        registry_paths = [
            r"Software\Classes\Directory\Background\shell\FileRenamer\command",
            r"Software\Classes\Directory\Background\shell\FileRenamer",
            r"Software\Classes\Directory\shell\FileRenamer\command",
            r"Software\Classes\Directory\shell\FileRenamer",
        ]

        failed_paths = []
        for path in registry_paths:
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, path)
            except FileNotFoundError:
                continue
            except OSError:
                failed_paths.append(path)

        if failed_paths:
            messagebox.showwarning("알림", "일부 우클릭 메뉴 항목을 제거하지 못하였다.")
            self.log_message(f"우클릭 메뉴 일부 제거 실패: {', '.join(failed_paths)}")
            return

        self.log_message("우클릭 메뉴 제거 완료")
        messagebox.showinfo("완료", "Windows 우클릭 메뉴에서 제거되었다.")

if __name__ == "__main__":
    initial_folder = sys.argv[1] if len(sys.argv) > 1 else None
    root = tk.Tk()
    app = FileRenamerApp(root, initial_folder)
    root.mainloop()

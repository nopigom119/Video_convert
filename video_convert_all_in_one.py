import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import moviepy.editor as mp
import threading
import queue # 스레드 간 안전한 통신을 위해 추가
from proglog import ProgressBarLogger
import shutil # 파일 이동을 위해 추가

# 지원하는 비디오 확장자 (확인용) - 필요에 따라 추가/수정
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
# 변환할 목표 포맷과 확장자 매핑
TARGET_FORMATS = {
    "MP4": "mp4",
    "AVI": "avi",
    "MOV": "mov",
    "WebM": "webm",
    "GIF": "gif" # GIF 변환 추가
}

# Moviepy 진행률 업데이트를 처리할 클래스
class ConversionLogger(ProgressBarLogger):
    def __init__(self, queue_, conversion_type="single", file_index=None, total_files=None, filename=None):
        super().__init__()
        self.queue = queue_
        self._last_percent = -1
        self.conversion_type = conversion_type # "single" or "batch"
        self.file_index = file_index
        self.total_files = total_files
        self.filename = filename

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == 'index':
            total = self.bars[bar]['total']
            percent = -1
            if total > 0:
                percent = min(int((value / total) * 100), 100)
            
            if percent != self._last_percent:
                progress_info = {
                    "type": "progress",
                    "conversion_type": self.conversion_type,
                    "percent": percent,
                    "file_index": self.file_index,
                    "total_files": self.total_files,
                    "filename": self.filename
                }
                self.queue.put(progress_info)
                self._last_percent = percent

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("비디오 변환기 (탭 지원)")
        self.root.geometry("650x620") # UI 크기 약간 조정 (상태 메시지 공간 고려)

        # --- 공용 변수 ---
        self.status = tk.StringVar()
        self.conversion_running = False
        self.progress_queue = queue.Queue()
        self.current_conversion_mode = None # "single" or "batch"

        # --- 단일 파일 변환용 변수 ---
        self.sf_input_filepath = tk.StringVar()
        self.sf_original_extension = tk.StringVar()
        self.sf_target_format = tk.StringVar()

        # --- 폴더 일괄 변환용 변수 ---
        self.bf_input_folder_path = tk.StringVar()
        self.bf_output_folder_originals_path = tk.StringVar() # 사용자가 선택한 원본 저장 폴더
        self.bf_target_format = tk.StringVar()
        self.bf_files_to_convert_list = []
        self.bf_converted_original_files_paths = []

        self.create_main_layout()
        self.status.set("모드를 선택하고 파일을 변환하세요.")
        self.root.after(100, self.process_queue) # 큐 폴링 시작

    def create_main_layout(self):
        # --- 메인 프레임 ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 탭 컨트롤 (Notebook) ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- 단일 파일 변환 탭 ---
        self.sf_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.sf_tab, text="단일 파일 변환")
        self.create_single_file_tab_widgets(self.sf_tab)

        # --- 폴더 일괄 변환 탭 ---
        self.bf_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.bf_tab, text="폴더 일괄 변환")
        self.create_batch_folder_tab_widgets(self.bf_tab)
        
        # --- 공통 상태 표시줄 ---
        status_frame = ttk.Frame(main_frame, padding="5")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Label(status_frame, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.on_tab_change() # 초기 상태 설정

    def on_tab_change(self, event=None):
        selected_tab_index = self.notebook.index(self.notebook.select())
        if selected_tab_index == 0: 
            self.status.set("단일 변환: 파일을 선택하고 변환할 포맷을 지정하세요.")
        elif selected_tab_index == 1: 
            self.status.set("일괄 변환: 폴더들을 선택하고 변환할 포맷을 지정하세요. 원본 저장 폴더는 선택 사항입니다.")
        self.enable_buttons()


    def create_single_file_tab_widgets(self, parent_frame):
        # 파일 선택
        file_frame = ttk.LabelFrame(parent_frame, text="파일 선택", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        ttk.Button(file_frame, text="파일 선택", command=self.sf_select_file).pack(side=tk.LEFT, padx=5)
        ttk.Entry(file_frame, textvariable=self.sf_input_filepath, state="readonly", width=40).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 원본 정보
        info_frame = ttk.LabelFrame(parent_frame, text="원본 파일 정보", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        ttk.Label(info_frame, text="원본 확장자:").pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame, textvariable=self.sf_original_extension).pack(side=tk.LEFT)

        # 변환 설정
        convert_frame = ttk.LabelFrame(parent_frame, text="변환 설정", padding="10")
        convert_frame.pack(fill=tk.X, pady=5)
        ttk.Label(convert_frame, text="변환할 포맷:").pack(side=tk.LEFT, padx=5)
        self.sf_format_combobox = ttk.Combobox(convert_frame, textvariable=self.sf_target_format,
                                            values=list(TARGET_FORMATS.keys()), state="readonly")
        self.sf_format_combobox.pack(side=tk.LEFT, padx=5)
        self.sf_format_combobox.bind("<<ComboboxSelected>>", self.enable_buttons)
        
        self.sf_convert_button = ttk.Button(convert_frame, text="변환 시작", command=self.sf_start_conversion_thread, state="disabled")
        self.sf_convert_button.pack(side=tk.LEFT, padx=10)

        # 진행률 표시줄
        progress_frame = ttk.Frame(parent_frame, padding=(0, 10, 0, 10))
        progress_frame.pack(fill=tk.X)
        self.sf_progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.sf_progress_bar.pack(fill=tk.X, expand=True)
        self.sf_current_file_label = ttk.Label(progress_frame, text="진행률: 0%") 
        self.sf_current_file_label.pack(fill=tk.X, pady=(2,0))


    def create_batch_folder_tab_widgets(self, parent_frame):
        # 입력 폴더 선택
        input_folder_frame = ttk.LabelFrame(parent_frame, text="입력 폴더 선택", padding="10")
        input_folder_frame.pack(fill=tk.X, pady=5)
        ttk.Button(input_folder_frame, text="폴더 선택", command=self.bf_select_input_folder).pack(side=tk.LEFT, padx=5)
        ttk.Entry(input_folder_frame, textvariable=self.bf_input_folder_path, state="readonly", width=50).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 원본 저장 폴더 선택 (선택 사항)
        output_originals_frame = ttk.LabelFrame(parent_frame, text="변환된 원본 저장 폴더 선택 (선택 사항)", padding="10")
        output_originals_frame.pack(fill=tk.X, pady=5)
        ttk.Button(output_originals_frame, text="폴더 선택", command=self.bf_select_output_folder_originals).pack(side=tk.LEFT, padx=5)
        ttk.Entry(output_originals_frame, textvariable=self.bf_output_folder_originals_path, state="readonly", width=50).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(output_originals_frame, text="선택 해제", command=self.bf_clear_output_folder_originals).pack(side=tk.LEFT, padx=5)


        # 변환 설정
        convert_frame = ttk.LabelFrame(parent_frame, text="변환 설정", padding="10")
        convert_frame.pack(fill=tk.X, pady=5)
        ttk.Label(convert_frame, text="변환할 포맷:").pack(side=tk.LEFT, padx=5)
        self.bf_format_combobox = ttk.Combobox(convert_frame, textvariable=self.bf_target_format,
                                            values=list(TARGET_FORMATS.keys()), state="readonly")
        self.bf_format_combobox.pack(side=tk.LEFT, padx=5)
        self.bf_format_combobox.bind("<<ComboboxSelected>>", self.enable_buttons)
        
        self.bf_convert_button = ttk.Button(convert_frame, text="일괄 변환 시작", command=self.bf_start_batch_conversion_thread, state="disabled")
        self.bf_convert_button.pack(side=tk.LEFT, padx=10)

        # 진행률 표시줄
        progress_frame = ttk.Frame(parent_frame, padding=(0, 5, 0, 10))
        progress_frame.pack(fill=tk.X)
        self.bf_current_file_label = ttk.Label(progress_frame, text="현재 파일: N/A")
        self.bf_current_file_label.pack(fill=tk.X, pady=(0,2))
        self.bf_progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.bf_progress_bar.pack(fill=tk.X, expand=True)
        
        self.bf_overall_progress_label = ttk.Label(progress_frame, text="전체 진행: 0/0")
        self.bf_overall_progress_label.pack(fill=tk.X, pady=(2,0))
        self.bf_overall_progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.bf_overall_progress_bar.pack(fill=tk.X, expand=True, pady=(0,5))

    def enable_buttons(self, event=None):
        # 단일 파일 변환 버튼 상태
        if not self.conversion_running and self.sf_input_filepath.get() and self.sf_target_format.get():
            self.sf_convert_button.config(state="normal")
        else:
            self.sf_convert_button.config(state="disabled")

        # 폴더 일괄 변환 버튼 상태
        # 원본 저장 폴더는 선택 사항이므로, 해당 조건 제거
        if not self.conversion_running and \
           self.bf_input_folder_path.get() and \
           self.bf_target_format.get():
            self.bf_convert_button.config(state="normal")
        else:
            self.bf_convert_button.config(state="disabled")
            
    # --- 단일 파일 변환 관련 메소드 ---
    def sf_select_file(self):
        if self.conversion_running:
            messagebox.showwarning("진행 중", "현재 다른 파일을 변환 중입니다.")
            return

        filepath = filedialog.askopenfilename(
            title="비디오 파일 선택",
            filetypes=[("비디오 파일", " ".join(f"*{ext}" for ext in VIDEO_EXTENSIONS)),
                       ("모든 파일", "*.*")]
        )
        if not filepath: return

        _, ext = os.path.splitext(filepath)
        ext_lower = ext.lower()

        if ext_lower in VIDEO_EXTENSIONS:
            self.sf_input_filepath.set(filepath)
            self.sf_original_extension.set(ext)
            self.status.set(f"단일: 파일 선택됨: {os.path.basename(filepath)}")
            self.sf_progress_bar['value'] = 0
            self.sf_current_file_label.config(text="진행률: 0%")
        else:
            self.sf_input_filepath.set("")
            self.sf_original_extension.set("")
            self.sf_target_format.set("") 
            self.sf_progress_bar['value'] = 0
            self.sf_current_file_label.config(text="진행률: 0%")
            self.status.set("선택한 파일이 지원하는 비디오 형식이 아닙니다.")
            messagebox.showerror("오류", "선택한 파일이 지원하는 비디오 형식이 아닙니다.\n지원 형식: " + ", ".join(VIDEO_EXTENSIONS))
        self.enable_buttons()

    def sf_start_conversion_thread(self):
        if not self.sf_input_filepath.get() or not self.sf_target_format.get():
            messagebox.showwarning("준비 미흡", "변환할 파일과 목표 포맷을 모두 선택해야 합니다.")
            return

        if self.conversion_running:
             messagebox.showwarning("진행 중", "이미 변환 작업이 진행 중입니다.")
             return

        self.conversion_running = True
        self.current_conversion_mode = "single"
        self.enable_buttons() 
        self.sf_format_combobox.config(state="disabled")
        self.sf_progress_bar['value'] = 0
        self.sf_progress_bar.config(mode='determinate')
        self.sf_current_file_label.config(text="진행률: 0%")
        self.status.set("단일 파일 변환 준비 중...")

        conversion_thread = threading.Thread(target=self.execute_single_conversion, daemon=True)
        conversion_thread.start()

    def execute_single_conversion(self):
        input_path = self.sf_input_filepath.get()
        selected_format_name = self.sf_target_format.get()
        target_ext = TARGET_FORMATS.get(selected_format_name)
        
        input_dir = os.path.dirname(input_path)
        input_filename_no_ext = os.path.splitext(os.path.basename(input_path))[0]
        output_filename = f"{input_filename_no_ext}_converted.{target_ext}" 
        output_path = os.path.join(input_dir, output_filename)

        video_clip = None
        filename_for_logger = os.path.basename(input_path)

        try:
            video_clip = mp.VideoFileClip(input_path)
            logger = ConversionLogger(self.progress_queue, conversion_type="single", 
                                      file_index=1, total_files=1, filename=filename_for_logger)

            if target_ext == 'gif':
                self.progress_queue.put({"type": "indeterminate_start", "conversion_type": "single", "filename": filename_for_logger})
                self.progress_queue.put({"type": "status_update", "message": f"GIF 변환 중: {filename_for_logger} (진행률 표시 안됨)", "conversion_type": "single"})
                video_clip.write_gif(output_path, fps=10, logger=logger)
                self.progress_queue.put({"type": "progress", "conversion_type": "single", "percent": 100, "filename": filename_for_logger})
            else:
                self.progress_queue.put({"type": "progress", "conversion_type": "single", "percent": 0, "filename": filename_for_logger})
                cpu_cores = max(1, os.cpu_count() // 2)
                try:
                    video_clip.write_videofile(
                        output_path, codec='h264_nvenc', audio_codec='aac', logger=logger,
                        ffmpeg_params=["-preset", "p4", "-tune", "hq", "-rc", "vbr", "-b:v", "5M"]
                    )
                except Exception:
                    self.progress_queue.put({"type": "status_update", "message": f"하드웨어 가속 실패. CPU로 변환 중: {filename_for_logger}", "conversion_type": "single"})
                    video_clip.write_videofile(
                        output_path, codec='libx264', audio_codec='aac', logger=logger,
                        preset='faster', threads=cpu_cores
                    )
            
            success_msg = f"단일 변환 완료: {output_filename}"
            self.progress_queue.put({"type": "single_success", "message": success_msg})

        except Exception as e:
            error_msg = f"단일 변환 오류 ({filename_for_logger}): {str(e)[:150]}"
            self.progress_queue.put({"type": "single_error", "message": error_msg})
            import traceback
            print(f"--- Single Conversion Error for {input_path} ---")
            traceback.print_exc()
            print("--- End Traceback ---")
        finally:
            if video_clip:
                try: video_clip.close()
                except Exception as close_err: print(f"Error closing video clip (single): {close_err}")

    # --- 폴더 일괄 변환 관련 메소드 ---
    def bf_select_input_folder(self):
        if self.conversion_running:
            messagebox.showwarning("진행 중", "현재 변환 작업이 진행 중입니다.")
            return
        folder_path = filedialog.askdirectory(title="동영상 파일이 있는 폴더 선택")
        if folder_path:
            self.bf_input_folder_path.set(folder_path)
            self.status.set(f"일괄: 입력 폴더 선택됨: {folder_path}")
            self.bf_progress_bar['value'] = 0
            self.bf_overall_progress_bar['value'] = 0
            self.bf_current_file_label.config(text="현재 파일: N/A")
            self.bf_overall_progress_label.config(text="전체 진행: 0/0")
            self.enable_buttons()

    def bf_select_output_folder_originals(self):
        if self.conversion_running:
            messagebox.showwarning("진행 중", "현재 변환 작업이 진행 중입니다.")
            return
        folder_path = filedialog.askdirectory(title="변환된 원본 파일을 저장할 폴더 선택")
        if folder_path:
            self.bf_output_folder_originals_path.set(folder_path)
            self.status.set(f"일괄: 원본 저장 폴더 선택됨: {folder_path}")
            self.enable_buttons()
            if self.bf_input_folder_path.get() and folder_path == self.bf_input_folder_path.get():
                messagebox.showwarning("경고", "입력 폴더와 원본 저장 폴더가 동일합니다. 원본 파일은 변환 후 이동될 때 덮어쓰이지 않도록 주의하세요.")
    
    def bf_clear_output_folder_originals(self):
        if self.conversion_running:
            messagebox.showwarning("진행 중", "현재 변환 작업이 진행 중입니다.")
            return
        self.bf_output_folder_originals_path.set("")
        self.status.set("일괄: 원본 저장 폴더 선택이 해제되었습니다. 입력 폴더 내 'Old_video_collection'에 저장됩니다.")
        self.enable_buttons()


    def bf_start_batch_conversion_thread(self):
        input_folder = self.bf_input_folder_path.get()
        # 사용자가 선택한 원본 저장 폴더 경로 가져오기
        output_originals_folder_user_selected = self.bf_output_folder_originals_path.get()
        target_format_name = self.bf_target_format.get()

        # 입력 폴더와 목표 포맷은 필수
        if not input_folder or not target_format_name:
            messagebox.showwarning("준비 미흡", "입력 폴더와 목표 포맷을 모두 선택해야 합니다.")
            return

        # 실제 원본 저장 폴더 경로 결정
        actual_output_originals_folder = ""
        if not output_originals_folder_user_selected:
            # 사용자가 폴더를 선택하지 않은 경우, 입력 폴더 내에 "Old_video_collection" 폴더 경로 생성
            actual_output_originals_folder = os.path.join(input_folder, "Old_video_collection")
            self.status.set(f"일괄: 원본 저장 폴더 미지정. 입력 폴더 내 'Old_video_collection'에 저장됩니다.")
        else:
            actual_output_originals_folder = output_originals_folder_user_selected
            # 사용자가 선택한 폴더가 입력 폴더와 동일한 경우 경고 (선택 사항이지만 유지)
            if input_folder == actual_output_originals_folder:
                if not messagebox.askyesno("확인", "입력 폴더와 원본 저장 폴더가 동일합니다. 계속 진행하시겠습니까?\n(이름이 같은 경우 원본이 덮어쓰일 수 있습니다.)"):
                    return
        
        target_ext = TARGET_FORMATS.get(target_format_name)
        if not target_ext:
            messagebox.showerror("오류", "선택된 목표 포맷에 해당하는 확장자를 찾을 수 없습니다.")
            return

        self.bf_files_to_convert_list = []
        for filename in os.listdir(input_folder):
            filepath = os.path.join(input_folder, filename)
            if os.path.isfile(filepath):
                _, ext = os.path.splitext(filename)
                if ext.lower() in VIDEO_EXTENSIONS and ext.lower() != f".{target_ext.lower()}":
                    self.bf_files_to_convert_list.append(filepath)
        
        if not self.bf_files_to_convert_list:
            messagebox.showinfo("알림", f"선택한 폴더에 '{target_format_name}'({target_ext})로 변환할 대상 파일이 없습니다.")
            return

        if self.conversion_running:
             messagebox.showwarning("진행 중", "이미 변환 작업이 진행 중입니다.")
             return

        self.conversion_running = True
        self.current_conversion_mode = "batch"
        self.enable_buttons() 
        self.bf_format_combobox.config(state="disabled")
        
        self.bf_progress_bar['value'] = 0
        self.bf_overall_progress_bar['value'] = 0
        self.bf_current_file_label.config(text="현재 파일: N/A")
        self.bf_overall_progress_label.config(text=f"전체 진행: 0/{len(self.bf_files_to_convert_list)}")
        # 상태 메시지는 위에서 actual_output_originals_folder 설정 시 이미 업데이트됨
        if not output_originals_folder_user_selected:
             self.status.set(f"일괄 변환 준비 중... 원본은 '{os.path.basename(actual_output_originals_folder)}'에 저장됩니다.")
        else:
            self.status.set("일괄 변환 준비 중...")

        self.bf_converted_original_files_paths = []

        conversion_thread = threading.Thread(target=self.execute_batch_conversion_and_move, 
                                             args=(input_folder, actual_output_originals_folder, target_format_name, target_ext), 
                                             daemon=True)
        conversion_thread.start()

    def execute_batch_conversion_and_move(self, input_folder, output_originals_folder_final, target_format_name, target_ext):
        total_files = len(self.bf_files_to_convert_list)
        
        for i, input_path in enumerate(self.bf_files_to_convert_list):
            filename = os.path.basename(input_path)
            self.progress_queue.put({
                "type": "status_update", 
                "message": f"파일 ({i+1}/{total_files}) 변환 시작: {filename}",
                "conversion_type": "batch", 
                "file_index": i + 1, "total_files": total_files, "filename": filename
            })
            
            success, original_file_path, _ = self._convert_one_batch_file(input_path, target_format_name, target_ext, i + 1, total_files)
            
            if success and original_file_path:
                self.bf_converted_original_files_paths.append(original_file_path)
            
            self.progress_queue.put({
                "type": "overall_progress", "current": i + 1, "total": total_files
            })

        if self.bf_converted_original_files_paths:
            self.progress_queue.put({"type": "status_update", "message": f"원본 파일 이동 시작 (대상: {output_originals_folder_final})...", "conversion_type": "batch"})
            moved_count, skipped_count = 0, 0
            try:
                # output_originals_folder_final 경로가 없으면 생성 (exist_ok=True로 이미 있어도 오류 없음)
                os.makedirs(output_originals_folder_final, exist_ok=True) 
                for original_path in self.bf_converted_original_files_paths:
                    if not os.path.exists(original_path):
                        skipped_count +=1; continue
                    original_filename = os.path.basename(original_path)
                    destination_path = os.path.join(output_originals_folder_final, original_filename)
                    if os.path.exists(destination_path):
                        print(f"Skipping move: {original_filename} already exists in {output_originals_folder_final}.")
                        self.progress_queue.put({"type": "status_update", "message": f"이동 건너뜀 (중복): {original_filename}", "conversion_type": "batch"})
                        skipped_count += 1; continue
                    shutil.move(original_path, destination_path)
                    moved_count += 1
                    self.progress_queue.put({"type": "status_update", "message": f"원본 이동: {original_filename}", "conversion_type": "batch"})
                move_summary = f"총 {len(self.bf_converted_original_files_paths)}개 원본 중 {moved_count}개 이동 ({output_originals_folder_final}), {skipped_count}개 건너뜀."
                self.progress_queue.put({"type": "status_update", "message": move_summary, "conversion_type": "batch"})
            except Exception as e:
                error_msg = f"원본 파일 이동 중 오류 ({output_originals_folder_final}): {str(e)[:150]}"
                self.progress_queue.put({"type": "status_update", "message": error_msg, "conversion_type": "batch"})
                self.progress_queue.put({"type": "batch_error", "message": error_msg}) # 오류 플래그
                return

        self.progress_queue.put({"type": "batch_success", "message": "모든 변환 및 원본 파일 이동 작업이 완료되었습니다."})

    def _convert_one_batch_file(self, input_path, selected_format_name, target_ext, file_index, total_files):
        input_dir = os.path.dirname(input_path)
        input_filename_no_ext, _ = os.path.splitext(os.path.basename(input_path))
        output_filename = f"{input_filename_no_ext}.{target_ext}"
        output_path = os.path.join(input_dir, output_filename) 

        video_clip = None
        original_file_to_move = input_path
        filename_for_logger = os.path.basename(input_path)

        try:
            video_clip = mp.VideoFileClip(input_path)
            logger = ConversionLogger(self.progress_queue, conversion_type="batch", 
                                      file_index=file_index, total_files=total_files, filename=filename_for_logger)

            if target_ext == 'gif':
                self.progress_queue.put({"type": "indeterminate_start", "conversion_type": "batch", "file_index": file_index, "total_files": total_files, "filename": filename_for_logger})
                self.progress_queue.put({"type": "status_update", "message": f"GIF 변환 중 ({file_index}/{total_files}): {filename_for_logger}", "conversion_type": "batch"})
                video_clip.write_gif(output_path, fps=10, logger=logger)
                self.progress_queue.put({"type": "progress", "conversion_type": "batch", "percent": 100, "file_index": file_index, "total_files": total_files, "filename": filename_for_logger})
            else:
                self.progress_queue.put({"type": "progress", "conversion_type": "batch", "percent": 0, "file_index": file_index, "total_files": total_files, "filename": filename_for_logger})
                cpu_cores = max(1, os.cpu_count() // 2)
                try:
                    video_clip.write_videofile(
                        output_path, codec='h264_nvenc', audio_codec='aac', logger=logger,
                        ffmpeg_params=["-preset", "p4", "-tune", "hq", "-rc", "vbr", "-b:v", "5M"]
                    )
                except Exception:
                    self.progress_queue.put({"type": "status_update", "message": f"하드웨어 가속 실패. CPU로 변환 중 ({file_index}/{total_files}): {filename_for_logger}", "conversion_type": "batch"})
                    video_clip.write_videofile(
                        output_path, codec='libx264', audio_codec='aac', logger=logger,
                        preset='faster', threads=cpu_cores
                    )
            
            self.progress_queue.put({"type": "status_update", "message": f"변환 완료 ({file_index}/{total_files}): {output_filename}", "conversion_type": "batch"})
            return True, original_file_to_move, output_path

        except Exception as e:
            error_msg = f"변환 오류 ({file_index}/{total_files} - {filename_for_logger}): {str(e)[:100]}"
            self.progress_queue.put({"type": "status_update", "message": error_msg, "conversion_type": "batch"})
            import traceback
            print(f"--- Batch Conversion Error for {input_path} ---")
            traceback.print_exc()
            print("--- End Traceback ---")
            return False, None, None
        finally:
            if video_clip:
                try: video_clip.close()
                except Exception as close_err: print(f"Error closing video clip (batch file): {close_err}")

    # --- 공용 큐 처리 메소드 ---
    def process_queue(self):
        try:
            message_obj = self.progress_queue.get_nowait()
            msg_type = message_obj.get("type")
            conv_type = message_obj.get("conversion_type") 

            if msg_type == "progress":
                percent = message_obj.get("percent", 0)
                fname = message_obj.get("filename", "N/A")
                
                if conv_type == "single":
                    self.sf_progress_bar['value'] = percent
                    self.sf_current_file_label.config(text=f"진행률: {percent}% ({fname})")
                    if percent < 100: self.status.set(f"단일 변환 중: {fname} {percent}%")
                elif conv_type == "batch":
                    file_idx = message_obj.get("file_index")
                    total_f = message_obj.get("total_files")
                    self.bf_progress_bar['value'] = percent
                    self.bf_current_file_label.config(text=f"현재 파일 ({file_idx}/{total_f}): {fname} [{percent}%]")
                    if percent < 100: self.status.set(f"일괄 변환 중 ({file_idx}/{total_f}): {fname} {percent}%")

            elif msg_type == "overall_progress": 
                current = message_obj.get("current", 0)
                total = message_obj.get("total", 0)
                self.bf_overall_progress_bar['value'] = (current / total) * 100 if total > 0 else 0
                self.bf_overall_progress_label.config(text=f"전체 진행: {current}/{total}")

            elif msg_type == "status_update":
                current_status = message_obj.get("message", "")
                # status_update 메시지에 conversion_type이 없을 수도 있으므로, 현재 모드를 참조
                active_conv_type = conv_type if conv_type else self.current_conversion_mode 
                
                self.status.set(current_status) # 공통 상태바 업데이트
                
                if active_conv_type == "batch": # 일괄 변환 중 특정 파일 상태 업데이트
                    file_idx = message_obj.get("file_index")
                    total_f = message_obj.get("total_files")
                    fname = message_obj.get("filename")
                    if fname and file_idx and total_f: # 파일 정보가 있는 경우에만 업데이트
                        self.bf_current_file_label.config(text=f"현재 파일 ({file_idx}/{total_f}): {fname}")
                    elif "원본 파일 이동 시작" in current_status or "원본 이동" in current_status or "이동 건너뜀" in current_status:
                        # 파일 이동 관련 메시지는 현재 파일 레이블을 일반 메시지로 변경
                         self.bf_current_file_label.config(text="파일 이동 중...")
                    # 그 외의 batch status update는 bf_current_file_label을 변경하지 않을 수 있음

                elif active_conv_type == "single": # 단일 변환 중 상태 업데이트
                    fname = message_obj.get("filename")
                    if fname: self.sf_current_file_label.config(text=f"파일: {fname}")


            elif msg_type == "indeterminate_start":
                fname = message_obj.get("filename", "N/A")
                if conv_type == "single":
                    self.sf_progress_bar.config(mode='indeterminate')
                    self.sf_progress_bar.start(10)
                    self.sf_current_file_label.config(text=f"GIF 변환 중: {fname}")
                elif conv_type == "batch":
                    file_idx = message_obj.get("file_index")
                    total_f = message_obj.get("total_files")
                    self.bf_progress_bar.config(mode='indeterminate')
                    self.bf_progress_bar.start(10)
                    self.bf_current_file_label.config(text=f"현재 파일 ({file_idx}/{total_f}): {fname} [GIF 변환 중]")
            
            elif msg_type == "single_success":
                self.status.set(message_obj.get("message", "단일 파일 변환 완료!"))
                if self.sf_progress_bar['mode'] == 'indeterminate': self.sf_progress_bar.stop()
                self.sf_progress_bar.config(mode='determinate')
                self.sf_progress_bar['value'] = 100
                self.sf_current_file_label.config(text=f"진행률: 100% (완료)")
                
                self.conversion_running = False
                self.current_conversion_mode = None
                self.sf_format_combobox.config(state="readonly") 
                self.enable_buttons()
                messagebox.showinfo("성공", message_obj.get("message", "단일 파일 변환이 완료되었습니다."))
            
            elif msg_type == "single_error":
                self.status.set(message_obj.get("message", "단일 파일 변환 오류."))
                if self.sf_progress_bar['mode'] == 'indeterminate': self.sf_progress_bar.stop()
                self.sf_progress_bar.config(mode='determinate')
                
                self.conversion_running = False
                self.current_conversion_mode = None
                self.sf_format_combobox.config(state="readonly")
                self.enable_buttons()
                messagebox.showerror("단일 변환 오류", message_obj.get("message", "오류가 발생했습니다."))

            elif msg_type == "batch_success":
                self.status.set(message_obj.get("message", "일괄 작업 완료!"))
                if self.bf_progress_bar['mode'] == 'indeterminate': self.bf_progress_bar.stop()
                self.bf_progress_bar.config(mode='determinate')
                self.bf_progress_bar['value'] = 100
                
                num_total_files = len(self.bf_files_to_convert_list) if self.bf_files_to_convert_list else 0
                self.bf_overall_progress_bar['value'] = 100
                self.bf_overall_progress_label.config(text=f"전체 진행: {num_total_files}/{num_total_files}")
                self.bf_current_file_label.config(text="현재 파일: 완료")

                self.conversion_running = False
                self.current_conversion_mode = None
                self.bf_format_combobox.config(state="readonly")
                self.enable_buttons()
                messagebox.showinfo("성공", message_obj.get("message", "모든 작업이 성공적으로 완료되었습니다."))
            
            elif msg_type == "batch_error":
                self.status.set(message_obj.get("message", "일괄 작업 중 오류 발생."))
                if self.bf_progress_bar['mode'] == 'indeterminate': self.bf_progress_bar.stop()
                self.bf_progress_bar.config(mode='determinate')
                
                self.conversion_running = False
                self.current_conversion_mode = None
                self.bf_format_combobox.config(state="readonly")
                self.enable_buttons()
                messagebox.showerror("일괄 변환 오류", message_obj.get("message", "오류가 발생하여 작업이 중단되거나 부분적으로 완료되었습니다."))

            self.root.after(100, self.process_queue)

        except queue.Empty:
            self.root.after(100, self.process_queue)
        except Exception as e:
            print(f"Error in process_queue: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(100, self.process_queue)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
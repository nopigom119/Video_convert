import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import moviepy.editor as mp
import threading
import queue # 스레드 간 안전한 통신을 위해 추가
from proglog import ProgressBarLogger
import shutil # 파일 이동을 위해 추가
import traceback # 상세 오류 로깅용

# --- Language Configuration ---
current_language = 'ko' # Default language: 'ko' for Korean, 'en' for English

LANG_STRINGS = {
    'en': {
        'window_title': "Video Converter (Tabbed)",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",

        # Tab Titles
        'tab_single_file': "Single File Conversion",
        'tab_batch_folder': "Batch Folder Conversion",

        # Common Labels & Buttons
        'label_target_format': "Target Format:",
        'button_select_file': "Select File",
        'button_select_folder': "Select Folder",
        'button_start_conversion': "Start Conversion",
        'button_start_batch_conversion': "Start Batch Conversion",
        'button_clear_selection': "Clear Selection",

        # Single File Tab Specific
        'sf_labelframe_select_file': "File Selection",
        'sf_labelframe_original_info': "Original File Info",
        'sf_label_original_extension': "Original Extension:",
        'sf_labelframe_conversion_settings': "Conversion Settings",
        'sf_label_progress_initial': "Progress: 0%",

        # Batch Folder Tab Specific
        'bf_labelframe_input_folder': "Input Folder Selection",
        'bf_labelframe_output_originals_folder': "Output Folder for Originals (Optional)",
        'bf_labelframe_conversion_settings': "Conversion Settings", # Can be same as single
        'bf_label_current_file_initial': "Current File: N/A",
        'bf_label_overall_progress_initial': "Overall Progress: 0/0",

        # Status Messages
        'status_initial_prompt': "Select mode and convert files.",
        'status_sf_prompt': "Single: Select file and target format.",
        'status_bf_prompt': "Batch: Select folders and target format. Output folder for originals is optional.",
        'status_sf_file_selected': "Single: File selected: {filename}",
        'status_file_not_supported_short': "Selected file is not a supported video format.",
        'status_sf_conversion_ready': "Single file conversion ready.",
        'status_bf_input_folder_selected': "Batch: Input folder selected: {folder_path}",
        'status_bf_output_originals_selected': "Batch: Output folder for originals selected: {folder_path}",
        'status_bf_output_originals_cleared': "Batch: Output folder for originals cleared. Will save in 'Old_video_collection' in input folder.",
        'status_bf_conversion_ready': "Batch conversion ready.",
        'status_sf_preparing': "Preparing single file conversion...",
        'status_bf_preparing': "Preparing batch conversion...",
        'status_bf_preparing_with_output_folder': "Preparing batch conversion... Originals will be saved in '{foldername}'.",
        'status_gif_conversion_no_progress': "Converting to GIF: {filename} (Progress not shown)",
        'status_hw_accel_failed_cpu': "Hardware acceleration failed. Converting with CPU: {filename}",
        'status_sf_converting_progress': "Single converting: {filename} {percent}%",
        'status_bf_converting_progress': "Batch converting ({file_idx}/{total_f}): {filename} {percent}%",
        'status_bf_file_conversion_start': "Starting conversion for file ({file_idx}/{total_f}): {filename}",
        'status_bf_gif_conversion_no_progress': "Converting to GIF ({file_idx}/{total_f}): {filename}",
        'status_bf_hw_accel_failed_cpu': "HW accel failed. CPU converting ({file_idx}/{total_f}): {filename}",
        'status_bf_file_converted': "Converted ({file_idx}/{total_f}): {output_filename}",
        'status_bf_moving_originals_start': "Starting to move original files (Target: {output_folder})...",
        'status_bf_moving_originals_skipped_duplicate': "Skipped moving (duplicate): {original_filename}",
        'status_bf_moving_originals_moved': "Moved original: {original_filename}",
        'status_bf_moving_originals_summary': "Moved {moved_count} of {total_originals} originals to '{output_folder}', {skipped_count} skipped.",
        'status_moving_originals_error': "Error moving original files to '{output_folder}': {error_message}",
        'status_sf_completed_progress': "Progress: 100% (Completed)",
        'status_bf_current_file_completed': "Current File: Completed",
        'status_file_moving_in_progress': "Moving files...", # For batch current file label during move

        # Dialog Titles
        'dialog_title_warning': "Warning",
        'dialog_title_error': "Error",
        'dialog_title_info': "Information",
        'dialog_title_success': "Success",
        'dialog_title_confirm': "Confirm",
        'dialog_title_select_video_file': "Select Video File",
        'dialog_title_select_input_folder': "Select Folder with Videos",
        'dialog_title_select_output_originals_folder': "Select Folder to Save Original Files",

        # Dialog Messages
        'dialog_msg_conversion_in_progress_warning': "Another conversion is currently in progress.",
        'dialog_msg_select_file_and_format_warning': "Please select both a file and a target format.",
        'dialog_msg_already_in_progress_warning': "A conversion is already in progress.",
        'dialog_msg_file_not_supported_error': "The selected file is not a supported video format.\nSupported formats: {formats}",
        'dialog_msg_input_folder_and_format_warning': "Please select both an input folder and a target format.",
        'dialog_msg_target_ext_not_found_error': "Could not find extension for the selected target format.",
        'dialog_msg_no_files_to_convert_info': "No files found in the selected folder to convert to '{target_format_name}' ({target_ext}).",
        'dialog_msg_input_output_originals_same_warning': "Input folder and output folder for originals are the same. Continue?\n(Originals might be overwritten if names conflict.)",
        'dialog_msg_sf_conversion_complete': "Single file conversion completed: {output_filename}",
        'dialog_msg_sf_conversion_error': "Single file conversion error ({filename}): {error_message}",
        'dialog_msg_bf_all_tasks_complete': "All batch conversion and file moving tasks are complete.",
        'dialog_msg_bf_error_partial_complete': "An error occurred. The batch process may be incomplete or partially completed.",

        # File types for dialog
        'filetype_video_files': "Video Files",
        'filetype_all_files': "All Files",
    },
    'ko': {
        'window_title': "비디오 변환기 (탭 지원)",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",

        # Tab Titles
        'tab_single_file': "단일 파일 변환",
        'tab_batch_folder': "폴더 일괄 변환",

        # Common Labels & Buttons
        'label_target_format': "변환할 포맷:",
        'button_select_file': "파일 선택",
        'button_select_folder': "폴더 선택",
        'button_start_conversion': "변환 시작",
        'button_start_batch_conversion': "일괄 변환 시작",
        'button_clear_selection': "선택 해제",

        # Single File Tab Specific
        'sf_labelframe_select_file': "파일 선택",
        'sf_labelframe_original_info': "원본 파일 정보",
        'sf_label_original_extension': "원본 확장자:",
        'sf_labelframe_conversion_settings': "변환 설정",
        'sf_label_progress_initial': "진행률: 0%",

        # Batch Folder Tab Specific
        'bf_labelframe_input_folder': "입력 폴더 선택",
        'bf_labelframe_output_originals_folder': "변환된 원본 저장 폴더 선택 (선택 사항)",
        'bf_labelframe_conversion_settings': "변환 설정",
        'bf_label_current_file_initial': "현재 파일: N/A",
        'bf_label_overall_progress_initial': "전체 진행: 0/0",

        # Status Messages
        'status_initial_prompt': "모드를 선택하고 파일을 변환하세요.",
        'status_sf_prompt': "단일: 파일을 선택하고 변환할 포맷을 지정하세요.",
        'status_bf_prompt': "일괄: 폴더들을 선택하고 변환할 포맷을 지정하세요. 원본 저장 폴더는 선택 사항입니다.",
        'status_sf_file_selected': "단일: 파일 선택됨: {filename}",
        'status_file_not_supported_short': "선택한 파일이 지원하는 비디오 형식이 아닙니다.",
        'status_sf_conversion_ready': "단일 파일 변환 준비 완료.",
        'status_bf_input_folder_selected': "일괄: 입력 폴더 선택됨: {folder_path}",
        'status_bf_output_originals_selected': "일괄: 원본 저장 폴더 선택됨: {folder_path}",
        'status_bf_output_originals_cleared': "일괄: 원본 저장 폴더 선택이 해제되었습니다. 입력 폴더 내 'Old_video_collection'에 저장됩니다.",
        'status_bf_conversion_ready': "일괄 변환 준비 완료.",
        'status_sf_preparing': "단일 파일 변환 준비 중...",
        'status_bf_preparing': "일괄 변환 준비 중...",
        'status_bf_preparing_with_output_folder': "일괄 변환 준비 중... 원본은 '{foldername}'에 저장됩니다.",
        'status_gif_conversion_no_progress': "GIF 변환 중: {filename} (진행률 표시 안됨)",
        'status_hw_accel_failed_cpu': "하드웨어 가속 실패. CPU로 변환 중: {filename}",
        'status_sf_converting_progress': "단일 변환 중: {filename} {percent}%",
        'status_bf_converting_progress': "일괄 변환 중 ({file_idx}/{total_f}): {filename} {percent}%",
        'status_bf_file_conversion_start': "파일 ({file_idx}/{total_f}) 변환 시작: {filename}",
        'status_bf_gif_conversion_no_progress': "GIF 변환 중 ({file_idx}/{total_f}): {filename}",
        'status_bf_hw_accel_failed_cpu': "하드웨어 가속 실패. CPU로 변환 중 ({file_idx}/{total_f}): {filename}",
        'status_bf_file_converted': "변환 완료 ({file_idx}/{total_f}): {output_filename}",
        'status_bf_moving_originals_start': "원본 파일 이동 시작 (대상: {output_folder})...",
        'status_bf_moving_originals_skipped_duplicate': "이동 건너뜀 (중복): {original_filename}",
        'status_bf_moving_originals_moved': "원본 이동: {original_filename}",
        'status_bf_moving_originals_summary': "총 {total_originals}개 원본 중 {moved_count}개 이동 ({output_folder}), {skipped_count}개 건너뜀.",
        'status_moving_originals_error': "원본 파일 이동 중 오류 ({output_folder}): {error_message}",
        'status_sf_completed_progress': "진행률: 100% (완료)",
        'status_bf_current_file_completed': "현재 파일: 완료",
        'status_file_moving_in_progress': "파일 이동 중...",

        # Dialog Titles
        'dialog_title_warning': "경고",
        'dialog_title_error': "오류",
        'dialog_title_info': "알림",
        'dialog_title_success': "성공",
        'dialog_title_confirm': "확인",
        'dialog_title_select_video_file': "비디오 파일 선택",
        'dialog_title_select_input_folder': "동영상 파일이 있는 폴더 선택",
        'dialog_title_select_output_originals_folder': "변환된 원본 파일을 저장할 폴더 선택",

        # Dialog Messages
        'dialog_msg_conversion_in_progress_warning': "현재 다른 파일을 변환 중입니다.",
        'dialog_msg_select_file_and_format_warning': "변환할 파일과 목표 포맷을 모두 선택해야 합니다.",
        'dialog_msg_already_in_progress_warning': "이미 변환 작업이 진행 중입니다.",
        'dialog_msg_file_not_supported_error': "선택한 파일이 지원하는 비디오 형식이 아닙니다.\n지원 형식: {formats}",
        'dialog_msg_input_folder_and_format_warning': "입력 폴더와 목표 포맷을 모두 선택해야 합니다.",
        'dialog_msg_target_ext_not_found_error': "선택된 목표 포맷에 해당하는 확장자를 찾을 수 없습니다.",
        'dialog_msg_no_files_to_convert_info': "선택한 폴더에 '{target_format_name}'({target_ext})로 변환할 대상 파일이 없습니다.",
        'dialog_msg_input_output_originals_same_warning': "입력 폴더와 원본 저장 폴더가 동일합니다. 계속 진행하시겠습니까?\n(이름이 같은 경우 원본이 덮어쓰일 수 있습니다.)",
        'dialog_msg_sf_conversion_complete': "단일 파일 변환이 완료되었습니다: {output_filename}",
        'dialog_msg_sf_conversion_error': "단일 변환 오류 ({filename}): {error_message}",
        'dialog_msg_bf_all_tasks_complete': "모든 변환 및 원본 파일 이동 작업이 완료되었습니다.",
        'dialog_msg_bf_error_partial_complete': "오류가 발생하여 작업이 중단되거나 부분적으로 완료되었습니다.",

        # File types for dialog
        'filetype_video_files': "비디오 파일",
        'filetype_all_files': "모든 파일",
    }
}

def get_string(key, **kwargs):
    """Retrieves a string from LANG_STRINGS for the current_language."""
    s = LANG_STRINGS[current_language].get(key, f"<{key}_NOT_FOUND_IN_{current_language.upper()}>")
    if kwargs:
        try:
            s = s.format(**kwargs)
        except KeyError as e:
            print(f"Warning: Formatting key {e} not found in string for '{key}' in language '{current_language}'")
    return s

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
    def __init__(self, root_window):
        self.root = root_window
        # self.root.title("비디오 변환기 (탭 지원)") # Updated by update_ui_language
        self.root.geometry("650x650") # UI 크기 약간 조정 (언어 버튼 및 상태 메시지 공간 고려)

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

        # --- UI 요소 저장용 변수 (언어 변경 시 업데이트 위함) ---
        self.lang_toggle_button = None
        self.sf_labelframe_select_file_widget = None
        self.sf_button_select_file_widget = None
        self.sf_labelframe_original_info_widget = None
        self.sf_label_original_extension_widget = None
        self.sf_labelframe_conversion_settings_widget = None
        self.sf_label_target_format_widget = None
        self.sf_convert_button_widget = None
        self.sf_current_file_label_widget = None
        self.bf_labelframe_input_folder_widget = None
        self.bf_button_select_input_folder_widget = None
        self.bf_labelframe_output_originals_folder_widget = None
        self.bf_button_select_output_folder_originals_widget = None
        self.bf_button_clear_output_folder_originals_widget = None
        self.bf_labelframe_conversion_settings_widget = None
        self.bf_label_target_format_widget = None
        self.bf_convert_button_widget = None
        self.bf_current_file_label_widget = None
        self.bf_overall_progress_label_widget = None
        self.status_label_widget = None
        self.notebook_widget = None
        self.sf_tab_frame = None
        self.bf_tab_frame = None


        self.create_main_layout()
        # self.status.set("모드를 선택하고 파일을 변환하세요.") # Updated by update_ui_language
        self.update_ui_language() # Set initial UI text
        self.root.after(100, self.process_queue) # 큐 폴링 시작

    def create_main_layout(self):
        # --- 언어 변경 버튼을 위한 상단 프레임 ---
        top_bar_frame = ttk.Frame(self.root, padding=(10, 5, 10, 0))
        top_bar_frame.pack(fill=tk.X)
        self.lang_toggle_button = ttk.Button(top_bar_frame, command=self.toggle_language) # Text set by update_ui_language
        self.lang_toggle_button.pack(side=tk.RIGHT, anchor='ne')

        # --- 메인 프레임 ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 탭 컨트롤 (Notebook) ---
        self.notebook_widget = ttk.Notebook(main_frame)
        self.notebook_widget.pack(fill=tk.BOTH, expand=True, pady=5)

        # --- 단일 파일 변환 탭 ---
        self.sf_tab_frame = ttk.Frame(self.notebook_widget, padding="10")
        self.notebook_widget.add(self.sf_tab_frame, text="") # Text set by update_ui_language
        self.create_single_file_tab_widgets(self.sf_tab_frame)

        # --- 폴더 일괄 변환 탭 ---
        self.bf_tab_frame = ttk.Frame(self.notebook_widget, padding="10")
        self.notebook_widget.add(self.bf_tab_frame, text="") # Text set by update_ui_language
        self.create_batch_folder_tab_widgets(self.bf_tab_frame)
        
        # --- 공통 상태 표시줄 ---
        status_frame = ttk.Frame(main_frame, padding="5")
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label_widget = ttk.Label(status_frame, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label_widget.pack(fill=tk.X)

        self.notebook_widget.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # self.on_tab_change() # 초기 상태 설정은 update_ui_language에서 처리

    def update_ui_language(self):
        """Updates all UI text elements to the current language."""
        global current_language
        self.root.title(get_string('window_title'))
        if self.lang_toggle_button:
            self.lang_toggle_button.config(text=get_string('toggle_lang_button_text_to_en') if current_language == 'ko' else get_string('toggle_lang_button_text_to_ko'))

        if self.notebook_widget:
            if self.sf_tab_frame: self.notebook_widget.tab(self.sf_tab_frame, text=get_string('tab_single_file'))
            if self.bf_tab_frame: self.notebook_widget.tab(self.bf_tab_frame, text=get_string('tab_batch_folder'))
        
        # Single File Tab
        if self.sf_labelframe_select_file_widget: self.sf_labelframe_select_file_widget.config(text=get_string('sf_labelframe_select_file'))
        if self.sf_button_select_file_widget: self.sf_button_select_file_widget.config(text=get_string('button_select_file'))
        if self.sf_labelframe_original_info_widget: self.sf_labelframe_original_info_widget.config(text=get_string('sf_labelframe_original_info'))
        if self.sf_label_original_extension_widget: self.sf_label_original_extension_widget.config(text=get_string('sf_label_original_extension'))
        if self.sf_labelframe_conversion_settings_widget: self.sf_labelframe_conversion_settings_widget.config(text=get_string('sf_labelframe_conversion_settings'))
        if self.sf_label_target_format_widget: self.sf_label_target_format_widget.config(text=get_string('label_target_format'))
        if hasattr(self, 'sf_convert_button_widget') and self.sf_convert_button_widget: self.sf_convert_button_widget.config(text=get_string('button_start_conversion'))
        if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
             # Reset progress label text if not actively converting
            if not (self.conversion_running and self.current_conversion_mode == "single"):
                self.sf_current_file_label_widget.config(text=get_string('sf_label_progress_initial'))


        # Batch Folder Tab
        if self.bf_labelframe_input_folder_widget: self.bf_labelframe_input_folder_widget.config(text=get_string('bf_labelframe_input_folder'))
        if self.bf_button_select_input_folder_widget: self.bf_button_select_input_folder_widget.config(text=get_string('button_select_folder'))
        if self.bf_labelframe_output_originals_folder_widget: self.bf_labelframe_output_originals_folder_widget.config(text=get_string('bf_labelframe_output_originals_folder'))
        if self.bf_button_select_output_folder_originals_widget: self.bf_button_select_output_folder_originals_widget.config(text=get_string('button_select_folder'))
        if self.bf_button_clear_output_folder_originals_widget: self.bf_button_clear_output_folder_originals_widget.config(text=get_string('button_clear_selection'))
        if self.bf_labelframe_conversion_settings_widget: self.bf_labelframe_conversion_settings_widget.config(text=get_string('bf_labelframe_conversion_settings'))
        if self.bf_label_target_format_widget: self.bf_label_target_format_widget.config(text=get_string('label_target_format'))
        if hasattr(self, 'bf_convert_button_widget') and self.bf_convert_button_widget: self.bf_convert_button_widget.config(text=get_string('button_start_batch_conversion'))
        if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
            if not (self.conversion_running and self.current_conversion_mode == "batch"):
                self.bf_current_file_label_widget.config(text=get_string('bf_label_current_file_initial'))
        if hasattr(self, 'bf_overall_progress_label_widget') and self.bf_overall_progress_label_widget:
            if not (self.conversion_running and self.current_conversion_mode == "batch"):
                self.bf_overall_progress_label_widget.config(text=get_string('bf_label_overall_progress_initial'))

        # Update status bar based on current tab (if not converting)
        if not self.conversion_running:
            self.on_tab_change() # This will set the appropriate initial status message
        
        # Update filedialog titles (commands need to be re-assigned with new titles)
        if hasattr(self, 'sf_button_select_file_widget') and self.sf_button_select_file_widget:
            self.sf_button_select_file_widget.config(command=self.sf_select_file)
        if hasattr(self, 'bf_button_select_input_folder_widget') and self.bf_button_select_input_folder_widget:
            self.bf_button_select_input_folder_widget.config(command=self.bf_select_input_folder)
        if hasattr(self, 'bf_button_select_output_folder_originals_widget') and self.bf_button_select_output_folder_originals_widget:
            self.bf_button_select_output_folder_originals_widget.config(command=self.bf_select_output_folder_originals)

    def toggle_language(self):
        """Switches the UI language and updates all text elements."""
        global current_language
        current_language = 'en' if current_language == 'ko' else 'ko'
        self.update_ui_language()


    def on_tab_change(self, event=None):
        if not self.notebook_widget: return # Avoid error during init
        selected_tab_index = self.notebook_widget.index(self.notebook_widget.select())
        if not self.conversion_running: # Only change status if not busy
            if selected_tab_index == 0: 
                self.status.set(get_string('status_sf_prompt'))
            elif selected_tab_index == 1: 
                self.status.set(get_string('status_bf_prompt'))
        self.enable_buttons()


    def create_single_file_tab_widgets(self, parent_frame):
        # 파일 선택
        self.sf_labelframe_select_file_widget = ttk.LabelFrame(parent_frame, padding="10") # Text set by update_ui_language
        self.sf_labelframe_select_file_widget.pack(fill=tk.X, pady=5)
        self.sf_button_select_file_widget = ttk.Button(self.sf_labelframe_select_file_widget, command=self.sf_select_file) # Text set by update_ui_language
        self.sf_button_select_file_widget.pack(side=tk.LEFT, padx=5)
        ttk.Entry(self.sf_labelframe_select_file_widget, textvariable=self.sf_input_filepath, state="readonly", width=40).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 원본 정보
        self.sf_labelframe_original_info_widget = ttk.LabelFrame(parent_frame, padding="10") # Text set by update_ui_language
        self.sf_labelframe_original_info_widget.pack(fill=tk.X, pady=5)
        self.sf_label_original_extension_widget = ttk.Label(self.sf_labelframe_original_info_widget) # Text set by update_ui_language
        self.sf_label_original_extension_widget.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.sf_labelframe_original_info_widget, textvariable=self.sf_original_extension).pack(side=tk.LEFT)

        # 변환 설정
        self.sf_labelframe_conversion_settings_widget = ttk.LabelFrame(parent_frame, padding="10") # Text set by update_ui_language
        self.sf_labelframe_conversion_settings_widget.pack(fill=tk.X, pady=5)
        self.sf_label_target_format_widget = ttk.Label(self.sf_labelframe_conversion_settings_widget) # Text set by update_ui_language
        self.sf_label_target_format_widget.pack(side=tk.LEFT, padx=5)
        self.sf_format_combobox = ttk.Combobox(self.sf_labelframe_conversion_settings_widget, textvariable=self.sf_target_format,
                                            values=list(TARGET_FORMATS.keys()), state="readonly")
        self.sf_format_combobox.pack(side=tk.LEFT, padx=5)
        self.sf_format_combobox.bind("<<ComboboxSelected>>", self.enable_buttons)
        
        self.sf_convert_button_widget = ttk.Button(self.sf_labelframe_conversion_settings_widget, command=self.sf_start_conversion_thread, state="disabled") # Text set by update_ui_language
        self.sf_convert_button_widget.pack(side=tk.LEFT, padx=10)

        # 진행률 표시줄
        progress_frame = ttk.Frame(parent_frame, padding=(0, 10, 0, 10))
        progress_frame.pack(fill=tk.X)
        self.sf_progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.sf_progress_bar.pack(fill=tk.X, expand=True)
        self.sf_current_file_label_widget = ttk.Label(progress_frame) # Text set by update_ui_language
        self.sf_current_file_label_widget.pack(fill=tk.X, pady=(2,0))


    def create_batch_folder_tab_widgets(self, parent_frame):
        # 입력 폴더 선택
        self.bf_labelframe_input_folder_widget = ttk.LabelFrame(parent_frame, padding="10") # Text set by update_ui_language
        self.bf_labelframe_input_folder_widget.pack(fill=tk.X, pady=5)
        self.bf_button_select_input_folder_widget = ttk.Button(self.bf_labelframe_input_folder_widget, command=self.bf_select_input_folder) # Text set by update_ui_language
        self.bf_button_select_input_folder_widget.pack(side=tk.LEFT, padx=5)
        ttk.Entry(self.bf_labelframe_input_folder_widget, textvariable=self.bf_input_folder_path, state="readonly", width=50).pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 원본 저장 폴더 선택 (선택 사항)
        self.bf_labelframe_output_originals_folder_widget = ttk.LabelFrame(parent_frame, padding="10") # Text set by update_ui_language
        self.bf_labelframe_output_originals_folder_widget.pack(fill=tk.X, pady=5)
        self.bf_button_select_output_folder_originals_widget = ttk.Button(self.bf_labelframe_output_originals_folder_widget, command=self.bf_select_output_folder_originals) # Text set by update_ui_language
        self.bf_button_select_output_folder_originals_widget.pack(side=tk.LEFT, padx=5)
        ttk.Entry(self.bf_labelframe_output_originals_folder_widget, textvariable=self.bf_output_folder_originals_path, state="readonly", width=50).pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.bf_button_clear_output_folder_originals_widget = ttk.Button(self.bf_labelframe_output_originals_folder_widget, command=self.bf_clear_output_folder_originals) # Text set by update_ui_language
        self.bf_button_clear_output_folder_originals_widget.pack(side=tk.LEFT, padx=5)


        # 변환 설정
        self.bf_labelframe_conversion_settings_widget = ttk.LabelFrame(parent_frame, padding="10") # Text set by update_ui_language
        self.bf_labelframe_conversion_settings_widget.pack(fill=tk.X, pady=5)
        self.bf_label_target_format_widget = ttk.Label(self.bf_labelframe_conversion_settings_widget) # Text set by update_ui_language
        self.bf_label_target_format_widget.pack(side=tk.LEFT, padx=5)
        self.bf_format_combobox = ttk.Combobox(self.bf_labelframe_conversion_settings_widget, textvariable=self.bf_target_format,
                                            values=list(TARGET_FORMATS.keys()), state="readonly")
        self.bf_format_combobox.pack(side=tk.LEFT, padx=5)
        self.bf_format_combobox.bind("<<ComboboxSelected>>", self.enable_buttons)
        
        self.bf_convert_button_widget = ttk.Button(self.bf_labelframe_conversion_settings_widget, command=self.bf_start_batch_conversion_thread, state="disabled") # Text set by update_ui_language
        self.bf_convert_button_widget.pack(side=tk.LEFT, padx=10)

        # 진행률 표시줄
        progress_frame = ttk.Frame(parent_frame, padding=(0, 5, 0, 10))
        progress_frame.pack(fill=tk.X)
        self.bf_current_file_label_widget = ttk.Label(progress_frame) # Text set by update_ui_language
        self.bf_current_file_label_widget.pack(fill=tk.X, pady=(0,2))
        self.bf_progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.bf_progress_bar.pack(fill=tk.X, expand=True)
        
        self.bf_overall_progress_label_widget = ttk.Label(progress_frame) # Text set by update_ui_language
        self.bf_overall_progress_label_widget.pack(fill=tk.X, pady=(2,0))
        self.bf_overall_progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.bf_overall_progress_bar.pack(fill=tk.X, expand=True, pady=(0,5))

    def enable_buttons(self, event=None):
        # 단일 파일 변환 버튼 상태
        if hasattr(self, 'sf_convert_button_widget') and self.sf_convert_button_widget:
            if not self.conversion_running and self.sf_input_filepath.get() and self.sf_target_format.get():
                self.sf_convert_button_widget.config(state="normal")
            else:
                self.sf_convert_button_widget.config(state="disabled")

        # 폴더 일괄 변환 버튼 상태
        if hasattr(self, 'bf_convert_button_widget') and self.bf_convert_button_widget:
            if not self.conversion_running and \
            self.bf_input_folder_path.get() and \
            self.bf_target_format.get():
                self.bf_convert_button_widget.config(state="normal")
            else:
                self.bf_convert_button_widget.config(state="disabled")
            
    # --- 단일 파일 변환 관련 메소드 ---
    def sf_select_file(self):
        if self.conversion_running:
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_conversion_in_progress_warning'))
            return

        filepath = filedialog.askopenfilename(
            title=get_string('dialog_title_select_video_file'),
            filetypes=[(get_string('filetype_video_files'), " ".join(f"*{ext}" for ext in VIDEO_EXTENSIONS)),
                       (get_string('filetype_all_files'), "*.*")]
        )
        if not filepath: return

        _, ext = os.path.splitext(filepath)
        ext_lower = ext.lower()

        if ext_lower in VIDEO_EXTENSIONS:
            self.sf_input_filepath.set(filepath)
            self.sf_original_extension.set(ext)
            self.status.set(get_string('status_sf_file_selected', filename=os.path.basename(filepath)))
            self.sf_progress_bar['value'] = 0
            if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
                self.sf_current_file_label_widget.config(text=get_string('sf_label_progress_initial'))
        else:
            self.sf_input_filepath.set("")
            self.sf_original_extension.set("")
            self.sf_target_format.set("") 
            self.sf_progress_bar['value'] = 0
            if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
                self.sf_current_file_label_widget.config(text=get_string('sf_label_progress_initial'))
            self.status.set(get_string('status_file_not_supported_short'))
            messagebox.showerror(get_string('dialog_title_error'), get_string('dialog_msg_file_not_supported_error', formats=", ".join(VIDEO_EXTENSIONS)))
        self.enable_buttons()

    def sf_start_conversion_thread(self):
        if not self.sf_input_filepath.get() or not self.sf_target_format.get():
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_select_file_and_format_warning'))
            return

        if self.conversion_running:
             messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_already_in_progress_warning'))
             return

        self.conversion_running = True
        self.current_conversion_mode = "single"
        self.enable_buttons() 
        self.sf_format_combobox.config(state="disabled")
        self.sf_progress_bar['value'] = 0
        self.sf_progress_bar.config(mode='determinate')
        if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
            self.sf_current_file_label_widget.config(text=get_string('sf_label_progress_initial'))
        self.status.set(get_string('status_sf_preparing'))

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
                self.progress_queue.put({"type": "status_update_key", "key": 'status_gif_conversion_no_progress', "conversion_type": "single", "filename": filename_for_logger})
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
                    self.progress_queue.put({"type": "status_update_key", "key": 'status_hw_accel_failed_cpu', "conversion_type": "single", "filename": filename_for_logger})
                    video_clip.write_videofile(
                        output_path, codec='libx264', audio_codec='aac', logger=logger,
                        preset='faster', threads=cpu_cores
                    )
            
            self.progress_queue.put({"type": "single_success", "key": 'dialog_msg_sf_conversion_complete', "output_filename": output_filename})

        except Exception as e:
            error_msg_str = str(e)[:150]
            self.progress_queue.put({"type": "single_error", "key": 'dialog_msg_sf_conversion_error', "filename": filename_for_logger, "error_message": error_msg_str})
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
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_conversion_in_progress_warning'))
            return
        folder_path = filedialog.askdirectory(title=get_string('dialog_title_select_input_folder'))
        if folder_path:
            self.bf_input_folder_path.set(folder_path)
            self.status.set(get_string('status_bf_input_folder_selected', folder_path=folder_path))
            self.bf_progress_bar['value'] = 0
            self.bf_overall_progress_bar['value'] = 0
            if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
                self.bf_current_file_label_widget.config(text=get_string('bf_label_current_file_initial'))
            if hasattr(self, 'bf_overall_progress_label_widget') and self.bf_overall_progress_label_widget:
                self.bf_overall_progress_label_widget.config(text=get_string('bf_label_overall_progress_initial'))
            self.enable_buttons()

    def bf_select_output_folder_originals(self):
        if self.conversion_running:
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_conversion_in_progress_warning'))
            return
        folder_path = filedialog.askdirectory(title=get_string('dialog_title_select_output_originals_folder'))
        if folder_path:
            self.bf_output_folder_originals_path.set(folder_path)
            self.status.set(get_string('status_bf_output_originals_selected', folder_path=folder_path))
            self.enable_buttons()
            if self.bf_input_folder_path.get() and folder_path == self.bf_input_folder_path.get():
                messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_input_output_originals_same_warning'))
    
    def bf_clear_output_folder_originals(self):
        if self.conversion_running:
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_conversion_in_progress_warning'))
            return
        self.bf_output_folder_originals_path.set("")
        self.status.set(get_string('status_bf_output_originals_cleared'))
        self.enable_buttons()


    def bf_start_batch_conversion_thread(self):
        input_folder = self.bf_input_folder_path.get()
        output_originals_folder_user_selected = self.bf_output_folder_originals_path.get()
        target_format_name = self.bf_target_format.get()

        if not input_folder or not target_format_name:
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_input_folder_and_format_warning'))
            return

        actual_output_originals_folder = ""
        if not output_originals_folder_user_selected:
            actual_output_originals_folder = os.path.join(input_folder, "Old_video_collection")
            # status set below
        else:
            actual_output_originals_folder = output_originals_folder_user_selected
            if input_folder == actual_output_originals_folder:
                if not messagebox.askyesno(get_string('dialog_title_confirm'), get_string('dialog_msg_input_output_originals_same_warning')):
                    return
        
        target_ext = TARGET_FORMATS.get(target_format_name)
        if not target_ext:
            messagebox.showerror(get_string('dialog_title_error'), get_string('dialog_msg_target_ext_not_found_error'))
            return

        self.bf_files_to_convert_list = []
        for filename in os.listdir(input_folder):
            filepath = os.path.join(input_folder, filename)
            if os.path.isfile(filepath):
                _, ext = os.path.splitext(filename)
                if ext.lower() in VIDEO_EXTENSIONS and ext.lower() != f".{target_ext.lower()}":
                    self.bf_files_to_convert_list.append(filepath)
        
        if not self.bf_files_to_convert_list:
            messagebox.showinfo(get_string('dialog_title_info'), get_string('dialog_msg_no_files_to_convert_info', target_format_name=target_format_name, target_ext=target_ext))
            return

        if self.conversion_running:
             messagebox.showwarning(get_string('dialog_title_warning'), get_string('dialog_msg_already_in_progress_warning'))
             return

        self.conversion_running = True
        self.current_conversion_mode = "batch"
        self.enable_buttons() 
        self.bf_format_combobox.config(state="disabled")
        
        self.bf_progress_bar['value'] = 0
        self.bf_overall_progress_bar['value'] = 0
        if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
            self.bf_current_file_label_widget.config(text=get_string('bf_label_current_file_initial'))
        if hasattr(self, 'bf_overall_progress_label_widget') and self.bf_overall_progress_label_widget:
            self.bf_overall_progress_label_widget.config(text=get_string('bf_label_overall_progress_initial', current=0, total=len(self.bf_files_to_convert_list)))
        
        if not output_originals_folder_user_selected:
             self.status.set(get_string('status_bf_preparing_with_output_folder', foldername=os.path.basename(actual_output_originals_folder)))
        else:
            self.status.set(get_string('status_bf_preparing'))

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
                "type": "status_update_key", 
                "key": 'status_bf_file_conversion_start',
                "conversion_type": "batch", 
                "file_idx": i + 1, "total_files": total_files, "filename": filename
            })
            
            success, original_file_path, _ = self._convert_one_batch_file(input_path, target_format_name, target_ext, i + 1, total_files)
            
            if success and original_file_path:
                self.bf_converted_original_files_paths.append(original_file_path)
            
            self.progress_queue.put({
                "type": "overall_progress", "current": i + 1, "total": total_files
            })

        if self.bf_converted_original_files_paths:
            self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_moving_originals_start', "conversion_type": "batch", "output_folder": os.path.basename(output_originals_folder_final)})
            moved_count, skipped_count = 0, 0
            try:
                os.makedirs(output_originals_folder_final, exist_ok=True) 
                for original_path in self.bf_converted_original_files_paths:
                    if not os.path.exists(original_path):
                        skipped_count +=1; continue
                    original_filename = os.path.basename(original_path)
                    destination_path = os.path.join(output_originals_folder_final, original_filename)
                    if os.path.exists(destination_path):
                        print(f"Skipping move: {original_filename} already exists in {output_originals_folder_final}.")
                        self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_moving_originals_skipped_duplicate', "conversion_type": "batch", "original_filename": original_filename})
                        skipped_count += 1; continue
                    shutil.move(original_path, destination_path)
                    moved_count += 1
                    self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_moving_originals_moved', "conversion_type": "batch", "original_filename": original_filename})
                
                self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_moving_originals_summary', 
                                         "conversion_type": "batch", "total_originals": len(self.bf_converted_original_files_paths),
                                         "moved_count": moved_count, "output_folder": os.path.basename(output_originals_folder_final), 
                                         "skipped_count": skipped_count})
            except Exception as e:
                error_msg_str = str(e)[:150]
                self.progress_queue.put({"type": "status_update_key", "key": 'status_moving_originals_error', "conversion_type": "batch", "output_folder": os.path.basename(output_originals_folder_final), "error_message": error_msg_str})
                self.progress_queue.put({"type": "batch_error", "key": 'dialog_msg_bf_error_partial_complete'}) 
                return

        self.progress_queue.put({"type": "batch_success", "key": 'dialog_msg_bf_all_tasks_complete'})

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
                self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_gif_conversion_no_progress', "conversion_type": "batch", "file_idx": file_index, "total_files": total_files, "filename": filename_for_logger})
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
                    self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_hw_accel_failed_cpu', "conversion_type": "batch", "file_idx": file_index, "total_files": total_files, "filename": filename_for_logger})
                    video_clip.write_videofile(
                        output_path, codec='libx264', audio_codec='aac', logger=logger,
                        preset='faster', threads=cpu_cores
                    )
            
            self.progress_queue.put({"type": "status_update_key", "key": 'status_bf_file_converted', "conversion_type": "batch", "file_idx": file_index, "total_files": total_files, "output_filename": output_filename})
            return True, original_file_to_move, output_path

        except Exception as e:
            error_msg_str = str(e)[:100]
            self.progress_queue.put({"type": "status_update_key", "key": 'dialog_msg_sf_conversion_error', "conversion_type": "batch", "filename": filename_for_logger, "error_message": error_msg_str, "file_idx": file_index, "total_files": total_files}) # Reusing sf error key, but context is batch
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
            msg_key = message_obj.get("key") # For internationalized messages

            # Prepare kwargs for get_string, removing non-string keys
            kwargs_for_get_string = {k: v for k, v in message_obj.items() if k not in ['type', 'conversion_type', 'key', 'percent', 'current', 'total', 'file_index', 'total_files']}


            if msg_type == "progress":
                percent = message_obj.get("percent", 0)
                fname = message_obj.get("filename", "N/A")
                
                if conv_type == "single":
                    self.sf_progress_bar['value'] = percent
                    if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
                        self.sf_current_file_label_widget.config(text=get_string('status_sf_converting_progress', filename=fname, percent=percent))
                    if percent < 100: self.status.set(get_string('status_sf_converting_progress', filename=fname, percent=percent))
                elif conv_type == "batch":
                    file_idx = message_obj.get("file_index")
                    total_f = message_obj.get("total_files")
                    self.bf_progress_bar['value'] = percent
                    if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
                        self.bf_current_file_label_widget.config(text=get_string('status_bf_converting_progress', file_idx=file_idx, total_f=total_f, filename=fname, percent=percent))
                    if percent < 100: self.status.set(get_string('status_bf_converting_progress', file_idx=file_idx, total_f=total_f, filename=fname, percent=percent))


            elif msg_type == "overall_progress": 
                current = message_obj.get("current", 0)
                total = message_obj.get("total", 0)
                self.bf_overall_progress_bar['value'] = (current / total) * 100 if total > 0 else 0
                if hasattr(self, 'bf_overall_progress_label_widget') and self.bf_overall_progress_label_widget:
                    self.bf_overall_progress_label_widget.config(text=get_string('bf_label_overall_progress_initial', current=current, total=total))


            elif msg_type == "status_update_key": # Use this for most status updates
                current_status = get_string(msg_key, **kwargs_for_get_string)
                self.status.set(current_status)
                
                active_conv_type = conv_type if conv_type else self.current_conversion_mode 
                if active_conv_type == "batch":
                    file_idx = message_obj.get("file_idx") # Note: some keys might not use these
                    total_f = message_obj.get("total_files")
                    fname = message_obj.get("filename")

                    # Update current file label specifically for certain batch messages
                    if msg_key in ['status_bf_file_conversion_start', 'status_bf_gif_conversion_no_progress', 'status_bf_hw_accel_failed_cpu', 'status_bf_file_converted']:
                        if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
                             self.bf_current_file_label_widget.config(text=current_status) # Show the full status here
                    elif msg_key in ['status_bf_moving_originals_start', 'status_bf_moving_originals_moved', 'status_bf_moving_originals_skipped_duplicate', 'status_bf_moving_originals_summary', 'status_moving_originals_error']:
                        if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
                            self.bf_current_file_label_widget.config(text=get_string('status_file_moving_in_progress'))


                elif active_conv_type == "single":
                    if msg_key in ['status_gif_conversion_no_progress', 'status_hw_accel_failed_cpu']:
                         if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
                            self.sf_current_file_label_widget.config(text=current_status)


            elif msg_type == "indeterminate_start":
                fname = message_obj.get("filename", "N/A")
                if conv_type == "single":
                    self.sf_progress_bar.config(mode='indeterminate')
                    self.sf_progress_bar.start(10)
                    if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
                        self.sf_current_file_label_widget.config(text=get_string('status_gif_conversion_no_progress', filename=fname))
                elif conv_type == "batch":
                    file_idx = message_obj.get("file_index")
                    total_f = message_obj.get("total_files")
                    self.bf_progress_bar.config(mode='indeterminate')
                    self.bf_progress_bar.start(10)
                    if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
                        self.bf_current_file_label_widget.config(text=get_string('status_bf_gif_conversion_no_progress', file_idx=file_idx, total_files=total_f, filename=fname))
            
            elif msg_type == "single_success":
                success_message = get_string(msg_key, **kwargs_for_get_string)
                self.status.set(success_message)
                if self.sf_progress_bar['mode'] == 'indeterminate': self.sf_progress_bar.stop()
                self.sf_progress_bar.config(mode='determinate')
                self.sf_progress_bar['value'] = 100
                if hasattr(self, 'sf_current_file_label_widget') and self.sf_current_file_label_widget:
                    self.sf_current_file_label_widget.config(text=get_string('status_sf_completed_progress'))
                
                self.conversion_running = False
                self.current_conversion_mode = None
                self.sf_format_combobox.config(state="readonly") 
                self.enable_buttons()
                messagebox.showinfo(get_string('dialog_title_success'), success_message)
            
            elif msg_type == "single_error":
                error_message = get_string(msg_key, **kwargs_for_get_string)
                self.status.set(error_message)
                if self.sf_progress_bar['mode'] == 'indeterminate': self.sf_progress_bar.stop()
                self.sf_progress_bar.config(mode='determinate')
                
                self.conversion_running = False
                self.current_conversion_mode = None
                self.sf_format_combobox.config(state="readonly")
                self.enable_buttons()
                messagebox.showerror(get_string('dialog_title_error'), error_message)

            elif msg_type == "batch_success":
                success_message = get_string(msg_key, **kwargs_for_get_string)
                self.status.set(success_message)
                if self.bf_progress_bar['mode'] == 'indeterminate': self.bf_progress_bar.stop()
                self.bf_progress_bar.config(mode='determinate')
                self.bf_progress_bar['value'] = 100
                
                num_total_files = len(self.bf_files_to_convert_list) if self.bf_files_to_convert_list else 0
                self.bf_overall_progress_bar['value'] = 100
                if hasattr(self, 'bf_overall_progress_label_widget') and self.bf_overall_progress_label_widget:
                    self.bf_overall_progress_label_widget.config(text=get_string('bf_label_overall_progress_initial', current=num_total_files, total=num_total_files))
                if hasattr(self, 'bf_current_file_label_widget') and self.bf_current_file_label_widget:
                    self.bf_current_file_label_widget.config(text=get_string('status_bf_current_file_completed'))

                self.conversion_running = False
                self.current_conversion_mode = None
                self.bf_format_combobox.config(state="readonly")
                self.enable_buttons()
                messagebox.showinfo(get_string('dialog_title_success'), success_message)
            
            elif msg_type == "batch_error":
                error_message = get_string(msg_key, **kwargs_for_get_string)
                self.status.set(error_message)
                if self.bf_progress_bar['mode'] == 'indeterminate': self.bf_progress_bar.stop()
                self.bf_progress_bar.config(mode='determinate')
                
                self.conversion_running = False
                self.current_conversion_mode = None
                self.bf_format_combobox.config(state="readonly")
                self.enable_buttons()
                messagebox.showerror(get_string('dialog_title_error'), error_message)

            self.root.after(100, self.process_queue)

        except queue.Empty:
            self.root.after(100, self.process_queue)
        except Exception as e:
            print(f"Error in process_queue: {e}")
            traceback.print_exc()
            self.root.after(100, self.process_queue)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
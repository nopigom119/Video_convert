# Video_Converter_All_In_One (Video Converter / 비디오 변환 프로그램)

An application that converts video files to various formats, supporting single file and batch folder conversions.

This is a GUI-based application developed in Python using Tkinter and `moviepy`, designed to convert video files between various common formats. It supports both individual file processing and batch conversion of all videos within a selected folder.

## Functionality and Purpose

This program provides a user-friendly interface to manage and execute video conversion tasks:

* **Tabbed Interface:** Separate tabs for "Single File Conversion" and "Batch Folder Conversion" for a clear workflow.
* **Supported Input Formats:** Works with common video formats like .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm.
* **Supported Output Formats:** Convert videos to MP4, AVI, MOV, WebM, or animated GIF.
* **Single File Conversion:**
    * Select an individual video file.
    * Choose the desired output format.
    * The converted file is saved in the same directory as the original with a `_converted` suffix.
* **Batch Folder Conversion:**
    * Select an input folder containing multiple video files.
    * Choose a target format for all convertible videos in the folder.
    * **Original File Management:** After successful conversion, original video files are moved to a user-specified backup folder or, if no folder is chosen, to a subfolder named "Old\_video\_collection" created within the input folder. This helps organize files and prevents accidental re-conversion.
* **Progress Indication:**
    * Displays real-time progress for individual file conversions (percentage and current file name).
    * For batch conversions, shows progress for the current file being processed and overall progress for the entire batch (e.g., "File 3/10").
* **Hardware Acceleration (for H.264 output):** Attempts to use NVENC (NVIDIA hardware acceleration) for faster MP4 encoding. If NVENC is unavailable or fails, it automatically falls back to CPU-based encoding (libx264).
* **User Interface:** Built with Tkinter for a simple and intuitive graphical user interface.
* **Video Processing Engine:** Utilizes the `moviepy` library for robust video manipulation.

This app is useful for changing video formats for compatibility across different devices or software, creating animated GIFs from video clips, or preparing videos for various platforms.

## Prerequisites

Before using this application, ensure you have the following:

1.  **Python (for running the script directly):** If you intend to run the Python script (`.py`), you'll need Python 3.x installed.
    * **Required Python Libraries:** `moviepy` and `tkinter` (Tkinter is usually included with standard Python installations). `proglog` and `shutil` are also used but `moviepy` should handle `proglog` as a dependency, and `shutil` is standard. You can install `moviepy` using pip:
        ```bash
        pip install moviepy
        ```
2.  **(Optional but Recommended for H.264 Hardware Acceleration):** An NVIDIA GPU with up-to-date drivers if you wish to utilize NVENC hardware acceleration for MP4 conversion. The application will still work using CPU-based encoding without it.
3.  **FFmpeg:** MoviePy relies on FFmpeg. While MoviePy attempts to download it automatically if not found, having FFmpeg installed and accessible in your system's PATH is recommended for smooth operation.

## How to Use

There are two ways to use this application:

**A. Using the Executable (`.exe` file - Recommended for most users):**

1.  Download the latest `Video_Converter_All_In_One.exe` file from the **[Releases](https://github.com/nopigom119/Video_convert/releases)** page of this repository.
2.  Run the `Video_Converter_All_In_One.exe` file.
3.  **Interface Overview:**
    * The application has two main tabs: "Single File Conversion" and "Batch Folder Conversion."
    * **Single File Conversion Tab:**
        * Click "파일 선택" (Select File) to choose a video file. The file path and original extension will be displayed.
        * Select the "변환할 포맷" (Target Format) from the dropdown list (MP4, AVI, MOV, WebM, GIF).
        * Click "변환 시작" (Start Conversion).
        * A progress bar and status messages will show the conversion progress.
    * **Batch Folder Conversion Tab:**
        * Click "폴더 선택" (Select Folder) next to "입력 폴더 선택" (Input Folder Selection) to choose a folder containing videos.
        * (Optional) Click "폴더 선택" (Select Folder) next to "변환된 원본 저장 폴더 선택" (Select Output Folder for Originals) to specify where original files should be moved after conversion. You can also "선택 해제" (Clear Selection) to use the default "Old\_video\_collection" subfolder.
        * Select the "변환할 포맷" (Target Format) from the dropdown list.
        * Click "일괄 변환 시작" (Start Batch Conversion).
        * Progress bars will show current file progress and overall batch progress.
    * A status bar at the bottom displays messages about the current operation or errors.
4.  Converted files will be saved in the input directory (for single conversion, with `_converted` suffix; for batch, with the new extension), and original files (in batch mode) will be moved.

**B. Running the Python Script (`.py` file):**

1.  Clone this repository or download the `video_convert_all_in_one.py` script from `https://github.com/nopigom119/Video_convert`.
2.  Ensure Python 3.x is installed (see Prerequisites).
3.  Install the required Python library:
    ```bash
    pip install moviepy
    ```
4.  Open a terminal or command prompt.
5.  Navigate to the directory where you saved the script.
6.  Run the script using the command: `python video_convert_all_in_one.py`
7.  Follow step 3 from the "Using the Executable" section above to operate the GUI.

## License

This program is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

* **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made.
* **Non-Commercial Use:** You may not use this program for commercial purposes.
* **Modification Allowed:** You can modify this program or create derivative works.
* **Same Conditions for Change Permission:** If you modify or create derivative works of this program, you must distribute your contributions under the same license as the original.

You can check the license details on the Creative Commons website: [https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en)

## Contact

For inquiries about this program, please contact [rycbabd@gmail.com].

---

# Video_Converter_All_In_One (비디오 변환 프로그램)

단일 파일 및 폴더 일괄 변환을 지원하여 비디오 파일을 다양한 형식으로 변환하는 애플리케이션입니다.

이 프로그램은 Tkinter와 `moviepy`를 사용하여 Python으로 개발된 GUI 기반 애플리케이션으로, 다양한 일반 비디오 파일 형식을 상호 변환하도록 설계되었습니다. 개별 파일 처리와 선택한 폴더 내 모든 비디오의 일괄 변환을 모두 지원합니다.

## 기능 및 목적

본 프로그램은 비디오 변환 작업을 관리하고 실행하는 사용자 친화적인 인터페이스를 제공합니다:

* **탭 인터페이스:** 명확한 작업 흐름을 위해 "단일 파일 변환"과 "폴더 일괄 변환" 탭을 분리하여 제공합니다.
* **지원 입력 형식:** .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm과 같은 일반적인 비디오 형식을 지원합니다.
* **지원 출력 형식:** 비디오를 MP4, AVI, MOV, WebM 또는 움직이는 GIF로 변환합니다.
* **단일 파일 변환:**
    * 개별 비디오 파일을 선택합니다.
    * 원하는 출력 형식을 선택합니다.
    * 변환된 파일은 원본과 동일한 디렉터리에 `_converted` 접미사가 붙어 저장됩니다.
* **폴더 일괄 변환:**
    * 여러 비디오 파일이 포함된 입력 폴더를 선택합니다.
    * 폴더 내 모든 변환 가능한 비디오에 대한 대상 형식을 선택합니다.
    * **원본 파일 관리:** 성공적으로 변환된 후, 원본 비디오 파일은 사용자가 지정한 백업 폴더 또는 폴더를 선택하지 않은 경우 입력 폴더 내에 생성된 "Old\_video\_collection" 하위 폴더로 이동됩니다. 이는 파일 정리를 돕고 실수로 다시 변환하는 것을 방지합니다.
* **진행률 표시:**
    * 개별 파일 변환에 대한 실시간 진행률(백분율 및 현재 파일 이름)을 표시합니다.
    * 일괄 변환의 경우, 현재 처리 중인 파일의 진행률과 전체 일괄 작업의 진행률(예: "파일 3/10")을 보여줍니다.
* **하드웨어 가속 (H.264 출력 시):** MP4 인코딩 속도 향상을 위해 NVENC(NVIDIA 하드웨어 가속) 사용을 시도합니다. NVENC를 사용할 수 없거나 실패하면 자동으로 CPU 기반 인코딩(libx264)으로 대체됩니다.
* **사용자 인터페이스:** 간단하고 직관적인 그래픽 사용자 인터페이스를 위해 Tkinter로 구축되었습니다.
* **비디오 처리 엔진:** 강력한 비디오 조작을 위해 `moviepy` 라이브러리를 활용합니다.

이 앱은 다양한 장치나 소프트웨어에서 호환성을 위해 비디오 형식을 변경하거나, 비디오 클립에서 움직이는 GIF를 만들거나, 다양한 플랫폼용 비디오를 준비하는 데 유용합니다.

## 사전 준비 사항

이 애플리케이션을 사용하기 전에 다음 사항을 확인하십시오.

1.  **Python (스크립트 직접 실행 시):** Python 스크립트(`.py`)를 직접 실행하려면 Python 3.x 버전이 설치되어 있어야 합니다.
    * **필수 Python 라이브러리:** `moviepy` 및 `tkinter` (Tkinter는 일반적으로 표준 Python 설치에 포함되어 있습니다). `proglog`와 `shutil`도 사용되지만, `moviepy`가 `proglog`를 의존성으로 처리해야 하며 `shutil`은 표준 라이브러리입니다. `moviepy`는 pip를 사용하여 설치할 수 있습니다:
        ```bash
        pip install moviepy
        ```
2.  **(선택 사항이지만 H.264 하드웨어 가속에 권장):** MP4 변환에 NVENC 하드웨어 가속을 활용하려면 최신 드라이버가 설치된 NVIDIA GPU가 필요합니다. 이것이 없어도 애플리케이션은 CPU 기반 인코딩을 사용하여 계속 작동합니다.
3.  **FFmpeg:** MoviePy는 FFmpeg에 의존합니다. MoviePy가 찾지 못하면 자동으로 다운로드를 시도하지만, 원활한 작동을 위해 시스템의 PATH에 FFmpeg가 설치되어 있고 접근 가능하도록 하는 것이 좋습니다.

## 사용 방법

이 애플리케이션을 사용하는 방법에는 두 가지가 있습니다.

**A. 실행 파일 (`.exe` 파일 사용 - 대부분 사용자에게 권장):**

1.  이 저장소의 **[Releases](https://github.com/nopigom119/Video_convert/releases)** 페이지에서 최신 `Video_Converter_All_In_One.exe` 파일을 다운로드합니다.
2.  `Video_Converter_All_In_One.exe` 파일을 실행합니다.
3.  **인터페이스 개요:**
    * 애플리케이션에는 "단일 파일 변환"과 "폴더 일괄 변환"의 두 가지 주요 탭이 있습니다.
    * **단일 파일 변환 탭:**
        * "파일 선택" 버튼을 클릭하여 비디오 파일을 선택합니다. 파일 경로와 원본 확장자가 표시됩니다.
        * 드롭다운 목록에서 "변환할 포맷"(MP4, AVI, MOV, WebM, GIF)을 선택합니다.
        * "변환 시작" 버튼을 클릭합니다.
        * 진행률 표시줄과 상태 메시지가 변환 진행 상황을 보여줍니다.
    * **폴더 일괄 변환 탭:**
        * "입력 폴더 선택" 옆의 "폴더 선택" 버튼을 클릭하여 비디오가 포함된 폴더를 선택합니다.
        * (선택 사항) "변환된 원본 저장 폴더 선택" 옆의 "폴더 선택" 버튼을 클릭하여 변환 후 원본 파일을 이동할 위치를 지정합니다. "선택 해제" 버튼을 사용하여 기본 "Old\_video\_collection" 하위 폴더를 사용할 수도 있습니다.
        * 드롭다운 목록에서 "변환할 포맷"을 선택합니다.
        * "일괄 변환 시작" 버튼을 클릭합니다.
        * 진행률 표시줄이 현재 파일 진행률과 전체 일괄 진행률을 보여줍니다.
    * 하단의 상태 표시줄은 현재 작업이나 오류에 대한 메시지를 표시합니다.
4.  변환된 파일은 입력 디렉터리(단일 변환의 경우 `_converted` 접미사 포함, 일괄 변환의 경우 새 확장자)에 저장되며, 원본 파일(일괄 변환 모드)은 이동됩니다.

**B. Python 스크립트 (`.py` 파일 실행):**

1.  `https://github.com/nopigom119/Video_convert`에서 이 저장소를 복제하거나 `video_convert_all_in_one.py` 스크립트를 다운로드합니다.
2.  Python 3.x가 설치되어 있는지 확인합니다 (사전 준비 사항 참조).
3.  필수 Python 라이브러리를 설치합니다:
    ```bash
    pip install moviepy
    ```
4.  터미널 또는 명령 프롬프트를 엽니다.
5.  스크립트를 저장한 디렉토리로 이동합니다.
6.  명령을 사용하여 스크립트를 실행합니다: `python video_convert_all_in_one.py`
7.  GUI를 작동하려면 위의 "실행 파일 사용" 섹션의 3단계를 따릅니다.

## 라이선스

본 프로그램은 **크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 4.0 국제 라이선스 (CC BY-NC-SA 4.0)** 에 따라 이용할 수 있습니다.

* **출처 표시:** 본 프로그램의 출처 (작성자 또는 개발팀)를 명시해야 합니다.
* **비상업적 이용:** 본 프로그램을 상업적인 목적으로 이용할 수 없습니다.
* **변경 가능:** 본 프로그램을 수정하거나 2차 저작물을 만들 수 있습니다.
* **동일 조건 변경 허락:** 2차 저작물에 대해서도 동일한 조건으로 이용 허락해야 합니다.

자세한 내용은 크리에이티브 커먼즈 홈페이지에서 확인하실 수 있습니다: [https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko)

## 문의

본 프로그램에 대한 문의사항은 [rycbabd@gmail.com] 로 연락주시기 바랍니다.

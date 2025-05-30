# Feature Request (기능 제안)

## Description (설명)

Add functionality to cancel an ongoing video conversion process, for both single file and batch conversions.

단일 파일 및 일괄 비디오 변환 모두에 대해 현재 진행 중인 변환 작업을 취소할 수 있는 기능 추가.

## Proposal (제안 내용)

Introduce a 'Cancel' button (or 'Cancel Current & Stop Batch' / 'Cancel All Batch' for batch mode) on the user interface (UI). When a conversion is in progress, this button would become active. Clicking it should perform the following:

1.  **For Single File Conversion:**
    * Immediately stop the current video encoding process.
    * Attempt to delete any partially created (incomplete) output file to avoid confusion and save disk space.
    * Reset the progress bar, status messages, and enable UI elements for a new conversion.

2.  **For Batch Folder Conversion:**
    * **Option A (Cancel Current & Stop Entire Batch):** Stop the conversion of the *current* file, attempt to delete its partial output file, and then terminate the entire batch process. Update overall progress and status to reflect the cancellation.
    * **(Alternative/Future Option B - Cancel Current & Continue Batch):** Stop the conversion of the *current* file, delete its partial output, mark this specific file as 'Cancelled' or 'Skipped' in the overall progress/log, and automatically proceed to the next file in the batch queue.

The UI should clearly indicate that the cancellation is in progress and then confirm when it's complete, resetting relevant UI components.

사용자 인터페이스(UI)에 '취소' 버튼 (일괄 모드의 경우 '현재 파일 취소 및 일괄 중단' / '전체 일괄 작업 취소')을 도입합니다. 변환이 진행 중일 때 이 버튼이 활성화됩니다. 클릭 시 다음과 같은 작업을 수행해야 합니다:

1.  **단일 파일 변환의 경우:**
    * 현재 비디오 인코딩 프로세스를 즉시 중지합니다.
    * 혼란을 피하고 디스크 공간을 절약하기 위해 부분적으로 생성된 (불완전한) 출력 파일을 삭제하려고 시도합니다.
    * 진행률 표시줄, 상태 메시지를 재설정하고 새 변환을 위해 UI 요소를 활성화합니다.

2.  **폴더 일괄 변환의 경우:**
    * **옵션 A (현재 파일 취소 및 전체 일괄 중단):** *현재* 파일의 변환을 중지하고, 부분 출력 파일을 삭제하려고 시도한 다음, 전체 일괄 처리 프로세스를 종료합니다. 전체 진행률 및 상태를 업데이트하여 취소를 반영합니다.
    * **(대안/향후 옵션 B - 현재 파일 취소 및 일괄 계속):** *현재* 파일의 변환을 중지하고, 부분 출력 파일을 삭제하고, 이 특정 파일을 전체 진행률/로그에서 '취소됨' 또는 '건너뜀'으로 표시한 다음, 일괄 대기열의 다음 파일로 자동으로 진행합니다.

UI는 취소가 진행 중임을 명확히 표시하고 완료 시 확인한 후 관련 UI 구성 요소를 재설정해야 합니다.

## Use Case / Motivation (사용 사례 / 동기)

Currently, if a user starts a long conversion (e.g., a large video file, a high-resolution output, or a large batch of files) and then realizes they've selected the wrong output format, an incorrect input file/folder, or simply needs their system resources for a more urgent task, there's no way to gracefully stop the ongoing conversion without closing the entire application. Closing the application abruptly might leave incomplete, unusable output files and can be a frustrating user experience.

A 'Cancel' feature would allow users to:
* Correct mistakes (e.g., wrong settings or files) without waiting for the entire process to finish.
* Free up system resources if needed urgently.
* Have better control over the application's operations, especially during lengthy batch jobs.

현재 사용자가 대용량 비디오 파일, 고해상도 출력 또는 다수의 파일로 구성된 대규모 일괄 작업과 같이 오래 걸리는 변환을 시작한 후, 잘못된 출력 형식, 잘못된 입력 파일/폴더를 선택했음을 깨닫거나, 단순히 더 긴급한 작업을 위해 시스템 리소스가 필요한 경우, 전체 애플리케이션을 종료하지 않고는 진행 중인 변환을 정상적으로 중지할 방법이 없습니다. 애플리케이션을 갑자기 종료하면 불완전하고 사용할 수 없는 출력 파일이 남을 수 있으며 사용자 경험을 저해할 수 있습니다.

'취소' 기능이 있다면 사용자는 다음을 수행할 수 있습니다:
* 전체 프로세스가 완료될 때까지 기다리지 않고 실수(예: 잘못된 설정 또는 파일)를 수정할 수 있습니다.
* 긴급하게 필요한 경우 시스템 리소스를 확보할 수 있습니다.
* 특히 장시간 소요되는 일괄 작업 중에 애플리케이션의 작동에 대한 더 나은 제어권을 가질 수 있습니다.

## Additional Information (추가 정보) (Optional - 선택 사항)

* **Visual Feedback:** During the cancellation process, a status message like "Cancelling conversion, please wait..." or "취소 중입니다, 잠시만 기다려주세요..." would be beneficial. After cancellation, a confirmation message (e.g., "Conversion cancelled by user.") should be displayed.
    (취소 과정 중 "변환 취소 중입니다, 잠시만 기다려주세요..."와 같은 상태 메시지는 사용자 경험에 도움이 될 것입니다. 취소 후에는 "사용자에 의해 변환이 취소되었습니다."와 같은 확인 메시지가 표시되어야 합니다.)

* **Resource Cleanup:** Ensure that when a conversion is cancelled, any FFmpeg processes spawned by MoviePy for that specific task are properly terminated to prevent orphaned processes.
    (변환이 취소될 때, 해당 특정 작업을 위해 MoviePy에 의해 생성된 모든 FFmpeg 프로세스가 올바르게 종료되어 고아 프로세스가 남지 않도록 해야 합니다.)

* **Examples of other programs where similar features are implemented:** Most file download managers, video editing software rendering queues, and data processing tools provide a way to cancel ongoing tasks.
    (유사한 기능이 구현된 다른 프로그램 예시: 대부분의 파일 다운로드 관리자, 비디오 편집 소프트웨어의 렌더링 대기열, 데이터 처리 도구는 진행 중인 작업을 취소할 수 있는 방법을 제공합니다.)

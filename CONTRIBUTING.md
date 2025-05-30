# Contributing to Video_Converter_All_In_One

Thank you for your interest in contributing to Video_Converter_All_In_One (Video Converter / 비디오 변환 프로그램)! All contributions are welcome.
We appreciate any form of contribution, be it bug fixes, feature additions, documentation improvements, or helping with testing.

## How to Contribute

### 1. Reporting Issues

* Please register new feature suggestions or bug reports on the [Video_Converter_All_In_One Issues page](https://github.com/nopigom119/Video_convert/issues).
* Make sure the issue title is concise and clear.
* Provide detailed descriptions of the problem or suggestion in the issue content. Please include:
    * Steps to reproduce the bug.
    * Expected behavior and actual behavior.
    * Your operating system and version.
    * The version of the Video_Converter_All_In_One application you are using.
    * Input video file format and codec (if known).
    * Output video format selected.
    * Screenshots or error messages (from the application, MoviePy, or FFmpeg if visible) if applicable.

### 2. Contributing Code

1.  Fork the [Video_Converter_All_In_One repository](https://github.com/nopigom119/Video_convert).
2.  Create a new branch in your forked repository for your contribution.
    * Branch names should be descriptive. (e.g., `feature/add-webm-output`, `bugfix/fix-audio-missing-error-23`)
3.  Write your code. Please adhere to the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style guidelines.
4.  Test your changes thoroughly, especially with various input video formats, codecs, resolutions, file sizes, and output format combinations. If adding new functionality that interacts with MoviePy, FFmpeg, or involves complex file processing, ensure proper error handling and resource management (e.g., closing video clips).
5.  Write concise and clear commit messages. (e.g., `feat: Add WebM output support`, `fix: Handle error when input video lacks audio stream (issue #23)`)
6.  Submit a [pull request](https://github.com/nopigom119/Video_convert/pulls) to the `main` branch of the original Video_Converter_All_In_One repository.
    * Clearly describe the changes you have made in your pull request.
    * Link to any relevant issues.

### 3. Contributing to Documentation

* You can contribute to improving documentation, such as the README file, comments within the code, code explanations, usage examples, or tips for troubleshooting.
* Make sure the documentation is clear, concise, and easy to understand.

## Code Writing Rules

* Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style guidelines.
* Write clear and descriptive docstrings for all public modules, classes, functions, and methods.
* Add comments to your code where necessary to explain complex logic.
* Pay special attention to how `moviepy.editor.VideoFileClip` objects (and similar resources from MoviePy or other libraries) are handled. Ensure they are properly closed (e.g., using `clip.close()` within a `finally` block or using context managers if applicable) to prevent resource leaks, especially in batch processing loops or error scenarios. User-provided file paths and data from video files should be handled carefully to prevent issues like crashes with malformed inputs.

## Commit Message Rules

* Write concise and clear commit messages.
* A good commit message should briefly describe the change.
* Consider using [Conventional Commits](https://www.conventionalcommits.org/) for a structured approach (e.g., `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).

## Pull Request Procedure

1.  Ensure your code adheres to the project's coding standards and all tests pass (if applicable).
2.  Create a pull request from your feature branch to the `main` branch of the `nopigom119/Video_convert` repository.
3.  Provide a clear description of the changes in the pull request.
4.  Be prepared to discuss your changes and make further modifications if requested by the maintainers.

## Inquiries

* For inquiries or discussions about contributing to Video_Converter_All_In_One, please use the [Video_Converter_All_In_One Issues page](https://github.com/nopigom119/Video_convert/issues).

## License

By contributing to Video_Converter_All_In_One, you agree that your contributions will be licensed under its CC BY-NC-SA 4.0 License.

---

# Video_Converter_All_In_One에 기여하기

Video_Converter_All_In_One (Video Converter / 비디오 변환 프로그램)에 관심을 가져주셔서 감사합니다! 모든 기여를 환영합니다.
버그 수정, 기능 추가, 문서 개선, 테스트 지원 등 어떤 형태의 기여든 감사하게 생각합니다.

## 기여 방법

### 1. 이슈 등록

* 새로운 기능 제안이나 버그 보고는 [Video_Converter_All_In_One 이슈 페이지](https://github.com/nopigom119/Video_convert/issues)에 등록해주세요.
* 이슈 제목은 간결하고 명확하게 작성해주세요.
* 이슈 내용에는 문제 상황이나 제안 내용을 상세하게 설명해주세요. 다음 정보를 포함해주세요:
    * 버그 재현 단계.
    * 예상되는 동작과 실제 동작.
    * 사용 중인 운영체제 및 버전.
    * 사용 중인 Video_Converter_All_In_One 애플리케이션 버전.
    * 입력 비디오 파일 형식 및 코덱 (알고 있는 경우).
    * 선택한 출력 비디오 형식.
    * 해당되는 경우 스크린샷 또는 오류 메시지 (애플리케이션, MoviePy, 또는 FFmpeg으로부터 보이는 경우).

### 2. 코드 기여

1.  [Video_Converter_All_In_One 저장소](https://github.com/nopigom119/Video_convert)를 포크해주세요.
2.  포크한 저장소에서 기여를 위한 새로운 브랜치를 만들어주세요.
    * 브랜치 이름은 설명적으로 작성해주세요. (예: `feature/WebM-출력-추가`, `bugfix/오디오-누락-오류-23-수정`)
3.  코드를 작성해주세요. [PEP 8](https://www.python.org/dev/peps/pep-0008/) 코딩 스타일 가이드라인을 준수해주세요.
4.  특히 다양한 입력 비디오 형식, 코덱, 해상도, 파일 크기 및 출력 형식 조합으로 변경 사항을 철저히 테스트해주세요. MoviePy, FFmpeg와 상호작용하거나 복잡한 파일 처리를 포함하는 새로운 기능을 추가하는 경우, 적절한 오류 처리 및 리소스 관리(예: 비디오 클립 닫기)를 확인해주세요.
5.  간결하고 명확한 커밋 메시지를 작성해주세요. (예: `feat: WebM 출력 지원 추가`, `fix: 입력 비디오에 오디오 스트림 없을 시 오류 처리 (이슈 #23)`)
6.  원본 Video_Converter_All_In_One 저장소의 `main` 브랜치로 [풀 리퀘스트](https://github.com/nopigom119/Video_convert/pulls)를 보내주세요.
    * 풀 리퀘스트에 변경한 내용을 명확하게 설명해주세요.
    * 관련된 이슈가 있다면 링크해주세요.

### 3. 문서 기여

* README 파일, 코드 내 주석, 코드 설명, 사용 예시, 문제 해결 팁 등 문서 개선에 기여해주실 수 있습니다.
* 문서 내용은 명확하고 간결하며 이해하기 쉽게 작성해주세요.

## 코드 작성 규칙

* [PEP 8](https://www.python.org/dev/peps/pep-0008/) 코딩 스타일 가이드라인을 준수해주세요.
* 모든 공개 모듈, 클래스, 함수, 메소드에 대해 명확하고 설명적인 독스트링(docstring)을 작성해주세요.
* 복잡한 로직을 설명하기 위해 필요한 경우 코드에 주석을 추가해주세요.
* `moviepy.editor.VideoFileClip` 객체 (및 MoviePy 또는 다른 라이브러리의 유사한 리소스)를 처리하는 방식에 특히 주의해주세요. 특히 일괄 처리 루프나 오류 시나리오에서 리소스 누수를 방지하기 위해 해당 객체들이 (`finally` 블록 내에서 `clip.close()`를 사용하거나 해당하는 경우 컨텍스트 관리자를 사용하는 등) 올바르게 닫히는지 확인해주세요. 사용자가 제공한 파일 경로나 비디오 파일의 데이터는 손상된 입력으로 인한 충돌과 같은 문제를 방지하기 위해 신중하게 처리해야 합니다.

## 커밋 메시지 규칙

* 간결하고 명확한 커밋 메시지를 작성해주세요.
* 좋은 커밋 메시지는 변경 사항을 간략하게 설명해야 합니다.
* 구조화된 접근 방식을 위해 [Conventional Commits](https://www.conventionalcommits.org/ko/v1.0.0/) 사용을 고려해보세요 (예: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).

## 풀 리퀘스트 절차

1.  코드가 프로젝트의 코딩 표준을 준수하고 모든 테스트를 통과하는지 확인해주세요 (해당되는 경우).
2.  기능 브랜치에서 `nopigom119/Video_convert` 저장소의 `main` 브랜치로 풀 리퀘스트를 생성해주세요.
3.  풀 리퀘스트에 변경 사항에 대한 명확한 설명을 제공해주세요.
4.  관리자의 요청이 있을 경우 변경 사항에 대해 논의하고 추가 수정을 할 준비가 되어 있어야 합니다.

## 문의

* Video_Converter_All_In_One 기여에 대한 문의나 논의는 [Video_Converter_All_In_One 이슈 페이지](https://github.com/nopigom119/Video_convert/issues)를 이용해주세요.

## 라이선스

Video_Converter_All_In_One에 기여함으로써 귀하의 기여물은 해당 프로젝트의 CC BY-NC-SA 4.0 라이선스에 따라 사용이 허가됨에 동의하는 것으로 간주됩니다.

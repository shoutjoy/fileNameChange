# FileRenamer
제작자: 박중희 
 연세대 심리학과 겸임교수 

Windows용 파일 일괄 이름 변경 도구입니다. 선택한 폴더 안의 파일에 접두사/접미사를 붙이거나, 지정한 기본 이름과 3자리 번호 형식으로 파일명을 한 번에 변경할 수 있습니다.
많은양의 파일들의 파일명을 일괄적으로 변경이 가능합니다. 


## 주요 기능

- 폴더 선택 후 해당 폴더의 파일명 일괄 변경
- 기존 파일명 앞뒤에 접두사, 접미사 추가
- `기본이름_001`, `기본이름_002` 형식으로 번호를 붙여 일괄 변경
- Windows 폴더 우클릭 메뉴에서 바로 실행 가능
- 프로그램 안에서 우클릭 메뉴 등록 및 제거 가능
- GitHub Actions로 Windows 실행 파일 자동 빌드 가능

## 파일 구성

- `code_artifact.py`: 프로그램 원본 Python 코드
- `dist/FileRenamer.exe`: 빌드된 실행 파일
- `FileRenamer.spec`: PyInstaller 빌드 설정 파일
- `install_context_menu.ps1`: Windows 우클릭 메뉴 등록 스크립트
- `code_artifact.bat`: 우클릭 메뉴 등록 스크립트를 실행하는 배치 파일
- `.github/workflows/build.yml`: GitHub Actions 빌드 워크플로

## 사용 방법

### 1. 실행 파일로 실행

[FileRenamer.exe](dist/FileRenamer.exe?raw=1)를 다운로드하거나 `dist` 폴더 안의 `FileRenamer.exe`를 실행합니다.

프로그램이 열리면 다음 순서로 사용합니다.

1. `폴더 찾아보기` 버튼을 눌러 파일명을 변경할 폴더를 선택합니다.
2. 원하는 변경 방식을 선택합니다.
3. 실행 결과는 하단 로그 영역에서 확인합니다.

### 2. 접두사/접미사 추가

선택한 폴더의 모든 파일 이름에 접두사 또는 접미사를 추가합니다.

예시:

- 원본 파일: `image.jpg`
- 접두사: `new_`
- 접미사: `_backup`
- 변경 결과: `new_image_backup.jpg`

확장자는 유지됩니다.

### 3. 일괄 이름 변경 및 번호 매기기

선택한 폴더의 파일을 정렬한 뒤, 입력한 기본 파일명과 번호로 변경합니다.

예시:

- 기본 파일명: `photo`
- 변경 결과:
  - `photo_001.jpg`
  - `photo_002.jpg`
  - `photo_003.png`

기존 확장자는 유지됩니다.

## 우클릭 메뉴 등록

Windows 탐색기에서 폴더를 우클릭했을 때 이 프로그램을 바로 실행하려면 프로그램 안의 `우클릭 메뉴에 등록` 버튼을 누릅니다.

등록 후 폴더 또는 폴더 빈 공간을 우클릭하면 다음 메뉴가 추가됩니다.

```text
일괄 파일명 변경 프로그램 열기
```

이 메뉴로 실행하면 선택한 폴더 경로가 프로그램에 자동으로 입력됩니다.

우클릭 메뉴를 삭제하려면 프로그램 안의 `우클릭 메뉴에서 제거` 버튼을 누릅니다.

기존 방식대로 `code_artifact.bat` 파일을 실행해도 우클릭 메뉴를 등록할 수 있습니다.

## Python으로 직접 실행

Python이 설치되어 있다면 원본 스크립트를 직접 실행할 수 있습니다.

```powershell
python code_artifact.py
```

특정 폴더를 처음부터 선택된 상태로 열 수도 있습니다.

```powershell
python code_artifact.py "C:\path\to\folder"
```

## 실행 파일 빌드

PyInstaller가 설치되어 있다면 다음 명령으로 실행 파일을 다시 만들 수 있습니다.

```powershell
pyinstaller FileRenamer.spec
```

빌드가 완료되면 `dist/FileRenamer.exe`가 생성됩니다.

## GitHub Actions 빌드

이 저장소에는 Windows 실행 파일을 자동으로 빌드하는 GitHub Actions 워크플로가 포함되어 있습니다.

실행 조건:

- `main` 또는 `master` 브랜치에 push
- pull request 생성 또는 업데이트
- GitHub Actions 화면에서 수동 실행

수동 실행 방법:

1. GitHub 저장소의 `Actions` 탭으로 이동합니다.
2. `Build FileRenamer` 워크플로를 선택합니다.
3. `Run workflow` 버튼을 눌러 실행합니다.
4. 빌드가 끝나면 실행 결과 페이지의 `Artifacts` 영역에서 `FileRenamer-windows`를 다운로드합니다.

업로드되는 파일:

```text
dist/FileRenamer.exe
```

## 주의사항

- 파일명 변경은 실제 파일에 바로 적용됩니다.
- 중요한 파일은 실행 전에 백업하는 것을 권장합니다.
- 같은 이름의 파일이 이미 있으면 해당 파일 변경은 실패하고 로그에 표시됩니다.
- 하위 폴더 안의 파일은 변경하지 않고, 선택한 폴더 바로 아래의 파일만 처리합니다.

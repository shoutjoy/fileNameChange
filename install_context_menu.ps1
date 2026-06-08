$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$appExe = Join-Path $scriptDir "dist\FileRenamer.exe"

if (-not (Test-Path -LiteralPath $appExe -PathType Leaf)) {
    Write-Host "[ERROR] Executable not found: $appExe"
    Write-Host "Build the executable first."
    exit 1
}

$menuText = "일괄 파일명 변경 프로그램 열기"
$backgroundShell = "HKCU:\Software\Classes\Directory\Background\shell\FileRenamer"
$backgroundCommand = Join-Path $backgroundShell "command"
$folderShell = "HKCU:\Software\Classes\Directory\shell\FileRenamer"
$folderCommand = Join-Path $folderShell "command"

New-Item -Path $backgroundShell -Force | Out-Null
New-Item -Path $backgroundCommand -Force | Out-Null
New-Item -Path $folderShell -Force | Out-Null
New-Item -Path $folderCommand -Force | Out-Null

Set-ItemProperty -Path $backgroundShell -Name "(default)" -Value $menuText
Set-ItemProperty -Path $backgroundCommand -Name "(default)" -Value "`"$appExe`" `"%V`""
Set-ItemProperty -Path $folderShell -Name "(default)" -Value $menuText
Set-ItemProperty -Path $folderCommand -Name "(default)" -Value "`"$appExe`" `"%1`""

Write-Host "[OK] Context menu registration completed."
Write-Host "The selected folder path will be passed to the program automatically."

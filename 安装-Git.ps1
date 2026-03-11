# 使用 winget 安装 Git for Windows
# 请右键「使用 PowerShell 运行」，或在 PowerShell 中执行: .\安装-Git.ps1

Write-Host "正在使用 winget 安装 Git for Windows，请稍候..." -ForegroundColor Cyan
Write-Host ""

$result = winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements 2>&1
$result | ForEach-Object { Write-Host $_ }

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Git 安装完成。请关闭本窗口，并重新打开终端后再使用 git / uvx。" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "若安装失败，可手动下载安装: https://git-scm.com/download/win" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按回车键关闭"

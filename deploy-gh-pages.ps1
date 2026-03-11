param(
  [string]$RepoUrl = "https://github.com/your-name/your-repo.git",
  [string]$BranchName = "001-wechat-audio-qrcode",
  [string]$AuthorName = "MissMidou",
  [string]$AuthorEmail = "missmidou@example.com"
)

$ErrorActionPreference = "Stop"

Write-Host "== Step 1: Change to project directory =="
Set-Location "E:\Cursor\test"

Write-Host "== Step 2: Build dist =="
python .\build\build.py

Write-Host "== Step 3: Configure origin if missing =="
$hasOrigin = $false
try {
  $remote = git remote get-url origin 2>$null
  if ($LASTEXITCODE -eq 0 -and $remote) {
    $hasOrigin = $true
  }
} catch {
}

if (-not $hasOrigin) {
  git remote add origin $RepoUrl
  Write-Host "Added origin: $RepoUrl"
} else {
  Write-Host "Origin already exists: $remote"
}

Write-Host "== Step 4: Commit and push branch =="
git checkout -B $BranchName
git add .
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
  $env:GIT_AUTHOR_NAME = $AuthorName
  $env:GIT_AUTHOR_EMAIL = $AuthorEmail
  $env:GIT_COMMITTER_NAME = $AuthorName
  $env:GIT_COMMITTER_EMAIL = $AuthorEmail
  git commit -m "implement wechat audio directory page"
} else {
  Write-Host "No staged changes to commit. Skip commit."
}
git push -u origin $BranchName

Write-Host "== Step 5: Publish dist to gh-pages =="
git subtree push --prefix dist origin gh-pages

Write-Host ""
Write-Host "Done."
Write-Host "Go to GitHub repository Settings -> Pages:"
Write-Host "- Source: Deploy from a branch"
Write-Host "- Branch: gh-pages / (root)"

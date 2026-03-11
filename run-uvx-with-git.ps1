# 运行 uvx 时确保能找到 Git（解决 "Git executable not found"）
# 用法: .\run-uvx-with-git.ps1 --from git+https://github.com/github/spec-kit.git specify init --here

$gitPaths = @(
    "C:\Program Files\Git\bin",
    "C:\Program Files\Git\cmd"
)
foreach ($p in $gitPaths) {
    if (Test-Path $p) {
        $env:Path = "$p;$env:Path"
        break
    }
}

& uvx @args

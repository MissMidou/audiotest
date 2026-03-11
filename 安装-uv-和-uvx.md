# 安装 uv 和 uvx（Windows）

`uvx` 来自 **[uv](https://github.com/astral-sh/uv)**（Astral 的 Python 包/项目管理工具）。安装 uv 后即可使用 `uvx`。

---

## 方法一：PowerShell 一键安装（推荐，需网络正常）

在 **PowerShell** 中执行：

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后：
- 关闭并重新打开 PowerShell（或重启终端），再执行 `uv --version` 和 `uvx --version` 验证。
- 若仍提示找不到命令，请按下面的「配置 PATH」把安装目录加入 PATH。

---

## 方法二：winget

在 **PowerShell** 或 **命令提示符** 中执行：

```powershell
winget install --id=astral-sh.uv -e
```

安装后同样需要**新开一个终端**再使用 `uv` / `uvx`。

---

## 方法三：手动下载（适合网络不稳定或无法访问 GitHub 时）

1. **下载 uv**  
   打开：  
   https://github.com/astral-sh/uv/releases  
   找到最新版本，下载 **uv-x86_64-pc-windows-msvc.zip**（64 位 Windows）。

2. **解压**  
   将 zip 解压到任意目录，例如：  
   `C:\Users\你的用户名\.local\bin`  
   或：  
   `D:\Tools\uv`  
   确保解压后该目录下有 `uv.exe` 和 `uvx.exe`。

3. **配置 PATH**  
   - 按 `Win + R`，输入 `sysdm.cpl` 回车。  
   - 打开「高级」→「环境变量」。  
   - 在「用户变量」里选中 `Path` →「编辑」→「新建」，添加你解压的目录（例如 `C:\Users\你的用户名\.local\bin` 或 `D:\Tools\uv`）。  
   - 确定保存后，**关闭所有 PowerShell/CMD 窗口**，再新开一个终端。

4. **验证**  
   新开终端中执行：
   ```powershell
   uv --version
   uvx --version
   ```

---

## 若当前网络超时

- 在**手机热点**或**其他网络**下重试「方法一」或「方法二」。  
- 或使用**方法三**：在能打开 GitHub 的电脑/浏览器上下载 zip，拷贝到本机再解压并配置 PATH。

完成上述任一步骤后，`uvx` 即可在终端中正常使用。

---

## 安装 Git（解决 “Git executable not found”）

用 `uvx` 安装来自 **git 仓库** 的包（例如 `specify-cli`）时，需要本机已安装 **Git**。

**在 PowerShell 中执行（等待安装完成）：**

```powershell
winget install --id Git.Git -e --accept-package-agreements --accept-source-agreements
```

安装完成后：**关闭当前终端，新开一个终端**，再执行你的 `uvx` 命令。

若 winget 失败，可到 https://git-scm.com/download/win 下载 **Git for Windows** 安装包，安装时勾选 “Add Git to PATH”。

**若已安装 Git 但 uvx 仍报 “Git executable not found”**（例如终端在安装 Git 之前就打开了）：  
可在项目目录下用脚本临时把 Git 加入 PATH 再执行 uvx：

```powershell
.\run-uvx-with-git.ps1 --from git+https://github.com/github/spec-kit.git specify init --here
```

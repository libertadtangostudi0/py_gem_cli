
# Custom GeminiCli — based on Gemini, python

A lightweight console client for Google Gemini API, optimized for local codebase analysis. 
It allows you to instantly feed your entire project context into the model for debugging, refactoring, or architectural review.

## 🚀 Quick Start

### 1. Install uv
This project requires [uv](https://github.com/astral-sh/uv) to manage Python and dependencies.
Refer to the official installation guide:
👉 **[uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)**

### 2. Setup Project
Clone the repository and synchronize the environment. `uv` will automatically provision Python 3.13.5 and all required packages:

```powershell
uv sync
```

### 3. Configure Environment
```
GEMINI_API_KEY=your_secret_api_key_here
```

### 4. Run
```powershell
uv run gcli
```

### ⌨️ In-Chat Commands
```powershell
/scan
```
— Collects the content of all text files in the current directory (respecting filters), builds a project context, and sends it to Gemini.
```powershell
exit
```
— Terminates the session.

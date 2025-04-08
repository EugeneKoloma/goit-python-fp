
# CLI Bot: Phone Book & Notes

This is a Python-based CLI bot for managing a phone book and notes.

## 🛠️ Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python** (version 3.8 or higher)
- **Git** (for cloning the repository)
- **Virtualenv** (`uv`), for managing Python environments
- **Pre-commit**, for managing code quality hooks

---

## 🚀 Installation and Setup

### 1. **Clone the Repository**

1. Go to the [repository page](https://github.com/EugeneKoloma/goit-python-fp).
2. Click on **Code** and copy the link for cloning.
3. Go to your working folder and clone the repository:

```bash
git clone https://github.com/EugeneKoloma/goit-python-fp.git
cd goit-python-fp
```

### 2. **Install `uv`**

If `uv` is not already installed, follow these steps based on your operating system:

#### For macOS and Linux:

1. Open a terminal and run the following command to install `uv`:

   ```bash
   sudo curl -Ls https://astral.sh/uv/install.sh | bash
   ```

2. This will:
   - Download the `uv` binary.
   - Place it in `~/.cargo/bin` (or `~/.local/bin`).
   - Set up shell integration (for bash, zsh, or fish).
   
3. If you use `fish`, ensure the directory exists:

   ```bash
   sudo mkdir -p ~/.config/fish/conf.d
   ```

4. Add `uv` to your `PATH`:

   ```bash
   sudo echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
   ```

5. Verify the installation by checking the version:

   ```bash
   uv --version
   ```

#### For Windows:

1. Open **PowerShell** and run the following command to install `uv`:

   ```bash
   irm https://astral.sh/uv/install.ps1 | iex
   ```

2. This will:
   - Download and install the `uv.exe` binary, usually into `%USERPROFILE%\.cargoin`.

3. If `uv` is not found after installation, manually add it to your `PATH`:
   - Open **System Environment Variables**.
   - Click **Edit** under the **Environment Variables** section.
   - Under **User variables**, select **Path** and click **Edit**.
   - Add:
     ```
     %USERPROFILE%\.cargoin
     ```

4. Verify the installation by checking the version:

   ```bash
   uv --version
   ```

---

### 3. **Initialize the Project**

Once `uv` is installed, follow these steps:

1. Inside your working folder (where you cloned the repository), run the following command to create a virtual environment:

   ```bash
   uv venv
   ```

2. Activate the virtual environment:
   - For **macOS/Linux**:

     ```bash
     source .venv/bin/activate
     ```

   - For **Windows**:
     - In **PowerShell**:

       ```bash
       . .venv\Scripts\Activate.ps1
       ```

     - In **CMD**:

       ```bash
       .venv\Scriptsctivate.bat
       ```

3. Install the project dependencies:

   ```bash
   uv sync
   ```

   ```bash
   uv add <pkg_name>
   ```

---

## 🧰 Setting up Pre-commit Hooks

Pre-commit hooks help ensure your code follows consistent formatting and linting standards before committing.

### 1. **Install Pre-commit**

Install the pre-commit package (if it’s not already installed):

```bash
pip install pre-commit
```

### 2. **Install the Pre-commit Hooks**

Once the environment is activated, install the hooks defined in the `.pre-commit-config.yaml` file:

```bash
pre-commit install
```

This sets up the hooks to automatically run on `git commit`.

### 3. **Manually Run Pre-commit Hooks (Optional)**

You can manually run pre-commit hooks on all files by running:

```bash
pre-commit run --all-files
```

This will apply the hooks to all files in the repository (useful for the initial setup or to check all files).

---

## 🧑‍💻 Usage

To run the bot, use the following command:

```bash
python src/main.py
```

This will start the bot and you can interact with it through the command line.

---

## ⚙️ How Pre-commit Hooks Work

- **Black**: Automatically formats your code to follow PEP 8 style guide.
- **Ruff**: A fast linter and formatter for Python code.
- **End of File Fixer**: Ensures every file ends with a newline.
- **Check Added Large Files**: Prevents adding large files to the repository.

These hooks will run automatically when you try to commit changes to your Git repository. They help ensure that your code remains clean, formatted, and free from common mistakes.

---

## 🛠️ Development Commands

- **Run Black Formatter**: Manually run `black` to format files.
  ```bash
  black src/main.py
  ```

- **Run Ruff Linter**: Manually run `ruff` to lint files.
  ```bash
  ruff check .
  ```

---

## 📝 File Structure

Here’s an overview of the project's file structure:

```
goit-python-fp/
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── src/
│   ├── main.py
│   ├── contacts/
│   ├── decorators/
│   ├── exceptions/
│   ├── notes/
│   └── output/
```

---

## 🛑 Troubleshooting

### 1. **Pre-commit Not Triggering?**

Make sure your files are **staged** before committing. The pre-commit hooks only run on files that are staged:

```bash
git add .
git commit -m "Your commit message"
```

### 2. **Manual Pre-commit Run**

If hooks don’t trigger automatically, run them manually with:

```bash
pre-commit run --all-files
```

---

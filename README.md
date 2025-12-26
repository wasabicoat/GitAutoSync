# GitAutoSync

GitAutoSync is a macOS desktop application that helps you manage multiple Git repositories simultaneously. It provides a simple interface to scan a directory for repositories and automatically commit and push changes with a single click, or on a scheduled interval.

## Features

-   **Recursive Scanning**: Automatically finds all Git repositories within a selected root folder.
-   **One-Click Sync**: Commit and push changes for all found repositories at once.
-   **Automated Scheduling**: Set a timer (e.g., every 10 minutes) to automatically sync your work.
-   **Status Logging**: View real-time logs of commit and push operations.
-   **Modern UI**: Built with CustomTkinter for a native macOS feel (Dark Mode supported).

## Installation

### Database / Pre-built App
You can download the latest release from the [Releases](https://github.com/wasabicoat/GitAutoSync/releases) page (if available) or build it yourself.

### Building from Source

1.  Clone the repository:
    ```bash
    git clone https://github.com/wasabicoat/GitAutoSync.git
    cd GitAutoSync
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application:
    ```bash
    python main.py
    ```

5.  (Optional) Build the macOS .app bundle:
    ```bash
    chmod +x build_app.sh
    ./build_app.sh
    ```
    The app will be located in `dist/GitAutoSync.app`.

## Usage

1.  **Select Root Folder**: Click the top button to choose the directory where your projects are located.
2.  **Commit Message**: Enter a custom message or use the default.
3.  **Sync**: Click **"Auto Commit & Push NOW"** to run immediately.
4.  **Schedule**: Enter an interval in minutes and click **"Start Scheduler"** to automate the process.

## License

This project is open source.

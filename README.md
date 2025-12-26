# GitAutoSync

GitAutoSync is a macOS desktop application that helps you manage multiple Git repositories simultaneously. It provides a simple interface to scan a directory for repositories and automatically commit and push changes with a single click, or on a scheduled interval.

## Features

-   **Multi-Path Monitoring**: Monitor multiple separate folders for Git repositories simultaneously.
-   **One-Click Sync**: Commit and push changes for all found repositories across all paths at once.
-   **Automated Scheduling**: Set a timer (e.g., every 10 minutes) to automatically sync your work.
-   **Countdown Timer**: Visual countdown to the next scheduled sync.
-   **Quick Access**: Open repositories in your browser ("Web") or local Finder ("Folder") directly from the app.
-   **Status Logging**: View real-time logs of commit and push operations.
-   **Modern UI**: Built with CustomTkinter for a native macOS feel (Dark Mode supported).

## Installation

### Database / Pre-built App
A standalone macOS application is available in the `dist` folder after building.

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

1.  **Add Folders**: Click **"Add Folder"** to select directories containing your Git projects. You can add as many as you like.
2.  **Repo Links**: Use the **"Web"** button to open the remote repository (e.g., GitHub) or **"Folder"** to open the local directory.
3.  **Commit Message**: Enter a custom message or use the default.
4.  **Sync**: Click **"Auto Commit & Push NOW"** to force a sync immediately.
5.  **Schedule**: Enter an interval in minutes and click **"Start Scheduler"**. The countdown timer will show when the next sync will occur.
6.  **Reset**: Click **"Reset"** to clear all monitored paths and start over.

## License

This project is open source.

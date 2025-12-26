import customtkinter as ctk
from tkinter import filedialog
import threading
import datetime
from git_manager import GitManager
from scheduler_manager import SchedulerManager

class GitAutoSyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GitAutoSync")
        self.geometry("900x700")

        # Managers
        self.git_manager = GitManager()
        self.scheduler_manager = SchedulerManager(job_func=self.scheduled_job_worker)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Repo List
        self.grid_rowconfigure(2, weight=0) # Controls
        self.grid_rowconfigure(3, weight=0) # Logs

        self.create_header()
        self.create_repo_list_area()
        self.create_controls_area()
        self.create_log_area()

        self.repos = []

    def create_header(self):
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="GitAutoSync", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side="left", padx=10, pady=10)

        self.scan_btn = ctk.CTkButton(self.header_frame, text="Select Root Folder & Scan", command=self.scan_folder)
        self.scan_btn.pack(side="right", padx=10, pady=10)

    def create_repo_list_area(self):
        self.repo_list_frame = ctk.CTkScrollableFrame(self, label_text="Repositories Found")
        self.repo_list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    def create_controls_area(self):
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Commit Message
        self.msg_label = ctk.CTkLabel(self.controls_frame, text="Commit Message:")
        self.msg_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.msg_entry = ctk.CTkEntry(self.controls_frame, width=300)
        self.msg_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.msg_entry.insert(0, "commit by GitAutoSync")

        # Auto Commit Button
        self.commit_btn = ctk.CTkButton(self.controls_frame, text="Auto Commit & Push NOW", command=self.manual_commit_all, fg_color="green")
        self.commit_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Schedule Config
        self.schedule_label = ctk.CTkLabel(self.controls_frame, text="Schedule (mins):")
        self.schedule_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        self.interval_entry = ctk.CTkEntry(self.controls_frame, width=60)
        self.interval_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="w")
        self.interval_entry.insert(0, "10")

        self.toggle_schedule_btn = ctk.CTkButton(self.controls_frame, text="Start Scheduler", command=self.toggle_scheduler)
        self.toggle_schedule_btn.grid(row=1, column=2, padx=10, pady=(0, 10), sticky="e")

    def create_log_area(self):
        self.log_textbox = ctk.CTkTextbox(self, height=150)
        self.log_textbox.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.log_textbox.insert("0.0", "Welcome to GitAutoSync. Please select a folder to scan.\n")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_textbox.insert("end", f"[{timestamp}] {message}\n")
        self.log_textbox.see("end")

    def scan_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        self.log(f"Scanning {folder_path}...")
        self.repos = self.git_manager.scan_for_repos(folder_path)
        self.log(f"Found {len(self.repos)} repositories.")
        
        self.update_repo_list()

    def update_repo_list(self):
        # Clear existing
        for widget in self.repo_list_frame.winfo_children():
            widget.destroy()

        if not self.repos:
            ctk.CTkLabel(self.repo_list_frame, text="No repositories found.").pack(pady=10)
            return

        for repo in self.repos:
            frame = ctk.CTkFrame(self.repo_list_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(frame, text=repo['name'], font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=repo['path'], text_color="gray").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=repo.get('last_status', 'Idle')).pack(side="right", padx=5)

    def manual_commit_all(self):
        threading.Thread(target=self.perform_commit_all).start()

    def perform_commit_all(self):
        msg = self.msg_entry.get()
        if not msg:
            msg = "commit by GitAutoSync"
            
        self.log(f"Starting auto commit/push for {len(self.repos)} repos...")
        
        for repo_dict in self.repos:
            path = repo_dict['path']
            self.log(f"Processing {repo_dict['name']}...")
            result = self.git_manager.commit_and_push(path, msg)
            
            status_text = "Success" if result["success"] else "Error"
            repo_dict['last_status'] = status_text
            self.log(f"-> {repo_dict['name']}: {result['message']}")
            
        self.log("Batch operation completed.")
        # Schedule UI update on main thread
        self.after(0, self.update_repo_list)

    def scheduled_job_worker(self):
        self.log("Running SCHEDULED task...")
        self.perform_commit_all()

    def toggle_scheduler(self):
        if self.scheduler_manager.running:
            self.scheduler_manager.stop_scheduler()
            self.toggle_schedule_btn.configure(text="Start Scheduler", fg_color=["#3B8ED0", "#1F6AA5"]) # Default blue
            self.log("Scheduler stopped.")
        else:
            try:
                interval = float(self.interval_entry.get())
                self.scheduler_manager.start_scheduler(interval)
                self.toggle_schedule_btn.configure(text="Stop Scheduler", fg_color="red")
                self.log(f"Scheduler started (Every {interval} mins).")
            except ValueError:
                self.log("Error: Invalid schedule interval.")

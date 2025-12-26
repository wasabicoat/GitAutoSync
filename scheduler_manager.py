import schedule
import time
import threading

class SchedulerManager:
    def __init__(self, job_func=None):
        self.running = False
        self.worker_thread = None
        self.job_func = job_func
        self.interval_minutes = 1

    def start_scheduler(self, interval_minutes):
        """Starts the scheduler with the given interval in minutes."""
        if self.running:
            return

        self.interval_minutes = interval_minutes
        self.running = True
        
        # Clear existing jobs to avoid duplicates on restart
        schedule.clear()
        
        if self.job_func:
            schedule.every(self.interval_minutes).minutes.do(self.job_func)

        self.worker_thread = threading.Thread(target=self._run_scheduler)
        self.worker_thread.daemon = True # Daemon thread so it closes when main app closes
        self.worker_thread.start()

    def stop_scheduler(self):
        """Stops the scheduler."""
        self.running = False
        schedule.clear()
        if self.worker_thread:
            self.worker_thread.join(timeout=1)
            self.worker_thread = None

    def _run_scheduler(self):
        """Internal loop to run pending jobs."""
        while self.running:
            schedule.run_pending()
            time.sleep(1)

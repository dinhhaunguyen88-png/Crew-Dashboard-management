"""
File Watcher Service for Crew Dashboard
Monitors CSV files and triggers automatic data refresh
"""

import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class CSVFileHandler(FileSystemEventHandler):
    """Handles file system events for CSV files"""
    
    def __init__(self, callback, debounce_seconds=2):
        super().__init__()
        self.callback = callback
        self.debounce_seconds = debounce_seconds
        self.last_modified = {}
        self.csv_extensions = ['.csv', '.CSV']
        
    def _is_csv_file(self, path):
        """Check if file is a CSV file"""
        return any(path.endswith(ext) for ext in self.csv_extensions)
    
    def _should_process(self, file_path):
        """Check if file should be processed (debouncing)"""
        now = time.time()
        last_time = self.last_modified.get(file_path, 0)
        
        if now - last_time > self.debounce_seconds:
            self.last_modified[file_path] = now
            return True
        return False
    
    def on_modified(self, event):
        """Called when a file is modified"""
        if not event.is_directory and self._is_csv_file(event.src_path):
            if self._should_process(event.src_path):
                print(f"[File Watcher] Detected change: {event.src_path}")
                self.callback(event.src_path, 'modified')
    
    def on_created(self, event):
        """Called when a file is created"""
        if not event.is_directory and self._is_csv_file(event.src_path):
            if self._should_process(event.src_path):
                print(f"[File Watcher] Detected new file: {event.src_path}")
                self.callback(event.src_path, 'created')

class FileWatcher:
    """File watcher service that monitors CSV files"""
    
    def __init__(self, watch_directory, callback):
        """
        Initialize file watcher
        
        Args:
            watch_directory: Directory to watch for CSV files
            callback: Function to call when CSV files change
                     Signature: callback(file_path: str, event_type: str)
        """
        self.watch_directory = Path(watch_directory)
        self.callback = callback
        self.observer = None
        self.is_running = False
        
    def start(self):
        """Start watching for file changes"""
        if self.is_running:
            print("[File Watcher] Already running")
            return
        
        if not self.watch_directory.exists():
            print(f"[File Watcher] Directory does not exist: {self.watch_directory}")
            return
        
        event_handler = CSVFileHandler(self.callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_directory), recursive=False)
        self.observer.start()
        self.is_running = True
        
        print(f"[File Watcher] Started monitoring: {self.watch_directory}")
        print(f"[File Watcher] Watching for changes to CSV files...")
    
    def stop(self):
        """Stop watching for file changes"""
        if not self.is_running:
            return
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            print("[File Watcher] Stopped monitoring")
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

def create_watcher(watch_directory, on_change_callback):
    """
    Factory function to create and start a file watcher
    
    Args:
        watch_directory: Directory to watch
        on_change_callback: Function to call on file changes
        
    Returns:
        FileWatcher instance
    """
    watcher = FileWatcher(watch_directory, on_change_callback)
    watcher.start()
    return watcher

# Example usage
if __name__ == "__main__":
    def on_csv_change(file_path, event_type):
        print(f"CSV file {event_type}: {file_path}")
        # Here you would trigger data refresh
        # processor.process_dayrep_csv() etc.
    
    # Watch current directory
    watcher = create_watcher(".", on_csv_change)
    
    try:
        print("Watching for CSV file changes... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        watcher.stop()

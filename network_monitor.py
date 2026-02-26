import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
from datetime import datetime

class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Traffic Monitor")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Configure dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#0078d4"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize network counters
        self.old_download = 0
        self.old_upload = 0
        self.download_speed = 0
        self.upload_speed = 0
        self.running = True
        
        # Track cumulative data
        self.total_download = 0
        self.total_upload = 0
        self.start_time = time.time()
        
        self.setup_ui()
        self.update_thread = threading.Thread(target=self.monitor_network, daemon=True)
        self.update_thread.start()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="Network Traffic Monitor",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        # Main display frame
        display_frame = tk.Frame(self.root, bg=self.bg_color)
        display_frame.pack(pady=10)
        
        # Download section
        download_frame = tk.Frame(display_frame, bg=self.bg_color, relief=tk.RIDGE, borderwidth=2)
        download_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        
        tk.Label(
            download_frame,
            text="⬇ DOWNLOAD",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg="#4CAF50"
        ).pack(pady=5)
        
        self.download_label = tk.Label(
            download_frame,
            text="0.00 KB/s",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.download_label.pack(pady=10)
        
        self.total_download_label = tk.Label(
            download_frame,
            text="Total: 0.00 MB",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        self.total_download_label.pack(pady=5)
        
        # Upload section
        upload_frame = tk.Frame(display_frame, bg=self.bg_color, relief=tk.RIDGE, borderwidth=2)
        upload_frame.pack(pady=10, padx=20, fill=tk.BOTH)
        
        tk.Label(
            upload_frame,
            text="⬆ UPLOAD",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg="#2196F3"
        ).pack(pady=5)
        
        self.upload_label = tk.Label(
            upload_frame,
            text="0.00 KB/s",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.upload_label.pack(pady=10)
        
        self.total_upload_label = tk.Label(
            upload_frame,
            text="Total: 0.00 MB",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        self.total_upload_label.pack(pady=5)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Monitoring active...",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#888888"
        )
        self.status_label.pack()
        
    def format_bytes(self, bytes_value):
        """Convert bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def monitor_network(self):
        """Monitor network traffic in background thread"""
        # Get initial network stats
        net_io = psutil.net_io_counters()
        self.old_download = net_io.bytes_recv
        self.old_upload = net_io.bytes_sent
        
        while self.running:
            time.sleep(1)  # Update every second
            
            # Get current network stats
            net_io = psutil.net_io_counters()
            current_download = net_io.bytes_recv
            current_upload = net_io.bytes_sent
            
            # Calculate speed (bytes per second)
            self.download_speed = current_download - self.old_download
            self.upload_speed = current_upload - self.old_upload
            
            # Update cumulative totals
            self.total_download += self.download_speed
            self.total_upload += self.upload_speed
            
            # Update old values
            self.old_download = current_download
            self.old_upload = current_upload
            
            # Update UI in main thread
            self.root.after(0, self.update_ui)
    
    def update_ui(self):
        """Update the UI with current network speeds"""
        # Update download speed
        download_text = self.format_bytes(self.download_speed) + "/s"
        self.download_label.config(text=download_text)
        
        # Update upload speed
        upload_text = self.format_bytes(self.upload_speed) + "/s"
        self.upload_label.config(text=upload_text)
        
        # Update totals
        self.total_download_label.config(text=f"Total: {self.format_bytes(self.total_download)}")
        self.total_upload_label.config(text=f"Total: {self.format_bytes(self.total_upload)}")
        
        # Update status with uptime
        uptime = int(time.time() - self.start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        self.status_label.config(text=f"Monitoring active | Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()

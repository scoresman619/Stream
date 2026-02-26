# Stream - Network Traffic Monitor

A portable real-time network traffic monitor for Windows 11 that displays upstream and downstream bandwidth usage.

## Features

- **Real-time monitoring**: Updates every second with current network speeds
- **Download & Upload tracking**: Separate displays for downstream and upstream traffic
- **Cumulative statistics**: Tracks total data transferred since application start
- **Session uptime**: Shows how long the monitor has been running
- **Modern UI**: Clean, dark-themed interface optimized for Windows 11
- **Portable**: No installation required, runs directly from Python

## Requirements

- Windows 11 (also compatible with Windows 10)
- Python 3.7 or higher
- Required Python packages:
  - `psutil` - For network statistics
  - `tkinter` - For GUI (included with Python)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/scoresman619/Stream.git
   cd Stream
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python network_monitor.py
```

The application window will display:
- **Download speed**: Current downstream bandwidth in real-time
- **Upload speed**: Current upstream bandwidth in real-time
- **Total downloaded**: Cumulative data received during the session
- **Total uploaded**: Cumulative data sent during the session
- **Uptime**: Session duration

## Creating a Portable Executable

To create a standalone executable that doesn't require Python to be installed:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**:
   ```bash
   pyinstaller --onefile --windowed --name "NetworkMonitor" network_monitor.py
   ```

3. The executable will be in the `dist` folder and can be run on any Windows 11 machine without Python installed.

## How It Works

The application uses the `psutil` library to access network interface statistics from Windows. It:
1. Reads byte counters from all network interfaces
2. Calculates the difference between readings taken 1 second apart
3. Displays the result as bytes per second in a user-friendly format (KB/s, MB/s, etc.)
4. Updates the GUI in real-time using threading to prevent UI freezing

## Limitations

- Shows combined traffic for all network interfaces
- Does not distinguish between different applications or connections
- Requires appropriate permissions to read network statistics

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

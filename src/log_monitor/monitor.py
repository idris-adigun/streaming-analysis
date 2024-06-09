import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = file_path
        self._cached_lines = self._read_lines()

    def _read_lines(self):
        with open(self.file_path, 'r') as file:
            return file.readlines()

    def on_modified(self, event):
        if event.src_path == self.file_path:
            new_lines = self._get_new_lines()
            if new_lines:
                print('New lines added:')
                for line in new_lines:
                    print(line, end='')

    def _get_new_lines(self):
        current_lines = self._read_lines()
        new_lines = current_lines[len(self._cached_lines):]
        self._cached_lines = current_lines
        return new_lines

def monitor_file(file_path):
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    observer.schedule(event_handler, path=file_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    file_path = 'path/to/your/file.txt'  # Replace with the path to your file
    monitor_file(file_path)

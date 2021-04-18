import logging
import os
import pathlib
import tempfile
import threading
import typing

import psutil


class FileLock:
    _lock_counter = 0
    _global_lock = threading.Lock()

    def __init__(self) -> None:
        self._lockfile = pathlib.Path(
            tempfile.gettempdir()) / "fridgecamera.lock"
        self._logger = logging.getLogger(__name__)

    def __enter__(self) -> None:
        if not self.acquire():
            raise RuntimeError(
                f"Failed to acquire file lock on: {self._lockfile}")

    def __exit__(self, *_: typing.Any) -> None:
        self.release()

    def acquire(self) -> bool:
        with FileLock._global_lock:
            acquired = self._create_lockfile()
            self._logger.debug(
                f"Lock file acquired: {acquired} (currently {FileLock._lock_counter} locks)")
            if acquired:
                FileLock._lock_counter += 1
            return acquired

    def _create_lockfile(self) -> bool:
        if self._lockfile.exists():
            pid = int(self._lockfile.read_text())
            self._logger.debug(f"Found lockfile with PID: {pid}")

            if pid == os.getpid():
                self._logger.debug("Current process already has lock")
                return True

            try:
                process = psutil.Process(pid)
            except psutil.NoSuchProcess:
                self._logger.debug("No such process exists")
            else:
                if process.is_alive():
                    self._logger.debug("Process is running")
                    return False

            self._logger.warning(
                "Lockfile found, but process is not alive. Previous run might have crashed")
            # Clean up lockfile, since process is not running anymore
            self._lockfile.unlink()

        # Create temporary file first and then move it, since rename is an
        # atomic operation (creating file and writing to it in place is not)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = pathlib.Path(tmpdir) / "tmp.lock"
            tmpfile.write_text(str(os.getpid()))
            tmpfile.rename(self._lockfile)

        return True

    def release(self) -> None:
        with FileLock._global_lock:
            if self._lockfile.exists() and self._lockfile.read_text() == str(os.getpid()):
                self._logger.debug(f"Lockfile exists (currently {FileLock._lock_counter} locks)")
                FileLock._lock_counter -= 1
                if FileLock._lock_counter <= 0:
                    self._logger.debug("Removing lock file")
                    self._lockfile.unlink()
                self._logger.debug("Released lock")

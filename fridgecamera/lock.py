import logging
import os
import pathlib
import tempfile

import psutil


class FileLock:
    def __init__(self) -> None:
        self._lockfile = pathlib.Path(
            tempfile.gettempdir()) / "fridgecamera.lock"
        self._logger = logging.getLogger(__name__)

    def __enter__(self) -> None:
        if not self.acquire():
            raise RuntimeError(
                f"Failed to acquire file lock on: {self._lockfile}")

    def __exit__(self) -> None:
        self.release()

    def acquire(self) -> bool:
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
        if self._lockfile.exists() and self._lockfile.read_text() == str(os.getpid()):
            self._lockfile.unlink()
            self._logger.debug("Removing lock file")

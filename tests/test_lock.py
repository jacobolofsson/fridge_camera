import os
from unittest.mock import MagicMock, patch

import psutil
import pytest

from fridgecamera.lock import FileLock


@pytest.fixture()
def lockfile(mock_tmp_dir):
    return mock_tmp_dir / "fridgecamera.lock"


def test_no_lock_file(lockfile):
    f = FileLock()
    assert not lockfile.exists()

    assert f.acquire()
    assert lockfile.exists()
    assert lockfile.read_text() == str(os.getpid())
    f.release()

    assert not lockfile.exists()


def test_existing_lock_file_no_process(lockfile):
    f = FileLock()
    lockfile.write_text("1234")

    with patch("psutil.Process") as mock_process:
        mock_process.side_effect = psutil.NoSuchProcess(1234)
        assert f.acquire()
        mock_process.assert_called_once_with(1234)

    assert lockfile.read_text() == str(os.getpid())
    f.release()


def test_existing_lock_file_dead_process(lockfile):
    f = FileLock()
    lockfile.write_text("1234")

    with patch("psutil.Process") as mock_process:
        mock_process.return_value.is_alive.return_value = False
        assert f.acquire()
        mock_process.assert_called_once_with(1234)

    assert lockfile.read_text() == str(os.getpid())
    f.release()


def test_existing_lock_file_alive_process(lockfile):
    f = FileLock()
    lockfile.write_text("1234")

    with patch("psutil.Process") as mock_process:
        mock_process.return_value.is_alive.return_value = True
        assert not f.acquire()
        mock_process.assert_called_once_with(1234)

    assert lockfile.read_text() == "1234"


def test_double_lock(lockfile):
    f1 = FileLock()
    f2 = FileLock()
    f1.acquire()
    assert lockfile.exists()
    f2.acquire()
    f2.release()
    assert lockfile.exists()
    f1.release()
    assert not lockfile.exists()


def test_context_manager():
    f = FileLock()
    f.acquire = MagicMock()
    f.release = MagicMock()
    with f:
        f.acquire.assert_called_once_with()
        f.release.assert_not_called()
    f.release.assert_called_once_with()


def test_context_manager_acquire_fail():
    f = FileLock()
    f.acquire = lambda: False
    with pytest.raises(RuntimeError):
        with f:
            assert False  # This should not be executed

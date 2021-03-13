import os
from unittest.mock import patch

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


def test_existing_lock_file_dead_process(lockfile):
    f = FileLock()
    lockfile.write_text("1234")

    with patch("psutil.Process") as mock_process:
        mock_process.return_value.is_alive.return_value = False
        assert f.acquire()
        mock_process.assert_called_once_with(1234)

    assert lockfile.read_text() == str(os.getpid())


def test_existing_lock_file_alive_process(lockfile):
    f = FileLock()
    lockfile.write_text("1234")

    with patch("psutil.Process") as mock_process:
        mock_process.return_value.is_alive.return_value = True
        assert not f.acquire()
        mock_process.assert_called_once_with(1234)

    assert lockfile.read_text() == "1234"

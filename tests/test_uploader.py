import pytest
import os
from unittest.mock import patch

from fridgecamera.uploader import Uploader

HOST = "test_host"
USER = "test_user"
PASS = "test_pass"
PATH = "test_path"


@pytest.fixture()
def uploader() -> Uploader:
    return Uploader(HOST, USER, PASS, PATH)


def test_upload(uploader: Uploader) -> None:
    test_path = "test_path"
    test_name = "test_name"
    with patch("ftplib.FTP") as mock_ftp:
        with patch("builtins.open") as mock_open:
            uploader.upload(test_path, test_name)
    mock_open.assert_called_once_with(os.path.join(test_path, test_name), "rb")
    mock_ftp.assert_called_once_with(host=HOST)
    mock_ftp.return_value.login.assert_called_once_with(user=USER, passwd=PASS)
    mock_ftp.return_value.cwd.assert_called_once_with(PATH)
    mock_ftp.return_value.storbinary.assert_called_once_with(
        f"STOR {test_name}",
        mock_open.return_value.__enter__.return_value
    )
    mock_ftp.return_value.quit.assert_called_once_with()

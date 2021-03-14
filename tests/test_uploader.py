from unittest.mock import MagicMock, patch

import pytest

from fridgecamera.uploader import Uploader

HOST = "test_host"
USER = "test_user"
PASS = "test_pass"
PATH = "test_path"


@pytest.fixture()
def uploader() -> Uploader:
    return Uploader(HOST, USER, PASS, PATH)


def test_upload(uploader: Uploader) -> None:
    test_path = MagicMock()
    with patch("ftplib.FTP") as mock_ftp:
        uploader.upload(test_path)
    test_path.open.assert_called_once_with(mode="rb")
    mock_ftp.assert_called_once_with(host=HOST)
    mock_ftp.return_value.login.assert_called_once_with(user=USER, passwd=PASS)
    mock_ftp.return_value.cwd.assert_called_once_with(PATH)
    mock_ftp.return_value.storbinary.assert_called_once_with(
        f"STOR {test_path.name}",
        test_path.open.return_value.__enter__.return_value
    )
    mock_ftp.return_value.quit.assert_called_once_with()

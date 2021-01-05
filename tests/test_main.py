from unittest.mock import MagicMock, patch

from fridgecamera.main import main


@patch("fridgecamera.main.get_config")
@patch("fridgecamera.main.Worker")
def test_main(mock_worker, mock_parser) -> None:
    mock_argv = MagicMock()
    mock_tmpdir = "/this/is/a/fake/temp/path"
    with patch("fridgecamera.main.gettempdir") as mock_gettempdir:
        mock_gettempdir.return_value = mock_tmpdir
        main(mock_argv)
    mock_parser.assert_called_once_with(mock_argv)
    mock_worker.assert_called_once_with(
        mock_parser.return_value.camid,
        mock_tmpdir + "/.fridgecamera",
        {
            "host": mock_parser.return_value.ftp_host,
            "user": mock_parser.return_value.ftp_user,
            "pass": mock_parser.return_value.ftp_pass,
            "path": mock_parser.return_value.ftp_path
        },
        mock_parser.return_value.fps,
    )

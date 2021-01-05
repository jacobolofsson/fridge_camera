from unittest.mock import patch

from fridgecamera.main import main


@patch("fridgecamera.main.Worker")
def test_main(mock_worker, tmp_config_file, cli_args) -> None:
    mock_tmpdir = "/this/is/a/fake/temp/path"
    with patch("fridgecamera.main.gettempdir") as mock_gettempdir:
        with patch("fridgecamera.main.Path.home") as mock_homepath:
            mock_gettempdir.return_value = mock_tmpdir
            mock_homepath.return_value = tmp_config_file.parent
            assert main(cli_args) == 0

    mock_worker.assert_called_once_with(
        99,
        mock_tmpdir + "/.fridgecamera",
        (200, 12800),
        {
            "host": "testhost",
            "user": "testuser",
            "pass": None,
            "path": None,
        },
        123,
    )
    mock_worker.return_value.serve_forever.assert_called_once_with()

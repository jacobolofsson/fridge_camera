from fridgecamera.configuration import parse_arguments


def test_default_args() -> None:
    args = parse_arguments([])
    assert not args.verbose
    assert args.imgpath == "images/"
    assert args.camid == 0
    assert args.fps == 2
    assert args.ftp_host is None
    assert args.ftp_user is None
    assert args.ftp_pass is None
    assert args.ftp_path is None


def test_parse_args() -> None:
    args = parse_arguments([
        "-v",
        "-p",
        "testpath",
        "--camid",
        "99",
        "--fps",
        "123",
        "--ftp_host",
        "testhost",
        "--ftp_user",
        "testuser",
        "--ftp_pass",
        "testpass",
        "--ftp_path",
        "testpath",
    ])
    assert args.verbose
    assert args.imgpath == "testpath"
    assert args.camid == 99
    assert args.fps == 123
    assert args.ftp_host == "testhost"
    assert args.ftp_user == "testuser"
    assert args.ftp_pass == "testpass"
    assert args.ftp_path == "testpath"

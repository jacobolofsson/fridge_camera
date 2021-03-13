import ftplib
import logging
import pathlib


class Uploader:
    def __init__(self, host: str, user: str, passwd: str, path: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.user = user
        self.passwd = passwd
        self.path = path

    def upload(self, path: pathlib.Path) -> None:
        self.logger.info(
            f"Uploading '{path}'"
        )
        # Open and close FTP connection for each transfer.
        # Might be a long time between transmissions.
        ftps = ftplib.FTP(host=self.host)
        ftps.login(user=self.user, passwd=self.passwd)
        ftps.cwd(self.path)
        with path.open(mode='rb') as image_fd:
            # Use same file name at destination as source
            ftps.storbinary('STOR ' + str(path.name), image_fd)
            ftps.quit()

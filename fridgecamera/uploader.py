import ftplib
import os


class Uploader:
    def __init__(self, host: str, user: str, passwd: str, path: str) -> None:
        self.host = host
        self.user = user
        self.passwd = passwd
        self.path = path

    def upload(self, filepath: str, filename: str) -> None:
        # Open and close FTP connection for each transfer.
        # Might be a long time between transmissions.
        ftps = ftplib.FTP(host=self.host)
        ftps.login(user=self.user, passwd=self.passwd)
        ftps.cwd(self.path)
        with open(os.path.join(filepath, filename), 'rb') as image_fd:
            # Use same file name at destination as source
            ftps.storbinary('STOR ' + filename, image_fd)
            ftps.quit()

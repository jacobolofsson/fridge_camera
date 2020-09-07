import ftplib

class Uploader:
    def __init__(self, host, user, passwd, path):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.path = path
    def upload(self, filepath, filename):
        # Open and close FTP connection for each transfer.
        # Might be a long time between transmissions.
        ftps = ftplib.FTP(host=self.host)
        ftps.login(user=self.user, passwd=self.passwd)
        ftps.cwd(self.path)
        image_fd = open(filepath + filename, 'rb');
        # Use same file name at destination as source
        ftps.storbinary('STOR ' + filename, image_fd);
        image_fd.close()
        ftps.quit()

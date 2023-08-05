"""Helper module for handling network related commands."""
import os

import requests

from phytoolkit.exception.installationexception import InstallationException


class NetHelper:
    """Runs network commands."""

    def __init__(self, config):
        self.config = config
        self.console = config.console

    def download_file(self, url, target_file):
        """Downloads file from URL to target file."""
        if not str.startswith(target_file, self.config.dest_dir):
            target_file = os.path.join(self.config.dest_dir, target_file)
        self.console.verbose_info("Downloading file %s from url %s." % (target_file, url))
        response = requests.get(url)
        if response.status_code not in [200, "200"]:
            self.console.verbose_error("Download failed with status code %s" % response.status_code)
            raise InstallationException("Download of file %s failed." % target_file)
        with open(target_file, "wb") as file_handle:
            self.console.verbose_info("Download completed. Writing to file %s." % target_file)
            file_handle.write(response.content)
        self.console.verbose_success("Download of %s completed." % target_file)

"""Helper module for handling OS related commands."""
import os
import platform
import subprocess

from phytoolkit.exception.installationexception import InstallationException


class OsHelper:
    """Runs shell commands."""

    def __init__(self, config):
        self.config = config
        self.console = config.console
        self.current_dir = os.getcwd()
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()

    def get_as_string(self):
        """Returns OS configuration."""
        return "%s - %s - %s" % (self.system, self.release, self.version)

    def validate(self):
        """Validates OS."""
        supported_platforms = ["Linux", ]
        self.console.verbose_info(
            "Validating against supported platforms %s." % ", ".join(supported_platforms))
        if self.system not in supported_platforms:
            raise InstallationException("Unsupported platform %s" % self.system)
        self.console.verbose_success("Platform %s is supported." % self.system)

        self.console.verbose_info("Checking for variant 'Ubuntu' in version.")
        if "Ubuntu" not in self.version:
            raise InstallationException(
                "Unsupported variant %s. Only 'Ubuntu' supported." % self.version)
        self.console.verbose_success("Variant %s is supported." % self.version)

        self.console.verbose_info("Installing to destination directory %s." % self.config.dest_dir)
        if not os.path.exists(self.config.dest_dir):
            os.makedirs(self.config.dest_dir)
        self.console.verbose_success("Destination directory created.")

    def run_shell_command(self, command, cwd=""):
        """Runs a shell command."""
        if cwd == "":
            cwd = self.config.dest_dir
        self.console.verbose_info("Running command %s from %s." % (" ".join(command), cwd))
        output = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=True)
        self.config.log_file.write(output.stdout.decode("UTF-8"))
        self.config.log_file.write(output.stderr.decode("UTF-8"))
        self.console.verbose_info("Command exited with status %s." % output.returncode)
        return output.returncode == 0

    def install_packages(self, packages, cwd=""):
        """Short cut for installing apt packages."""
        self.console.verbose_info("Installing packages %s." % ", ".join(packages))
        return self.run_shell_command(["sudo", "apt", "install", "-y"] + packages, cwd)

    def extract_tar_file(self, file, cwd=""):
        """Extracts tar file."""
        self.console.verbose_info("Extracting tar file %s." % file)
        return self.run_shell_command(["tar", "xf", file], cwd)

    def write_file(self, file, content):
        """Writes content into file."""
        self.console.verbose_info("Writing contents\n %s \nto file %s." % (content, file))
        with open(file, "w") as file_handle:
            file_handle.write(content)
        self.console.verbose_success("File write completed.")

    def append_file(self, file, content):
        """Appends content into file."""
        self.console.verbose_info("Appending contents\n %s \nto file %s." % (content, file))
        with open(file, "a") as file_handle:
            file_handle.write(content)
        self.console.verbose_success("File append completed.")

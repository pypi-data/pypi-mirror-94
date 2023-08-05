"""Module for common installation logic."""

from abc import ABC, abstractmethod

from phytoolkit.exception.installationexception import InstallationException
from phytoolkit.helper.consolehelper import ConsoleHelper
from phytoolkit.helper.nethelper import NetHelper
from phytoolkit.helper.oshelper import OsHelper


class BaseInstaller(ABC):
    """Base installer with common installation operations and general behaviour."""

    def __init__(self, config):
        self.config = config
        self.required_os_packages = []
        self.console = ConsoleHelper(config.log_file, config.verbose)

        self.console.verbose_info("Initializing OS Helper.")
        self.os_helper = OsHelper(config)
        self.console.verbose_success("OS Helper initialized.")

        self.console.verbose_info("Validating OS and installation location.")
        self.os_helper.validate()
        self.console.verbose_success("Validation successful.")

        self.console.verbose_info("Initializing Net Helper.")
        self.net_helper = NetHelper(config)
        self.console.verbose_success("Net Helper initialized.")

    def install(self):
        """Controlling logic which calls other sub-steps."""
        self.console.verbose_info("Beginning installation.")
        self.console.verbose_info("OS details: %s" % self.os_helper.get_as_string())

        self.install_required_os_packages()

        self.console.verbose_info("Running pre-installation steps.")
        self.pre_installation()
        self.console.verbose_success("Pre-installation steps completed.")

        self.console.verbose_info("Running installation steps.")
        self.installation()
        self.console.verbose_success("Installation steps completed.")

        self.console.verbose_info("Running post-installation steps.")
        self.post_installation()
        self.console.verbose_success("Post installation steps completed.")

        self.console.success("Installation completed.")

    def install_required_os_packages(self):
        """Installs required packages on the OS."""
        if self.config.verbose:
            self.console.verbose_info("Updating package repository.")
        if not self.os_helper.run_shell_command(["sudo", "apt", "update"]):
            raise InstallationException("Package repository update failed.")
        if self.config.verbose:
            self.console.verbose_success("Package repository updated.")
            self.console.verbose_info("Installing required OS packages.")
        if not self.os_helper.install_packages(self.required_os_packages):
            raise InstallationException("Installation of required packages failed.")
        if self.config.verbose:
            self.console.verbose_success("OS packages installed.")

    @abstractmethod
    def pre_installation(self):
        """Placeholder for pre-installation logic."""

    @abstractmethod
    def installation(self):
        """Placeholder for main installation logic."""

    @abstractmethod
    def post_installation(self):
        """Placeholder for post-installation logic."""

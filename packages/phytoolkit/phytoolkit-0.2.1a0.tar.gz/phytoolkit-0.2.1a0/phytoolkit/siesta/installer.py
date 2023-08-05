"""Install Siesta and dependencies."""
import click

from phytoolkit.base.installer import BaseInstaller


class SiestaInstaller(BaseInstaller):
    """Installs Siesta suite."""

    def __init__(self, config):
        super().__init__(config)
        self.required_os_packages = ["python", "curl", "unzip", "hwloc", "sysstat",
                                     "build-essential", "g++", "gfortran", "libreadline-dev",
                                     "m4", "xsltproc", "mpich", "libmpich-dev"]

    def pre_installation(self):
        pass

    def installation(self):
        pass

    def post_installation(self):
        click.echo("Installation of Siesta suite completed.", file=self.config.log_file)
        click.echo("Siesta binaries siesta, transiesta and tbtrans installed to /usr/local/bin.",
                   file=self.config.log_file)

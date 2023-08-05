"""Main class for handling the CLI commands and groups."""
import sys

import click

from phytoolkit.exception.installationexception import InstallationException
from phytoolkit.helper.consolehelper import ConsoleHelper


class Config:
    """Configuration class for storing installation configuration."""

    def __init__(self):
        self.verbose = False
        self.log_file = None
        self.dest_dir = None
        self.vasp_source = None
        self.siesta_version = None
        self.console = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--verbose", is_flag=True)
@pass_config
def cli(config, verbose):
    """Command line utility to manage the most commonly used tools for material simulations."""
    config.verbose = verbose


@cli.group()
@click.option("--dest-dir", type=click.Path(), default=".",
              help="Destination directory where the tool should be "
                   "installed.")
@click.option("--log-file", type=click.File("w"), default="-",
              help="File to store the installation log.")
@pass_config
def install(config, dest_dir, log_file):
    """Install a simulation tool on your system."""
    config.dest_dir = dest_dir
    config.log_file = log_file
    config.console = ConsoleHelper(log_file, config.verbose)
    config.console.verbose_info("Logging output in verbose mode.")


@install.command()
@click.option("--vasp-source", type=click.Path(), default=".",
              help="Path to vasp.5.4.4.tar.gz file.")
@pass_config
def vasp(config, vasp_source):
    """Installs the Vienna Ab-initio Simulation Package. We currently support VASP
    installation using MPICH library only. The source of VASP is not bundled due to licence
    restrictions. Please obtain a copy of vasp-5.4.4.tar.gz file
    and provide the path as configuration."""
    config.vasp_source = vasp_source

    try:
        from phytoolkit.vasp.installer import VaspInstaller
        vasp_installer = VaspInstaller(config)
        vasp_installer.install()
    except InstallationException as exception:
        config.console.error(str(exception))
        sys.exit(1)


@install.command()
@click.option("--siesta-version", type=click.Choice("4.1-b3", "4.1-b4"), default="4.1-b3",
              help="Version of Siesta to be installed.")
@pass_config
def siesta(config, siesta_version):
    """Installs Siesta suite, including Siesta, TranSiesta, TBtrans."""
    try:
        config.siesta_version = siesta_version
        from phytoolkit.siesta.installer import SiestaInstaller
        siesta_installer = SiestaInstaller(config)
        siesta_installer.install()
    except InstallationException as exception:
        config.console.error(str(exception))
        sys.exit(1)

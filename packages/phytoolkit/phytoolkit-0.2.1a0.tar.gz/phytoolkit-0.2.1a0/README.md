# phytoolkit
Installation kit for material simulation tools. Currently, it supports installation of:
- VASP 5.4.4

In progress:
- Siesta
- Quantum ESPRESSO

## How to use this tool

### Prerequisites
It is only tested with Ubuntu 18.04 and 20.04 and Python 3. Rest of the platforms may or may not work.

### Steps to install
```bash
python3 -m pip install phytoolkit
```

### Accessing documentation
```bash
phytoolkit --help
```

If the above command doesn't work, it means that you have installed the Python packages locally. Add
your local `bin` folder to path. Usually `~/.local/bin`. You can do this by adding the following to
the end of your `.bashrc` file.

```bash
export PATH=$PATH:~/.local/bin
```

Once you have done this, you have to restart the terminal application or run the following command.

```bash
source ~/.bashrc
```

## Notice
VASP source is licensed content. It is not shipped with this tool. You need to obtain it from the authorized parties. See: https://www.vasp.at/faqs/

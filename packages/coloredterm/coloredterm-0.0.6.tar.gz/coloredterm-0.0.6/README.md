<h1>ColoredTerm</h1>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Downloads](https://pepy.tech/badge/coloredterm)](https://pepy.tech/project/coloredterm)
[![Documentation Status](https://readthedocs.org/projects/coloredterm/badge/?version=latest)](https://coloredterm.readthedocs.io/en/latest/?badge=latest)

Coloredterm is a collection of functions to help you make text in your terminal a different color.

With fg, bg, Fore, Back, Style, colored and cprint functions.

<details>
<summary>Table of contents</summary>

- [Getting started](#getting-started)
  - [Installing](#installing)
  - [Usage](#usage)

</details>

# Getting started



## Installing

To install the package you will need python2.7 or higher and pip installed.

With those installed you can start.

To install it go to your terminal and put in this command:
```bash
pip install coloredterm
```
Or you can download it from github.
You can do that with:
```bash
pip install git+https://github.com/hostedposted/coloredterm.git
```

## Usage

Here is a quick example:

```python
from coloredterm import Fore, Back # Importing The Fore and Back class from coloredterm.

print(f"{Fore.BLUE}{Back.YELLOW}Foreground of Blue Background of yellow.") # Printing text with a Foreground of Blue and Background of Yellow.
```

For more please go to the [documentation](https://coloredterm.readthedocs.io/en/latest/).




[contributors-shield]: https://img.shields.io/github/contributors/hostedposted/coloredterm.svg?style=for-the-badge
[contributors-url]: https://github.com/hostedposted/coloredterm/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/hostedposted/coloredterm.svg?style=for-the-badge
[forks-url]: https://github.com/hostedposted/coloredterm/network/members
[stars-shield]: https://img.shields.io/github/stars/hostedposted/coloredterm.svg?style=for-the-badge
[stars-url]: https://github.com/hostedposted/coloredterm/stargazers
[issues-shield]: https://img.shields.io/github/issues/hostedposted/coloredterm.svg?style=for-the-badge
[issues-url]: https://github.com/hostedposted/coloredterm/issues
[license-shield]: https://img.shields.io/github/license/hostedposted/coloredterm.svg?style=for-the-badge
[license-url]: https://github.com/hostedposted/coloredterm/blob/master/LICENSE.txt
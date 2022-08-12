[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

# bgp_extrapolator_pkg
This package simulates BGP Extrapolation, and is a wrapper around Sam Secondo's [extrapolator engine](https://github.com/Same4254/BGPExtrapolator). This package also contains additional functionality for testing, and for verification of results.

* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#license)
* [TODO](#todo)

## Package Description

TODO

## Usage
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

TODO

## Installation
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

Install python and pip if you have not already. Then run:

```bash
pip3 install pip --upgrade
pip3 install wheel
```

For production:

```bash
pip3 install git@github.com:jfuruness/bgp_extrapolator_pkg.git
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/bgp_extrapolator_pkg.git
cd bgp_extrapolator_pkg
pip3 install -e .[test]
```

To test the development package: [Testing](#testing)


## Testing
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

To test the package after installation:

```
cd bgp_extrapolator_pkg
pytest bgp_extrapolator_pkg
flake8 bgp_extrapolator_pkg
mypy bgp_extrapolator_pkg
```

To view the PDF after it completes:

```
pytest bgp_extrapolator_pkg --view
```

If you want to run it across multiple environments, and have python 3.9 installed:

```
cd bgp_extrapolator_pkg
tox
```


## Development/Contributing
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Add an engine test if you've made a change in the propagation logic, or a system/unit test if the framework was modified
5. Run tox (for faster iterations: flake8, mypy, and pytest can be helpful)
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin my-new-feature`
8. Ensure github actions are passing tests
9. Email me at jfuruness@gmail.com

## History
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

* 0.0.0 Initial version, merely templating out parts of the framework. Non functional.

## Credits
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

Thanks to Sam Secondo and his [extrapolator engine](https://github.com/Same4254/BGPExtrapolator) as well as carrying this project over the finish line

## License
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

BSD License (see license file)

## TODO
* [bgp_extrapolator_pkg](#bgp_extrapolator_pkg)

TODO

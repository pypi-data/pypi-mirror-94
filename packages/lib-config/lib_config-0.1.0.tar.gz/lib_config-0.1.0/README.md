# lib\_config
This package contains helper functions for accessing a config file. Basically a wrapper for [this](https://docs.python.org/3/library/configparser.html)

* [lib\_config](#lib_config)
* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#license)

## Package Description
* [lib\_config](#lib_config)

This package contains wrapper functions useful for accessing credentials for various services. Utilizes [this](https://docs.python.org/3/library/configparser.html)


## Usage
* [lib\_config](#lib_config)

```python
from lib_config import Config
# init config
# path is now: /etc/<my_package_name>.conf
conf = Config(package="my_package_name")
# Writes the credentials to a section called db
conf.write_section("db", {"username": "Bob", "password": "insecure"})
# Access various tags
username, password = conf.get_creds("db", tags=["username", "password"])
# Access only one tag
username = conf.read("db", "username")
```

Config file format is as follows:
```
[db]
username = Bob
password = insecure
```

## Installation
* [lib\_config](#lib_config)

Must use linux, since the base path starts in /etc

Install python and pip if you have not already. Then run:

```bash
pip3 install wheel
pip3 install lib_config
```
This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/lib_config.git
cd lib_config
pip3 install wheel
pip3 install -e .
```

To test the development package: [Testing](#testing)


## Testing
* [lib\_config](#lib_config)

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
(Note that you must have all dependencies installed first)
```python3 setup.py test```

To test from pip install:
```bash
pip3 install wheel
# janky but whatever. Done to install deps
pip3 install lib_config
pip3 uninstall lib_config
pip3 install lib_config --install-option test
```

## Development/Contributing
* [lib\_config](#lib_config)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because idk how to even check those messages

## History
* [lib\_config](#lib_config)
* 0.1.0 First production release

## Credits
* [lib\_config](#lib_config)

Credits to Drew Monroe and the UITS team for inspiring this library.

## License
* [lib\_config](#lib_config)

BSD License (see license file)

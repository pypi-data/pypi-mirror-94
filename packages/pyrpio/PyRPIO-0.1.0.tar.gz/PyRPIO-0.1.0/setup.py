# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrpio']

package_data = \
{'': ['*'], 'pyrpio': ['lib/*']}

setup_kwargs = {
    'name': 'pyrpio',
    'version': '0.1.0',
    'description': 'Python-wrapped RPIO',
    'long_description': "# PyRPIO\n\n![./icon.png](./icon.png)\n\nA Python 3 addon which provides high-speed access to the Raspberry Pi GPIO interface, supporting regular GPIO as well as i²c, PWM, SPI, and MDIO.\n\nThis package is inspired by [node-rpio](https://github.com/jperkin/node-rpio) which is a node.js addon.\n\n![PyPI](https://img.shields.io/pypi/v/pyrpio)\n\n## Compatibility\n\n- Raspberry Pi Models: A, B (revisions 1.0 and 2.0), A+, B+, 2, 3, 3+, 3 A+, 4, Compute Module 3, Zero.\n- Python 3.6+\n\n## Install\n\nInstall the latest from PyPi:\n\n> `pip install pyrpio`\n\n## Supported Interfaces\n\n- GPIO\n- PWM\n- I2C\n- MDIO\n- SPI\n\n## Examples\n\n```python\nfrom pyrpio import i2c, mdio\n\n### I2C Operations ###\n\ni2c_bus = i2c.I2C('/dev/i2c-3')\ni2c_bus.open()\n\ni2c_bus.set_address(0x50)\n\n# Read 8-bit value using 8-bit addressing\nval = i2c_bus.read_register(0x0)\ni2c_bus.set_address(0x21)\n\n# Read uint16_t using 8-bit addressing\nval = i2c_bus.read_register(0x0, reg_nbytes=1, val_nbytes=2)\n\n# Read int16_t using 8-bit addressing\nval = i2c_bus.read_register(0x0, reg_nbytes=1, val_nbytes=2, signed=True)\n\n# Seq read 8 regs starting @ 0x0 using I2C repeat start\nregs = i2c_bus.read_register_sequential(0,8)\n\n# Close up shop\ni2c_bus.close()\n\n### MDIO Operations ###\n\n# Create bus using GPIO pins 23 and 24 (bit-bang)\nmdio_bus = mdio.MDIO(clk_pin=23, data_pin=24, path='/dev/gpiochip0')\nmdio_bus.open()\n\n# Read register 0x10 from device 0x30 (CLAUSE-45)\nmdio_bus.read_c45_register(0x30, 0x00, 0x10)\n\n# Read register set from device 0x30 (CLAUSE-45)\nmdio_bus.read_c45_registers(0x30, 0x00, [0,1,2,3,4])\n\n# Close up shop\nmdio_bus.close()\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n## Maintainers\n\n- [Samtec - ASH](https://samtec-ash.com)\n",
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Samtec-ASH/pyrpio',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

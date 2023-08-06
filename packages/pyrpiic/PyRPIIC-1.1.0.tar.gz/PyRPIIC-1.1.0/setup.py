# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrpiic',
 'pyrpiic.clock',
 'pyrpiic.eeprom',
 'pyrpiic.eeprom.tests',
 'pyrpiic.ioexpander',
 'pyrpiic.sensor']

package_data = \
{'': ['*']}

install_requires = \
['PyRPIO>=0.1.0,<0.2.0', 'bitarray>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'pyrpiic',
    'version': '1.1.0',
    'description': 'Python RPI interface to low-level ICs',
    'long_description': "# PyRPIIC\n\n![./icon.png](./icon.png)\n\nA [Py]thon 3 addon for [R]aspberry [Pi] that enables [i]nterfacing w/ a variety of low-level board [IC]s.\n\n![PyPI](https://img.shields.io/pypi/v/pyrpiic)\n\n## Compatibility\n\n- Raspberry Pi Models: A, B (revisions 1.0 and 2.0), A+, B+, 2, 3, 3+, 3 A+, 4, Compute Module 3, Zero.\n- Python 3.7+\n\n## Install\n\nInstall the latest from PyPi:\n\n`pip install pyrpiic`\n\n## Modules\n\n### Clocks\n\n- LMK612\n- SI570\n\n### EEPROMs\n\n- Generic\n- M24C02\n\n### I2C-GPIO Expanders\n\n- TCA6416A\n\n### Sensors\n\n- LDC1412\n- LDC1414\n- LDC1612\n- LDC1614\n\n## Examples\n\n### Clocks (Programmable Oscillators)\n\n```python\n\nfrom pyrpio.i2c import I2C\nfrom pyrpiic.clock.lmk61e2 import LMK61E2\n\n# Create and open I2C-3 bus\ni2c3 = I2C('/dev/i2c-3')\ni2c3.open()\n\n# Create clock\nclock = LMK61E2(i2c3, 0x5A)\n\n# Perform various clock operations\nclock.set_frequency(156_250_000)\nfreq, regs = clock.get_frequency()\nclock.regs2freq(regs)\nclock.set_registers(regs)\n\n# Close I2C-3 bus\ni2c3.close()\n```\n\n### I2C-GPIO Expander Example\n\n```python\n\nfrom pyrpio.i2c import I2C\nfrom pyrpiic.ioexpander.tca6416a import TCA6416A\n\n# Create and open I2C-3 bus\ni2c3 = I2C('/dev/i2c-3')\ni2c3.open()\n\n# Create gpio expander\ngpio_exp = TCA6416A(i2c3, 0x21)\n\n# Set GPIO P00 as output pulled high\ngpio_exp.set_gpio_direction('P00', 'OUT')\ngpio_exp.set_gpio_output('P00', high=True)\n\n# Set GPIO P01 as input w/ flipped polarity and read value\ngpio_exp.set_gpio_direction('P01', 'IN')\ngpio_exp.set_gpio_polarity('P01', flipped=True)\ngpio_exp.get_gpio_input('P01')\n\n# Close I2C-3 bus\ni2c3.close()\n```\n",
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Samtec-ASH/pyrpiic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

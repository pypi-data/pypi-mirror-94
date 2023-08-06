# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amortize']

package_data = \
{'': ['*']}

install_requires = \
['numpy-financial>=1.0.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['amortize = amortize.amortize:main']}

setup_kwargs = {
    'name': 'amortize',
    'version': '0.0.9',
    'description': 'Easy-to-use Python Library for Amortization Schedule and Refinance',
    'long_description': '## __amortize__\n### **Easy-to-use Python Library for Amortization Schedule and Refinance**\n\n<p align=left>\n    <a target="_blank" ><img src="https://img.shields.io/pypi/pyversions/amortize?style=flat-square"></a>\n    <a target="_blank" ><img src="https://img.shields.io/pypi/v/amortize"></a>\n    <a href="https://www.codefactor.io/repository/github/ahmetserguns/amortize/overview/main"></a>\n    <a target="_blank" ><img src="https://www.codefactor.io/repository/github/ahmetserguns/amortize/badge/main" alt="CodeFactor" /></a>\n    <a target="_blank" ><img alt="Travis (.com) branch" src="https://img.shields.io/travis/com/ahmetserguns/amortize/main?logo=Travis"></a>\n    <a target="_blank" ><img src="https://img.shields.io/static/v1?label=status&message=stable&color=<Green>"></a>\n    <a target="_blank" ><img src="https://pepy.tech/badge/amortize"></a>\n</p>\n\n## __Inspiration__\n\n The bank with the lowest rate is not always the best choice. APR is important because the interest rate that gets quoted by the lender, isn\'t always the interest rate that you will pay. The APR includes interest rate and fees charged by the lender, and lets you compare mortgage offers. __APR, reflects the true cost of borrowing.__ However, the borrower will see this figure after the approval and signing of the contract!\n\nIf you want something that is straight to the point, this python library can be a good reference.\n\n- You can estimate the mortgage amount that works with your budget.\n- See true cost of borrowing.\n- If you wish, you can see a payment breakdown for every single month of the loan duration.\n- It allows the side-by-side comparison of the existing or refinanced loan.\n- The break-even point shows how long it\'ll take for the savings to outweigh the cost.\n- You can export amortization schedule to excel.\n- It doesn’t show you graphs, pie charts, or amortization charts!\n\n\n## __Installation__\n\nInstall with `pip` or your favorite PyPi package manager.\n\n    pip install amortize\n\n## __Dependencies__\n\n* numpy-financial = 1.0.0\n* tabulate = 0.8.7\n* pandas = "1.2.1\n\n\n## __Usage__\n    \n    Mortgage(\n        loan amount,\n        annual interest rate,\n        loan period in months,\n        fees)\n\n```python\nfrom amortize.calc import Mortgage    \nm=Mortgage(300000,6,12,0)\n```\n\n    >> m.afford()           : Determine how much house you can afford\n    >> m.summary()          : Repayment summary\n    >> m.table()            : Amortization table\n    >> m.refinance()        : Refinance\n    >> m.excel()            : Send amortization table to excel\n   \n\n## __CLI__\n    usage: amortize [-h] -a AMOUNT -i INTEREST -m MONTHS -f FEES [-s] [-t] [-r] [-c] [-e]\n\n    Easy-to-use Python Library for Amortization Schedule and Refinance\n\n    optional arguments:\n    -h, --help            show this help message and exit\n    -s, --summary         Repayment summary\n    -t, --table           Amortization table\n    -r, --refinance       Refinance\n    -c, --afcalc          Affordability calculator\n    -e, --excel           Export to excel\n\n    required arguments:\n    -a AMOUNT, --amount AMOUNT  Loan amount\n    -i INTEREST, --interest INTEREST Annual interest rate\n    -m MONTHS, --months MONTHS Loan period in months\n    -f FEES, --fees FEES  Extra payments\n\n\n\n## __Screenshots__\n   \n    Repayment Summary:\n    amortize -a300000 -i6 -m12 -f6000 -s\n![](https://github.com/ahmetserguns/amortize/raw/main/images/summary.png) \n\n\n    Amortization Table:\n    amortize -a300000 -i6 -m12 -f0 -t\n![](https://github.com/ahmetserguns/amortize/raw/main/images/table.png) \n\n    Refinance:\n    amortize -a300000 -i6 -m12 -f9000 -r\n![](https://github.com/ahmetserguns/amortize/raw/main/images/refinance.png) \n\n\n    Affordability:\n    amortize -a0 -i2.61 -m360 -f0 -c\n![](https://github.com/ahmetserguns/amortize/raw/main/images/affords.png) \n\n\n\n\n## __Thank You__\nThanks for checking out the package.    \n',
    'author': 'ahmetserguns',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.

# This program is free software; you can redistribute it and/or modify it under
# the terms of the MIT license.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the MIT License for more details.


import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
    
with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()

setuptools.setup(
        name        = 'HEBO',
        packages    = setuptools.find_packages(),
        description = 'Heteroscedastic Evolutionary Bayesian Optimisation',
        long_description = long_description,
        install_requires = required,
        long_description_content_type = "text/markdown",
        version = "0.1.0",
        author = "Alexander I. Cowen-Rivers & Huawei Noah's Ark",
        license = "MIT",
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        url = "https://github.com/Yard1/noah-research/tree/master/HEBO",
        )

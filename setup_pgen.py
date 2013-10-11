# import os
from setuptools import setup, find_packages
__VERSION__='0.8.1'

setup(
    name="pyjs_pgen",
    version=__VERSION__,
    packages=['pgen', 'pgen.lib2to3', 'pgen.lib2to3.pgen2', 'pgen.lib2to3.compiler', ], 
    # package_dir = {'pyjs':''},
    zip_safe = False,
    )


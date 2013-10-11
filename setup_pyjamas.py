# import os
from setuptools import setup, find_packages
__VERSION__='0.8.1'

setup(
    name="pyjs_pyjamas",
    version=__VERSION__,
    # py_modules=['__pyjamas__', 'pygwt', 'pyjslib.PyJS', 'pyjslib.pysm',
    #             'dynamic', 'pygwt.browser', 'pyjslib.PyV8'],
    packages=['pyjamaslibrary', 'pyjamaslibrary.pyjamas',
              'pyjamaslibrary.pyjamas.Canvas', 'pyjamaslibrary.pyjamas.builder',
              'pyjamaslibrary.pyjamas.chart', 'pyjamaslibrary.pyjamas.django',
              'pyjamaslibrary.pyjamas.dnd', 'pyjamaslibrary.pyjamas.feed',
              'pyjamaslibrary.pyjamas.gears', 'pyjamaslibrary.pyjamas.gears.database',
              'pyjamaslibrary.pyjamas.gears.localserver', 'pyjamaslibrary.pyjamas.gears.workerpool',
              'pyjamaslibrary.pyjamas.gmaps', 'pyjamaslibrary.pyjamas.graphael', 
              'pyjamaslibrary.pyjamas.logging', 'pyjamaslibrary.pyjamas.media', 
              'pyjamaslibrary.pyjamas.raphael', 'pyjamaslibrary.pyjamas.selection', 
              'pyjamaslibrary.pyjamas.ui', 'pyjamaslibrary.pyjamas.ui.public',
              ],
    package_dir = {'pyjamaslibrary':'library'},
    package_data={'pyjamaslibrary': ['*.js',],
                  'pyjamaslibrary/pyjamas/ui': ['public/*.html', 'public/css.d/*.css', 
                                                'public/images/*.png', 'public//images/*.gif'],
                  },
#    data_files=[('pyjamaslibrary', ['library/*.js',]),
#                ('pyjamaslibrary/pyjamas/ui/public',        ['library/pyjamas/ui/public/*.html',]),
#                ('pyjamaslibrary/pyjamas/ui/public/css.d',  ['library/pyjamas/ui/public/css.d/*.css',]),
#                ('pyjamaslibrary/pyjamas/ui/public/images', ['library/pyjamas/ui/public//images/*.png',
#                                                              'library/pyjamas/ui/public//images/*.gif',]),
#                ],
#    data_files=[('pyjamaslibrary', ['library/dynamicajax.js',]),],
    zip_safe = False,
    # include_package_data = False,
    # install_requires = [],
    # extras_require = dict(test=['zope.testing']),
    # entry_points = {'console_scripts':[
    #     'build=pyjs.browser:build_script',
    #     'translate=pyjs.translator:main',
    #     'smbuild=pyjs.sm:build_script',
    # ]},
    )


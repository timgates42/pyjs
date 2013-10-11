# import os
from setuptools import setup, find_packages
__VERSION__='0.8.1'

setup(
    name="pyjs_compiler",
    version=__VERSION__,
    packages=['pyjs', 'pyjs.builtin', 'pyjs.lib', 'pyjs.lib.os', 'pyjs.lib.test',
              'pyjs.lib_trans', 'pyjs.lib_trans.pycompiler', 'pyjs.lib_trans.pyparser', 'pyjs.lib_trans.test', 
              'pyjs.boilerplate'],
    package_dir = {'pyjs':'pyjs/src/pyjs'},
    package_data={'pyjs': ['boilerplate/*.html', 'boilerplate/pyjampiler_wrapper.js.tmpl', 
                           'builtin/__builtin__.py.in', 'builtin/public/*.js',],
                  },
#    data_files=[('pyjs/boilerplate', ['pyjs/src/pyjs/boilerplate/all.cache.html', 
#                                      'pyjs/src/pyjs/boilerplate/home.nocache.html', 
#                                      'pyjs/src/pyjs/boilerplate/pyjampiler_wrapper.js.tmpl']),
#                ('pyjs/builtin/public', ['pyjs/src/pyjs/builtin/public/_pyjs.js',
#                                         'pyjs/src/pyjs/builtin/public/bootstrap.js',
#                                         'pyjs/src/pyjs/builtin/public/bootstrap_progress.js']),],
    zip_safe = False,
    # include_package_data = False,
    install_requires = ['pyjs_pgen'],
    # extras_require = dict(test=['zope.testing']),
    entry_points = {'console_scripts':[
        # 'build=pyjs.browser:build_script',
        # 'translate=pyjs.translator:main',
        # 'smbuild=pyjs.sm:build_script',
        'pyjampiler=pyjs.pyjampiler:Builder',
        'pyjscompile=pyjs.translator:main',
        'pyjsbuild=pyjs.browser:build_script',
    ]},
    )


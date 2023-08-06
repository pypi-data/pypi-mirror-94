
# necessary to push to PyPI
# cf. http://peterdowns.com/posts/first-time-with-pypi.html
# cf. https://tom-christie.github.io/articles/pypi/
# cf. https://pythonhosted.org/setuptools/setuptools.html

# commands:
# python setup.py sdist upload -r testpypi
# python setup.py sdist upload -r pypi


from distutils.util import convert_path
from setuptools import setup, find_packages


##################################################
module = 'ipypivot'
##################################################

# get version from __meta__
meta_ns = {}
path = convert_path(module + '/__meta__.py')
with open(path) as meta_file:
    exec(meta_file.read(), meta_ns)


# read requirements.txt
with open('requirements.txt', 'r') as f:
    content = f.read()
li_req = content.split('\n')
install_requires = [e.strip() for e in li_req if len(e)]


name = module
name_url = name.replace('_', '-')

packages = [module]
version = meta_ns['__version__']
description = 'Jupyter widget (or ipywidget) wrapping the very convenient pivotTable.js library'
long_description = 'See github repo README'
author = 'PierreMarion23'
author_email = 'pierre23.marion@free.fr'
# github template
url = 'https://github.com/{}/{}'.format(author,
                                        name_url)
download_url = 'https://github.com/{}/{}/tarball/{}'.format(author,
                                                            name_url,
                                                            version)
keywords = ['jupyter-widget',
            'javascript',
            'pivottable',
            ]
license = 'MIT'
classifiers = ['Development Status :: 4 - Beta',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6'
               ]
include_package_data = True
data_files = [
    ('share/jupyter/nbextensions/ipypivot', [
        'ipypivot/static/extension.js',
        'ipypivot/static/index.js',
        'ipypivot/static/index.js.map',
    ]),
    ('etc/jupyter/nbconfig/notebook.d', [
        'enable_ipypivot.json'
    ])

]
install_requires = install_requires
zip_safe = False


# ref https://packaging.python.org/tutorials/distributing-packages/
setup(
    name=name,
    version=version,
    packages=packages,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    url=url,
    download_url=download_url,
    keywords=keywords,
    license=license,
    classifiers=classifiers,
    include_package_data=include_package_data,
    data_files=data_files,
    install_requires=install_requires,
    zip_safe=zip_safe,
)

from setuptools import setup, find_packages

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = '0.1.3'

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

ext_modules = [
    Pybind11Extension(
        "mt2",
        ["src/main.cpp", "src/lester_mt2_bisect_v4.h"],
        # Example: passing in the version to the compiled code
        define_macros=[('VERSION_INFO', __version__)],
    ),
]


setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', ]

setup(
    author="Thomas Gillam",
    author_email='tpgillam@googlemail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Stransverse mass computation as a numpy ufunc.",
    install_requires=["numpy"],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mt2',
    name='mt2',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tpgillam/mt2',
    version=__version__,
    ext_modules=ext_modules,
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)

from setuptools import setup


setup(
    name='starlette-cli',
    versioning='dev',
    setup_requires='setupmeta',
    modules=['starlette_cli'],
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/starlette-cli',
    include_package_data=True,
    license='MIT',
    keywords='starlette cli',
    python_requires='>=3',
    install_requires=['starlette-apps>=0.1.6'],
)

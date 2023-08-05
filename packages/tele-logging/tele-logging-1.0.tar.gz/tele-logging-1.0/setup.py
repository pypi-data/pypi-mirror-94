from setuptools import setup, find_packages


setup(
    name = "tele-logging",
    version = "1.0",
    url='https://github.com/kiri11-mi1',
    author='kiri11-mi1',
    author_email='kirill.mil.0310@mail.ru',
    packages = find_packages(),
    long_description = 'Long description',
    install_requires=[
        'requests==2.25.1',
    ],
    zip_safe=False,
)
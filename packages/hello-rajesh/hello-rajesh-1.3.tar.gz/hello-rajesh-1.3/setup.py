import setuptools

install_requires = []

setuptools.setup(
    name="hello-rajesh",
    version="1.3",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'hello = hello.main:main',
        ],
    },
)

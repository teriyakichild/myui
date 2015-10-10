from sys import path

from setuptools import setup

path.insert(0, '.')

NAME = "myui"

if __name__ == "__main__":

    setup(
        name=NAME,
        version="0.2.1",
        author="Tony Rogers",
        author_email="tony.rogers@rackspace.com",
        url="https://github.com/teriyakichild/myui",
        license='internal use',
        packages=[NAME],
        package_dir={NAME: NAME},
        package_data={
                  'myui': ['myui/*'],
                     },
        include_package_data=True,
        description="MyUI - Easily customizable Tornado UI",

        install_requires=['tornado>=4.0'],
        entry_points={
            'console_scripts': ['myui = myui:main',
                                'myui-create-tables = myui:create_tables'],
        }
    )

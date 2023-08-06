from setuptools import find_packages, setup

setup(
    name='date-range-cli',
    version='0.0.4',
    description='A cli too that generates a range of dates or timestamps',
    author='Mark Jackson',
    url="https://github.com/captainrandom/daterange",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',  # TODO: need to come back and change this at some point
        'Topic :: Software Development :: Build Tools',  # TODO: need to come back and change this at some point
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # TODO: need to come back and change this at some point
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['daterange=date_range.daterange:main']
    },
    install_requires=['pendulum==2.0.5'],
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)

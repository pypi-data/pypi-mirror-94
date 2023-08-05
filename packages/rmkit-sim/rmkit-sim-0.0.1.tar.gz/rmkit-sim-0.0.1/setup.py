from setuptools import setup
import os

setup(
    name='rmkit-sim',
    version='0.0.1',
    packages=['remarkable_sim'],
    author="rmkit-dev",
    author_email="",
    description="fork of remarkable-sim",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="GPLv3",
    keywords="remarkable evdev sim simulator simulation tablet",
    url="https://github.com/rmkit-dev/remarkable_sim",
    entry_points={
        'console_scripts': [
            'resim = remarkable_sim.sim:main',
            'remarkable_sim = remarkable_sim.sim:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "pillow"
    ]
)

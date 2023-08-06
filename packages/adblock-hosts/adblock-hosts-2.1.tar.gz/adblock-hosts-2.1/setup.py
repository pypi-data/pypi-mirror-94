from setuptools import setup

setup(
    name='adblock-hosts',
    version='2.1',
    packages=['adblock'],
    url='',
    license='MIT',
    author="Keane O'Kelley",
    author_email='dev@keane.space',
    description='Automatically fetch and merge adblock hosts.',
    install_requires=[
        'requests-futures',
        'PyYAML',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'adblock=adblock:main',
        ]
    },
    include_package_data=True,
)

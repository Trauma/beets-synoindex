from setuptools import setup

setup(
    name='beets-synoindex',
    version='0.2-dev',
    description='beets plugin to manage multiple files',
    long_description=open('README.md').read(),
    author='neomilium',
    author_email='neomilium@no.where',
    url='https://github.com/Trauma/beets-synoindex',
    license='MIT',
    platforms='ALL',
    packages=['beetsplug'],
    install_requires=[
        'beets>=1.3.13',
        'futures',
    ],

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Players :: MP3',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)

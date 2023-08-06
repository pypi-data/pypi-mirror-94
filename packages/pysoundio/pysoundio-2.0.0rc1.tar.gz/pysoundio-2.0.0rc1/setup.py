"""
PySoundIo

A robust, cross-platform solution for real-time audio.
"""
from setuptools import setup

__version__ = '2.0.0rc1'

setup(
    name='pysoundio',
    version=__version__,
    description='Python wrapper for libsoundio',
    long_description='A robust, cross-platform solution for real-time audio',
    license='MIT',
    author='Joe Todd',
    author_email='joextodd@gmail.com',
    url='http://pysoundio.readthedocs.io/en/latest/',
    download_url='https://github.com/joextodd/pysoundio/archive/' + __version__ + '.tar.gz',
    include_package_data=True,
    packages=['pysoundio', 'examples'],
    setup_requires=['cffi>=1.4.0'],
    install_requires=['cffi>=1.4.0'],
    python_requires='>=3.6',
    cffi_modules=['pysoundio/builder/soundio.py:ffibuilder'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'pysio_devices = examples.devices:main',
            'pysio_play = examples.play:main',
            'pysio_record = examples.record:main',
            'pysio_sine = examples.sine:main',
        ],
    },
    keywords=['audio', 'sound', 'stream'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Multimedia :: Sound/Audio',
    ],
)

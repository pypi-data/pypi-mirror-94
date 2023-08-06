from setuptools import setup

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='pianoviewer',
    version='0.0.1',
    description='Displays key presses from MIDI.',
    long_description=LONG_DESCRIPTION,
    url='https://git.brokenmouse.studio/ever/pianoviewer',
    author='EV3R4',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio :: MIDI',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',

        'Operating System :: OS Independent',

        'Natural Language :: English',
    ],
    keywords=['midi', 'piano'],
    packages=['pianoviewer'],
    install_requires=['mido', 'pygame', 'python-rtmidi'],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'pianoviewer=pianoviewer.__main__:main',
        ],
    },
)

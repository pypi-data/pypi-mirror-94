from setuptools import setup

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='nato-cli',
    version='0.0.1',
    url='https://github.com/seaty6/nato-cli',
    author='Sampath Eaty',
    author_email='s.eaty6@gmail.com',
    description='Allows quick translation of a string to its letters in NATO form.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['nato'],
    entry_points={'console_scripts': ['nato = nato:main']},
    package_dir={'': 'src'},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop'
    ],
)
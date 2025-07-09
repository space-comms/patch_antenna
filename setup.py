from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='patch-antenna-designer',
    version='1.0.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Advanced patch antenna design with material database and automated Gerber generation',
    url='https://github.com/space-comms/patch_antenna',
    author='Al-Musbahi',
    author_email='musbahi.git@gmail.com',
    maintainer='Leeds SpaceComms',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'scipy>=1.9.0',
        'gerber-writer>=0.3.4'
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'flake8'],
        'docs': ['sphinx', 'sphinx-rtd-theme']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='antenna design patch microstrip rf gerber pcb',
    project_urls={
        'Bug Reports': 'https://github.com/space-comms/patch_antenna/issues',
        'Source': 'https://github.com/space-comms/patch_antenna',
        'Documentation': 'https://github.com/space-comms/patch_antenna#readme',
    }
)

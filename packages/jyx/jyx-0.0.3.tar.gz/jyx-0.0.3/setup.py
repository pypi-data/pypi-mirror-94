from setuptools import setup
import jyx
from os.path import join

f = open(join('jyx', 'readme.md'), mode='r', encoding='utf8')
long_desc = f.read()
f.close()

setup(
    # Metadata
    name='jyx',
    version=jyx.__version__,

    license="MIT",

    author='Damien Gouteux',
    author_email='damien.gouteux@gmail.com',
    url="https://xitog.github.io/dgx/index.html",
    maintainer='Damien Gouteux',
    maintainer_email='damien.gouteux@gmail.com',
    
    description='A simple text editor',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Text Editors',
    ],
    keywords=['jyx', 'editor', 'programming language', 'script', 'text'],
    
    packages=['jyx'],  #same as name
    python_requires='>=3.5',
    #install_requires = ['xxx'],
)

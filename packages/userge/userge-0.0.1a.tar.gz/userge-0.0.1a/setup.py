from distutils.core import setup

from userge import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='userge',
    packages=['userge'],
    version=__version__,
    description='userbot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPLv3',
    author='rking32',
    author_email='rking32@usergeteam.org',
    url='https://github.com/rking32/userge',
    download_url='https://github.com/rking32/userge/releases/latest',
    keywords=['pyrogram', 'userbot', 'telegram'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)

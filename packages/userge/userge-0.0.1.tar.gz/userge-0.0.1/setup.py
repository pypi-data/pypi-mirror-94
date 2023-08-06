from distutils.core import setup


setup(
  name = 'userge',
  packages = ['userge'],
  version = '0.0.1',
  license='GPLv3',
  description = 'userbot',
  author = 'rking32',
  author_email = 'rking32@usergeteam.org',
  url = 'https://github.com/rking32/userge',
  download_url = 'https://github.com/rking32/userge/releases/latest',
  keywords = ['pyrogram', 'userbot', 'telegram'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

from distutils.core import setup
setup(
  name = 'talkmore',
  packages = ['talkmore'],
  version = '0.1',
  license='MIT',
  description = 'Send sms, add and read contacts with through the talkmore web interface',
  author = 'Ola Kanten',
  author_email = 'okgit@protonmail.com',
  url = 'https://github.com/okanten/talkmore',
  download_url = 'https://github.com/okanten/talkmore/archive/v_01.tar.gz',
  keywords = ['talkmore', 'talkmore sms', 'talkmore-sms', 'sms', 'norge'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)

from distutils.core import setup
setup(
  name = 'pyCoach',
  packages = ['pyCoach'],
  version = '0.1',
  license='MIT',
  description = 'With pyCoach start coding with relevant solutions from Google to the errors, right on spot.',
  author = 'Muhammad Haider Zaidi',
  author_email = 'mhaiderzaidi21@gmail.com',
  url = 'https://github.com/MuhammadHaiderZaidi/pyCoach',
  download_url = 'https://github.com/MuhammadHaiderZaidi/pyCoach/archive/0.1.tar.gzz',
  keywords = ['Solution', 'Error', 'Stackoverflow'],
  install_requires=[ 
          'google',
          'beautifulsoup4',
          'requests',
          'IPython'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
#! /usr/bin/env python
#

DESCRIPTION = "htmcatalog: Hierarchical Triangular Mesh Catalogs"
LONG_DESCRIPTION = """ Tool to query existing catalogs stored in Hierarchical Triangular Mesh format (htm) """

DISTNAME = 'htmcatalog'
AUTHOR = 'Mickael Rigault'
MAINTAINER = 'Mickael Rigault' 
MAINTAINER_EMAIL = 'm.rigault@ipnl.in2p3.fr'
URL = 'https://github.com/MickaelRigault/htmcatalog/'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/MickaelRigault/htmcatalog/tarball/0.1'
VERSION = '0.1.1'


from setuptools import setup, find_packages


def check_dependencies():
    install_requires = []

    # Just make sure dependencies exist, I haven't rigorously
    # tested what the minimal versions that will work are
    # (help on that would be awesome)
    try:
        import HMpTy
    except ImportError:
        install_requires.append('HMpTy')
        
    return install_requires

if __name__ == "__main__":

    # Dependencies
    install_requires = check_dependencies()
    # Internal Packages (following __init__.py)
    packages = find_packages()

    setup(name=DISTNAME,
          author=AUTHOR,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=install_requires,
#          scripts=[],
          packages=packages,
          include_package_data=True,
#          package_data={'pysedm': ['data/*.*']},
          classifiers=[
              'Intended Audience :: Science/Research',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.5',              
              'License :: OSI Approved :: BSD License',
              'Topic :: Scientific/Engineering :: Astronomy',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS'],
          )

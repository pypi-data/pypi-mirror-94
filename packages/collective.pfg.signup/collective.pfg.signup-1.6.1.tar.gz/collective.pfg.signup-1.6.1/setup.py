from setuptools import setup, find_packages

version = '1.6.1'
short_description = "A PloneFormGen adapter that saves signup form"
long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective.pfg.signup',
      version=version,
      description=short_description,
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        ],
      keywords='plone ploneformgen form signup users',
      author='Pretaweb',
      author_email='mailto:support@pretaweb.com',
      url='http://github.com/collective/collective.pfg.signup',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.pfg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'Products.PloneFormGen',
          'plone.api >= 1.3.0', # for api.user.has_permission
          'collective.monkeypatcher',
      ],
      extras_require={
        'test': ['plone.app.testing',
                 'plone.app.robotframework',
                 'plone.api',
                 'Products.ATContentTypes'],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

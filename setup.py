from distutils.core import setup

setup(
    name='PyInq',
    version='0.1.1',
    author='Austin Noto-Moniz',
    author_email='metalnut4@netscape.net',
    url='http://pypi.python.org/pypi/PyInq',
    packages=['pyinq','pyinq.asserts','pyinq.tags','pyinq.printers','pyinq.printers.html','pyinq.printers.cli','pyinq.printers.cli.console','pyinq.printers.cli.bash'],
    description='Python unit test framework, an alternative to unittest.',
    long_description=open('README').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Testing'
   ]
)

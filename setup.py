from setuptools import setup

setup(
    name='PyInq',
    version='0.2.1',
    author='Austin Noto-Moniz',
    author_email='pyinq.test@gmail.com',
    url='http://auzzy.github.io/pyinq/',
    packages=['pyinq', 'pyinq.asserts', 'pyinq.tags', 'pyinq.printers', 'pyinq.printers.html', 'pyinq.printers.cli', 'pyinq.printers.cli.console', 'pyinq.printers.cli.bash', 'pyinq.parsers'],
    description='Python unit test framework, an alternative to unittest.',
    long_description=open('README.txt').read(),
    license='ISCL',
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

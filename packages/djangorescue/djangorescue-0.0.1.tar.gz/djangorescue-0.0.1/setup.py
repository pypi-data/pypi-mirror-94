import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='djangorescue',
    version='0.0.1',
    author='Iakov Gnusin',
    author_email='y.gnusin@gmail.com',
    description='Package to let you serve static and media files via Django pipeline with DEBUG = False.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ignusin/djangorescue',
    packages=setuptools.find_packages(),
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

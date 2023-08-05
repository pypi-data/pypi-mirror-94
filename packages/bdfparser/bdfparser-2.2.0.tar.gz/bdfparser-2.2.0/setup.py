import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bdfparser',
    author='Tom Chen',
    author_email='tomchen.org@gmail.com',
    description='BDF (Glyph Bitmap Distribution Format) Bitmap Font File Parser in Python',
    keywords='bdf, bitmap, font, parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tomchen/bdfparser',
    project_urls={
        'Documentation': 'https://github.com/tomchen/bdfparser',
        'Bug Reports':
        'https://github.com/tomchen/bdfparser/issues',
        'Source Code': 'https://github.com/tomchen/bdfparser',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    extras_require={
        'dev': ['check-manifest'],
    },
)

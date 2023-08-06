from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='msrdm',
    version='0.0.2',
    description='Multi-Stage Robust Decision Making',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Shunichiro Nomura',
    author_email='nomura@space.t.u-tokyo.ac.jp',
    install_requires=[
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    url='https://github.com/shunichironomura/msrdm',
    download_url='https://github.com/shunichironomura/msrdm/archive/v0.0.2.tar.gz',
    license='BSD 3-Clause',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
    zip_safe=False,
)
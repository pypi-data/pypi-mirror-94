from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='chun_codes',
    version='0.8.0',
    packages=['chun_codes'],
    url='https://github.com/astrochun/chun_codes',
    license='MIT',
    author='Chun Ly',
    author_email='astro.chun@gmail.com',
    description='Set of Python 2.7 and 3.xx codes used in astrochun\'s codes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy'],
    extras_require={
        ':python_version == "2.7"': ['pdfmerge', 'matplotlib==2.2.5', 'astropy==2.0.16'],
        ':python_version >= "3.0"': ['matplotlib', 'astropy']
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)

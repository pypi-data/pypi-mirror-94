from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pylogtools',
    version='1.0.0',
    description='Useful logging tools',
    long_description_content_type="text/markdown",
    long_description=f"{README}\n\n{HISTORY}",
    license='MIT',
    packages=find_packages(),
    author='kkoyias',
    author_email='sdi1500071@di.uoa.gr',
    keywords=['Message', 'Logging', 'Console'],
    url='https://pypi.org/project/pylogtools/',
    download_url='https://pypi.org/project/pylogtools/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
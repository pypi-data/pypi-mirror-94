from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='LanguageIdentifier',
    version='1.0.0',
    description='Language identifier based on an LSTM model',
    long_description_content_type="text/markdown",
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    # author='Mads, Søren, Manuel',
    # author_email='mabeto5p@live.dk',
    keywords=['Lid', 'LSTM', 'Language identifier',  'Language'],
    # url='https://github.com/ncthuc/elastictools',
    download_url='https://pypi.org/project/LanguageIdentifier/'
)

install_requires = [
    'torch'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)
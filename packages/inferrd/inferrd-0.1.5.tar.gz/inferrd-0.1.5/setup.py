from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='inferrd',
    version='0.1.5',
    description='inferrd.com Package',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='inferrd.com',
    author_email='contact@inferrd.com',
    keywords=['Inferrd', 'Hosting', 'TensorFlow', 'Deploy'],
    url='https://inferrd.com',
    download_url='https://pypi.org/project/inferrd/'
)

install_requires = [
    'joblib',
    'easysettings',
    'tensorflow',
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
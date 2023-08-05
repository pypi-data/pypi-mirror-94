import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call

class PostInstallCommand(install):
    def run(self):
        check_call([sys.executable, '-m', 'natex', 'setup', 'en'])
        print('By default, NatEx only installs the English models for stanza.\nUse the command `python -m natex setup <language_code>` to download a model for another language. Visit https://github.com/secretsauceai/natex-py for a full list of supported language codes.')
        install.run(self)

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = "natex",
	version = "1.0.8",
	author = "Dan Borufka",
	author_email = "danborufka@gmail.com",
	description = "Regular Expressions turbo-charged with notations for part-of-speech and dependency tree tags",
	license = "MIT",
	keywords = "regex regular expression nlp pos dep",
	url = "https://github.com/polygoat/natex-py",
	packages=find_packages(),
	cmdclass={
        'install': PostInstallCommand
    },
	install_requires=[
        "pydash",
		"stanza"
    ],
    include_package_data=True,
	long_description=read('README.md'),
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3",
		"Development Status :: 3 - Alpha",
		"Topic :: Utilities",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires='>=3.6'
)

print('done.')
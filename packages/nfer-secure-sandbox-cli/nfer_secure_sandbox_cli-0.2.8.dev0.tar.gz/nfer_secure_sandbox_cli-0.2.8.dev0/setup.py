from setuptools import setup, find_packages
import os
import codecs
os.system("export SLUGIFY_USES_TEXT_UNIDECODE=yes")

here = os.path.abspath(os.path.dirname(__file__))
long_description = ""
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()

setup(
  name = 'nfer_secure_sandbox_cli',
  packages=find_packages(),
  version = 'v0.2.8-dev',
  #python_requires=">=3.4.0",
  license='MIT',
  description = 'Nfer Secure Sandbox CLI - helps client run algorithm securely over sandboxes',
  long_description=long_description,
  long_description_content_type="text/markdown",
  scripts=["nfer_secure_sandbox_cli/cpscli.sh","nfer_secure_sandbox_cli/nfer-sandbox-cli","nfer_secure_sandbox_cli/scli.sh"],
  author = 'sumitkhanna@nference.net',
  author_email = 'sumitkhanna@nference.net',
  url = 'https://github.com/lumenbiomics/nfer-secure-sandbox-cli',
  download_url = 'https://github.com/lumenbiomics/nfer-secure-sandbox-cli/archive/v0.2.8-dev.tar.gz',
  include_package_data=True, 
  keywords = ['Nference', 'Sandbox', 'Confidential-Computing'],
  install_requires=[
          'requests==2.25.0',
          'certifi==2020.11.8',
          'chardet==3.0.4',
          'cryptography==3.2.1',
          'entrypoints==0.3',
          'Flask==1.1.2',
          'Flask-Cors==3.0.9',
          'GitPython==3.1.11',
          'gitdb==4.0.5',
          'healthcheck==1.3.3',
          'in-place==0.4.0',
          'Jinja2==2.11.2',
          'jsonschema==3.2.0',
          'keyring==21.5.0',
          'markdown2==2.3.10',
          'md-to-html==0.7.3',
          'pygrok==1.0.0',
          'python-dateutil==2.8.1',
          'PyYAML==5.3.1',
          'regex==2020.11.13',
          'six==1.15.0',
          'urllib3==1.25.11',
          'Werkzeug==1.0.1',
          'pyOpenSSL==19.1.0',
          'pycryptodome==3.9.9',
          'Flask==1.1.2',
          'Flask-Cors==3.0.9',
          'healthcheck==1.3.3',
          'py-healthcheck==1.10.1',
          'docker==4.4.1'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)


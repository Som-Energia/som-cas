from setuptools import find_packages, setup

from som_cas import VERSION

setup(
    name="som_cas",
    version=VERSION,
    description="Cas authentication system for Som Energia",
    author="Som Energia SCCL",
    author_email="info@somenergia.coop",
    url='https://github.com/Som-Energia/pool_transport',
    long_description_content_type='text/markdown',
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    packages=find_packages(exclude=['*[tT]est*']),
)

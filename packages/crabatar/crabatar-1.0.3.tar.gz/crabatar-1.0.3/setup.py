from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='crabatar',
    version='1.0.3',
    description='Generate crab-themed avatars procedurally from usernames.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jake Ledoux',
    author_email='contactjakeledoux@gmail.com',
    url='https://github.com/jakeledoux/crabatar',
    license='GNU General Public License v2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'gizeh',
        'Pillow'
    ],
    include_package_data=True
)

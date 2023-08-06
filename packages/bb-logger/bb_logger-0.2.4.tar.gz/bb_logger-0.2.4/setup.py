from setuptools import setup
with open('README.md') as f:
    long_description = f.read()

# https://github.com/bast/pypi-howto
setup(
    name='bb_logger',
    packages=['bb_logger'],
    version='0.2.4',
    # Chose a license from here:
    # https://help.github.com/articles/licensing-a-repository
    license='MIT',
    description='setup logger bb',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='le du',
    author_email='dulx96@gmail.com',
    # Provide either the link to your github or to your website
    url='https://github.com/dulx96/bb_logger.git',
    keywords=['BB', 'LOGGER', 'LOGGING'],
    install_requires=[],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)

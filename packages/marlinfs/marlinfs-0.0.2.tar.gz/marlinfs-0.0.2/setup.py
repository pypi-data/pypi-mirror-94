from setuptools import setup, find_packages

requires = ['grpcio-tools==1.33.2',
            'grpcio==1.33.2',
            'googleapis-common-protos==1.52.0',
            'pyarrow==1.0.1',
            'fsspec==0.8.4',
            'pandas==1.1.3',
            's3fs==0.5.1',
            'pytest==6.1.1',
            'mock==4.0.2',
            'pyrebase==3.0.27',
            'numpy==1.19.5']
setup(
    name='marlinfs',
    version='0.0.2',
    author='Tern',
    author_email='support@tern.ai',
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/marlin-fs/marlin-python-client',
    license='MIT',
    description='Python Client for Marlin Feature Store',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Tracker": "https://github.com/marlin-fs/marlin-python-client/issues",
        "Documentation": "https://docs.tern.ai/",
        "Source Code": "https://github.com/marlin-fs/marlin-python-client",
    },
    install_requires=requires
)

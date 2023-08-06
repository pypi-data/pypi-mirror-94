import setuptools
import os

own_dir = os.path.abspath(os.path.dirname(__file__))


def requirements():
    with open(os.path.join(own_dir, 'requirements.txt')) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            yield line


def modules():
    return [
    ]


def version():
    with open(os.path.join(own_dir, 'VERSION')) as f:
        return f.read().strip()


setuptools.setup(
    name='whitesource_api_extension',
    version=version(),
    description='backend for whitesource-api-extension',
    python_requires='>=3.8.*',
    py_modules=modules(),
    packages=['whitesource_backend'],
    package_data={
        'ci':['version'],
    },
    entry_points={
    },
)

import setuptools

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

setuptools.setup(
    name="CASlibrary",
    version="0.1.0",
    author="FF Woernitz",
    author_email="technik@ff-woernitz.de",
    description="The universal lib used in the CAS system",
    url="https://github.com/FF-Woernitz/CAS_lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=parse_requirements('requirements.txt'),
    python_requires='>=3.6',
)
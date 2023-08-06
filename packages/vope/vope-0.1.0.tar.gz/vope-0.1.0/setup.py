from setuptools import find_packages, setup
setup(
    name="vope",
    packages=find_packages(include=["vope"]),
    version="0.1.0",
    description="Improving laparoscopy image visualization.",
    author="Sharif Natheir",
    author_email = 'sharif.natheir@mail.mcgill.ca',
    url = 'https://github.com/snatheir',
    license="MIT",
    keywords = ['LAPAROSCOPY', 'VISION', 'CLEAR'],
    install_requires=["numpy"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"],
    test_suite="tests",
)
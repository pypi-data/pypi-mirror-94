from setuptools import find_packages, setup

setup(
    name='SModelWrap',
    py_modules=['SModelWrap'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version='1.0.0',
    description='Quick wrapper to get predictions to work with AWS Sagemaker',
    author='Stephen Mott',
    author_email="stephen@mott.email",
    python_requires=">=3.6",
    install_requires=["pandas", "numpy"],
    url="https://github.com/SrzStephen/ModelWrap",
    classifiers=["Development Status :: 3 - Alpha"],
    licence="WTFPL"
)

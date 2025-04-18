from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='suryansh verma',
    author_email='suryanshv.ug23.ee@nitp.ac.in',
    install_requires=["langchain","python-dotenv","langchain_google_genai","streamlit","PyPdf2"],
    packages=find_packages()
)
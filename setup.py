from setuptools import setup, find_packages

setup(
    name="financial_analysis_system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "requests>=2.28.1",
        "python-dotenv>=1.0.0",
        "pandas>=1.5.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
        "numpy>=1.23.0",
        "plotly>=5.10.0",
        "beautifulsoup4>=4.12.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.1.0",
    ],
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="reactor-agent",
    version="0.1.0",
    author="Jacques Lemieux",
    author_email="jacques.lemieux@gmail.com",
    description="A ReAct (Reasoning + Acting) agent framework for AI-powered reasoning and tool execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jalemieux/reactor-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.98.0",
        "tavily-python>=0.7.10",
        "pydantic>=2.11.7",
        "httpx>=0.28.1",
        "requests>=2.32.4",
        ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=7.3.0",
            "build>=1.2.2",
        ],
    },
    keywords="ai, agent, reasoning, react, tools, openai, tavily",
    project_urls={
        "Bug Reports": "https://github.com/jalemieux/reactor-agent/issues",
        "Source": "https://github.com/jalemieux/reactor-agent",
    },
) 
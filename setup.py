from setuptools import find_packages, setup

from io import open

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="VocaroLyrics",
    version="1.0.5",
    description="보카로 가사 위키에서 가사를 검색해주는 라이브러리",
    author="노토리",
    install_requires=requirements,
    packages=find_packages(),
    long_description="[보카로 가사 위키](http://vocaro.wikidot.com/)",
    url="https://github.com/NO-TORY/VocaroLyricsSearcher",
    long_description_content_type="text/markdown",
    include_package_data=True
)

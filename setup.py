try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name="VocaroLyrics",
    version="1.0.3",
    description="보카로 가사 위키에서 가사를 검색해주는 라이브러리",
    author="노토리",
    install_requires=["requests", "regex", "future-annotations; python_version < 3"],
    py_modules=["VocaroLyrics"],
    long_description="[보카로 가사 위키](http://vocaro.wikidot.com/)",
    url="https://github.com/NO-TORY/VocaroLyricsSearcher",
    long_description_content_type="text/markdown",
    include_package_data=True
)

class Error(Exception):
    def __init__(self, name: str, *reason: object):
        """Base class for rising errors."""
        super().__init__(name + ": " + str(*reason))

class SongNotFound(Error):
    def __init__(self):
        super().__init__(self.__class__.__name__, "노래를 찾을 수 없습니다.")

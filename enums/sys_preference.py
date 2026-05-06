from enum import Enum


class SysPreference(Enum):

    VIDEO_SHORT = (1, "影片短")
    QUESTION_MORE = (2, "題目多")
    TEACHER_GOOD = (3, "老師講解清楚")

    def __init__(self, code: int, label: str):
        self.code = code
        self.label = label

    def __str__(self):
        return self.label

    @classmethod
    def from_code(cls, code: int):
        for item in cls:
            if item.code == code:
                return item

        raise ValueError(f"無效的 preference code: {code}")

    @classmethod
    def get_label(cls, code: int):
        return cls.from_code(code).label
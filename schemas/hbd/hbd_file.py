from typing import List

from pydantic import BaseModel

from models import UserHappyBirthday


class HbdFileBarChart(BaseModel):
    month: str
    count: int
    bar_str: str


class HbdFile(BaseModel):
    hbds: List
    bar_chart: List[HbdFileBarChart]

    @staticmethod
    def gen_bar_chart(hbd_list: List[UserHappyBirthday]):
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        result = []
        obj = {}
        for i in range(0, len(months)):
            obj[months[i]] = len(
                list(
                    filter(
                        lambda hbd: int(hbd.person_birthdate.strftime("%m")) - 1 == i,
                        hbd_list,
                    )
                )
            )
        max_bar = max(obj.values())
        bar_nan = "⚪"
        bar_full = "⚫"
        for key, value in obj.items():
            perc = int(round(value / max_bar, 1) * 10)
            bar_chart = HbdFileBarChart(
                month=key, count=value, bar_str=f"{bar_full*perc}{bar_nan*(10-perc)}"
            )
            result.append(bar_chart)
        return result

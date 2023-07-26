import datetime
from torch_snippets.loader import flatten, Debug
from itertools import combinations_with_replacement
from torch_snippets import io

x = flatten(
    [
        [
            "%d{s1}%m{s2}%Y".format(s1=s1, s2=s2),
            "%Y{s1}%m{s2}%d".format(s1=s1, s2=s2),
            "%d{s1}%b{s2}%Y".format(s1=s1, s2=s2),
            "%b{s1}%d{s2}%Y".format(s1=s1, s2=s2),
            "%m{s1}%d{s2}%Y".format(s1=s1, s2=s2),
        ]
        for s1, s2 in combinations_with_replacement(".-/ ", r=2)
    ]
)
x = x + [_x.replace("%b", "%B") for _x in x]
x = x + [_x.replace("%Y", "%y") for _x in x]
x = x + [_x.replace("%d", "%-d") for _x in x]
x = x + [_x.replace("%m", "%-m") for _x in x]

ALL_DATE_FORMATS = x + ["%Y-%m-%d %H:%M:%S"]


@io
def make_uniform_date_format(value, target_fmt="%d.%m.%Y", mode="raise"):
    available_modes = ["raise", "return", "default"]
    if isinstance(value, datetime.datetime):
        return value.strftime(target_fmt)
    for fmt in ALL_DATE_FORMATS:
        try:
            output = datetime.datetime.strptime(value, fmt).strftime(target_fmt)
            Debug(f"{value=}, {output=}, {fmt=}")
            return output
        except:
            ...
    if mode == "raise":
        raise NotImplementedError(f"Unable to give a proper date for `{value}`")
    elif mode in {"return"}:
        return None
    elif mode == "default":
        return "01.01.1900"
    else:
        raise NotImplementedError(
            f"`mode` can only be one of {available_modes} (Case sensitive)"
        )

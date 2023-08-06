import re
import textwrap


def justify_both(txt: str, width: int) -> str:
    prev_txt = txt
    while((l := width-len(txt)) > 0):
        txt = re.sub(r"(\s+)", r"\1 ", txt, count=l)
        print(txt)
        if(txt == prev_txt):
            break
    return txt.rjust(width)


def justify_text(_text, w, align, fill=" "):
    wrapper = textwrap.TextWrapper(width=w)
    dedented_text = textwrap.dedent(text=_text)
    txt = wrapper.fill(text=dedented_text)
    _justify_res = ""
    if align == 'left':
        for l in txt.splitlines():
            _justify_res += l.ljust(w, fill)+"\n"
    elif align == 'right':
        for l in txt.splitlines():
            _justify_res += l.rjust(w, fill)+"\n"
    elif align == 'center':
        for l in txt.splitlines():
            _justify_res += l.center(w, fill)+"\n"
    elif align == 'justify':
        for l in txt.splitlines():
            _justify_res += justify_both(l, w)+"\n"

    return _justify_res

import re
from pprint import pprint
from more_itertools import split_at, split_before
from drafting.geometry import Point, Line, Rect


SH_UNARY_SUFFIX_FUNCS = {
    "~": "reverse",
}

SH_UNARY_TO_STRING = {
    "←": "W",
    "↑": "N",
    "→": "E",
    "↓": "S",
    "↖": "NW",
    "↗": "NE",
    "↘": "SE",
    "↙": "SW",
    "•": "C",
}

SH_UNARY_SUFFIX_PROPS = {
    "⊢": "ew",
    "⊣": "ee",
    "⊤": "en",
    "⊥": "es",
    "⌶": "ecx",
    "Ｈ": "ecy",
    "←": "pw",
    "↑": "pn",
    "→": "pe",
    "↓": "ps",
    "↖": "pnw",
    "↗": "pne",
    "↘": "pse",
    "↙": "psw",
    "•": "pc",
    "⍺": "start",
    "⍵": "end",
    "µ": "mid",
}

SH_BINARY_OPS = {
    "I": "inset",
    "𝓘": "inset",
    "O": "offset",
    "𝓞": "offset",
    "C": "columns",
    "𝓒": "columns",
    "R": "rows",
    "𝓡": "rows",
    "@": "__getitem__",
    "↕": "extr",
}

SH_BINARY_OPS_EDGEAWARE = {
    "T": "take",
    "S": "subtract",
    "E": "expand",
    "M": "maxima",
}

SH_JOINS = {
    "⨝": ["join"],
    "∩": ["intersection"],
    "∮": lambda a, b: f"DP().mt({a}.start).lt({a}.end).lt({b}.end).lt({b}.start).cp()"
}

SH_BACKREFS = {
    "〱": "_last",
}

SH_EXPLODES = {
    "〻": "_last",
}

SH_PATH_OPS = {
    "ɜ": "endPath",
    "ɞ": "closePath",
    "Я": "reverse"
}

def shchain(s):
    chars = list(SH_BINARY_OPS_EDGEAWARE.keys())
    chars.extend(SH_BINARY_OPS.keys())
    chars.extend(SH_UNARY_SUFFIX_PROPS)
    chars.extend(SH_UNARY_SUFFIX_FUNCS)
    chars.append(">")
    chars.append("Ƨ")
    
    cs = ["".join(x) for x in split_before(s, lambda x: x in chars) if x[0] != ">"]
    out = cs[0]
    spre = re.compile(",|—")
    skip = False

    for c in cs[1:]:
        f = c[0]
        if f == "Ƨ":
            skip = True
            continue
        elif skip:
            skip = False
            continue

        if f in SH_BINARY_OPS:
            fn = SH_BINARY_OPS[f]
            d = None
            if c[1] in ["X", "Y"]:
                d = c[1]
                args = spre.split(c[2:])
            else:
                args = spre.split(c[1:])
            if d:
                fn += "_" + d.lower()
            for i, a in enumerate(args):
                if a == "auto" or a == "a":
                    args[i] = '"auto"'
            out += f".{fn}({','.join(args)})"
        elif f in SH_BINARY_OPS_EDGEAWARE:
            fn = SH_BINARY_OPS_EDGEAWARE[f]
            d = "XY"
            if c[1] in ["X", "Y"]:
                d = c[1]
                args = spre.split(c[2:])
            else:
                args = spre.split(c[1:])
            for i, a in enumerate(args):
                if a[0] == "-":
                    e = "mn"
                elif a[0] == "=":
                    e = "md"
                elif a[0] == "+":
                    e = "mx"
                else:
                    raise Exception("Edge not matched", args[0])
                if d == "XY":
                    args[i] = (a[1:], '"'+e+"xy"[i]+'"')
                else:
                    args[i] = (a[1:], '"'+e+d.lower()+'"')
                out += f".{fn}({','.join(args[i])})"
        elif f in SH_UNARY_SUFFIX_PROPS:
            fn = SH_UNARY_SUFFIX_PROPS[f]
            out += f".{fn}" #+ c[1:]
        elif f in SH_UNARY_SUFFIX_FUNCS:
            fn = SH_UNARY_SUFFIX_FUNCS[f]
            out += f".{fn}()" #+ c[1:]
    
    return out

def shterm(s:str):
    return shchain(s)

def shphrase(s):
    terms = []
    splits = list(SH_JOINS.keys())
    for idx, _t in enumerate(split_at(s, lambda x: x in splits, keep_separator=1)):
        t = "".join(_t)
        if idx % 2 == 0:
            terms.append("("+shterm(t)+")")
        else:
            terms.append(t)

    out = ""
    t1 = terms[0]
    i = 1
    if i == len(terms):
        return t1    
    else:
        while i < len(terms):
            op_s = terms[i]
            if op_s in SH_JOINS:
                op = SH_JOINS[op_s]
                t2 = terms[i+1]
                
                for k, v in SH_BACKREFS.items():
                    t2 = t2.replace(k, f"({t1})")
                
                if callable(op):
                    out += op(t1, t2)
                else:
                    out += f"({t1}.{op[0]}({t2}))"
                i += 2
    return out

def shgroup(s):
    if s.startswith("Ƨ"):
        return None

    s = s.replace("(", "[").replace(")", "]")
    rg = re.compile(r"\[([^\]]+)\]")

    def expand(m):
        return f"({shphrase(m.group(1))})"

    rm = rg.findall(s)
    while len(rm) > 0:
        s = rg.sub(expand, s)
        rm = rg.findall(s)
    
    return shphrase(s)

def sh(s, ctx={}, dps=None):
    evaled = []
    last_locals = {}
    s = s.replace("_", "")
    s = "ƒ"+re.sub(r"[\s\n]+", "ƒ", s).strip()

    def expand_multisuffix(m):
        out = []
        arrows = list(m.group(2))
        for a in arrows:
            out.append(m.group(1)+a)
        return "ƒ".join(out)
    
    def do_eval(phrase):
        py = (shgroup(phrase))
        if not py:
            return None
        py = py.replace("$", "ctx.c.")
        py = py.replace("&", "ctx.")
        if hasattr(ctx, "bx"):
            py = py.replace("□", "ctx.bx")
        else:
            py = py.replace("□", "ctx.bounds()")
        if dps is not None:
            py = py.replace("■", "_dps.bounds()")

        try:
            res = eval(py, dict(
                ctx=ctx,
                _last=evaled[-1] if len(evaled) > 0 else None,
                _dps=dps,
                Point=Point,
                Line=Line,
                Rect=Rect,
                DP=dps.single_pen_class if dps is not None else None)
                , last_locals)
            return res
        except SyntaxError as e:
            print("SYNTAX ERROR", e, phrase, py)
            return None

    s = re.sub(r"([\$\&]{1}[a-z]+)([↖↑↗→↘↓↙←•⍺⍵µ]{2,})", expand_multisuffix, s)

    for k, v in SH_PATH_OPS.items():
        s = s.replace(k, '"' + v + '"')

    join_to_path = False
    splits = ["ƒ"]
    splits.extend(SH_EXPLODES.keys())

    for phrase in split_before(s, lambda x: x in splits):
        phrase = "".join(phrase).strip()
        last = None
        if not phrase:
            continue
        if phrase.startswith("-"):
            continue
        if phrase[0] in SH_EXPLODES:
            phrase = "_last"+phrase[1:]
        #    last = evaled[-1]
        if phrase[0] == "ƒ":
            phrase = phrase[1:]
        if not phrase:
            continue

        if phrase == "∫":
            join_to_path = True
            continue

        more = []
        if "|" in phrase:
            tuple = phrase.split("|")
            for i, t in enumerate(tuple):
                if isinstance(t, str):
                    if len(t) > 1:
                        if t[0] in SH_UNARY_TO_STRING:
                            tuple[i] = [SH_UNARY_TO_STRING[x] for x in t]
                            continue
                    else:
                        if t in SH_UNARY_TO_STRING:
                            tuple[i] = SH_UNARY_TO_STRING[t]
                            continue
                tuple[i] = do_eval(t)
            more = tuple
            phrase = tuple[-1]

        if more:
            evaled.append(more)
        else:
            evaled.append(do_eval(phrase))
        if dps is not None:
            dps.append(evaled[-1])
    
    if join_to_path and dps:
        return [dps.single_pen_class().gs(evaled)]
    return evaled
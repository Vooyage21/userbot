
from .. import udB


def get_stuff():
    return udB.get_key("GBLACKLISTS") or []


def add_gblacklist(id):
    ok = get_stuff()
    if id not in ok:
        ok.append(id)
        return udB.set_key("GBLACKLISTS", ok)


def rem_gblacklist(id):
    ok = get_stuff()
    if id in ok:
        ok.remove(id)
        return udB.set_key("GBLACKLISTS", ok)


def is_gblacklisted(id):
    return id in get_stuff()

def black_aja():
    return udB.get_key("GBLACKLISTS") or {}

def list_bl(id):
    ok = black_aja()
    for id in ok:
        return "".join(f"**๏** `{z}`\n" for z in ok)
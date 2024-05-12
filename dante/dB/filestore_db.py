

from .. import udB


def get_stored():
    return udB.get_key("FILE_STORE") or {}


def store_msg(hash, msg_id):
    all = get_stored()
    all.update({hash: msg_id})
    return udB.set_key("FILE_STORE", all)


def list_all_stored_msgs():
    all = get_stored()
    return list(all.keys())


def get_stored_msg(hash):
    all = get_stored()
    if all.get(hash):
        return all[hash]


def del_stored(hash):
    all = get_stored()
    all.pop(hash)
    return udB.set_key("FILE_STORE", all)

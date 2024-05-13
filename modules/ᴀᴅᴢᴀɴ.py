"""
✘ **Bantuan Untuk Adzan**

๏ **Perintah:** `adzan` <nama kota>
◉ **Keterangan:** Dapatkan jadwal adzan.
"""
import json

import requests

from . import *


@dante_cmd(pattern="adzan(?:\\s|$)([\\s\\S]*)")
async def cek(event):
    LOKASI = event.pattern_match.group(1)
    if not LOKASI:
        await event.eor("<i>Silahkan Masukkan Nama Kota Anda</i>")
        return True
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        return await eor(event, get_string("adzan1").format(LOKASI))
    result = json.loads(request.text)
    catresult = f"""
**Jadwal Shalat Hari Ini:**
**📆 Tanggal **`{result['items'][0]['date_for']}`
**📍 Kota** `{result['query']}` | `{result['country']}`
**Terbit  : **`{result['items'][0]['shurooq']}`
**Subuh : **`{result['items'][0]['fajr']}`
**Zuhur  : **`{result['items'][0]['dhuhr']}`
**Ashar  : **`{result['items'][0]['asr']}`
**Maghrib : **`{result['items'][0]['maghrib']}`
**Isya : **`{result['items'][0]['isha']}`
"""
    await eor(event, catresult)

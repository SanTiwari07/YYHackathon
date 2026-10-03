# -*- coding: utf-8 -*-
"""Build the native, editable AgroStruxure deck.

    python presentation/build/build_deck.py            # writes ./AgroStruxure_YuvaYodha_2026_Final.pptx (repo root)
    powershell presentation/build/export_office.ps1    # PowerPoint -> PDF + PNG proofs (needs desktop PowerPoint)
"""
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import kit
from kit import new_deck

OUT = os.path.join(ROOT, "AgroStruxure_YuvaYodha_2026_Final.pptx")


def prep_assets():
    a = os.path.join(HERE, "assets")
    logo = os.path.join(a, "schneider_logo.png")
    crop = os.path.join(a, "schneider_logo_crop.png")
    im = Image.open(logo).convert("RGBA")
    im.crop(im.getchannel("A").getbbox()).save(crop)
    kit.LOGO = (crop,)
    tomato = Image.open(os.path.join(ROOT, "assets", "tomato_harvest.jpg")).convert("RGB")
    tomato.thumbnail((900, 1300))
    tomato.save(os.path.join(a, "tomato_still.jpg"), quality=88)
    return a


def main():
    prep_assets()
    import slides_a
    import slides_b
    import slides_c
    prs = new_deck()
    prs.core_properties.title = "AgroStruxure — Yuva Yodha Energy Tech Hackathon 2026 (Challenge 01)"
    prs.core_properties.author = "Team AgroStruxure"
    prs.core_properties.subject = "Solar-synchronised agri-energy microgrid and precision irrigation"
    prs.core_properties.keywords = "PM-KUSUM, FAO-56, Altivar ATV320, TeSys D, EcoStruxure, cold chain"
    for fn in (slides_a.slide01, slides_a.slide02, slides_a.slide03, slides_a.slide04,
               slides_b.slide05, slides_b.slide06, slides_b.slide07,
               slides_c.slide08, slides_c.slide09, slides_c.slide10):
        fn(prs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prs.save(OUT)
    print("saved", OUT, os.path.getsize(OUT) // 1024, "KB,", len(prs.slides), "slides")


if __name__ == "__main__":
    main()

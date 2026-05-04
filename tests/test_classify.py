"""Test section-level multi-label classification."""
from __future__ import annotations

import pandas as pd

from ips_review.classify import classify
from ips_review.screen import screen


def test_era_assignment(dictionary):
    df = pd.DataFrame(
        [
            {"Title": "Indoor positioning system",
             "Abstract": "WiFi indoor positioning",
             "Author_Keywords": "indoor positioning",
             "Document_Type": "Article",
             "Year": str(y),
             "Cited_By": "0",
             "DOI": f"10.x/{y}"}
            for y in (2005, 2012, 2017, 2023)
        ]
    )
    scr = screen(df, dictionary)
    out = classify(scr, dictionary)
    eras = out.set_index("Year")["Sec_III_Era"].to_dict()
    assert eras[2005] == "Era1"
    assert eras[2012] == "Era2"
    assert eras[2017] == "Era3"
    assert eras[2023] == "Era4"


def test_sensing_multilabel(dictionary):
    df = pd.DataFrame(
        [
            {
                "Title": "Hybrid WiFi/BLE indoor positioning",
                "Abstract": "We fuse WiFi RSSI and BLE beacon signals.",
                "Author_Keywords": "wifi;ble;fusion;indoor positioning",
                "Document_Type": "Article",
                "Year": "2021",
                "Cited_By": "10",
                "DOI": "10.x/multi",
            }
        ]
    )
    scr = screen(df, dictionary)
    out = classify(scr, dictionary)
    row = out.iloc[0]
    assert bool(row["Sec_IV_Sensing_Wi-Fi"]) is True
    assert bool(row["Sec_IV_Sensing_BLE"]) is True
    assert bool(row["Sec_IV_Sensing_UWB"]) is False

# Search Strategy

Each raw bibliographic export was produced by running the queries below
on the corresponding database. Reproducing these queries on the same
database at a later date will yield a slightly larger corpus due to new
publications.

## Scopus

```
TITLE-ABS-KEY ( "indoor positioning"  OR  "indoor localization"  OR
                "indoor localisation"  OR  "indoor location system"  OR
                "indoor navigation"  OR  "indoor tracking"  OR
                ( "fingerprint*"  AND  ( "indoor"  OR  "wifi"  OR  "wi-fi"  OR  "ble"  OR  "rssi"  OR  "csi" ) )  OR
                "radio map"  OR  "site survey"  OR  "floor detection" )
AND  PUBYEAR  >  1999  AND  PUBYEAR  <  2027
AND  ( LIMIT-TO ( DOCTYPE , "ar" )  OR  LIMIT-TO ( DOCTYPE , "cp" )  OR
       LIMIT-TO ( DOCTYPE , "ch" )  OR  LIMIT-TO ( DOCTYPE , "re" )  OR
       LIMIT-TO ( DOCTYPE , "cr" ) )
```

Export format: CSV, all available fields. Save as `scopus_1.csv`,
`scopus_2.csv`, ... if results exceed Scopus's per-export limit.

## Web of Science (Core Collection)

```
TS = ( "indoor positioning"  OR  "indoor localization"  OR
       "indoor localisation"  OR  "indoor location system"  OR
       "indoor navigation"  OR  "indoor tracking"  OR
       ( "fingerprint*"  AND  ( "indoor"  OR  "wifi"  OR  "wi-fi"  OR  "ble"  OR  "rssi"  OR  "csi" ) )  OR
       "radio map"  OR  "site survey"  OR  "floor detection" )
AND  PY = ( 2000-2026 )
```

Export format: Excel, all available fields. WoS limits exports to ~500
records per file; save as `savedrecs.xls`, `savedrecs(1).xls`, ...

## IEEE *Xplore*

```
( "Indoor Positioning"  OR  "Indoor Localization"  OR  "Indoor Localisation"  OR
  "Indoor Location System"  OR  "Indoor Navigation"  OR  "Indoor Tracking"  OR
  ( "Fingerprint*"  AND  ( "Indoor"  OR  "WiFi"  OR  "Wi-Fi"  OR  "BLE"  OR  "RSSI"  OR  "CSI" ) )  OR
  "Radio Map"  OR  "Site Survey"  OR  "Floor Detection" )
Filters: 2000–2026
```

Export format: CSV. Save conference papers as `conf_*.csv` and journal /
magazine / early-access papers as any other filename — the IEEE loader
infers Document_Type from the filename prefix.

## Snapshot dates used in the published paper

| Database | Query date |
|---|---|
| Scopus | YYYY-MM-DD |
| Web of Science | YYYY-MM-DD |
| IEEE *Xplore* | YYYY-MM-DD |

(Replace with your actual query dates before submission.)

## Known caveats

- Scopus, WoS, and IEEE periodically reclassify documents (e.g.,
  "Conference review" → "Article"); re-running these queries later may
  shift the I-Core / I-Context counts by ≤1%.
- IEEE's "Article Citation Count" is updated continuously; citation-based
  T1/T2 tier assignments may shift over time.
- Some legacy WoS records have empty `Author Keywords`; the harmonizer
  does not synthesize keywords for these records, so they may end up in
  E-Exclude / no-IPS-relevance even when the title clearly indicates IPS.

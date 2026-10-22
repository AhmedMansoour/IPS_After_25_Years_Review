# Public release and licensing audit — action required

**Current issue:** Publicly tracked repository paths under `data/raw/scopus/`, `data/raw/wos/`, and `data/raw/ieee/` contain vendor bibliographic export files. An existing repository data README simultaneously says raw exports are not redistributed. This inconsistency requires immediate review by the rights holder/institution.

1. Inventory files and their actual licenses/terms; determine whether each is permitted for public redistribution. Do not treat all bibliographic metadata as categorically forbidden or categorically open.
2. Check for personally identifying or confidential records, source restrictions, and copyrighted full-text materials.
3. If a file should not be public, remove it from the current tree and evaluate history-rewrite/removal procedures: merely deleting it in a later commit does not make it disappear from history or forks.
4. Publish only permitted derived statistics, author-licensed data, source identifiers, scripted search procedures, and synthetic demonstration records.
5. Protect the integrity of original work: preserve an appropriately restricted archive of source material before any purge and retain a checksum-only manifest when permitted.
6. Before creating a public Zenodo archive, inspect the archive contents for licensed exports. A release snapshot of files still on the current tree may redistribute them again.
7. Do not assert full independent regeneration when raw licensed inputs are unavailable to the public; distinguish reproducible code/tests from restricted-data regeneration.

**This development branch has not rewritten history or removed the already tracked exports.** It adds no further vendor files. Administrative remediation of current and historical exposures remains open.

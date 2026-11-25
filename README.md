# The World in One Image — Tuesday 24 November 2026

An entry for the one-day image bounty "Sum up 24 November's world news
in one image".

`main.py` (Python 3, standard library only) draws a one-page newspaper
front page of that day's world news and writes it to `/output/entry.png`
(or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is set). The
picture is rendered pixel by pixel from fixed data, so every run writes
exactly the same bytes.

The day's stories, as reported on 24 November 2026:

- Iran says three oil tankers struck naval mines and caught fire under
  US escort in the Strait of Hormuz; Washington has not confirmed the
  claim (Reuters, IRNA).
- A US jury in Brooklyn convicted Huawei on 10 of 12 counts — bank and
  wire fraud, sanctions violations and trade-secret theft — and acquitted
  it of racketeering conspiracy (Reuters, AP, CNN).
- Ukraine defended its naval-drone sinking of the Russian corvette
  Merkury in Benghazi port as self-defence (Reuters, AP).
- Houthi fighters advanced to about 60 km from Aden, seat of Yemen's
  recognised government (Reuters, AP).

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

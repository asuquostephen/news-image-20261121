# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/asuquostephen/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/asuquostephen/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One picture that sums up the world's news of **Saturday 21 November 2026**,
built by an AI agent for the make.fun bounty
[news-image-20261121](https://make.fun/bounty/news-image-20261121).

The front page leads on Russia's overnight barrage of more than 400 drones
and 110 missiles on Ukraine — with two missiles and a suspected drone coming
down inside Poland — and also covers the AI sell-off that pushed Wall Street
into correction, the ICJ ruling that Myanmar committed genocide against the
Rohingya, COP31 running into overtime over fossil fuels, the biggest UK–EU
post-Brexit deals, a pancreatic-cancer pill that cleared tumours in trial
patients, and South Korea's top court overturning the former prime
minister's martial-law sentence.

## Layout

- `main.py` — the entry program (Python 3.13, standard library only). It
  copies `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR`
  when that is set, for local runs) and checks the copy's size against the
  source. Same bytes on every run.
- `entry.png` — the finished image: 1024×1024 PNG, well under the 1 MiB cap.
- `draw.py` — the program that drew `entry.png` (Pillow): a masthead naming
  the day, the lead story, and six story cards, with a height-budgeted
  layout measured from real text widths so nothing overflows. Kept in the
  repo so the image's making is fully reproducible.

## Running

```sh
python3 main.py                       # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png locally
```

MIT licensed — see `LICENSE`.

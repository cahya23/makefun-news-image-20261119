# makefun-news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cahya23/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/cahya23/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page summing up the world news of **Thursday, 19 November 2026**,
built for the make.fun competition `news-image-20261119`.

## The image

`entry.png` (1024×1024) is a front page titled **THE WORLD TODAY**, rendered
programmatically with Python and PIL (sharp text, no generated imagery), with
simple shape-drawn illustrations for each story (see `render.py`):

- **Lead story — Trump, Xi and Putin meet in first-ever summit in Shenzhen:**
  Donald Trump, Xi Jinping and Vladimir Putin hold the first three-way
  summit of the three leaders at Kylin Villa, on the sidelines of the APEC
  summit. Agenda: nuclear arms control, Ukraine and the war with Iran.
  (Sources: Yonhap, Reuters, BBC, USA Today, Le Monde.)
- **GTA 6 is out today:** Grand Theft Auto VI launches on PlayStation 5 and
  Xbox Series X|S, with a rolling midnight-local unlock. File up to 212 GB;
  99 on Metacritic; no PC version at launch.
- **Anthropic's record $81.3bn IPO:** Anthropic prices its IPO at $83 a
  share, raising $81.3 billion — the largest IPO on record, topping
  SpaceX's $75bn. Shares start trading on the Nasdaq today under ticker
  ANT. (Sources: Reuters, PYMNTS, Hindu BusinessLine.)
- **Kerch Bridge hit a third time:** the Crimean Bridge is attacked again
  overnight, the third strike this week. Traffic is suspended while damage
  is assessed. (Source: Reuters.)
- **Tanker struck in the Strait of Hormuz:** a tanker is hit as US–Iran
  strikes continue across the Gulf; Trump says Iran is exploring chemical
  and biological weapons.
- **The Hague rules on Rohingya genocide:** the International Court of
  Justice delivers its judgment today on whether Myanmar committed genocide
  against the Rohingya — the first time a state could be held responsible.
  No verdict outcome is stated: none had been reported when this page was
  drawn.
- **Also today:** Israel's president Herzog asks ex-army chief Gadi Eisenkot
  to try to form the next government, bypassing PM Netanyahu; Pew report:
  Islam set to become the world's largest religion by 2035; Australia,
  Canada, Italy and the UK jointly call on Israel to let aid reach flooded
  Gaza.

No speculation is presented as fact. The ICJ story reports only that the
judgment is delivered today, not its outcome.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. Standard library
only, no network, deterministic — every run writes the same bytes
(verified: two runs produce identical sha256, 145,633 bytes).

To re-render the page from scratch: `python3 render.py` (PIL required).

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=b7cc1mhs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>

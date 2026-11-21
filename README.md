# Friday 20 November 2026 — The World's News in One Image

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Rzfr123/news-image-20261120-round2/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Rzfr123/news-image-20261120-round2/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A dense newspaper front page summing up Friday 20 November 2026: 35 dated stories across 7 regions — 13 drawn panels, 22 more briefs, a world map with numbered pins, and a date check. Round 2 of our entry: same day, more stories, tighter date discipline than round 1 (9 stories).

Bounty: https://make.fun/bounty/news-image-20261120

## Stories

- **Lead — missiles over Kyiv**: hours after the three leaders' peace declaration in Shenzhen, Russia fires 100+ missiles and 400 drones at Ukraine; three Kyiv bridges hit, 8 killed, 28 injured.
- **Cyclone Akvan** comes ashore near Gopalpur, Odisha, about 8 am; 300,000+ moved to shelters, winds 70–80 km/h, no deaths reported.
- **AI sell-off sinks Asia's markets**: Taiwan −6.2%, Seoul −5.2%, Tokyo −5.1%; SoftBank −14%.
- **UK and EU seal a "reset" deal** (food trade, youth visas, carbon link); **COP31** reaches its last day with no deal; a Russian cruise missile lands in **Poland**; Iraq's army enters a militia stronghold; Italy holds a general strike; Japan's inflation hits 2.3%; Kenya drills its first oil well; Bukele files for a third term; Phillips hits 118 against India.
- Briefs 14–35: the US–Venezuela deal, the Senate's 51–48 Iran vote, the Pete Rose pardon, 1,000+ UK drones for Ukraine, the E3 ceasefire call, the Nvidia probe, a pancreatic cancer pill, BepiColombo at Mercury, and more.

## Date check

The Shenzhen summit itself met on Thursday 19 Nov — Friday's news is the declaration and the missiles that followed. The ICJ's Myanmar ruling and Anthropic's $83 debut were Thursday; Friday's news is the reaction in the camps and the second day of trading.

## How it was made

`render.py` draws the front page programmatically with Pillow — no AI image generation, so every headline is exact. `main.ts` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) and validates its PNG magic bytes, IHDR dimensions (1024x1024), format and size first.

## License

MIT — see LICENSE.

# Lattice Labs brand assets

Official logos, app icons and social images for Lattice Labs and its products:

| Product | What it is | Accent (dark backgrounds) | Accent (light backgrounds) |
|---|---|---|---|
| **Lattice Labs** | The company | `#39c3cd` teal | `#0b8291` |
| **Lattice Look** | Compliance intelligence platform ([latticelook.au](https://latticelook.au)) | `#ea580c` copper | `#c2410c` |
| **Lattice Learn** | The learning management system (LMS) built into Lattice Look | `#10b981` emerald | `#059669` |
| **Lattice Listen** | A Lattice Labs product | `#6b62ff` indigo | `#3c30f8` |
| **Lattice Log** | Field companion app to Lattice Look. Its mark is split diagonally, red and white (red and dark ink on light backgrounds) | `#ef4444` red | `#dc2626` |

Every SVG is font-independent: wordmarks and monograms are drawn as outlines, so the marks render the same everywhere, with no fonts installed.

## What is here

Each product folder has the same three sets:

```
<product>/icon/<product>-icon-<size>-for-dark-bg.svg    square app icon, transparent, 11 sizes
<product>/icon/<product>-icon-<size>-for-light-bg.svg   (16, 24, 32, 48, 64, 96, 128, 180, 256, 512, 1024)
<product>/wide/<product>-wide-for-dark-bg.svg           horizontal logo: icon plus two-line wordmark
<product>/wide/<product>-wide-for-light-bg.svg
<product>/social/<product>-og-transparent.svg           1200 x 630 social / Open Graph image
<product>/social/<product>-og-dark-bg.svg
<product>/social/<product>-og-light-bg.svg
```

- **for-dark-bg** files use the bright accent and belong on dark surfaces. **for-light-bg** files use the deeper accent and belong on white or light surfaces.
- Icons and wide logos have no background. Use them on a plain surface with clear space of at least a quarter of the icon's width on every side.
- Lattice Look email collateral: `email-embed.html` (signature banner), `email-marketing-card-embed.html` (card for email bodies), and `email-marketing-card.html`, the source page for `look/social/email-marketing-card.png` (rendered at 1200 x 800, 2x).

## Using the marks

Please do:

- use the files as supplied, scaled proportionally;
- pick the dark-bg or light-bg variant to suit the surface behind it.

Please do not:

- recolour, stretch, rotate, outline, add effects to or redraw a mark;
- rearrange the icon and wordmark, or combine a mark with another logo into a new lockup;
- use a mark in a way that suggests Lattice Labs sponsors, endorses or partners with you unless we have agreed it in writing;
- use a mark, or anything confusingly similar, as part of your own name, logo, domain or app icon.

## Licence

**All rights reserved.** The marks, names and images in this repository belong to Lattice Labs Pty Ltd. They are published so people can refer to Lattice Labs and its products accurately, not as open-source artwork. The short permitted-use grant, and everything it does not cover, is in [LICENSE](LICENSE). For anything else, ask us at hello@latticelabs.au.

## Regenerating the SVGs

`generate.py` builds every SVG from the mark geometry:

```
pip install fonttools brotli
python generate.py path/to/taro-semi-bold.otf path/to/Sora-SemiBold.ttf
```

The wordmarks use Taro SemiBold and the LL monogram uses Sora SemiBold. Neither font is included in this repository; only the outlines of the letters used appear in the SVGs.

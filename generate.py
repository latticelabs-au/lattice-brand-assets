"""Generate all Lattice Labs, Lattice Look, Lattice Learn, Lattice Listen and Lattice Log brand SVGs.

Every SVG is font-independent: the wordmarks and the LL monogram are glyph outlines,
so nothing depends on the viewer having a font installed.

Usage:
    python generate.py WORDMARK_FONT MONOGRAM_FONT

    WORDMARK_FONT  Taro SemiBold (taro-semi-bold.otf), used for the LATTICE / product wordmarks
    MONOGRAM_FONT  Sora SemiBold (any Sora 600 .ttf, .otf or .woff2), used for the LL monogram

Output is written next to this script. The fonts are not part of this repository.
"""
import glob
import os
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

if len(sys.argv) != 3:
    sys.exit(__doc__)

WORDMARK_FONT, MONOGRAM_FONT = sys.argv[1], sys.argv[2]
OUT = os.path.dirname(os.path.abspath(__file__))


def load_glyphs(path, chars):
    font = TTFont(path)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    glyphs = {}
    for char in chars:
        pen = SVGPathPen(glyph_set)
        name = cmap[ord(char)]
        glyph_set[name].draw(pen)
        glyphs[char] = (pen.getCommands(), glyph_set[name].width)
    return font, glyphs


_, GLYPHS = load_glyphs(WORDMARK_FONT, "LATICEOKBSRNG")

# ============================================================
# LL MONOGRAM (Sora SemiBold outlines)
# Reproduces <text x="100" y="100" text-anchor="middle" dominant-baseline="central"
# font-family="Sora" font-weight="600" font-size="42">LL</text> as paths.
# ============================================================
MONOGRAM_SIZE = 42
_sora, _sora_glyphs = load_glyphs(MONOGRAM_FONT, "L")
_scale = MONOGRAM_SIZE / _sora["head"].unitsPerEm
_hhea = _sora["hhea"]
_baseline = 100 + (_hhea.ascent + _hhea.descent) / 2 * _scale  # "central" baseline at y=100
_l_path, _l_advance = _sora_glyphs["L"]
_x = 100 - _l_advance * 2 * _scale / 2  # text-anchor="middle"
MONOGRAM_LL = "\n  ".join(
    f'<path d="{_l_path}" fill="{{t}}" transform="translate({_x + i * _l_advance * _scale:.2f},{_baseline:.2f}) scale({_scale:.4f},{-_scale:.4f})"/>'
    for i in range(2)
)


# ============================================================
# ICON (no background ever)
# ============================================================
ICON_CORE = '''<polygon points="100,20 169.28,60 134.64,80 100,60" fill="{c}" opacity="0.15"/>
  <polygon points="100,20 100,60 65.36,80 30.72,60" fill="{c}" opacity="0.12"/>
  <polygon points="169.28,60 169.28,140 134.64,120 134.64,80" fill="{c}" opacity="0.08"/>
  <polygon points="30.72,60 65.36,80 65.36,120 30.72,140" fill="{c}" opacity="0.10"/>
  <polygon points="169.28,140 100,180 100,140 134.64,120" fill="{c}" opacity="0.05"/>
  <polygon points="30.72,140 65.36,120 100,140 100,180" fill="{c}" opacity="0.06"/>
  <polygon points="100,60 134.64,80 134.64,120 100,140 65.36,120 65.36,80" fill="{f}"/>
  <g stroke="{c}" stroke-width="6" fill="none" stroke-linejoin="round">
    <polygon points="100,20 169.28,60 169.28,140 100,180 30.72,140 30.72,60"/>
    <polygon points="100,60 134.64,80 134.64,120 100,140 65.36,120 65.36,80"/>
    <line x1="100" y1="20" x2="100" y2="60"/>
    <line x1="169.28" y1="60" x2="134.64" y2="80"/>
    <line x1="169.28" y1="140" x2="134.64" y2="120"/>
    <line x1="100" y1="180" x2="100" y2="140"/>
    <line x1="30.72" y1="140" x2="65.36" y2="120"/>
    <line x1="30.72" y1="60" x2="65.36" y2="80"/>
    <line x1="100" y1="60" x2="134.64" y2="40"/>
    <line x1="134.64" y1="120" x2="134.64" y2="160"/>
    <line x1="65.36" y1="120" x2="30.72" y2="100"/>
  </g>
  <g fill="{c}">
    <circle cx="100" cy="20" r="6.5"/><circle cx="169.28" cy="60" r="6.5"/>
    <circle cx="169.28" cy="140" r="6.5"/><circle cx="100" cy="180" r="6.5"/>
    <circle cx="30.72" cy="140" r="6.5"/><circle cx="30.72" cy="60" r="6.5"/>
  </g>
  {m}'''


# Lattice Log's mark is half red, half white (owner, 22 Oct 2026): split on the diagonal along the cube's own 30 degree
# edge line through the centre: the upper-left half red, the lower-right half white, or a light warm grey on light backgrounds so the white half still reads. Keyed by the red the brand passes in.
SPLIT = {"#ef4444": "#ffffff", "#dc2626": "#2a0e0e"}


def icon_core(color, inner_fill, text_color, monogram):
    m = monogram.format(t=text_color)
    if color not in SPLIT:
        return ICON_CORE.format(c=color, f=inner_fill, m=m)
    # The LL monogram is cut on the same diagonal: red in the red half, white in the white half.
    left = ICON_CORE.format(c=color, f=inner_fill, m=monogram.format(t=color))
    right = ICON_CORE.format(c=SPLIT[color], f=inner_fill, m=monogram.format(t="#fffefe"))
    return ('<defs><clipPath id="log-l"><polygon points="0,0 200,0 200,42.26 0,157.74"/></clipPath>'
            '<clipPath id="log-r"><polygon points="200,42.26 200,200 0,200 0,157.74"/></clipPath></defs>\n  '
            f'<g clip-path="url(#log-l)">{left}</g>\n  <g clip-path="url(#log-r)">{right}</g>')


def make_icon(color, inner_fill, text_color, monogram, size):
    core = icon_core(color, inner_fill, text_color, monogram)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 200 200">\n  {core}\n</svg>'

# ============================================================
# VECTORISED TEXT
# ============================================================
def render_word(word, x_start, y_baseline, scale, color):
    """Render word as SVG <path> elements. Font Y is up, SVG Y is down: flip with negative Y scale."""
    paths = []
    x = x_start
    letter_gap = 40 * scale  # extra space between letters
    for char in word:
        d, w = GLYPHS[char]
        paths.append(f'<path d="{d}" fill="{color}" transform="translate({x:.1f},{y_baseline:.1f}) scale({scale:.4f},{-scale:.4f})"/>')
        x += (w * scale) + letter_gap
    return "\n    ".join(paths), x - letter_gap  # return end x without trailing gap

# ============================================================
# WIDE LOGO (no background, tight viewBox)
# ============================================================
def make_wide(color, inner_fill, text_color, top_color, bot_color, word_top, word_bot, monogram):
    # Fixed proportions matching the test page that looked good:
    # Icon ~56px, text ~20px font size, tight gap
    W, H = 280, 60
    icon_scale = 56 / 200  # 0.28
    icon_y = (H - 56) / 2  # vertically center icon

    text_x = 56 + 8  # icon width + gap
    text_scale = 0.011  # tuned so text height ≈ 15px
    line_h = 1352 * text_scale
    gap_between_lines = 4
    text_top_y = (H / 2) - (gap_between_lines / 2)  # baseline of top line
    text_bot_y = text_top_y + line_h + gap_between_lines

    top_paths, _ = render_word(word_top, text_x, text_top_y, text_scale, top_color)
    bot_paths, _ = render_word(word_bot, text_x, text_bot_y, text_scale, bot_color)

    core = icon_core(color, inner_fill, text_color, monogram)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" fill="none">
  <g transform="translate(0,{icon_y:.1f}) scale({icon_scale})">
    {core}
  </g>
    {top_paths}
    {bot_paths}
</svg>'''

# ============================================================
# SOCIAL OG (1200x630, no background)
# ============================================================
def make_social(color, inner_fill, text_color, top_color, bot_color, word_top, word_bot, monogram):
    icon_scale = 1.4
    icon_x = 250
    icon_y = 155
    text_scale = 0.038
    text_x = icon_x + 200 * icon_scale + 30
    line_h = 1352 * text_scale
    line1_y = 315 - line_h / 2
    line2_y = line1_y + line_h + 6

    top_paths, _ = render_word(word_top, text_x, line1_y, text_scale, top_color)
    bot_paths, _ = render_word(word_bot, text_x, line2_y, text_scale, bot_color)
    core = icon_core(color, inner_fill, text_color, monogram)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <g transform="translate({icon_x},{icon_y}) scale({icon_scale})">
    {core}
  </g>
    {top_paths}
    {bot_paths}
</svg>'''

# ============================================================
# GENERATE
# ============================================================
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='\n') as f:
        f.write(content)
    print(f"  {os.path.relpath(path, OUT)}")

# Color configs: (color, innerFill, textColor, topTextColor, botTextColor)
LABS_DARK  = ("#39c3cd", "#13263b", "#39c3cd", "#7ab8c4", "#39c3cd")
LABS_LIGHT = ("#0b8291", "#13263b", "#fffefe", "#122638", "#0b8291")
LOOK_DARK  = ("#ea580c", "#292524", "#ea580c", "#fafaf9", "#ea580c")
LOOK_LIGHT = ("#c2410c", "#292524", "#fffefe", "#1c1917", "#c2410c")
# Lattice Learn: emerald accent, distinct from Look copper and Labs teal.
LEARN_DARK  = ("#10b981", "#06231d", "#10b981", "#ecfdf5", "#10b981")
LEARN_LIGHT = ("#059669", "#06231d", "#fffefe", "#06231d", "#059669")
# Lattice Listen: indigo, sampled from the Listen poster.
LISTEN_DARK  = ("#6b62ff", "#120f3d", "#6b62ff", "#eef0ff", "#6b62ff")
LISTEN_LIGHT = ("#3c30f8", "#120f3d", "#fffefe", "#120f3d", "#3c30f8")
# Lattice Log: red and white; the mark is split half red, half white (see SPLIT).
LOG_DARK  = ("#ef4444", "#2a0e0e", "#ef4444", "#fef2f2", "#ef4444")
LOG_LIGHT = ("#dc2626", "#2a0e0e", "#fffefe", "#2a0e0e", "#dc2626")

# (brand, top word, bottom word, dark, light, dark OG background, monogram)
BRANDS = [
    ("labs", "LATTICE", "LABS", LABS_DARK, LABS_LIGHT, "#0c1e2e", MONOGRAM_LL),
    ("look", "LATTICE", "LOOK", LOOK_DARK, LOOK_LIGHT, "#1c1917", MONOGRAM_LL),
    ("learn", "LATTICE", "LEARN", LEARN_DARK, LEARN_LIGHT, "#06231d", MONOGRAM_LL),
    ("listen", "LATTICE", "LISTEN", LISTEN_DARK, LISTEN_LIGHT, "#120f3d", MONOGRAM_LL),
    ("log", "LATTICE", "LOG", LOG_DARK, LOG_LIGHT, "#2a0e0e", MONOGRAM_LL),
]

SIZES = [16, 24, 32, 48, 64, 96, 128, 180, 256, 512, 1024]

print("=== ICONS (transparent only, no backgrounds) ===")
for brand, _, _, dark, light, _, mono in BRANDS:
    for size in SIZES:
        # Dark-context version (bright color, for use on dark backgrounds)
        write(f"{OUT}/{brand}/icon/{brand}-icon-{size}-for-dark-bg.svg",
              make_icon(dark[0], dark[1], dark[2], mono, size))
        # Light-context version (dark color, for use on light backgrounds)
        write(f"{OUT}/{brand}/icon/{brand}-icon-{size}-for-light-bg.svg",
              make_icon(light[0], light[1], light[2], mono, size))

print("\n=== WIDE LOGOS (transparent, vectorised text) ===")
for brand, word_top, word_bot, dark, light, _, mono in BRANDS:
    write(f"{OUT}/{brand}/wide/{brand}-wide-for-dark-bg.svg",
          make_wide(*dark, word_top, word_bot, mono))
    write(f"{OUT}/{brand}/wide/{brand}-wide-for-light-bg.svg",
          make_wide(*light, word_top, word_bot, mono))

print("\n=== SOCIAL / OG (1200x630, with background options) ===")
for brand, word_top, word_bot, dark, light, bg_dark, mono in BRANDS:
    # Transparent
    write(f"{OUT}/{brand}/social/{brand}-og-transparent.svg",
          make_social(*dark, word_top, word_bot, mono))

    # With dark bg
    svg = make_social(*dark, word_top, word_bot, mono)
    svg = svg.replace('viewBox="0 0 1200 630">',
        f'viewBox="0 0 1200 630">\n  <rect width="1200" height="630" fill="{bg_dark}"/>')
    write(f"{OUT}/{brand}/social/{brand}-og-dark-bg.svg", svg)

    # With white bg
    svg = make_social(*light, word_top, word_bot, mono)
    svg = svg.replace('viewBox="0 0 1200 630">',
        'viewBox="0 0 1200 630">\n  <rect width="1200" height="630" fill="#ffffff"/>')
    write(f"{OUT}/{brand}/social/{brand}-og-light-bg.svg", svg)

count = len(glob.glob(f"{OUT}/**/*.svg", recursive=True))
print(f"\nDONE! {count} SVGs generated.")

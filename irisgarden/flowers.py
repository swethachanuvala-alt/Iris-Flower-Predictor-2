"""Hand-drawn SVG irises (no image files needed)."""
from __future__ import annotations

import itertools

_uid = itertools.count(1)

SPECIES = {
    0: dict(name="Setosa", latin="Iris setosa", common="Bristle-pointed iris",
            tip="#D6DFFF", base="#4863E6", vein="#27379F", accent="#5B7BFF",
            tint_a="#F1F4FF", tint_b="#D5E0FF", std=(30, 9), fall=(64, 31)),
    1: dict(name="Versicolor", latin="Iris versicolor", common="Blue flag iris",
            tip="#F8D3EE", base="#B02F8A", vein="#7A1B62", accent="#D857A6",
            tint_a="#FFF1FA", tint_b="#F6D3EC", std=(46, 17), fall=(66, 32)),
    2: dict(name="Virginica", latin="Iris virginica", common="Virginia blue flag",
            tip="#DCC9FF", base="#5A26B3", vein="#34136F", accent="#7A3FD1",
            tint_a="#F6F0FF", tint_b="#E0D2FB", std=(57, 22), fall=(72, 37)),
}
LEAF = "#3E8E6A"
LEAF_LIGHT = "#5BAA84"
GOLD = "#F4C03F"


def _petal(L, w, vein, beard=False):
    d = (f"M0,0 C{-w:.1f},{-L*0.28:.1f} {-w*0.95:.1f},{-L*0.82:.1f} 0,{-L:.1f} "
         f"C{w*0.95:.1f},{-L*0.82:.1f} {w:.1f},{-L*0.28:.1f} 0,0 Z")
    veins = "".join(
        f'<path d="M0,{-L*0.06:.1f} Q{dx:.1f},{-L*0.4:.1f} {dx*1.5:.1f},{-L*0.78:.1f}" '
        f'stroke="{vein}" stroke-opacity=".35" stroke-width=".9" fill="none"/>'
        for dx in (-w * 0.38, 0, w * 0.38))
    extra = ""
    if beard:
        extra = (f'<ellipse cx="0" cy="{-L*0.3:.1f}" rx="{w*0.15:.1f}" ry="{L*0.22:.1f}" fill="{GOLD}"/>'
                 f'<ellipse cx="0" cy="{-L*0.3:.1f}" rx="{w*0.05:.1f}" ry="{L*0.18:.1f}" fill="#fff" fill-opacity=".7"/>')
    return d, veins, extra


def flower_group(idx, cx=100, cy=100, scale=1.0, rot=0):
    """<g> with one iris head centred on (cx, cy)."""
    s = SPECIES[idx]
    gid = f"iris{next(_uid)}"
    out = [f'<g transform="translate({cx} {cy}) scale({scale}) rotate({rot})">',
           f'<defs><linearGradient id="{gid}" x1="0" y1="1" x2="0" y2="0">'
           f'<stop offset="0" stop-color="{s["base"]}"/><stop offset="1" stop-color="{s["tip"]}"/>'
           f'</linearGradient></defs>']
    for angle, (L, w), beard in [(a, s["fall"], True) for a in (60, 180, 300)] + \
                                [(a, s["std"], False) for a in (0, 120, 240)]:
        d, veins, extra = _petal(L, w, s["vein"], beard)
        out.append(f'<g transform="rotate({angle})"><path d="{d}" fill="url(#{gid})" '
                   f'stroke="{s["vein"]}" stroke-opacity=".35" stroke-width="1"/>{veins}{extra}</g>')
    out.append(f'<circle r="6" fill="{GOLD}"/><circle r="2.6" fill="#fff" fill-opacity=".8"/></g>')
    return "".join(out)


def _leaves(x, y_base, h, flip=1):
    """Two sword-shaped leaves at the foot of a stem."""
    l1 = (f'<path d="M{x},{y_base} C{x-34},{y_base-h*0.25} {x-48},{y_base-h*0.65} {x-40*flip},{y_base-h} '
          f'C{x-14},{y_base-h*0.6} {x-4},{y_base-h*0.3} {x},{y_base} Z" fill="{LEAF}"/>')
    l2 = (f'<path d="M{x},{y_base} C{x+30},{y_base-h*0.2} {x+46},{y_base-h*0.5} {x+38*flip},{y_base-h*0.85} '
          f'C{x+14},{y_base-h*0.5} {x+4},{y_base-h*0.25} {x},{y_base} Z" fill="{LEAF_LIGHT}"/>')
    return l1 + l2


def flower_svg(idx, size=220, stem=False):
    """One iris, optionally with stem and leaves."""
    if stem:
        body = (f'<path d="M100,100 C95,170 106,240 100,318" stroke="{LEAF}" stroke-width="5" '
                f'stroke-linecap="round" fill="none"/>' + _leaves(100, 318, 120) +
                flower_group(idx, 100, 100, 1.0))
        return (f'<svg viewBox="0 0 200 320" width="{size}" xmlns="http://www.w3.org/2000/svg" '
                f'role="img" aria-label="{SPECIES[idx]["name"]} iris">{body}</svg>')
    return (f'<svg viewBox="0 0 200 200" width="{size}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{SPECIES[idx]["name"]} iris">{flower_group(idx, 100, 100, 1.1)}</svg>')


def garden_svg():
    """Hero scene: all three irises at dusk."""
    gid = f"glow{next(_uid)}"
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" fill-opacity="{o}"/>'
                    for x, y, r, o in [(40, 40, 1.6, .7), (120, 70, 1.2, .5), (300, 30, 1.8, .7),
                                       (470, 60, 1.4, .6), (360, 100, 1.1, .4), (60, 150, 1.2, .4),
                                       (500, 170, 1.6, .6), (205, 25, 1.3, .5)])
    stems = ""
    for x, y, dx in [(110, 190, -6), (262, 130, 4), (415, 195, 6)]:
        stems += (f'<path d="M{x},{y} C{x+dx},{y+70} {x-dx},{y+130} {x},430" stroke="{LEAF}" '
                  f'stroke-width="6" stroke-linecap="round" fill="none"/>')
    leaves = _leaves(110, 430, 150) + _leaves(262, 430, 200, -1) + _leaves(415, 430, 160)
    flowers = (flower_group(0, 110, 190, 0.95, -8) + flower_group(1, 262, 130, 1.25, 6) +
               flower_group(2, 415, 195, 1.1, 10))
    return (f'<svg viewBox="0 0 520 430" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="Three irises: setosa, versicolor and virginica">'
            f'<defs><radialGradient id="{gid}" cx=".5" cy=".4" r=".6">'
            f'<stop offset="0" stop-color="#8E6BFF" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="#8E6BFF" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="520" height="430" fill="url(#{gid})"/>{stars}{stems}{leaves}{flowers}</svg>')

# pip install schemdraw
import matplotlib as mpl
import schemdraw
import schemdraw.elements as elm

# Use local LaTeX for high-quality text rendering
# Requires a LaTeX distribution (MiKTeX/TeX Live) and dvipng/ghostscript.
mpl.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    # Enable Cyrillic support if you label in Ukrainian/Russian
    'text.latex.preamble': r'\usepackage[utf8]{inputenc}\usepackage[T2A]{fontenc}\usepackage[ukrainian,english]{babel}'
})

d = schemdraw.Drawing(unit=1.0)
d.config(lw=2, fontsize=12)

# ---- Сітка вузлів (щоб все було рівно) ----
xL, xM, xR = 0, 8, 16   # ліво, центр, право
yT, yM, yB = 10, 6, 2   # верх, середина, низ

TL = (xL, yT); TM = (xM, yT); TR = (xR, yT)
ML = (xL, yM); MC = (xM, yM); MR = (xR, yM)
BL = (xL, yB); BR = (xR, yB)

# ---- Верхня гілка (дріт + вузол по центру) ----
d.add(elm.Line().at(TL).to(TR))
d.add(elm.Dot().at(TM))

# ---- Ліва вертикальна: R (TL -> ML) ----
d.add(elm.Resistor().down().at(TL).to(ML))
d.add(elm.Dot().at(ML))

# ---- Права вертикальна: R (TR -> MR) ----
d.add(elm.Resistor().down().at(TR).to(MR))
d.add(elm.Dot().at(MR))

# ---- Середня горизонталь: R (ML -> MC), R (MC -> MR) ----
d.add(elm.Resistor().right().at(ML).to(MC))
d.add(elm.Dot().at(MC))
d.add(elm.Resistor().right().at(MC).to(MR))

# ---- Центральна вертикальна: джерело НАПРУГИ (E2) вгору MC -> TM ----
# Полярність за замовчуванням: «+» зверху, «-» знизу
d.add(elm.SourceV().up().at(MC).to(TM).label('$E_2$', loc='right'))

# ---- Нижня гілка зліва вниз від ML до BL ----
d.add(elm.Line().down().at(ML).to(BL))

# ---- Джерело НАПРУГИ (E1) горизонтально праворуч на нижній гілці ----
# Якщо хочеш «+» зліва — додай .reverse()
d.add(elm.SourceV().right().at(BL).length(4).label('$E_1$', loc='bottom'))

# ---- Резистор праворуч на нижній гілці ----
d.add(elm.Resistor().right().length(6))

# ---- Доводимо дріт до правого низу BR, піднімаємось до MR і втикаємось у вузол ----
d.add(elm.Line().right().to(BR))
d.add(elm.Line().up().to(MR))

# ---- (необов’язково) Крапки для видимих вузлів ---
d.add(elm.Dot().at(ML))
d.add(elm.Dot().at(MC))
d.add(elm.Dot().at(MR))
d.add(elm.Dot().at(TM))

# ---- Фінал ----
d.draw()
d.save('scheme_ansi_v.png')
print('Saved: scheme_ansi_v.png')

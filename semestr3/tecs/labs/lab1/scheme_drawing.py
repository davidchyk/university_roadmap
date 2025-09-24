# pip install schemdraw
import schemdraw
import schemdraw.elements as elm
import matplotlib as mpl

# LaTeX-рендеринг (потрібен встановлений TeX)
mpl.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.size': 30,
    'text.latex.preamble': r'\usepackage{amsmath}\usepackage{amssymb}'
})

d = schemdraw.Drawing(unit=1.0)
d.config(lw=2, fontsize=30)

# ---- компактні координати по X ----
xL, xM, xR = 0, 6, 12     # <— було 0,8,16; тепер вужче
yT, yM, yB = 10, 6, 2

TL = (xL, yT); TM = (xM, yT); TR = (xR, yT)
ML = (xL, yM); MC = (xM, yM); MR = (xR, yM)
BL = (xL, yB); BR = (xR, yB)

# Верхня шина
d.add(elm.Line().at(TL).to(TR))
d.add(elm.Dot().at(TM))
d.add(elm.Arrow().left().at((xL+3.8, yT+0.3)).length(2.4).label(r'$\vec{I}_1$', loc='top'))
d.add(elm.Arrow().left().at((xM+4.6, yT+0.3)).length(2.4).label(r'$\vec{I}_6$', loc='top'))

# Ліва вертикаль: R1
d.add(elm.Resistor().down().at(TL).to(ML))
d.add(elm.Dot().at(ML))
d.add(elm.Label().at((TL[0]-0.7, (TL[1]+ML[1])/2+0.1)).label(r'$R_1$'))

# Права вертикаль: R6
d.add(elm.Resistor().down().at(TR).to(MR))
d.add(elm.Dot().at(MR))
d.add(elm.Label().at((TR[0]+0.5, (TR[1]+MR[1])/2+0.1)).label(r'$R_6$'))

# Середня гілка: R2, R4
d.add(elm.Resistor().right().at(ML).to(MC))
d.add(elm.Dot().at(MC))
d.add(elm.Resistor().right().at(MC).to(MR))
d.add(elm.Label().at(((ML[0]+MC[0])/2, yM+0.5)).label(r'$R_2$'))
d.add(elm.Label().at(((MC[0]+MR[0])/2, yM+0.5)).label(r'$R_4$'))
d.add(elm.Arrow().right().at((MC[0]-2.2, yM-0.3)).length(2.0).label(r'$\vec{I}_2$', loc='bottom'))
d.add(elm.Arrow().right().at((MR[0]-2.3, yM-0.3)).length(2.0).label(r'$\vec{I}_4$', loc='bottom'))

# Центральна гілка: E2
d.add(elm.SourceV().up().at(MC).to(TM))
d.add(elm.Label().at((xM+0.9, (yM+yT)/2-0.1)).label(r'$E_2$'))

# Нижня гілка: E1 і R3
d.add(elm.Line().down().at(ML).to(BL))
e1 = d.add(elm.SourceV().right().at(BL).length(4))
d.add(elm.Label().at((BL[0]+1.9, yB+0.7)).label(r'$E_1$'))

d.add(elm.Resistor().right().length(6))     # резистор буде з x=4 до x=10
d.add(elm.Line().right().to(BR))
d.add(elm.Line().up().to(MR))

# Підпис R3 — у центрі резистора на нижній гілці (x ~ 7)
d.add(elm.Label().at((BL[0]+7.1, yB-0.7)).label(r'$R_3$'))

# Стрілка I3 (вліво) — трохи правіше центра нижньої гілки
d.add(elm.Arrow().right().at((xM+1.8, yB+0.3)).length(3.2).label(r'$\vec{I}_3$', loc='top'))

# Дублюємо видимі вузли
for pt in (ML, MC, MR):
    d.add(elm.Dot().at(pt))

# ---- Нумерація вузлів (притиснуто до точок) ----
o = 0.33
d.add(elm.Label().at((TM[0]-0.1, TM[1] + o-0.1)).label(r'1'))        # над TM
d.add(elm.Label().at((MR[0] + o-0.1, MR[1]-0.1)).label(r'2'))        # праворуч від MR
d.add(elm.Label().at((MC[0]-0.09, MC[1] - o-0.1)).label(r'3'))        # під MC
d.add(elm.Label().at((ML[0] - o, ML[1]-0.1)).label(r'4'))        # ліворуч від ML

# Стрілка I5 (вгору) біля E2
d.add(elm.Arrow().up()
       .at((xM+0.3, (yM+yT)/2 - 1.7))   # координати трохи лівіше від E2
       .length(1.0)
       .label(r'$\vec{I}_5$', loc='bottom'))

d.add(elm.LoopArrow().at((xL+3.0, yM+2))
       .scale(1.3)
       .reverse()   # ← робить обертання проти годинникової
       .label(r'$1$', loc='center')           # ← число прямо всередині
)

d.add(elm.LoopArrow().at((xL+9.0, yM+2))
       .scale(1.3)
       .reverse()   # ← робить обертання проти годинникової
       .label(r'$2$', loc='center')           # ← число прямо всередині
)

d.add(elm.LoopArrow().at((xL+6.0, yM-2.0))
       .scale(1.3)
       .reverse()   # ← робить обертання проти годинникової
       .label(r'$3$', loc='center')           # ← число прямо всередині
)
# Малюємо/зберігаємо з мінімальними полями
d.draw()
# d.save('scheme_compact.png', bbox_inches='tight', pad_inches=0.05, dpi=200)

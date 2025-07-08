from rectpack import newPacker 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Label:
    def __init__(self, altura:float, largura:float):
        self.altura = altura
        self.largura = largura

r1 = Label(29.0, 53.4)
r2 = Label(142.6, 75.7)
r3 = Label(90.3, 24.0)
r4 = Label(170.6, 146.4)

#Label :  Qtd
labels: dict[Label,int] = {
    r1: 4,
    r2: 5,
    r3: 7,
    r4: 3,
}

MARGIN = 7.5
SPACING = 4.3
SCALE = 10

labels_int = {(int((r.altura+SPACING)*SCALE), int((r.largura+SPACING)*SCALE)) : i for r, i in labels.items()}
bin_width = int((485 - 2*MARGIN) * SCALE)  
bin_height = int((500 - 2*MARGIN) * SCALE) 

packer = newPacker(rotation=False)

for r, h in labels_int.items():
    for _ in range(h):
        packer.add_rect(*r)

packer.add_bin(bin_width, bin_height, count=1)
packer.pack() #type: ignore

placements = packer.rect_list()
placements_mm = []
for b, x, y, w, h, rid in placements:
    if b == 0:  
        x_mm = x/SCALE + MARGIN
        y_mm = y/SCALE + MARGIN
        w_mm = w/SCALE - SPACING
        h_mm = h/SCALE - SPACING
        placements_mm.append((x_mm, y_mm, w_mm, h_mm))


def create_layout(placemetns: list[tuple], margin: float) -> None:
    fig, ax = plt.subplots()
    for (x, y, w, h) in placemetns:
        rect = Rectangle((x, y), w, h, edgecolor='blue', facecolor='skyblue', alpha=0.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, f"{w:.0f}×{h:.0f}", ha='center', va='center')

    ax.add_patch(Rectangle((margin, margin), 485-2*margin, 500-2*margin, 
                            fill=False, ls='--', ec='red', lw=1, label="Área útil"))
    ax.add_patch(Rectangle((0, 0), 485, 500, fill=False, ec='black', lw=1, label="Folha"))
    ax.set_xlim(0, 485); ax.set_ylim(0, 500); ax.set_aspect('equal')
    plt.savefig(r"Rectpack\layout2.png")

if __name__ == '__main__':
    create_layout(placements_mm, MARGIN)
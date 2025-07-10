from rectpack import newPacker, PackingMode, MaxRectsBssf

import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Rotulos:
    def __init__(self, altura:float, largura:float):
        self.altura = altura
        self.largura = largura

r1 = Rotulos(29.0, 53.4)
r2 = Rotulos(142.6, 75.7)
r3 = Rotulos(90.3, 24.0)
r4 = Rotulos(170.6, 146.4)

fila = {
    r1: 4,
    r2: 5,
    r3: 7,  
    r4: 4,
}

MARGIN = 7.5
SPACING = 4.3

largura_folha = 485 - 2*MARGIN   
altura_folha  = 500 - 2*MARGIN   

SCALE = 10
L = int(largura_folha * SCALE)
H = int(altura_folha * SCALE)

rotulos_int = {(int((r.altura + SPACING) *SCALE), int((r.largura + SPACING)*SCALE)): i for  r, i in fila.items()}

# packer = newPacker(mode=PackingMode.Offline , rotation=True)
packer = newPacker(pack_algo=MaxRectsBssf, rotation=False)

for (w, h), i in rotulos_int.items():
    for _ in range(i):
        packer.add_rect(w, h)

packer.add_bin(L, H)
packer.pack() #type: ignore

def create_layout(rotulos_posicionados:list[tuple], largura_folha:float, altura_folha:float, escala:int = 10, titulo:str = "Layout de Impressão") -> None:
    """A partir de uma lista de dimensões dos rótulos e o tamanho do plot, criar um layout de impressão"""
    _, ax = plt.subplots(figsize=(8.27, 11.69))  # tamanho em polegadas ~ A4
    
    ax.set_xlim(0, largura_folha)
    ax.set_ylim(0, altura_folha)
    ax.set_title(titulo)
    ax.set_xlabel("mm")
    ax.set_ylabel("mm")
    ax.set_aspect('equal')
    ax.invert_yaxis() 

    for i, (x, y, w, h) in enumerate(rotulos_posicionados):
        x_mm, y_mm = x / escala, y / escala
        w_mm, h_mm = w / escala, h / escala
        rect = patches.Rectangle((x_mm, y_mm), w_mm, h_mm, linewidth=1, edgecolor='black', facecolor='skyblue')
        ax.add_patch(rect)
        ax.text(x_mm + 1, y_mm + 1, f"{i+1}", fontsize=6, color='black')

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(r'Rectpack\MaxRectsBssf.png')


recs = [(rect.x, rect.y, rect.width, rect.height)for rect in packer[0]]

if __name__ == "__main__":
    create_layout(recs, largura_folha, altura_folha)
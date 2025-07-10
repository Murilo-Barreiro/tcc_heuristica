from rectpack import newPacker, MaxRectsBssf, GuillotineBlsfSas, SkylineMwfl

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from typing import Any

class Label:
    _instances = []

    def __init__(self, altura:float, largura:float):
        self.altura = altura
        self.largura = largura

        self.__class__._instances.append(self)

    @classmethod
    def determine_priority(cls):
        return [(instance.name, instance.largura) for instance in cls._instances]
    
    @classmethod
    def count_instances(cls):
        return len(cls._instances)


class Grid:
    def __init__(self, margin:float, spacing:float, scale:float, height:float, width:float):
        self.margin = margin
        self.spacing = spacing
        self.scale = scale
        self.height = height
        self.width = width

    def total_usable_area(self) -> float:
        return (self.height - 2 * self.margin) * (self.width - 2 * self.margin)

    def bin_width(self) -> int:
        return int((self.width - 2 * self.margin) * self.scale)

    def bin_height(self) -> int:
        return int((self.height - 2 * self.margin) * self.scale)


def genarate_algorithms(algorithms:list, labels:list[int], scale:float, margin:float, spacing:float) -> list[tuple]:
                        
    packer = newPacker(pack_algo=algorithms, rotation=True) 

    for r, h in labels.items():
        for _ in range(h):
            packer.add_rect(*r)

    packer.add_bin(bin_width, bin_height, count=1)
    packer.pack() #type: ignore

    placements = packer.rect_list()
    placements_mm = []
    for b, x, y, w, h, rid in placements:
        if b == 0:  
            x_mm = x/scale + margin
            y_mm = y/scale + margin
            w_mm = w/scale - spacing
            h_mm = h/scale - spacing
            placements_mm.append((x_mm, y_mm, w_mm, h_mm))
    
    return placements_mm


def create_layout(placemetns: list[tuple], margin: float, alg: Any, width:int, height:int) -> None:
    fig, ax = plt.subplots()
    for (x, y, w, h) in placemetns:
        rect = Rectangle((x, y), w, h, edgecolor='blue', facecolor='skyblue', alpha=0.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, f"{w:.0f}×{h:.0f}", ha='center', va='center')

    ax.add_patch(Rectangle((margin, margin), width-2*margin, height-2*margin, 
                            fill=False, ls='--', ec='red', lw=1, label="Área útil"))
    ax.add_patch(Rectangle((0, 0), width, height, fill=False, ec='black', lw=1, label="Folha"))
    ax.set_xlim(0, width); ax.set_ylim(0, height); ax.set_aspect('equal')
    plt.savefig(fr"Grids\{alg.__name__}.png")

if __name__ == '__main__':

    heuristicas = [MaxRectsBssf, GuillotineBlsfSas, SkylineMwfl]

    r1 = Label(29.0, 53.4)
    r2 = Label(142.6, 75.7)
    r3 = Label(90.3, 24.0)
    r4 = Label(170.6, 146.4)

    #Label :  Qtdz
    labels: dict[Label,int] = {
        r1: 4,
        r2: 4,
        r3: 4,
        r4: 4,
    }

    grid = Grid(margin=7.5, spacing=4.3, scale=10.0, height=500.0, width=485.0)

    ajusted_labels = {(int((r.altura+grid.spacing)*grid.scale), int((r.largura+grid.spacing)*grid.scale)) : i for r, i in labels.items()}

    bin_width = grid.bin_width()
    bin_height = grid.bin_height()

    for alg in heuristicas:
        positions = genarate_algorithms(alg, ajusted_labels, grid.scale, grid.margin, grid.spacing)
        create_layout(positions, grid.margin, alg, grid.width, grid.height)

        print(f"Grid gerados com {Label.count_instances()} rótulos, usando {alg.__name__} com {len(positions)} posições.")
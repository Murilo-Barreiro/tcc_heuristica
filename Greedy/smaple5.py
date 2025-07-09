from pprint import pprint

from matplotlib import pyplot as plt


labels = [(50,30), (60,70), (80,60), (120,40), (30,30),
          (70,20), (20,80), (90,100), (40,90), (100,50)]
margin = 7.5; spacing = 4.3
usable_w = 485 - 2*margin  # 470 mm
usable_h = 500 - 2*margin  # 485 mm

# Ordenar por altura descendente (considerando a maior dimensão se rotacionável)
labels_sorted = sorted(labels, key=lambda dim: max(dim[0], dim[1]), reverse=True)

positions = []  # armazenará (x, y, w, h) para cada rótulo colocado
x_cursor = 0
y_cursor = 0
current_row_h = 0
for (w, h) in labels_sorted:
    # Tentar encaixar na linha atual
    # Se cabe diretamente
    if x_cursor == 0:
        # Início de linha
        rotated = False
        if w > usable_w and h <= usable_w:
            # rotacionar se não cabe deitado mas em pé cabe
            w, h = h, w
            rotated = True
        if w <= usable_w:
            # Colocar na posição atual
            positions.append((x_cursor, y_cursor, w, h))
            x_cursor += w  # ocupar espaço na linha
            current_row_h = h
        else:
            # mesmo rotacionado não cabe em linha vazia (ignorar ou erro)
            continue
    else:
        placed = False
        # Tentar sem rotação
        if x_cursor + spacing + w <= usable_w and h <= current_row_h:
            x_cursor += spacing  # espaçamento antes de colocar
            positions.append((x_cursor, y_cursor, w, h))
            x_cursor += w
            placed = True
            if h > current_row_h: 
                current_row_h = h
        # Tentar com rotação se não coube
        if not placed and x_cursor + spacing + h <= usable_w and w <= current_row_h:
            # rotacionar e colocar
            x_cursor += spacing
            positions.append((x_cursor, y_cursor, h, w))
            x_cursor += h
            placed = True
            if w > current_row_h:
                current_row_h = w
        if not placed:
            # Não coube na linha atual, quebrar para nova linha
            x_cursor = 0
            y_cursor += current_row_h + spacing  # descer para próxima prateleira com espaçamento
            current_row_h = 0
            # Colocar o rótulo na nova linha (sem espaçamento à esquerda porque é início)
            if w > usable_w and h <= usable_w:
                w, h = h, w  # rotacionar se necessário
            if w <= usable_w:
                positions.append((0, y_cursor, w, h))
                x_cursor = w
                current_row_h = h
            else:
                continue

pprint(positions)

sheet_width, sheet_height = 485, 500
margin = 7.5
usable_width = sheet_width - 2 * margin
usable_height = sheet_height - 2 * margin

# Criar figura
fig, ax = plt.subplots(figsize=(10, 10))

# Desenhar os rótulos
for (x, y, w, h) in positions:
    rect = plt.Rectangle((x, y), w, h, edgecolor='green', facecolor='lightgreen', alpha=0.7)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, f"{int(w)}×{int(h)}", ha='center', va='center', fontsize=8)

# Desenhar margens e folha
ax.add_patch(plt.Rectangle((0, 0), sheet_width, sheet_height, fill=False, edgecolor='black', lw=1, label='Folha'))
ax.add_patch(plt.Rectangle((margin, margin), usable_width, usable_height,
                           fill=False, edgecolor='red', linestyle='--', lw=1, label='Área útil'))

# Ajustes de eixos
ax.set_xlim(0, sheet_width)
ax.set_ylim(0, sheet_height)
ax.set_aspect('equal')
ax.set_title("Arranjo de rótulos com Algoritmo Guloso (Prateleiras)")
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
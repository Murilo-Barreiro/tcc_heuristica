from ortools.sat.python import cp_model
import matplotlib.pyplot as plt

labels = [
    (50, 30),
    (60, 70),
    (80, 60),
    (120, 40),
    (30, 30),
    (70, 20),
    (20, 80),
    (90, 100),
    (40, 90),
    (100, 50),
    (50, 30),
    (60, 70),
    (80, 60),
    (120, 40),
    (30, 30),
    (70, 20),
    (20, 80),
    (90, 100),
    (40, 90),
    (100, 50),
    (50, 30),
    (60, 70),
    (80, 60),
    (120, 40),
    (30, 30),
    (70, 20),
    (20, 80),
    (90, 100),
    (40, 90),
    (100, 50),

]

model = cp_model.CpModel()
N = len(labels)
# Escala para décimos de mm (inteiros) para evitar floats
SCALE = 10
MARGIN = 7.5

U_w = int((485 - 2 * MARGIN) * SCALE)  # largura utilizável em décimos
U_h = int((500 - 2 * MARGIN) * SCALE)  # altura utilizável
w = [int(lbl[0] * SCALE) for lbl in labels]  # larguras escaladas
h = [int(lbl[1] * SCALE) for lbl in labels]  # alturas escaladas

# Variáveis de posição e rotação
x = [model.NewIntVar(0, U_w, f"x{i}") for i in range(N)]
y = [model.NewIntVar(0, U_h, f"y{i}") for i in range(N)]
r = [model.NewBoolVar(f"r{i}") for i in range(N)]  # 0 ou 1

# Impor limites (dentro da área útil)
for i in range(N):
    # x[i] + largura_eff <= U_w
    model.Add(x[i] + (w[i] * (1 - r[i]) + h[i] * r[i]) <= U_w)
    # y[i] + altura_eff <= U_h
    model.Add(y[i] + (h[i] * (1 - r[i]) + w[i] * r[i]) <= U_h)

# Restrições de não sobreposição com espaçamento
S = int(4.3 * SCALE)  # espaçamento em décimos
for i in range(N):
    for j in range(i + 1, N):
        # Booleans para cada possível separação
        no_overlap = []
        no_overlap.append(model.NewBoolVar(f"sepL_{i}_{j}"))  # i left of j
        no_overlap.append(model.NewBoolVar(f"sepR_{i}_{j}"))  # i right of j
        no_overlap.append(model.NewBoolVar(f"sepB_{i}_{j}"))  # i below j
        no_overlap.append(model.NewBoolVar(f"sepA_{i}_{j}"))  # i above j
        # i à esquerda de j
        model.Add(x[i] + (w[i] * (1 - r[i]) + h[i] * r[i]) + S <= x[j]).OnlyEnforceIf(
            no_overlap[0]
        )
        # i à direita de j
        model.Add(x[j] + (w[j] * (1 - r[j]) + h[j] * r[j]) + S <= x[i]).OnlyEnforceIf(
            no_overlap[1]
        )
        # i abaixo de j
        model.Add(y[i] + (h[i] * (1 - r[i]) + w[i] * r[i]) + S <= y[j]).OnlyEnforceIf(
            no_overlap[2]
        )
        # i acima de j
        model.Add(y[j] + (h[j] * (1 - r[j]) + w[j] * r[j]) + S <= y[i]).OnlyEnforceIf(
            no_overlap[3]
        )
        # Pelo menos uma separação deve ocorrer
        model.AddBoolOr(no_overlap)

# (Opcional) Definir objetivo de maximizar área total colocada, se necessário
# ...

# Resolver o modelo
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 30  # limite de tempo, por exemplo
result = solver.Solve(model)
placements_ortools = []
if result == cp_model.OPTIMAL or result == cp_model.FEASIBLE:
    for i in range(N):
        xi = solver.Value(x[i])
        yi = solver.Value(y[i])
        wi = w[i] if solver.Value(r[i]) == 0 else h[i]
        hi = h[i] if solver.Value(r[i]) == 0 else w[i]
        placements_ortools.append(
            (xi / SCALE + MARGIN, yi / SCALE + MARGIN, wi / SCALE, hi / SCALE)
        )

sheet_width, sheet_height = 485, 500
MARGIN = 7.5
usable_width = sheet_width - 2 * MARGIN
usable_height = sheet_height - 2 * MARGIN

# Criar figura
fig, ax = plt.subplots(figsize=(10, 10))

# Rótulos
for x, y, w, h in placements_ortools:
    rect = plt.Rectangle((x, y), w, h, edgecolor="blue", facecolor="skyblue", alpha=0.7)
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h / 2, f"{int(w)}×{int(h)}", ha="center", va="center", fontsize=8
    )

# Desenhar margens e folha
ax.add_patch(
    plt.Rectangle(
        (0, 0),
        sheet_width,
        sheet_height,
        fill=False,
        edgecolor="black",
        lw=1,
        label="Folha",
    )
)
ax.add_patch(
    plt.Rectangle(
        (MARGIN, MARGIN),
        usable_width,
        usable_height,
        fill=False,
        edgecolor="red",
        linestyle="--",
        lw=1,
        label="Área útil",
    )
)

# Ajustes de eixos
ax.set_xlim(0, sheet_width)
ax.set_ylim(0, sheet_height)
ax.set_aspect("equal")
ax.set_title("Arranjo de rótulos com Google OR-Tools")
ax.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

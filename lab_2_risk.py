import math


def read_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            x = float(input(prompt).replace(",", "."))
        except ValueError:
            print("Введіть число.")
            continue
        if (min_val is not None and x < min_val) or (max_val is not None and x > max_val):
            print(f"Значення має бути в межах [{min_val}, {max_val}].")
            continue
        return x


def read_int(prompt, min_val=1):
    while True:
        try:
            x = int(input(prompt))
        except ValueError:
            print("Введіть ціле число.")
            continue
        if x < min_val:
            print(f"Мінімум: {min_val}.")
            continue
        return x


n = read_int("Кількість проектів: ")

print("\nЩо означає X?")
print("1 - витрати/збитки (менше = краще)")
print("2 - прибуток (більше = краще)")
mode = read_int("Ваш вибір (1/2): ")
minimize = (mode == 1)

projects = []

for i in range(n):
    name = input(f"\nНазва проекту {i + 1}: ")
    m = read_int(f"Кількість варіантів для {name}: ")

    while True:
        values, probs = [], []
        for j in range(m):
            values.append(read_float(f"Значення {j + 1}: "))
            probs.append(read_float(f"Ймовірність {j + 1}: ", 0, 1))
        if math.isclose(sum(probs), 1.0, abs_tol=1e-6):
            break
        print(f"Сума ймовірностей = {sum(probs):.4f}, а має бути 1. Введіть варіанти заново.")

    m_x = sum(v * p for v, p in zip(values, probs))
    d_x = sum(p * (v - m_x) ** 2 for v, p in zip(values, probs))
    sigma = math.sqrt(d_x)
    cv = sigma / abs(m_x) if m_x != 0 else float("inf")

    projects.append({"name": name, "m": m_x, "d": d_x, "sigma": sigma, "cv": cv})

print("\n--- Результати ---")
for p in projects:
    print(f"Проект: {p['name']}")
    print(f"M(X) = {p['m']:.2f}")
    print(f"Дисперсія D(X) = {p['d']:.2f}")
    print(f"Сер. кв. відхилення σ = {p['sigma']:.2f}")
    print(f"Коефіцієнт варіації CV = {p['cv']:.4f}")
    print("-" * 15)

best_m = min(projects, key=lambda p: p["m"]) if minimize else max(projects, key=lambda p: p["m"])
best_cv = min(projects, key=lambda p: p["cv"])

print("\nВисновок:")
print(f"За очікуваним значенням M(X): {best_m['name']}")
print(f"За найменшим ризиком (CV): {best_cv['name']}")

if best_m is best_cv:
    print(f"Обираємо {best_m['name']}, бо він найкращий за обома показниками.")
else:
    print(f"Обираємо {best_m['name']} за вигідністю, або {best_cv['name']}, якщо головне - уникнути ризику.")
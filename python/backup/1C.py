import numpy as np

# Vectores ortogonales
u1 = np.array([0, 2, 0])
u2 = np.array([4, 0, -3])
u3 = np.array([3, 0, 4])

# Normalizamos los vectores
e1 = u1 / np.linalg.norm(u1)
e2 = u2 / np.linalg.norm(u2)
e3 = u3 / np.linalg.norm(u3)

# Mostramos los vectores normalizados
print("e1 (normalizado):", e1)
print("e2 (normalizado):", e2)
print("e3 (normalizado):", e3)

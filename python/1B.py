import numpy as np

# Definimos los vectores como columnas de una matriz
v1 = np.array([0, 2, 0])
v2 = np.array([4, -1, -3])
v3 = np.array([3, 2, 4])

# Creamos la matriz con los vectores
A = np.column_stack((v1, v2, v3))

# Calculamos el determinante
determinante = np.linalg.det(A)

print(f"Determinante: {determinante}")

# Comprobamos si son coplanarios
if np.isclose(determinante, 0):
    print("Los vectores son coplanarios.")
else:
    print("Los vectores no son coplanarios.")
    
    

import numpy as np

# Definimos los vectores originales
v1 = np.array([0, 2, 0])
v2 = np.array([4, -1, -3])
v3 = np.array([3, 2, 4])

# Función de proyección de un vector sobre otro
def projection(u, v):
    return (np.dot(v, u) / np.dot(u, u)) * u

# Proceso de Gram-Schmidt
u1 = v1

# Calculamos u2
proj_v2_u1 = projection(u1, v2)
u2 = v2 - proj_v2_u1

# Calculamos u3
proj_v3_u1 = projection(u1, v3)
proj_v3_u2 = projection(u2, v3)
u3 = v3 - proj_v3_u1

# Verificamos los vectores ortogonales
print("u1 (ortogonal a los otros):", u1)
print("u2 (ortogonal a u1):", u2)
print("u3 (ortogonal a u1 y u2):", u3)

# Verificar ortogonalidad: el producto punto entre cada par de vectores debería ser cero
print("u1 · u2 =", np.dot(u1, u2))  # Debería ser 0
print("u1 · u3 =", np.dot(u1, u3))  # Debería ser 0
print("u2 · u3 =", np.dot(u2, u3))  # Debería ser 0


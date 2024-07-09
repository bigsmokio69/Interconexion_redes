import bcrypt

# Lista de usuarios y contraseñas
usuarios = [
    ("Estrella", "123"),
    ("Emiliano", "456"),
    ("Luis", "789")
]

# Generar hashes de contraseñas
for usuario, contrasena in usuarios:
    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"INSERT INTO usuarios (nombre_usuario, contrasenia) VALUES ('{usuario}', '{hashed_password}');")

import re

# Abre el archivo de texto
with open("summary.txt", "r") as f:
    # Crea un diccionario vacío para almacenar las relaciones
    hosts = {}
    # Crea una variable para almacenar la dirección IP actual
    current_host = None
    # Itera sobre cada línea del archivo
    for line in f:
        # Busca una dirección IP en la línea actual
        match = re.search(r"Host (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
        if match:
            # Si se encuentra una dirección IP, almacena la dirección IP actual
            current_host = match.group(1)
            # Agrega la dirección IP actual al diccionario de hosts si aún no existe
            if current_host not in hosts:
                hosts[current_host] = []
        # Busca una línea que contenga "NVT" en la línea actual
        match = re.search(r"NVT:", line)
        if match:
            # Si se encuentra una línea que contenga "NVT", agrega la línea al diccionario de hosts para la dirección IP actual
            if line.strip() not in hosts[current_host]:
                hosts[current_host].append(line.strip())

    # Crea un diccionario vacío para almacenar las relaciones inversas (NVT a host)
    nvts = {}
    # Itera sobre cada dirección IP en el diccionario de hosts
    for host in hosts:
        # Itera sobre cada línea que contenga "NVT" para la dirección IP actual
        for nvt in hosts[host]:
            # Agrega la relación NVT a host al diccionario de nvts si aún no existe
            if nvt not in nvts:
                nvts[nvt] = []
            if host not in nvts[nvt]:
                nvts[nvt].append(host)

    # Crea un archivo de texto para almacenar los resultados
    with open("resultados.txt", "w") as f:
        # Imprime las relaciones de host a NVT y NVT a host para cada dirección IP válida en el archivo de texto
        for host in hosts:
            if len(hosts[host]) > 0:
                f.write(f"Host {host}\n")
                for nvt in hosts[host]:
                    f.write(nvt + "\n")
                    f.write(str([h for h in nvts[nvt] if h != host]) + "\n")
                    f.write("\n")

    print("Los resultados se han guardado en el archivo 'resultados.txt'.")

import re

# Nombre del archivo de salida
output_file = input("Nombre del archivo de salida: ")
# Nombre del archivo axuiliar para los promts
ai_info = input("Nombre del archivo para los promts: ")
# Instriccion para la IA
promt = " en espanol describe en 3 puntos lo siguiente: \nLa vulnerabilidad consiste en \nUna explotacion exitosa \nLa mitigacion sugerida es"
# Mensaje de vulnerabilidad duplicada
mensaje = "Dicha vulnerabilidad ya fue descrita con anterioridad."
# Resumen del Host
host_resum = "A continuacion la siguiente imagen muestra un resumen de los puertos afectados del host en particular."
# Introduccion de la vulnerabilidad
intro_nvt = "La siguiente vulnerabilidad es denominada "
# Abre el archivo de texto
with open("summary.txt", "r") as f:
    # Crea un diccionario vacío para almacenar las relaciones
    hosts = {}
    # Crea un lista para NVT unicos
    uniq_nvt = []
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
            temp_nvt = line
            # Si se encuentra una línea que contenga "NVT", agrega la línea al diccionario de hosts para la dirección IP actual
            if line.strip() not in hosts[current_host]:
                hosts[current_host].append(line.strip())
            # Revisa si es un NVT unico
            if line.strip() not in uniq_nvt:
                text = line.strip() + promt
                uniq_nvt.append(text)
                

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
    with open(output_file, "w") as f:
        # Imprime las relaciones de host a NVT y NVT a host para cada dirección IP válida en el archivo de texto
        for host in hosts:
            if len(hosts[host]) > 0:
                f.write(f"Host {host}\n")
                f.write("\n")
                f.write(f"{host_resum}\n")
                f.write("\n")
                f.write("\n")

                for nvt in hosts[host]:
                    if len(nvts[nvt]) > 0:
                        if nvts[nvt][0] == host:
                            f.write(intro_nvt + nvt + "\n")
                            f.write(str([h for h in nvts[nvt] if h != host]) + "\n")
                            f.write("\n")
                        else:
                            f.write(intro_nvt + nvt + "\n")
                            f.write("\n")
                            f.write(f"{mensaje}\n")
                            f.write("\n")
        f.close()
    print(f"Los resultados se han guardado en el archivo '{output_file}'.")
    with open(ai_info, "w") as f:
        for line in uniq_nvt:
            if len(hosts) > 0:
                f.write(f"{line}\n")
                f.write("\n")

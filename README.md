# ExtractorAI

#La idea principal es seguir desarrollando el codigo para que pueda crear el solo el docuemnto y pueda crear peticiones para poder describir en cierto formato las vulnerabilidades 

El archivo de entrada debe de contener solo los parametros de Host y NVT, esto se logra con los siguientes comandos
cat report.txt | grep "^Host\|NVT" >> summary.txt

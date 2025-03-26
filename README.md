# Censura de Tor Browser en Entorno Empresarial
![Nota. Elaboración propia](https://github.com/Manuel67623934/Tor-Browser-Censorship/blob/main/Blank%20diagram%20-%20EDL%26RMT.png)

## Justificación del Proyecto

* Riesgo de ransomware y backdoors.
* Evasión de políticas de seguridad por parte de los empleados.
* Venta de datos en la dark web y filtración de información.

## Resumen Ejecutivo

Se implementó un mecanismo para bloquear los circuitos onion de la red Tor dentro de una LAN empresarial. Para ello, se incorporaron las direcciones IP públicas de los repetidores onion y los puentes Tor a la lista negra del firewall Shorewall. Con el fin de capturar continuamente las direcciones IP onion, se desplegó un repetidor medio intruso en la red Tor (VPS ubicado en el Reino Unido). Se desarrollaron scripts en Python para automatizar el proceso de actualización de la lista negra, realizándose de forma dinámica cada 30 minutos.

## Resumen Técnico

El mecanismo implementa un ciclo de actualización de listas negras de firewall basado en la recopilación y validación de direcciones IP de repetidores Tor y puentes. Se utilizan scripts para:

* Capturar direcciones de puentes desde un repetidor Tor (VPS).
* Descargar listas de direcciones IP desde EDLs y el VPS.
* Validar las direcciones mediante pings y combinarlas en un archivo único.
* Formatear la lista para Shorewall y aplicarla al firewall.
* Obtener direcciones de puentes desde Telegram y compararlas con la lista negra para evitar bloqueos innecesarios.
* Monitorear el tráfico web legítimo desde navegadores permitidos.

El sistema se ejecuta de forma automatizada, actualizando las listas negras cada 30 minutos y renovando los puentes de Tor cada 24 horas.

## Función de los Scripts

* **script_firewall:** Actualiza dinámicamente listas negras de Shorewall con direcciones IP validadas, es el core y desencadenante del mecanismo.
* **script_tor:** Realiza y registra conexiones desde Tor Browser.
* **script_chrome:** Realiza y registra solicitudes legítimas desde Chrome.
* **script_telegram:** Obtiene direcciones de puentes Tor a través del bot de Telegram.
* **script_samba:** Gestiona la extracción de listas de direcciones IP desde un directorio compartido Samba.
* **script_vps:** Recopila y valida direcciones IP de puentes Tor desde un relay medio onion para su inclusión en listas negras.

## Resultados

Los scripts se ejecutaron por 14 días. Se observó un bloqueo del 67.27% de las conexiones de Tor Browser, con una media de 194.06 conexiones bloqueadas de un total de 288.50 diarias. No afectó la navegación por Chrome.

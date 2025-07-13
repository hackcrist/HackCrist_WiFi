 #!/bin/bash
# HackCrist WiFi Audit Script Installer - Improved Version

# --- Colores para la Terminal ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Función para limpiar la pantalla ---
clear_screen() {
    printf "\033c" # Comando ANSI para limpiar la pantalla
}

# --- Función para mostrar mensajes de error y salir ---
error_exit() {
    echo -e "${RED}[-] Error: $1${NC}"
    exit 1
}

# --- Función para verificar permisos de superusuario ---
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}[-] Este script necesita permisos de superusuario.${NC}"
        echo -e "${YELLOW}[!] Por favor, ejecuta con 'sudo bash $0' o como usuario root.${NC}"
        exit 1
    fi
}

# --- Detección del gestor de paquetes ---
detect_package_manager() {
    if command -v apt &> /dev/null; then
        echo "apt"
    elif command -v dnf &> /dev/null; then
        echo "dnf"
    elif command -v yum &> /dev/null; then -r
        echo "yum"
    elif command -v pacman &> /dev/null; then
        echo "pacman"
    elif command -v pkg &> /dev/null; then # Termux
        echo "pkg"
    else
        error_exit "No se encontró un gestor de paquetes compatible (apt, dnf, yum, pacman, pkg)."
    fi
}

# --- Inicio del script ---
clear_screen
echo -e "${CYAN}🚀 HackCrist WiFi Audit Script - Instalador Mejorado${NC}"
echo -e "${BLUE}[+] Iniciando proceso de instalación...${NC}"
sleep 1

check_root

PKG_MANAGER=$(detect_package_manager)
echo -e "${BLUE}[+] Gestor de paquetes detectado: ${PKG_MANAGER}${NC}"
sleep 1

# --- Actualizar paquetes ---
echo -e "${BLUE}[+] Actualizando paquetes del sistema...${NC}"
case "$PKG_MANAGER" in
    apt)
        sudo apt update -y && sudo apt upgrade -y || error_exit "Falló la actualización de paquetes (apt)."
        ;;
    dnf|yum)
        sudo $PKG_MANAGER update -y && sudo $PKG_MANAGER upgrade -y || error_exit "Falló la actualización de paquetes ($PKG_MANAGER)."
        ;;
    pacman)
        sudo pacman -Sy --noconfirm && sudo pacman -Su --noconfirm || error_exit "Falló la actualización de paquetes (pacman)."
        ;;
    pkg)
        pkg update -y && pkg upgrade -y || error_exit "Falló la actualización de paquetes (pkg/Termux)."
        ;;
esac
echo -e "${GREEN}[+] Paquetes del sistema actualizados.${NC}"
sleep 1

# --- Instalar Python y pip ---
echo -e "${BLUE}[+] Verificando e instalando Python y pip...${NC}"
if ! command -v python3 &> /dev/null; then
    case "$PKG_MANAGER" in
        apt)
            sudo apt install python3 python3-pip -y || error_exit "Falló la instalación de Python y pip (apt)."
            ;;
        dnf|yum)
            sudo $PKG_MANAGER install python3 python3-pip -y || error_exit "Falló la instalación de Python y pip ($PKG_MANAGER)."
            ;;
        pacman)
            sudo pacman -S python python-pip --noconfirm || error_exit "Falló la instalación de Python y pip (pacman)."
            ;;
        pkg)
            pkg install python -y || error_exit "Falló la instalación de Python (pkg/Termux)."
            pip install pip || error_exit "Falló la instalación de pip (Termux)."
            ;;
    esac
    echo -e "${GREEN}[+] Python y pip instalados.${NC}"
else
    echo -e "${GREEN}[+] Python y pip ya están instalados.${NC}"
fi
sleep 1

# --- Instalar pywifi ---
echo -e "${BLUE}[+] Instalando la librería pywifi...${NC}"
# Usamos python3 -m pip para asegurar que usamos el pip correcto asociado con python3
if command -v python3 &> /dev/null; then
    if [[ $PKG_MANAGER == "pkg" ]]; then # Termux
        python3 -m pip install pywifi || error_exit "Falló la instalación de pywifi (Termux)."
    else
        sudo python3 -m pip install pywifi || error_exit "Falló la instalación de pywifi."
    fi
else
    error_exit "Python 3 no encontrado, no se puede instalar pywifi."
fi
echo -e "${GREEN}[+] pywifi instalado correctamente.${NC}"
sleep 1

echo -e "${GREEN}\n[+] ¡Instalación completa!${NC}"
echo -e "${YELLOW}[*] ¡Ahora puedes ejecutar tu script de auditoría WiFi!${NC}"
echo -e "${BLUE}[+] Abriendo canal de TikTok...${NC}"

# --- Abrir TikTok ---
if command -v termux-open-url &> /dev/null; then
    termux-open-url "https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1"
elif command -v xdg-open &> /dev/null; then
    xdg-open "https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1"
else
    echo -e "${YELLOW}[!] No se pudo abrir el navegador automáticamente. Por favor, visita este enlace manualmente:${NC}"
    echo -e "${CYAN}    https://www.tiktok.com/@ethicalcore?_t=ZT-8xeJ7JR4paQ&_r=1${NC}"
fi

echo -e "${GREEN}[+] ¡Sígueme en TikTok @ethicalcore! ❤️${NC}"
echo -e "${NC}" # Restablecer color

#!/bin/bash
# Instalación simple del servicio Mushroom Client

echo "Instalando Mushroom Client..."

# Copiar servicio
sudo cp mushroom-client.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar para que inicie automáticamente
sudo systemctl enable mushroom-client

# Iniciar servicio
sudo systemctl start mushroom-client

echo "✓ Servicio instalado e iniciado"
echo ""
echo "Ver estado: sudo systemctl status mushroom-client"
echo "Ver logs:   sudo journalctl -u mushroom-client -f"

# Configuration Wi-Fi RTL8192EU

Guide complet pour configurer l'adaptateur USB Wi-Fi Realtek RTL8192EU sur Ubuntu Server 22.04.

## 📋 Informations

- **Adaptateur** : Realtek RTL8192EU (ID: 0bda:818b)
- **Pilote utilisé** : [Mange rtl8192eu-linux-driver](https://github.com/Mange/rtl8192eu-linux-driver)
- **OS testé** : Ubuntu Server 22.04 LTS (noyau 6.8.0-40-generic)

## ❌ Problème

Le pilote natif `rtl8xxxu` du noyau Linux ne supporte pas correctement cet adaptateur :
- Pas d'interface Wi-Fi détectée
- Ou interface instable (NO-CARRIER, timeout DHCP)

## ✅ Solution

Utiliser le pilote Mange compilé via DKMS.

## 🔧 Installation

### 1. Vérifier la détection de l'adaptateur
```bash
lsusb | grep Realtek
```

Résultat attendu :
```
Bus 002 Device 003: ID 0bda:818b Realtek Semiconductor Corp.
```

### 2. Installer les dépendances
```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

### 3. Blacklister le pilote natif
```bash
echo "blacklist rtl8xxxu" | sudo tee /etc/modprobe.d/rtl8xxxu.conf
```

Ou copier le fichier depuis ce repo :
```bash
sudo cp config/modprobe.d/rtl8xxxu.conf /etc/modprobe.d/
```

### 4. Cloner et installer le pilote Mange
```bash
cd ~
git clone https://github.com/Mange/rtl8192eu-linux-driver.git
cd rtl8192eu-linux-driver
sudo dkms add .
sudo dkms install rtl8192eu/1.0
```

### 5. Désactiver le power management
```bash
echo "options rtl8192eu rtw_power_mgnt=0 rtw_enusbss=0" | sudo tee /etc/modprobe.d/rtl8192eu.conf
```

Ou copier depuis ce repo :
```bash
sudo cp config/modprobe.d/rtl8192eu.conf /etc/modprobe.d/
```

### 6. Redémarrer
```bash
sudo reboot
```

### 7. Vérifier l'interface Wi-Fi
```bash
ip link show
```

Vous devriez voir une interface `wlx` (exemple : `wlx001ea63024db`).
```bash
# Scanner les réseaux disponibles
sudo iwlist wlx001ea63024db scan | grep ESSID
```

## 🌐 Configuration Netplan

### Créer/éditer le fichier netplan
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Utiliser la configuration depuis ce repo :
```bash
sudo cp config/netplan/50-cloud-init.yaml.example /etc/netplan/50-cloud-init.yaml
```

Éditer avec vos informations :
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Remplacer :
- `wlx001ea63024db` par votre interface (voir avec `ip link show`)
- `VOTRE_SSID` par le nom de votre réseau Wi-Fi
- `VOTRE_MOT_DE_PASSE` par votre mot de passe Wi-Fi

### Appliquer la configuration
```bash
sudo netplan apply
```

### Tester la connexion
```bash
# Vérifier l'adresse IP
ip addr show wlx001ea63024db

# Tester la connexion Internet
ping -c 4 8.8.8.8
ping -c 4 google.com
```

## ✅ Résultat

- Interface Wi-Fi détectée et active
- Connexion stable
- Reconnexion automatique après reboot

## 🐛 Dépannage

### L'interface disparaît après un reboot

Vérifier que le module est chargé :
```bash
lsmod | grep 8192eu
```

Si absent, charger manuellement :
```bash
sudo modprobe 8192eu
```

### Après une mise à jour du kernel

Recompiler le module DKMS :
```bash
cd ~/rtl8192eu-linux-driver
sudo dkms remove rtl8192eu/1.0 --all
sudo dkms add .
sudo dkms install rtl8192eu/1.0
sudo reboot
```

### Timeout DHCP ou NO-CARRIER

Vérifier que le power management est bien désactivé :
```bash
cat /sys/module/8192eu/parameters/rtw_power_mgnt
```

Devrait afficher : `0`

Forcer la reconnexion :
```bash
sudo ip link set wlx001ea63024db down
sudo ip link set wlx001ea63024db up
sudo netplan apply
```

### Logs de dépannage
```bash
# Voir les logs système
sudo journalctl -u systemd-networkd -f

# Logs du kernel
sudo dmesg | grep 8192eu
```

## 📚 Références

- [Mange RTL8192EU Driver](https://github.com/Mange/rtl8192eu-linux-driver)
- [Ubuntu Netplan Documentation](https://netplan.io/)

---

**Dernière mise à jour** : 2025-01-12
```

4. **Message de commit :**
```
docs: guide complet configuration Wi-Fi RTL8192EU

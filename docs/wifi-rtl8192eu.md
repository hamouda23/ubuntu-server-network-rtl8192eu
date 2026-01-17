# Configuration Wi-Fi RTL8192EU

Guide complet pour configurer l'adaptateur USB Wi-Fi Realtek RTL8192EU sur Ubuntu Server 22.04.

## 📋 Informations

- **Adaptateur** : Realtek RTL8192EU (ID: 0bda:818b)
- **Pilote utilisé** : [Mange rtl8192eu-linux-driver](https://github.com/Mange/rtl8192eu-linux-driver)
- **Gestionnaire réseau** : NetworkManager (au lieu de netplan)
- **OS testé** : Ubuntu Server 22.04 LTS (noyau 6.8.0-40-generic)

## ❌ Problème

Le pilote natif `rtl8xxxu` du noyau Linux ne supporte pas correctement cet adaptateur :
- Pas d'interface Wi-Fi détectée
- Ou interface instable (NO-CARRIER, timeout DHCP)

## ✅ Solution

1. Installer le pilote Mange compilé via DKMS
2. Utiliser NetworkManager pour la gestion automatique du Wi-Fi

## 🔧 Installation du pilote

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

### 6. Redémarrer

```bash
sudo reboot
```

### 7. Vérifier l'interface Wi-Fi

```bash
ip link show
```

Vous devriez voir une interface `wlx` (exemple : `wlx001ea63024db`).

## 🌐 Configuration avec NetworkManager

### 1. Installer NetworkManager

```bash
sudo apt install network-manager
```

### 2. Activer NetworkManager

```bash
sudo systemctl start NetworkManager
sudo systemctl enable NetworkManager
```

### 3. Scanner les réseaux disponibles

```bash
nmcli device wifi list
```

### 4. Se connecter au Wi-Fi

```bash
sudo nmcli device wifi connect "VOTRE_SSID" password "VOTRE_MOT_DE_PASSE"
```

Remplacez :
- `VOTRE_SSID` par le nom de votre réseau Wi-Fi
- `VOTRE_MOT_DE_PASSE` par votre mot de passe Wi-Fi

### 5. Vérifier la connexion

```bash
# Voir l'état des interfaces
nmcli device status

# Voir l'IP attribuée
ip addr show wlx001ea63024db

# Tester Internet
ping -c 4 8.8.8.8
```

## ✅ Connexion automatique

NetworkManager enregistre automatiquement la connexion. Après un reboot, le Wi-Fi se reconnecte tout seul !

**Test :**
```bash
sudo reboot
# Après redémarrage
ip addr show wlx001ea63024db  # L'IP doit apparaître automatiquement
```

## 🔧 Commandes utiles NetworkManager

### Voir toutes les connexions enregistrées
```bash
nmcli connection show
```

### Voir l'état du Wi-Fi
```bash
nmcli device wifi
```

### Se déconnecter
```bash
nmcli device disconnect wlx001ea63024db
```

### Se reconnecter à un réseau enregistré
```bash
nmcli connection up "NOM_DU_RESEAU"
```

### Supprimer une connexion
```bash
nmcli connection delete "NOM_DU_RESEAU"
```

### Modifier le mot de passe
```bash
nmcli connection modify "NOM_DU_RESEAU" wifi-sec.psk "NOUVEAU_MOT_DE_PASSE"
```

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

### Wi-Fi ne se connecte pas automatiquement

Vérifier que NetworkManager est actif :
```bash
systemctl status NetworkManager
```

Reconnecter manuellement :
```bash
sudo nmcli device wifi connect "VOTRE_SSID" password "VOTRE_MOT_DE_PASSE"
```

### L'IP n'apparaît pas

Forcer l'obtention d'une IP :
```bash
sudo dhclient wlx001ea63024db
```

Ou redémarrer NetworkManager :
```bash
sudo systemctl restart NetworkManager
```

### Après une mise à jour du kernel

Le module DKMS doit être recompilé :
```bash
cd ~/rtl8192eu-linux-driver
sudo dkms remove rtl8192eu/1.0 --all
sudo dkms add .
sudo dkms install rtl8192eu/1.0
sudo reboot
```

### Voir les logs NetworkManager

```bash
journalctl -u NetworkManager -f
```

### Voir les logs du pilote Wi-Fi

```bash
sudo dmesg | grep 8192eu
```

## 📊 Vérification de la configuration

### Checklist finale

- [ ] Interface `wlx001ea63024db` apparaît dans `ip link show`
- [ ] NetworkManager est actif : `systemctl status NetworkManager`
- [ ] Connexion Wi-Fi enregistrée : `nmcli connection show`
- [ ] IP attribuée : `ip addr show wlx001ea63024db`
- [ ] Internet fonctionne : `ping 8.8.8.8`
- [ ] Reconnexion automatique après reboot testée

## ❓ NetworkManager vs netplan

**NetworkManager** (ce guide) :
- ✅ Gestion automatique du Wi-Fi
- ✅ Reconnexion automatique
- ✅ Changement de réseau facile
- ✅ Commandes simples (nmcli)
- 👍 Recommandé pour Wi-Fi

**netplan** (alternative) :
- Configuration via fichiers YAML
- Plus de contrôle manuel
- Standard sur Ubuntu Server
- Mieux pour configuration statique fixe

Pour un serveur avec Wi-Fi, **NetworkManager est plus pratique**.

## 📚 Références

- [Mange RTL8192EU Driver](https://github.com/Mange/rtl8192eu-linux-driver)
- [NetworkManager Documentation](https://networkmanager.dev/)
- [nmcli Examples](https://networkmanager.dev/docs/api/latest/nmcli-examples.html)

---

**Dernière mise à jour** : 2025-01-17  
**Configuration testée** : Wi-Fi avec reconnexion automatique via NetworkManager

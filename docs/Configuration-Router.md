# Configuration Dragino MS14N — Passerelle VPN & Wake-on-LAN

**Statut : Opérationnel** | Dernière mise à jour : Avril 2026

**Objectif** : Accès distant sécurisé (WireGuard) vers un serveur Ubuntu (HP Z800) avec capacité de réveil à distance (WoL).

---

## 1. Topologie Réseau

```
INTERNET (IP Publique : 70.81.172.196)
    ↓ Port 51820 UDP
Box FAI (Fizz - 192.168.0.1)
    ↓ Redirection (Port Forwarding)
Dragino MS14N (WAN WiFi: 192.168.0.67 | LAN Eth: 10.130.1.1)
    ↓ Câble Ethernet (RJ45)
Serveur Ubuntu "AI" (enp1s0: 10.130.1.226)
```

---

## 2. Matériel

| Composant | Détail |
|-----------|--------|
| Appareil | Dragino MS14N-V1.3 (PRO2) |
| Module WiFi | Dragino HE (CE0700) |
| Module XBee | Digi International XBee S2 |
| MAC | A8:40:41:16:C4:D3 |
| Serveur | HP Z800 — Ubuntu Server 22.04 |
| Interface réseau serveur | enp1s0 (MAC: 2c:27:d7:f0:1c:a2) |

---

## 3. Flash du Firmware

### Firmware utilisé
```
dragino-lgw--v5.4.1773647212-squashfs-sysupgrade.bin
```
Téléchargement :
```
[http://www.dragino.com/downloads/index.php?dir=motherboards/ms14/Firmware/IoT/](https://www.dragino.com/downloads/index.php?dir=LoRa_Gateway/LIG16/Firmware/Release/old_release/lgw--build-v5.4.1628078462-20210804-2002/
```

### Procédure Mode Failsafe

**Étape 1 — PC en IP statique**
```
IP :        192.168.255.2
Masque :    255.255.255.0
```

**Étape 2 — Entrer en mode failsafe**
1. Branchez câble Ethernet PC → port LAN du Dragino
2. Éteignez le Dragino
3. Maintenez le bouton RESET enfoncé
4. Branchez l'alimentation en gardant RESET appuyé
5. Comptez **4 clignotements** des LEDs puis relâchez
6. LEDs clignotent très vite une fois → mode failsafe actif

**Étape 3 — Flasher**
1. Ouvrez Chrome sur `http://192.168.255.1`
2. Sélectionnez `squashfs-sysupgrade.bin`
3. Cliquez **Update** — attendez 3-4 minutes sans débrancher

**Étape 4 — Après le reboot**
```
IP PC :     172.31.255.253
Masque :    255.255.255.252
```
Interface : `http://172.31.255.254`
- Username : `root`
- Password : `dragino`

### SSH Legacy (obligatoire pour ce firmware)
```bash
ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 \
    -oHostKeyAlgorithms=+ssh-rsa \
    -oMACs=+hmac-sha1 \
    root@172.31.255.254
```

---

## 4. Configuration WiFi Client (Dragino → Fizz)

```bash
uci set wireless.sta.ssid='VOTRE_SSID'
uci set wireless.sta.encryption='psk2'
uci set wireless.sta.key='VOTRE_MOT_DE_PASSE'
uci commit wireless
wifi restart
```

Vérification :
```bash
ifconfig wlan0 | grep inet
# inet addr:192.168.0.67 → IP du Dragino sur le réseau Fizz
```

---

## 5. Configuration WireGuard

### Le Dragino agit comme Serveur VPN

> **Note importante** : Ce n'est pas un simple port forwarding (DNAT).
> C'est un **tunnel VPN Site-to-Site chiffré** où le Dragino est le point d'entrée.

### Installation sur le Dragino
```bash
opkg update
opkg install luci-app-wireguard
```

### Règles Firewall permanentes (`/etc/firewall.user`)
```bash
# Autoriser l'entrée WireGuard
iptables -I INPUT -p udp --dport 51820 -j ACCEPT

# Autoriser le transit VPN <-> Ethernet
iptables -I FORWARD -i wg0 -o eth0 -j ACCEPT
iptables -I FORWARD -i eth0 -o wg0 -j ACCEPT

# Masquerading (NAT) pour le retour des paquets
iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
```

### Config Client Windows
```ini
[Interface]
PrivateKey = <CLE_PRIVEE_PC>
Address = 10.1.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = <CLE_PUBLIQUE_DRAGINO>
AllowedIPs = 10.1.0.0/24, 10.130.1.0/24
Endpoint = 70.81.172.196:51820
PersistentKeepalive = 25
```

> **AllowedIPs** : Le sous-réseau `10.130.1.0/24` est indispensable pour que
> le PC Windows envoie le trafic vers le serveur dans le tunnel et non sur le WiFi local.

### Config Serveur Ubuntu (`/etc/wireguard/wg0.conf`)
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <CLE_PRIVEE_SERVEUR>
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp1s0 -j MASQUERADE

[Peer]
PublicKey = <CLE_PUBLIQUE_CLIENT>
AllowedIPs = 10.0.0.2/32
```

### Box FAI (Fizz) — Port Forwarding
```
Port public  : 51820 UDP
IP locale    : 192.168.0.67 (IP WiFi du Dragino)
Port privé   : 51820
```

---

## 6. Configuration Serveur Ubuntu

### Activer la carte Ethernet au démarrage
```yaml
# /etc/netplan/00-installer-config.yaml
network:
  ethernets:
    enp1s0:
      dhcp4: true
  version: 2
```
```bash
sudo chmod 600 /etc/netplan/00-installer-config.yaml
sudo netplan apply
```

### Activer le forwarding IP
```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
# Permanent :
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
```

### Vérifier la route par défaut
```bash
ip route
# default via 10.130.1.1 dev enp1s0 → correct !
```

---

## 7. Wake-on-LAN (Réveil à distance)

### Côté Serveur Ubuntu
```bash
# Activer WoL sur enp1s0
sudo ethtool -s enp1s0 wol g

# Vérifier
sudo ethtool enp1s0 | grep Wake
```

### Côté Dragino
```bash
opkg install etherwake
```

### Commande de réveil depuis PC distant
```powershell
ssh -oHostKeyAlgorithms=+ssh-rsa root@10.1.0.1 "etherwake -i eth0 2c:27:d7:f0:1c:a2"
```

---

## 8. Dépannage

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Handshake did not complete` | Port 51820 UDP bloqué | Vérifier redirection Box FAI + règle `INPUT` iptables Dragino |
| `Ping 10.1.0.1 OK, 10.130.1.226 KO` | Manque route ou NAT | Ajouter `10.130.1.0/24` dans `AllowedIPs` + `MASQUERADE` sur Dragino |
| `Unable to negotiate... ssh-rsa` | Client SSH trop moderne | Utiliser `-oHostKeyAlgorithms=+ssh-rsa` |
| `tcpdump` muet sur Ubuntu | Forwarding désactivé | `echo 1 > /proc/sys/net/ipv4/ip_forward` sur le Dragino |
| IP Dragino change sur réseau Fizz | DHCP dynamique | Mettre à jour la règle port forwarding sur Box FAI |

---

## 9. Pourquoi ces choix ?

1. **Port 51820** : Port standard WireGuard — évite les conflits avec HTTPS (443)
2. **AllowedIPs étendu** : Sans `10.130.1.0/24`, le trafic vers le serveur ne passe pas dans le tunnel
3. **VPN vs DNAT** : Tunnel chiffré WireGuard >> simple port forwarding pour sécuriser le serveur "AI"
4. **Dragino comme point d'entrée** : Élimine la clé WiFi USB du serveur et centralise la connexion

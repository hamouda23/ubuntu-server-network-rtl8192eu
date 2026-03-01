Guide pour configurer l'accès SSH sécurisé au serveur HP Z800.
## 🎯 Objectifs
- Accès distant au serveur sans écran/clavier
- Authentification par clé (plus sécurisée que mot de passe)
- Protection contre les attaques brute-force
- Accès depuis n'importe où
## 📋 Prérequis
- [ ] Wi-Fi configuré et fonctionnel
- [ ] Connexion réseau stable
- [ ] Accès physique au serveur (pour la première config)
## 🔧 Installation
### 1. Installer OpenSSH Server
```bash
sudo apt update
sudo apt install openssh-server
```
### 2. Démarrer et activer SSH
```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```
### 3. Vérifier que SSH fonctionne
```bash
sudo systemctl status ssh
```
Devrait afficher : `active (running)`
### 4. Trouver l'IP du serveur
```bash
ip addr show wlx001ea63024db | grep inet
```
Notez l'adresse IP (exemple : `192.168.1.100`)
## 🔐 Première connexion
Depuis un autre ordinateur sur le même réseau :
```bash
ssh votre_utilisateur@192.168.1.100
```
Si ça fonctionne, vous êtes connecté ! ✅
## 🛡️ Sécurisation (Recommandé)
### 1. Créer une paire de clés SSH
**Sur votre ordinateur client** (pas sur le serveur) :
```bash
# Générer une clé SSH
ssh-keygen -t ed25519 -C "votre_email@example.com"
# Appuyez sur Entrée pour accepter l'emplacement par défaut
# Créez un mot de passe (optionnel mais recommandé)
```
### 2. Copier la clé vers le serveur
```bash
ssh-copy-id votre_utilisateur@192.168.1.100
```
Entrez votre mot de passe une dernière fois.
### 3. Tester la connexion par clé
```bash
ssh votre_utilisateur@192.168.1.100
```
Vous ne devriez plus avoir besoin du mot de passe ! ✅
### 4. Désactiver l'authentification par mot de passe
**Sur le serveur** :
```bash
sudo nano /etc/ssh/sshd_config
```
Trouver et modifier ces lignes :
```
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
```
Redémarrer SSH :
```bash
sudo systemctl restart ssh
```
## 🌐 IP statique (Recommandé pour headless)
Modifier `/etc/netplan/50-cloud-init.yaml` :
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp1s0:
      dhcp4: true
      optional: true
  wifis:
    wlx001ea63024db:
      dhcp4: false  # Désactiver DHCP
      addresses:
        - 192.168.1.100/24  # Votre IP statique choisie
      routes:
        - to: default
          via: 192.168.1.1  # Gateway de votre routeur
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
      optional: true
      access-points:
        "VOTRE_SSID":
          password: "VOTRE_MOT_DE_PASSE"
```
Appliquer :
```bash
sudo netplan apply
```
## 🔒 Protection Fail2ban (Optionnel)
Protège contre les tentatives de connexion multiples :
```bash
# Installer
sudo apt install fail2ban
# Activer
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
# Vérifier
sudo fail2ban-client status sshd
```
## ✅ Test final
### Sur le serveur
```bash
# Vérifier que SSH écoute
sudo ss -tlnp | grep ssh
```
### Depuis votre PC
```bash
# Se connecter
ssh votre_utilisateur@192.168.1.100
# Test de commande à distance
ssh votre_utilisateur@192.168.1.100 "uname -a"
```


## 🌍 Accès distant sécurisé avec WireGuard VPN

Plutôt qu'exposer SSH directement sur internet, WireGuard crée un tunnel VPN chiffré.
Tu te connectes d'abord au VPN, puis SSH fonctionne comme si tu étais sur le réseau local.

### Pourquoi WireGuard ?

| Méthode | Sécurité | Complexité |
|---|---|---|
| SSH port 22 direct | ❌ Faible | Simple |
| SSH + clés + fail2ban | ✅ Correct | Moyen |
| **WireGuard VPN** | ✅✅ **Meilleur** | Moyen |

- Le port SSH n'est **jamais exposé** sur internet
- Cryptographie moderne (Curve25519, ChaCha20)
- Très léger et performant
- Un attaquant qui scanne tes ports ne voit rien

---

### 📋 Prérequis

- [ ] SSH fonctionnel sur le réseau local (voir section précédente)
- [ ] Accès à l'interface de ton routeur (pour la redirection de port)
- [ ] WireGuard installé sur le client (Windows/Mac/Linux/Mobile)

---

### 🔧 Installation sur le serveur

```bash
sudo apt update
sudo apt install wireguard
```

---

### 🔑 Génération des clés

Passer en root pour avoir les permissions nécessaires :

```bash
sudo su
```

Générer les clés du **serveur** :

```bash
wg genkey | tee /etc/wireguard/server_private.key | wg pubkey > /etc/wireguard/server_public.key
chmod 600 /etc/wireguard/server_private.key
```

Générer les clés du **client** (ton PC) :

```bash
wg genkey | tee /etc/wireguard/client_private.key | wg pubkey > /etc/wireguard/client_public.key
```

Afficher les clés pour les noter :

```bash
cat /etc/wireguard/server_private.key   # → SERVER_PRIVATE_KEY
cat /etc/wireguard/server_public.key    # → SERVER_PUBLIC_KEY
cat /etc/wireguard/client_private.key   # → CLIENT_PRIVATE_KEY
cat /etc/wireguard/client_public.key    # → CLIENT_PUBLIC_KEY
```

Quitter le mode root :

```bash
exit
```

---

### ⚙️ Configuration du serveur

Trouver le nom de l'interface réseau :

```bash
ip a   # ex: eth0, enp3s0, wlx001ea63024db...
```

Créer le fichier de configuration :

```bash
sudo nano /etc/wireguard/wg0.conf
```

```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = SERVER_PRIVATE_KEY

# Remplacer eth0 par votre interface réseau réelle
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# PC client
PublicKey = CLIENT_PUBLIC_KEY
AllowedIPs = 10.0.0.2/32
```

Activer le forwarding IP :

```bash
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

Démarrer et activer WireGuard au démarrage :

```bash
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
```

Vérifier que WireGuard tourne :

```bash
sudo wg show
```

Ouvrir le port dans le firewall :

```bash
sudo ufw allow 51820/udp
sudo ufw reload
```

---

### 🔀 Redirection de port sur le routeur

Dans l'interface de ta box/routeur :

| Paramètre | Valeur |
|---|---|
| Port externe | 51820 |
| Port interne | 51820 |
| Protocole | **UDP** |
| IP de destination | IP locale du serveur (ex: 192.168.1.100) |

---

### 💻 Configuration du client (Windows)

1. Télécharger WireGuard : [wireguard.com](https://www.wireguard.com/install/)
2. Créer un fichier `client.conf` :

```ini
[Interface]
Address = 10.0.0.2/24
PrivateKey = CLIENT_PRIVATE_KEY
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = TON_IP_PUBLIQUE:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

> 💡 `AllowedIPs = 10.0.0.0/24` → seul le trafic VPN passe par le tunnel (navigation normale préservée)  
> 💡 `AllowedIPs = 0.0.0.0/0` → tout le trafic passe par le VPN

3. Dans l'app WireGuard : **Import tunnel(s) from file** → sélectionner `client.conf`
4. Cliquer sur **Activate**

---

### ✅ Test de connexion

Trouver ton IP publique depuis le serveur :

```bash
curl -4 ifconfig.me
```

Activer le VPN sur le client, puis tester :

```bash
# Ping du serveur via VPN
ping 10.0.0.1

# Connexion SSH via VPN
ssh votre_utilisateur@10.0.0.1
```

Sur le serveur, vérifier que le client est connecté :

```bash
sudo wg show
# Doit afficher "latest handshake" avec la date/heure récente
```

---

### 🔄 Flux de connexion

```
PC Client → WireGuard (chiffré) → Box internet (UDP 51820) → Serveur → SSH local
```

---

### ➕ Ajouter d'autres clients (smartphone, etc.)

Pour chaque nouveau client, générer une nouvelle paire de clés et ajouter un bloc `[Peer]` supplémentaire dans `/etc/wireguard/wg0.conf` avec une IP unique (`10.0.0.3/32`, `10.0.0.4/32`, etc.).

```bash
sudo wg set wg0 peer NOUVELLE_CLIENT_PUBLIC_KEY allowed-ips 10.0.0.3/32
sudo wg-quick save wg0
```

## 🐛 Dépannage

### SSH refuse la connexion
```bash
# Vérifier que le service tourne
sudo systemctl status ssh

# Voir les logs
sudo tail -f /var/log/auth.log
```

### Connexion lente
```bash
# Désactiver DNS lookup
sudo nano /etc/ssh/sshd_config
# Ajouter : UseDNS no
sudo systemctl restart ssh
```

### Clé SSH refusée
```bash
# Vérifier les permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

## 📝 Checklist mode headless

Avant de déconnecter écran/clavier :

- [ ] SSH fonctionne depuis un autre PC
- [ ] Authentification par clé configurée
- [ ] IP statique configurée (ou DHCP reservation sur routeur)
- [ ] Testé un reboot et reconnexion SSH
- [ ] Fail2ban installé (optionnel)







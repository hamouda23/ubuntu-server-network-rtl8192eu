# Configuration SSH sécurisée

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







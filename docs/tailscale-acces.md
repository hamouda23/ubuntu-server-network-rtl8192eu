# Accès distant au serveur HP Z800 via Tailscale

Guide pour se connecter au serveur Z800 depuis n'importe où, sans VPN complexe.

---

## 🧠 Qu'est-ce que Tailscale ?

Tailscale crée un réseau privé virtuel (VPN mesh) entre tes appareils.
Une fois installé, le Z800 est accessible via une IP fixe `100.86.17.82`, **même depuis chez toi**, sans avoir à ouvrir des ports ou configurer un routeur.

---

## 📋 Ce dont tu as besoin

- Un compte Tailscale (gratuit)
- Une invitation envoyée par Samir (voir Étape 2)
- Un client SSH (terminal sur Linux/Mac, PuTTY ou Windows Terminal sur Windows)

---

## Étape 1 — Créer un compte Tailscale

1. Va sur [https://tailscale.com](https://tailscale.com)
2. Clique sur **"Get started"**
3. Connecte-toi avec ton compte Google, GitHub ou Microsoft (le plus simple)

---

## Étape 2 — Demander une invitation à Samir

Tailscale permet de **partager un appareil** sans avoir le même compte.

**Samir doit faire ça (une seule fois) :**

```bash
# Sur le Z800, partager l'accès avec le binôme
tailscale share create --to <email-du-binome@gmail.com>
```

Ou via l'interface web Tailscale :
- Aller sur [https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines)
- Cliquer sur le Z800 (`ai` / `100.86.17.82`)
- Cliquer sur **"Share"** → entrer l'email du binôme → envoyer l'invitation

**Le binôme reçoit un email** avec un lien pour accepter l'accès.

---

## Étape 3 — Installer Tailscale sur ta machine

### Linux (Ubuntu/Debian)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Le terminal va afficher un lien — ouvre-le dans ton navigateur pour authentifier.

### Windows

1. Télécharge l'installateur depuis [https://tailscale.com/download/windows](https://tailscale.com/download/windows)
2. Lance l'installateur `.exe`
3. Tailscale apparaît dans la barre des tâches (icône)
4. Clique dessus → **"Log in"** → connecte-toi avec ton compte

### macOS

```bash
brew install tailscale
sudo tailscale up
```

Ou télécharge depuis le Mac App Store : cherche "Tailscale".

---

## Étape 4 — Vérifier que le Z800 est visible

Une fois connecté à Tailscale, vérifie que tu vois le serveur :

```bash
tailscale status
```

Tu dois voir une ligne avec `100.86.17.82` (le Z800).

---

## Étape 5 — Se connecter en SSH au Z800

```bash
ssh samir@100.86.17.82
```

La première connexion demande de confirmer l'empreinte du serveur — tape `yes`.

> **Si tu as une erreur "Permission denied"** : Samir doit t'ajouter une clé SSH ou activer l'authentification par mot de passe. Demande-lui.

---

## Commandes utiles

| Action | Commande |
|--------|----------|
| Vérifier le statut Tailscale | `tailscale status` |
| Voir son IP Tailscale | `tailscale ip` |
| Se connecter au Z800 | `ssh samir@100.86.17.82` |
| Copier un fichier vers le Z800 | `scp fichier.py samir@100.86.17.82:/mnt/deep-learning/` |
| Ouvrir un tunnel VNC | `ssh -L 5900:localhost:5900 samir@100.86.17.82` |
| Déconnecter Tailscale | `tailscale down` |

---

## Problèmes fréquents

### "connection timed out" ou "no route to host"

- Vérifie que Tailscale tourne sur **ta machine** : `tailscale status`
- Vérifie que Tailscale tourne sur le **Z800** : demande à Samir
- Accepte bien l'invitation reçue par email

### "Permission denied (publickey)"

SSH sur le Z800 utilise l'authentification par clé. Pour ajouter ta clé :

```bash
# Sur ta machine : générer une clé si tu n'en as pas
ssh-keygen -t ed25519 -C "ton-email@gmail.com"

# Envoyer ta clé au Z800 (Samir doit l'approuver)
# Envoie le contenu de ~/.ssh/id_ed25519.pub à Samir
cat ~/.ssh/id_ed25519.pub
```

Samir l'ajoute sur le Z800 :
```bash
echo "ta-clé-publique" >> ~/.ssh/authorized_keys
```

### Tailscale bloqué derrière un firewall d'école/entreprise

Tailscale utilise le port UDP 41641 ou tombe en repli sur HTTPS (port 443).
Si UDP est bloqué, Tailscale bascule automatiquement — ça marche dans la plupart des cas.

---

## Référence rapide

| Info | Valeur |
|------|--------|
| IP Tailscale du Z800 | `100.86.17.82` |
| Utilisateur SSH | `samir` |
| OS du serveur | Ubuntu 22.04 LTS |
| GPU | NVIDIA Quadro P4000 (8 GB) |

---

*Documentation générée le 2026-05-19 — Tailscale v1.96.4*

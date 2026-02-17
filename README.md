# HP Z800 - Serveur Deep Learning & NAS

Transformation d'une HP Z800 Workstation (2009) en serveur Ubuntu pour Deep Learning et stockage NAS.

## 🎯 Objectifs du projet

- ✅ **Serveur headless** : Accès distant SSH, sans écran/clavier
- ✅ **Wi-Fi stable** : Adaptateur USB Realtek RTL8192EU fonctionnel
- 🚧 **Deep Learning** : Utilisation du GPU NVIDIA Quadro P4000 pour l'entraînement de modèles
- ⏳ **NAS** : Serveur de stockage réseau
- ✅ **Disponibilité 24/7** : Monitoring et reconnexion automatique

## 🔧 Matériel

| Composant | Spécifications |
|-----------|---------------|
| **Modèle** | HP Z800 Workstation (2009-2010) |
| **CPU** | 2× Intel Xeon E5640 @ 2.67 GHz (8 cœurs, 16 threads) |
| **RAM** | 12 GB DDR3 ECC (actuellement ~4 GB utilisables) |
| **GPU** | NVIDIA Quadro P4000 (8 GB GDDR5, 1792 CUDA cores) |
| **Wi-Fi** | Adaptateur USB Realtek RTL8192EU (ID: 0bda:818b) |
| **OS** | Ubuntu Server 22.04 LTS (noyau 6.8.0-40-generic HWE) |

## 📊 État d'avancement

- [x] ✅ Installation Ubuntu Server 22.04
- [x] ✅ Configuration Wi-Fi RTL8192EU
- [x] ✅ Configuration SSH sécurisée
- [x] ✅ Installation pilotes NVIDIA + CUDA
- [x] ✅ Configuration environnement Deep Learning (PyTorch/TensorFlow)
- [x] ✅ Configuration NAS (Samba/NFS)
- [x] ✅ Monitoring système

## 🛜 Configuration Wi-Fi (Résolue)

### Problème
L'adaptateur RTL8192EU n'est pas supporté nativement par le pilote `rtl8xxxu` du noyau Linux.

### Solution
Utilisation du pilote [Mange RTL8192EU](https://github.com/Mange/rtl8192eu-linux-driver) via DKMS.

### Étapes suivies

**1. Installation des dépendances**
```bash
sudo apt install build-essential dkms git linux-headers-$(uname -r)
```

**2. Blacklist du pilote natif**
```bash
echo "blacklist rtl8xxxu" | sudo tee /etc/modprobe.d/rtl8xxxu.conf
```

**3. Installation du pilote Mange**
```bash
git clone https://github.com/Mange/rtl8192eu-linux-driver.git
cd rtl8192eu-linux-driver
sudo dkms add .
sudo dkms install rtl8192eu/1.0
```

**4. Désactivation du power management**
```bash
echo "options rtl8192eu rtw_power_mgnt=0 rtw_enusbss=0" | sudo tee /etc/modprobe.d/rtl8192eu.conf
```

**5. Redémarrage et vérification**
```bash
sudo reboot
# Après redémarrage
ip link show  # Interface wlx001ea63024db doit apparaître
```

### Configuration Netplan

Fichier : `/etc/netplan/50-cloud-init.yaml`

```yaml
network:
  version: 2
  renderer: networkd
  wifis:
    wlx001ea63024db:
      dhcp4: true
      optional: true
      access-points:
        "VOTRE_SSID":
          password: "VOTRE_MOT_DE_PASSE"
```

Application :
```bash
sudo netplan apply
ping -c 4 8.8.8.8  # Test de connexion
```

### Résultat
- ✅ Interface Wi-Fi détectée : `wlx001ea63024db`
- ✅ Connexion stable
- ✅ Scan des réseaux fonctionnel
- ✅ Reconnexion automatique après reboot

## 🚀 Prochaines étapes

### 1. SSH sécurisé
- Installation OpenSSH
- Authentification par clé
- Fail2ban pour sécurité

### 2. Deep Learning
- Installation pilotes NVIDIA (version compatible P4000)
- Installation CUDA Toolkit
- Installation PyTorch avec support GPU
- Tests de performance GPU

### 3. NAS
- Configuration Samba ou NFS
- Montage réseau
- Backup automatique

## 📚 Documentation

- [Guide Wi-Fi RTL8192EU](docs/wifi-rtl8192eu.md) - Configuration complète de l'adaptateur Wi-Fi

### Fichiers de configuration

- [Guide technique détaillé GPU et termes Deep Learning](docs/gpu-technical-guide.md)
- [Netplan Wi-Fi + Ethernet](config/netplan/50-cloud-init.yaml.example)
- [Blacklist rtl8xxxu](config/modprobe.d/rtl8xxxu.conf)
- [Options RTL8192EU](config/modprobe.d/rtl8192eu.conf)
- [Guide Wi-Fi RTL8192EU](docs/wifi-rtl8192eu.md) - Configuration complète de l'adaptateur Wi-Fi
- [Guide Wi-Fi RTL8192EU](docs/wifi-rtl8192eu.md) - Configuration avec NetworkManager
- [Guide SSH sécurisé](docs/ssh-setup.md) - Accès distant et sécurisation
- [Netplan Wi-Fi + Ethernet](config/netplan/50-cloud-init.yaml.example)
- [Blacklist rtl8xxxu](config/modprobe.d/rtl8xxxu.conf)
- [Options RTL8192EU](config/modprobe.d/rtl8192eu.conf)
- [Guide Deep Learning NVIDIA/CUDA](docs/deep-learning-setup.md) - Configuration GPU pour Deep Learning
- [Benchmark GPU](docs/gpu-benchmark.md) - Résultats de performance Quadro P4000
- [Configuration stockage](docs/storage-setup.md)
- [Configuration stockage Final](docs/storage-final-setup.md)


## 🐛 Problèmes connus

- **RAM limitée** : Seulement ~4 GB utilisables sur 12 GB installés (à investiguer)
- **Wi-Fi après mise à jour kernel** : Nécessite recompilation du module DKMS

## 🙏 Ressources

- [Mange RTL8192EU Driver](https://github.com/Mange/rtl8192eu-linux-driver)
- [Ubuntu Server Documentation](https://ubuntu.com/server/docs)
- [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/)

---

**Dernière mise à jour** : 2025-01-12  
**Statut** : 🚧 En développement actif

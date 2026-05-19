# Installation VM KVM pour Blender avec GPU Passthrough
**Serveur** : HP Z800 | **Date** : 2026-05-10 | **OS** : Ubuntu 22.04

---

## Contexte et problème de départ

### Pourquoi une VM ?
L'objectif est de faire tourner **Blender** avec accès au GPU (Quadro P4000) tout en gardant
**Ollama** opérationnel pour OpenClaw. Le problème central :

- Blender-MCP nécessite une interface graphique → impossible sur serveur headless
- Xvfb (affichage virtuel) = trop lourd
- bpy standalone = rendu médiocre
- **Solution retenue** : VM KVM avec GPU passthrough dynamique

### Conflit GPU entre Ollama et Blender

Un GPU ne peut pas être partagé entre le système hôte et une VM en même temps.
Il faut choisir à chaque utilisation :

```
Mode Ollama  → driver nvidia   sur la P4000 (host)
Mode Blender → driver vfio-pci sur la P4000 (VM)
```

Le switching se fait manuellement : arrêt Ollama → détachement nvidia → attachement vfio-pci → démarrage VM.

---

## Configuration matérielle

| Composant | Détail |
|-----------|--------|
| Machine | HP Z800 |
| GPU principal | NVIDIA Quadro P4000 — 8 GB GDDR5 |
| GPU secondaire | NVIDIA Quadro 400 (ancien, non utilisé) |
| CPU | 16 cores Intel (VT-x activé) |
| RAM | 32 GB |

### Disques
| Disque | Taille | Montage | Usage |
|--------|--------|---------|-------|
| sda | 111.8 GB | `/` | OS Ubuntu |
| sdb | 931.5 GB | `/mnt/deep-learning` | IA / OpenClaw |
| sdc | 232.9 GB | `/mnt/storage2` | Stockage |
| sdd | 931.5 GB | `/mnt/storage1` | VM + ISO |

---

## Étape 1 — Vérifier le support IOMMU et virtualisation

### Qu'est-ce que l'IOMMU ?
L'IOMMU (Input-Output Memory Management Unit) permet d'isoler les périphériques PCI
pour les passer à une VM. Sans IOMMU, le GPU passthrough est impossible.

```bash
# Vérifier que le CPU supporte la virtualisation (vmx = Intel, svm = AMD)
# Résultat attendu : nombre > 0
egrep -c '(vmx|svm)' /proc/cpuinfo
# Résultat obtenu : 16 ✅

# Vérifier la présence de DMAR (table IOMMU Intel VT-d dans le BIOS)
sudo dmesg | grep -e DMAR -e IOMMU | head -5
# Résultat obtenu : DMAR table présente ✅ mais IOMMU pas encore activé dans le kernel
```

---

## Étape 2 — Activer IOMMU dans GRUB

### Pourquoi ?
Le hardware supporte IOMMU mais le kernel Linux ne l'active pas par défaut.
Il faut passer les paramètres au kernel via GRUB au démarrage.

```bash
sudo nano /etc/default/grub
```

Modifier la ligne :
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash intel_iommu=on iommu=pt"
```

- `intel_iommu=on` : active l'IOMMU Intel VT-d
- `iommu=pt` : mode "passthrough", optimise les performances

```bash
# Régénérer la configuration GRUB et redémarrer
sudo update-grub && sudo reboot
```

### Vérification après reboot
```bash
sudo dmesg | grep -e "IOMMU enabled" -e "Intel-IOMMU"
# Résultat obtenu : [0.072019] DMAR: IOMMU enabled ✅
```

---

## Étape 3 — Installer KVM

### Qu'est-ce que KVM ?
KVM (Kernel-based Virtual Machine) est le système de virtualisation intégré au kernel Linux.
- **qemu-kvm** : émulateur qui fait tourner la VM
- **libvirt** : daemon qui gère les VMs (démarrage, arrêt, réseau)
- **virt-manager** : interface graphique optionnelle
- **bridge-utils** : gestion du réseau virtuel

```bash
sudo apt install qemu-kvm libvirt-daemon-system virt-manager bridge-utils -y
```

Pendant l'installation, Ubuntu demande quels services redémarrer → valider avec Ok (par défaut).

### Vérification
```bash
kvm --version
# QEMU emulator version 6.2.0 ✅

sudo systemctl status libvirtd
# Active: active (running) ✅
```

---

## Étape 4 — Identifier le GPU pour VFIO

### Qu'est-ce que VFIO ?
VFIO (Virtual Function I/O) est le driver Linux qui permet de "réserver" un périphérique
PCI pour une VM, en l'isolant du système hôte.

```bash
# Trouver l'adresse PCI de la P4000
lspci | grep -i nvidia
# 42:00.0 VGA compatible controller: NVIDIA GP104GL [Quadro P4000]
# 42:00.1 Audio device: NVIDIA GP104 High Definition Audio Controller

# Obtenir les IDs vendor:device nécessaires pour VFIO
lspci -n -s 42:00
# 42:00.0 0300: 10de:1bb1 (GPU)
# 42:00.1 0403: 10de:10f0 (Audio HDMI du GPU)
```

Il faut passer les DEUX composants (GPU + audio) à VFIO — ils forment un groupe IOMMU.

---

## Étape 5 — Configurer VFIO

```bash
# Dire à vfio-pci quels périphériques il doit gérer
echo "options vfio-pci ids=10de:1bb1,10de:10f0" | sudo tee /etc/modprobe.d/vfio.conf

# Charger les modules VFIO au démarrage du kernel
echo -e "vfio\nvfio_iommu_type1\nvfio_pci\nvfio_virqfd" | sudo tee /etc/modules-load.d/vfio.conf
```

- `vfio` : module de base
- `vfio_iommu_type1` : gestion des groupes IOMMU
- `vfio_pci` : binding des périphériques PCI
- `vfio_virqfd` : gestion des interruptions virtuelles

```bash
# Mettre à jour l'initramfs pour inclure les modules au boot
sudo update-initramfs -u && sudo reboot
```

### Vérification après reboot
```bash
lspci -k -s 42:00
# 42:00.0 Kernel driver in use: nvidia   ← normal (voir section Problème ci-dessous)
# 42:00.1 Kernel driver in use: vfio-pci ✅
```

### Problème rencontré : GPU toujours sur driver nvidia

**Cause** : nvidia se charge avant vfio-pci au démarrage. C'est voulu dans notre cas
car on veut garder Ollama fonctionnel sur le host.

**Solution retenue** : switching dynamique (pas de binding permanent à vfio-pci).
Un script bascule le driver selon le mode d'utilisation.

---

## Étape 6 — Ajouter l'utilisateur aux groupes KVM

```bash
# Permettre à samir de gérer les VMs sans sudo
sudo usermod -aG libvirt,kvm samir && newgrp libvirt
```

---

## Étape 7 — Créer la VM

```bash
# Télécharger l'ISO Ubuntu Desktop 22.04
wget -P /mnt/storage1/ https://releases.ubuntu.com/22.04/ubuntu-22.04.5-desktop-amd64.iso
# Taille : 4.44 GB — durée : ~20 min

# Créer le disque virtuel de la VM (format qcow2 = taille dynamique)
sudo qemu-img create -f qcow2 /mnt/storage1/blender-vm.qcow2 80G
```

### Qu'est-ce que qcow2 ?
Format de disque virtuel QEMU. Avantages :
- Taille dynamique (n'occupe pas 80 GB réels immédiatement)
- Supporte les snapshots
- Compression intégrée

```bash
# Créer et démarrer la VM
sudo virt-install \
  --name blender-vm \
  --ram 16384 \
  --vcpus 8 \
  --disk path=/mnt/storage1/blender-vm.qcow2,format=qcow2 \
  --cdrom /mnt/storage1/ubuntu-22.04.5-desktop-amd64.iso \
  --os-variant ubuntu22.04 \
  --graphics vnc,listen=0.0.0.0 \
  --noautoconsole \
  --boot cdrom,hd
```

- `--ram 16384` : 16 GB RAM pour la VM
- `--vcpus 8` : 8 cœurs CPU
- `--graphics vnc,listen=0.0.0.0` : accès via VNC sur toutes les interfaces
- `--noautoconsole` : ne pas ouvrir de console locale
- `--boot cdrom,hd` : démarrer sur l'ISO, puis sur le disque

---

## Étape 8 — Accès VNC à la VM

### Problème : connexion refusée depuis Windows

**Cause** : le serveur est accessible uniquement via Tailscale SSH, pas directement.
Le port 5900 (VNC) n'est pas exposé publiquement.

**Solution** : tunnel SSH

```bash
# Sur la machine Windows (PowerShell)
# Redirige le port 5900 du serveur vers localhost:5900 en local
ssh -L 5900:localhost:5900 samir@100.86.17.82

# Puis dans VNC Viewer se connecter à :
localhost:5900
```

### Commandes de gestion VM
```bash
sudo virsh list --all          # lister toutes les VMs
sudo virsh start blender-vm    # démarrer la VM
sudo virsh shutdown blender-vm # arrêter proprement la VM
sudo virsh destroy blender-vm  # forcer l'arrêt
sudo virsh vncdisplay blender-vm  # afficher le port VNC
```

---

## À faire (prochaines étapes)

- [ ] Finaliser l'installation Ubuntu dans la VM via VNC
- [ ] Installer les drivers NVIDIA dans la VM
- [ ] Installer Blender dans la VM
- [ ] Créer le script de switching dynamique GPU (nvidia ↔ vfio-pci)
- [ ] Tester le GPU passthrough avec Blender

---

## Résumé des fichiers modifiés

| Fichier | Modification |
|---------|-------------|
| `/etc/default/grub` | Ajout `intel_iommu=on iommu=pt` |
| `/etc/modprobe.d/vfio.conf` | IDs GPU pour vfio-pci |
| `/etc/modules-load.d/vfio.conf` | Modules VFIO au démarrage |
| `/mnt/storage1/blender-vm.qcow2` | Disque VM 80 GB |
| `/mnt/storage1/ubuntu-22.04.5-desktop-amd64.iso` | ISO Ubuntu |

# Configuration finale du stockage

Configuration complète des 4 disques physiques de la HP Z800 Workstation.

## 📊 Vue d'ensemble des disques

### Configuration matérielle

| Disque physique | Device | Taille | Type | Point de montage | Utilisation |
|-----------------|--------|--------|------|------------------|-------------|
| **SSD Kingston** | /dev/sda | 112 GB | SSD | `/` | Système Ubuntu |
| **HDD Seagate 1** | /dev/sdb | 931 GB | HDD | `/mnt/deep-learning` | Projets Deep Learning actifs |
| **HDD Seagate 2** | /dev/sdc | 233 GB | HDD | `/mnt/storage2` | Stockage général |
| **HDD Seagate 3** | /dev/sdd | 931 GB | HDD | `/mnt/storage1` | Stockage général |

### Espace disponible
```bash
$ df -h
/dev/mapper/ubuntu--vg-ubuntu--lv  108G   34G   69G  34% /
/dev/sdb1                          916G   19G  852G   3% /mnt/deep-learning
/dev/sdc1                          229G   48K  217G   1% /mnt/storage2
/dev/sdd1                          916G   28K  870G   1% /mnt/storage1
```

**Total disponible** : ~1.9 To

## 🔧 Configuration détaillée

### Disque 1 : SSD Système (sda - 112 GB)

**Utilisation** : Système Ubuntu Server 22.04 uniquement
```bash
Partitions :
├── sda1 (1 MB)   : BIOS boot
├── sda2 (2 GB)   : /boot
└── sda3 (110 GB) : / (LVM)
```

**Ne PAS utiliser pour** :
- ❌ Projets Deep Learning (manque d'espace)
- ❌ Datasets volumineux
- ❌ Checkpoints de modèles

**Réservé pour** :
- ✅ Système d'exploitation
- ✅ Packages système
- ✅ Miniconda (environnements Python)
- ✅ Configurations système

### Disque 2 : HDD Deep Learning (sdb - 931 GB)

**Point de montage** : `/mnt/deep-learning`  
**Format** : ext4  
**UUID** : [À compléter avec votre UUID]

**Structure des dossiers** :
```
/mnt/deep-learning/
├── projects/          # Code source des projets
├── datasets/          # Datasets (CIFAR, ImageNet, etc.)
├── models/            # Modèles pré-entraînés téléchargés
├── checkpoints/       # Sauvegardes pendant entraînement
├── results/           # Résultats, logs, graphiques
└── miniconda3/        # Environnements conda
```

**Lien symbolique** : `~/dl` → `/mnt/deep-learning`

**Configuration** :
```bash
# Montage automatique dans /etc/fstab
UUID=VOTRE_UUID /mnt/deep-learning ext4 defaults 0 2

# Création de la structure
mkdir -p /mnt/deep-learning/{projects,datasets,models,checkpoints,results}

# Lien symbolique
ln -s /mnt/deep-learning ~/dl

# Permissions
sudo chown -R samir:samir /mnt/deep-learning
```

### Disque 3 : HDD Storage 1 (sdd - 931 GB)

**Point de montage** : `/mnt/storage1`  
**Format** : ext4  
**UUID** : 2bdd9b96-a337-461d-8945-cb91c9b34681

**Utilisations recommandées** :
- 📦 Datasets volumineux (ImageNet, COCO)
- 🎬 Données vidéo pour Computer Vision
- 📊 Résultats d'expériences archivés
- 💾 Backup manuel de projets importants

**Montage automatique** :
```bash
# Dans /etc/fstab
UUID=2bdd9b96-a337-461d-8945-cb91c9b34681 /mnt/storage1 ext4 defaults 0 2
```

### Disque 4 : HDD Storage 2 (sdc - 233 GB)

**Point de montage** : `/mnt/storage2`  
**Format** : ext4  
**UUID** : 1a3fc3fd-a33e-4ac7-b814-be5acf02a557

**Utilisations recommandées** :
- 📚 Documentation et papiers de recherche
- 🖼️ Datasets moyens (MNIST, CIFAR, Fashion-MNIST)
- 📝 Résultats de benchmarks
- 🔬 Projets terminés archivés

**Montage automatique** :
```bash
# Dans /etc/fstab
UUID=1a3fc3fd-a33e-4ac7-b814-be5acf02a557 /mnt/storage2 ext4 defaults 0 2
```

## 📁 Organisation recommandée des projets

### Projet Deep Learning type
```
/mnt/deep-learning/projects/mon-projet/
├── src/
│   ├── train.py
│   ├── model.py
│   ├── dataset.py
│   └── utils.py
├── configs/
│   └── config.yaml
├── notebooks/
│   └── exploration.ipynb
├── data/              # Lien symbolique vers dataset
│   └── -> /mnt/storage1/datasets/cifar10/
├── checkpoints/
│   ├── epoch_10.pth
│   └── best_model.pth
├── results/
│   ├── logs/
│   └── tensorboard/
├── requirements.txt
└── README.md
```

### Workflow de développement
```bash
# 1. Créer un nouveau projet
cd ~/dl/projects
mkdir my-new-project
cd my-new-project

# 2. Activer environnement conda
conda activate ml

# 3. Créer structure
mkdir -p {src,configs,notebooks,checkpoints,results}

# 4. Lier dataset (si volumineux)
ln -s /mnt/storage1/datasets/imagenet data

# 5. Développer
code .  # Ouvrir dans VSCode
```

## 🔄 Montage automatique (fstab)

### Configuration complète

Fichier : `/etc/fstab`
```bash
# Disque système (automatique via LVM)
/dev/mapper/ubuntu--vg-ubuntu--lv / ext4 defaults 0 1
/dev/sda2 /boot ext4 defaults 0 2

# Disque Deep Learning principal (931 GB)
UUID=VOTRE_UUID_SDB1 /mnt/deep-learning ext4 defaults 0 2

# Disques de stockage additionnels
UUID=2bdd9b96-a337-461d-8945-cb91c9b34681 /mnt/storage1 ext4 defaults 0 2
UUID=1a3fc3fd-a33e-4ac7-b814-be5acf02a557 /mnt/storage2 ext4 defaults 0 2
```

### Signification des options

| Colonne | Valeur | Signification |
|---------|--------|---------------|
| 1 | UUID=xxx | Identifiant unique du disque |
| 2 | /mnt/xxx | Point de montage |
| 3 | ext4 | Type de système de fichiers |
| 4 | defaults | Options de montage (rw, suid, dev, etc.) |
| 5 | 0 | Dump (backup) : 0 = pas de backup automatique |
| 6 | 2 | fsck ordre : 1 = prioritaire (/), 2 = secondaire |

### Test du montage automatique
```bash
# Démonter tous les disques externes
sudo umount /mnt/deep-learning
sudo umount /mnt/storage1
sudo umount /mnt/storage2

# Remonter automatiquement via fstab
sudo mount -a

# Vérifier
df -h | grep mnt
```

**Résultat attendu** :
```
/dev/sdb1  916G  19G  852G   3% /mnt/deep-learning
/dev/sdc1  229G  48K  217G   1% /mnt/storage2
/dev/sdd1  916G  28K  870G   1% /mnt/storage1
```

## 🛠️ Commandes utiles

### Gestion des disques
```bash
# Lister tous les disques
lsblk

# Voir l'espace utilisé
df -h

# Taille d'un dossier spécifique
du -sh /mnt/deep-learning/projects/

# UUID des disques
sudo blkid

# Informations détaillées
sudo fdisk -l
```

### Montage/Démontage manuel
```bash
# Monter un disque
sudo mount /dev/sdb1 /mnt/deep-learning

# Démonter
sudo umount /mnt/deep-learning

# Forcer le démontage (si occupé)
sudo umount -l /mnt/deep-learning

# Voir ce qui utilise le disque
sudo lsof | grep deep-learning
sudo fuser -m /dev/sdb1
```

### Vérification santé des disques
```bash
# État SMART des disques
sudo apt install smartmontools
sudo smartctl -H /dev/sdb
sudo smartctl -H /dev/sdc
sudo smartctl -H /dev/sdd

# Test de lecture/écriture (attention: destructif!)
# sudo hdparm -Tt /dev/sdb
```

## 📊 Monitoring de l'espace

### Script de monitoring

Créer `/home/samir/scripts/check-disk-space.sh` :
```bash
#!/bin/bash

echo "=== État des disques ==="
echo ""

df -h | grep -E "Filesystem|/dev/sd|/dev/mapper" | \
    awk '{printf "%-30s %10s %10s %10s %5s %s\n", $1, $2, $3, $4, $5, $6}'

echo ""
echo "=== Alertes ==="

# Alerte si un disque > 90%
df -h | grep -E "/dev/sd|/dev/mapper" | awk '{
    usage = int($5)
    if (usage > 90) {
        printf "⚠️  ATTENTION: %s est plein à %d%%\n", $6, usage
    }
}'

echo ""
echo "=== Top 5 dossiers volumineux (deep-learning) ==="
du -sh /mnt/deep-learning/*/ 2>/dev/null | sort -rh | head -5
```
```bash
# Rendre exécutable
chmod +x ~/scripts/check-disk-space.sh

# Lancer
~/scripts/check-disk-space.sh
```

## 🔐 Permissions et sécurité

### Propriétaire des disques
```bash
# Tous les disques de travail appartiennent à l'utilisateur
sudo chown -R samir:samir /mnt/deep-learning
sudo chown -R samir:samir /mnt/storage1
sudo chown -R samir:samir /mnt/storage2

# Vérifier
ls -la /mnt/
```

### Permissions recommandées
```bash
# Lecture/écriture pour propriétaire, lecture pour groupe
chmod 755 /mnt/deep-learning
chmod 755 /mnt/storage1
chmod 755 /mnt/storage2
```

## 💡 Bonnes pratiques

### Organisation des datasets
```bash
# Datasets petits (< 5 GB) → /mnt/deep-learning/datasets/
/mnt/deep-learning/datasets/
├── cifar10/
├── mnist/
└── fashion-mnist/

# Datasets moyens (5-50 GB) → /mnt/storage2/datasets/
/mnt/storage2/datasets/
├── coco-subset/
├── celeba/
└── oxford-pets/

# Datasets volumineux (> 50 GB) → /mnt/storage1/datasets/
/mnt/storage1/datasets/
├── imagenet/
├── coco-full/
└── places365/
```

### Gestion des checkpoints
```bash
# Checkpoints actifs → /mnt/deep-learning/checkpoints/
# Meilleurs modèles → /mnt/deep-learning/models/best/
# Modèles archivés → /mnt/storage1/archived-models/
```

### Nettoyage régulier
```bash
# Supprimer les checkpoints intermédiaires (garder best + last)
cd /mnt/deep-learning/checkpoints/mon-projet/
ls -t *.pth | tail -n +3 | xargs rm

# Nettoyer cache pip/conda
conda clean --all -y
pip cache purge
```

## 🐛 Troubleshooting

### Disque non monté au démarrage

**Symptôme** : Après reboot, `/mnt/deep-learning` est vide

**Solution** :
```bash
# Vérifier fstab
cat /etc/fstab | grep deep-learning

# Vérifier les logs
sudo journalctl -b | grep mount

# Monter manuellement
sudo mount -a

# Si erreur UUID, mettre à jour fstab avec bon UUID
sudo blkid /dev/sdb1
sudo nano /etc/fstab
```

### Erreur "Device or resource busy"

**Symptôme** : Impossible de démonter un disque

**Solution** :
```bash
# Trouver ce qui utilise le disque
sudo lsof | grep /mnt/deep-learning
sudo fuser -m /dev/sdb1

# Tuer les processus
sudo kill -9 PID_DU_PROCESSUS

# Ou forcer le démontage
sudo umount -l /mnt/deep-learning
```

### Disque en lecture seule

**Symptôme** : "Read-only file system"

**Solution** :
```bash
# Remonter en lecture-écriture
sudo mount -o remount,rw /mnt/deep-learning

# Si ça persiste, vérifier le disque
sudo fsck -y /dev/sdb1
```

## 📈 Évolution future

### Upgrades possibles

- [ ] Ajouter SSD NVMe (PCIe) pour cache de datasets
- [ ] RAID 1 sur les 2× HDD 1 To pour redondance
- [ ] NAS réseau pour backup automatique
- [ ] SSD plus grand pour système (500 GB)

### Migration vers configuration RAID

Si redondance nécessaire :
```bash
# RAID 1 avec sdb + sdd (931 GB miroir)
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdd1
```

---

**Dernière mise à jour** : 2026-01-17  
**Configuration testée** : HP Z800 + 4 disques (1× SSD + 3× HDD)  
**Espace total** : 2.1 To (~1.9 To disponible)
```

---

**Message de commit :**
```
docs: configuration complète stockage 4 disques (2 To)

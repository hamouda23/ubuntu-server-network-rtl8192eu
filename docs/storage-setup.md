# Configuration du stockage

Guide pour configurer les disques supplémentaires pour les projets Deep Learning.

## 📊 Configuration des disques

### Disques disponibles

| Disque | Modèle | Taille | Type | Utilisation |
|--------|--------|--------|------|-------------|
| **sda** | Kingston SV300S3 | 112 GB | SSD | Système Ubuntu (/) |
| **sdb** | Seagate ST3250318AS | 233 GB | HDD | Non utilisé |
| **sdc** | Intel SSDSA2M160 | 149 GB | SSD | **Stockage projets DL** |

### État actuel
```bash
$ df -h
/dev/mapper/ubuntu--vg-ubuntu--lv   54G   40G   12G  79% /
/dev/sdc1                          150G  7.6G  142G   6% /mnt/data
```

⚠️ **Disque système (sda) presque plein** : 79% utilisé, seulement 12 GB libres

✅ **Disque données (sdc1)** : 142 GB libres pour projets Deep Learning

## 🔧 Montage du disque sdc1

### 1. Installation du support NTFS
```bash
sudo apt install ntfs-3g -y
```

### 2. Création du point de montage
```bash
sudo mkdir -p /mnt/data
```

### 3. Montage manuel
```bash
sudo mount -t ntfs-3g /dev/sdc1 /mnt/data
```

### 4. Vérification
```bash
df -h | grep sdc
ls -la /mnt/data
```

### 5. Configuration des permissions
```bash
sudo chown -R samir:samir /mnt/data
```

### 6. Montage automatique au démarrage

**Trouver l'UUID du disque :**
```bash
sudo blkid /dev/sdc1
```

Résultat :
```
/dev/sdc1: LABEL="AMGIO" UUID="BE20A9E20AA5CE1" TYPE="ntfs"
```

**Éditer fstab :**
```bash
sudo nano /etc/fstab
```

**Ajouter à la fin :**
```
# Disque Intel SSD pour projets Deep Learning
UUID=BE20A9E20AA5CE1 /mnt/data ntfs-3g defaults,uid=1000,gid=1000 0 0
```

**Tester le montage :**
```bash
sudo umount /mnt/data
sudo mount -a
df -h | grep sdc
```

## 📁 Structure du projet Deep Learning

### Organisation des dossiers
```bash
/mnt/data/deep-learning/
├── projects/          # Code source des projets
├── datasets/          # Datasets (CIFAR, ImageNet, etc.)
├── models/            # Modèles pré-entraînés téléchargés
├── checkpoints/       # Sauvegardes pendant entraînement
└── results/           # Résultats, logs, graphiques
```

**Création de la structure :**
```bash
mkdir -p /mnt/data/deep-learning/{projects,datasets,models,checkpoints,results}
```

### Lien symbolique pour accès rapide
```bash
ln -s /mnt/data/deep-learning ~/dl

# Maintenant accessible via :
cd ~/dl
cd ~/dl/projects
cd ~/dl/datasets
```

## 🖥️ Configuration VSCode

### Ajouter le disque à l'espace de travail

1. Ouvrir VSCode connecté en SSH
2. `File` → `Add Folder to Workspace`
3. Entrer : `/mnt/data/deep-learning`
4. Cliquer OK

**Résultat dans l'explorateur :**
```
📁 SAMIR [SSH: 192.168.1.108]    ← /home/samir/
📁 deep-learning                  ← /mnt/data/deep-learning/
   📁 projects
   📁 datasets
   📁 models
   📁 checkpoints
   📁 results
```

## 💾 Utilisation pratique

### Créer un nouveau projet

**Méthode 1 : Via VSCode**

1. Clic droit sur `deep-learning/projects`
2. New Folder → `mon-projet`
3. New File → `train.py`

**Méthode 2 : Via terminal**
```bash
cd /mnt/data/deep-learning/projects
mkdir mon-nouveau-projet
cd mon-nouveau-projet

# Activer environnement conda
conda activate ml

# Créer fichiers
touch train.py model.py utils.py
```

### Où stocker quoi ?

| Type de fichier | Emplacement | Raison |
|----------------|-------------|--------|
| **Code Python** | `/mnt/data/deep-learning/projects/` | Espace disponible |
| **Datasets** | `/mnt/data/deep-learning/datasets/` | Peut être volumineux |
| **Checkpoints** | `/mnt/data/deep-learning/checkpoints/` | Sauvegardes fréquentes |
| **Modèles pré-entraînés** | `/mnt/data/deep-learning/models/` | ResNet, BERT, etc. |
| **Logs TensorBoard** | `/mnt/data/deep-learning/results/runs/` | Historique entraînements |
| **Scripts système** | `/home/samir/scripts/` | Petits fichiers système |

### Exemple complet
```bash
# Créer un projet CIFAR-10
cd /mnt/data/deep-learning/projects
mkdir cifar10-classification
cd cifar10-classification

# Activer environnement
conda activate ml

# Créer structure
mkdir {data,models,logs}
touch train.py model.py dataset.py config.py

# Le dataset sera téléchargé automatiquement dans data/
# Les checkpoints dans models/
# Les logs TensorBoard dans logs/
```

## 📊 Monitoring de l'espace disque

### Voir l'utilisation globale
```bash
df -h
```

### Voir l'utilisation par dossier
```bash
du -h --max-depth=1 /mnt/data/deep-learning/
```

### Trouver les gros fichiers
```bash
# Top 10 des plus gros fichiers
find /mnt/data/deep-learning/ -type f -exec du -h {} + | sort -rh | head -10
```

### Nettoyer l'espace
```bash
# Supprimer les anciens checkpoints
rm -rf /mnt/data/deep-learning/checkpoints/old_experiments/

# Supprimer les datasets non utilisés
rm -rf /mnt/data/deep-learning/datasets/unused/
```

## ⚠️ Précautions

### Sauvegarde

Le disque sdc1 est en NTFS (format Windows). Si vous reformatez la machine :

✅ **Avantages NTFS** :
- Lisible sous Windows si vous démarrez en dual-boot
- Pas besoin de backup pour réinstallation Ubuntu

⚠️ **Inconvénients NTFS** :
- Légèrement moins performant que ext4 (natif Linux)
- Permissions Unix limitées

### Alternative : Reformater en ext4

Si vous n'avez pas besoin de Windows :
```bash
# ⚠️ ATTENTION : Efface toutes les données !
sudo umount /mnt/data
sudo mkfs.ext4 /dev/sdc1

# Remonter
sudo mount /dev/sdc1 /mnt/data
```

**Avantages ext4** :
- ✅ Plus rapide (5-10%)
- ✅ Meilleure gestion des permissions
- ✅ Plus stable pour Linux

**Inconvénients ext4** :
- ❌ Non lisible sous Windows

## 🔍 Vérification de la configuration

### Checklist

- [ ] Disque sdc1 monté sur `/mnt/data`
- [ ] Permissions correctes (propriétaire : samir)
- [ ] Montage automatique configuré dans `/etc/fstab`
- [ ] Structure des dossiers créée
- [ ] Lien symbolique `~/dl` créé
- [ ] VSCode configuré avec les 2 workspaces
- [ ] Test d'écriture réussi

### Test d'écriture
```bash
# Créer un fichier test
echo "Test stockage Deep Learning" > /mnt/data/deep-learning/test.txt

# Lire via différents chemins
cat /mnt/data/deep-learning/test.txt
cat ~/dl/test.txt

# Les deux doivent afficher le même contenu ✅
```

## 📚 Commandes utiles
```bash
# Voir tous les disques
lsblk

# Détails des partitions
sudo fdisk -l

# Espace disque utilisé
df -h

# UUID des disques
sudo blkid

# Taille d'un dossier
du -sh /mnt/data/deep-learning/

# Monter manuellement
sudo mount /dev/sdc1 /mnt/data

# Démonter
sudo umount /mnt/data

# Vérifier le montage automatique
cat /etc/fstab | grep sdc
```

---

**Dernière mise à jour** : 2026-01-17  
**Configuration testée** : HP Z800 + 3 disques (sda, sdb, sdc)  
**Disque utilisé** : Intel SSD 149 GB (sdc1) monté sur `/mnt/data`
```

**Message de commit :**
```
docs: configuration complète du stockage sur disque sdc1

# Configuration Deep Learning - NVIDIA CUDA

Guide complet pour configurer le GPU NVIDIA Quadro P4000 pour le Deep Learning sur Ubuntu Server 22.04.

## 🎯 Objectifs

- Installer les pilotes NVIDIA
- Configurer CUDA Toolkit
- Installer PyTorch avec support GPU
- Tester les performances
- Préparer l'environnement pour Deep Learning

## 🔧 Matériel

- **GPU** : NVIDIA Quadro P4000
- **VRAM** : 8 GB GDDR5
- **CUDA Cores** : 1792
- **Architecture** : Pascal (Compute Capability 6.1)

## 📋 Prérequis

- [ ] Ubuntu Server 22.04 installé
- [ ] SSH configuré
- [ ] Connexion Internet stable

## 🚀 Installation des pilotes NVIDIA

### 1. Vérifier la détection du GPU

```bash
# Voir si le GPU est détecté
lspci | grep -i nvidia
```

Résultat attendu :
```
05:00.0 VGA compatible controller: NVIDIA Corporation GP104GL [Quadro P4000]
```

### 2. Mettre à jour le système

```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Ajouter le repository NVIDIA

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
```

### 4. Voir les pilotes disponibles

```bash
ubuntu-drivers devices
```

### 5. Installer le pilote recommandé

**Option A - Installation automatique (recommandé) :**
```bash
sudo ubuntu-drivers autoinstall
```

**Option B - Installation manuelle d'une version spécifique :**
```bash
# Installer une version spécifique (exemple: 535)
sudo apt install nvidia-driver-535
```

### 6. Redémarrer

```bash
sudo reboot
```

### 7. Vérifier l'installation

```bash
nvidia-smi
```

**Résultat attendu :**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xxx      Driver Version: 535.xxx      CUDA Version: 12.2    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Quadro P4000        Off  | 00000000:05:00.0 Off |                  N/A |
| 46%   32C    P8    10W / 105W |      0MiB /  8192MiB |      0%      Default |
+-----------------------------------------------------------------------------+
```

✅ Si vous voyez ça, les pilotes sont installés !

## 🔥 Installation CUDA Toolkit

### 1. Vérifier la version CUDA supportée

```bash
nvidia-smi
```

Notez la version CUDA affichée en haut à droite (ex: `CUDA Version: 12.2`)

### 2. Télécharger CUDA Toolkit

Pour CUDA 12.2 (adaptez selon votre version) :

```bash
# Télécharger le keyring
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb

# Installer le keyring
sudo dpkg -i cuda-keyring_1.1-1_all.deb

# Mettre à jour
sudo apt update
```

### 3. Installer CUDA

```bash
# Installer CUDA Toolkit (version 13.0)
sudo apt install cuda-toolkit-13-0

# Ou pour la dernière version disponible
sudo apt install cuda-toolkit
```

### 4. Configurer les variables d'environnement

```bash
# Éditer .bashrc
nano ~/.bashrc
```

Ajouter à la fin du fichier :

```bash
# CUDA Configuration
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

Sauvegarder (`Ctrl+O`, `Enter`, `Ctrl+X`)

```bash
# Recharger la configuration
source ~/.bashrc
```

### 5. Vérifier l'installation CUDA

```bash
nvcc --version
```

Résultat attendu :
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Tue_Aug_15_22:02:13_PDT_2023
Cuda compilation tools, release 12.2, V12.2.140
```

### 6. Test de compilation CUDA

```bash
# Compiler un exemple
cd /usr/local/cuda/samples/1_Utilities/deviceQuery
sudo make

# Exécuter
./deviceQuery
```

Résultat attendu affiche les détails de votre GPU ✅

docs: utilisation conda au lieu de venv pour Deep Learning

## 🐍 Configuration Python avec Conda

### 1. Installer Miniconda
```bash
# Télécharger Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Installer
bash Miniconda3-latest-Linux-x86_64.sh
```

Pendant l'installation :
- Appuyez sur `Enter` pour lire la licence
- Tapez `yes` pour accepter
- `Enter` pour l'emplacement par défaut
- `yes` pour initialiser conda
```bash
# Recharger le terminal
source ~/.bashrc

# Vérifier
conda --version
python --version
```

### 2. Créer un environnement conda
```bash
# Créer environnement Deep Learning avec Python 3.10
conda create -n ml python=3.10 -y

# Activer l'environnement
conda activate ml
```

Votre prompt devrait changer : `(ml) samir@ai:~$`

### 3. Mettre à jour conda
```bash
conda update conda -y
```
```

**Message de commit :**
```


## 🔥 Installation PyTorch avec CUDA

### 1. Vérifier la compatibilité CUDA

Allez sur https://pytorch.org/get-started/locally/

Installer PyTorch avec CUDA 12.1 (compatible avec votre CUDA 13.0) :

```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
```

Pour **CUDA 11.8** (si pilote plus ancien) :

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Tester PyTorch avec GPU

```bash
python3 << EOF
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Nombre de GPUs: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"GPU actuel: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Capability: {torch.cuda.get_device_capability(0)}")
EOF
```

**Résultat attendu :**
```
PyTorch version: 2.x.x
CUDA disponible: True
CUDA version: 12.1
Nombre de GPUs: 1
GPU actuel: Quadro P4000
CUDA Capability: (6, 1)
```

✅ Si `CUDA disponible: True`, c'est bon !

## 🧪 Test de performance GPU

### Test simple de calcul

```python
# Créer un fichier test
nano ~/gpu_test.py
```

Contenu :

```python
import torch
import time

# Vérifier CUDA
print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")

# Taille de la matrice
size = 10000

# Test sur CPU
print("\n--- Test CPU ---")
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

start = time.time()
c_cpu = torch.matmul(a_cpu, b_cpu)
cpu_time = time.time() - start
print(f"Temps CPU: {cpu_time:.4f} secondes")

# Test sur GPU
print("\n--- Test GPU ---")
a_gpu = torch.randn(size, size).cuda()
b_gpu = torch.randn(size, size).cuda()

# Warm-up
_ = torch.matmul(a_gpu, b_gpu)

start = time.time()
c_gpu = torch.matmul(a_gpu, b_gpu)
torch.cuda.synchronize()
gpu_time = time.time() - start
print(f"Temps GPU: {gpu_time:.4f} secondes")

print(f"\n🚀 Accélération: {cpu_time/gpu_time:.2f}x plus rapide sur GPU")
```

Exécuter :

```bash
python3 ~/gpu_test.py
```

Vous devriez voir une accélération significative ! 🚀

## 📦 Installation des bibliothèques Deep Learning

### Bibliothèques essentielles

```bash
# Activer l'environnement virtuel
source ~/ml-env/bin/activate

# NumPy, Pandas, Matplotlib
pip install numpy pandas matplotlib seaborn

# Jupyter Notebook (pour travailler depuis VSCode)
pip install jupyter ipykernel

# scikit-learn
pip install scikit-learn

# TensorBoard (monitoring)
pip install tensorboard

# Transformers (NLP)
pip install transformers

# OpenCV (vision)
pip install opencv-python
```

### Pour TensorFlow (alternative à PyTorch)

```bash
# TensorFlow avec GPU
pip install tensorflow[and-cuda]

# Tester TensorFlow
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## 🖥️ Configuration Jupyter depuis VSCode

### 1. Sur le serveur

```bash
# Activer l'environnement
source ~/ml-env/bin/activate

# Installer Jupyter kernel
python -m ipykernel install --user --name=ml-env
```

### 2. Sur VSCode (votre PC)

1. Installer l'extension **"Jupyter"** dans VSCode
2. Créer un fichier `.ipynb` sur le serveur
3. VSCode détecte automatiquement le kernel `ml-env`
4. Vous pouvez coder en Python avec support GPU ! 🎉

## 📊 Monitoring GPU

### nvidia-smi en continu

```bash
watch -n 1 nvidia-smi
```

### nvtop (monitoring interactif)

```bash
# Installer nvtop
sudo apt install nvtop

# Lancer
nvtop
```

### Depuis Python

```python
import torch

# Mémoire GPU utilisée
print(f"Mémoire allouée: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
print(f"Mémoire réservée: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
```

## 🐛 Dépannage

### CUDA not available

```bash
# Vérifier que les pilotes NVIDIA sont chargés
nvidia-smi

# Réinstaller PyTorch avec la bonne version CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### GPU non détecté après mise à jour kernel

```bash
# Réinstaller les headers
sudo apt install linux-headers-$(uname -r)

# Reconstruire le module NVIDIA
sudo dkms autoinstall
sudo reboot
```

### Out of Memory (OOM)

```python
# Vider le cache GPU
import torch
torch.cuda.empty_cache()

# Réduire la taille du batch dans votre code
```

### Vérifier la compatibilité CUDA

```bash
# Version du driver
nvidia-smi

# Version CUDA installée
nvcc --version

# Version CUDA supportée par PyTorch
python -c "import torch; print(torch.version.cuda)"
```

## 📝 Checklist finale

- [ ] `nvidia-smi` fonctionne
- [ ] `nvcc --version` fonctionne
- [ ] PyTorch installé : `pip list | grep torch`
- [ ] CUDA disponible dans PyTorch : `torch.cuda.is_available()` = True
- [ ] Test de performance GPU effectué
- [ ] Jupyter configuré dans VSCode
- [ ] Environnement virtuel créé

## 🚀 Exemples de projets Deep Learning

### Entraînement CNN simple

```python
import torch
import torch.nn as nn

# Modèle simple
model = nn.Sequential(
    nn.Conv2d(3, 64, 3),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(64 * 31 * 31, 10)
).cuda()

# Données d'exemple
x = torch.randn(32, 3, 64, 64).cuda()  # Batch de 32 images
y = model(x)

print(f"Input shape: {x.shape}")
print(f"Output shape: {y.shape}")
print("✅ Modèle fonctionne sur GPU!")
```

### Transfer Learning avec ResNet

```python
import torch
import torchvision.models as models

# Charger ResNet pré-entraîné
model = models.resnet50(pretrained=True).cuda()
model.eval()

# Test
x = torch.randn(1, 3, 224, 224).cuda()
with torch.no_grad():
    y = model(x)

print(f"Prédictions: {y.shape}")
print("✅ Transfer Learning prêt!")
```

## 📚 Ressources

- [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- [TensorFlow GPU Guide](https://www.tensorflow.org/install/gpu)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)

## 🎓 Prochaines étapes

- [ ] Tester un projet de classification d'images
- [ ] Configurer TensorBoard pour monitoring
- [ ] Setup Docker pour isolation des environnements
- [ ] Configuration NAS pour stocker datasets
- [ ] Benchmarks comparatifs CPU vs GPU

---

**Dernière mise à jour** : 2025-01-17  
**Configuration testée** : NVIDIA Quadro P4000 + CUDA 13.0 + PyTorch 2.x

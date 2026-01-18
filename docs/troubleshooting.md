# Troubleshooting - Problèmes courants et solutions

## 🐛 Jupyter Kernel non détecté dans VSCode Remote SSH

### Problème
Les kernels conda n'apparaissent pas dans VSCode lors de la sélection du kernel pour les notebooks (.ipynb).

### Cause
Conflit de versions entre :
- Python du serveur
- Extension Jupyter de VSCode
- Extension Remote SSH

### Solution

**Downgrade des extensions VSCode** (sur le serveur distant) :

1. Dans VSCode connecté en SSH
2. Extensions → Jupyter
3. Clic droit → "Install Another Version"
4. Choisir une version antérieure stable

**Versions testées qui fonctionnent** :
- Jupyter : v2023.x.x (au lieu de 2024+)
- Python : v2023.x.x
- Remote SSH : [version stable]

### Vérification
```bash
# Sur le serveur
conda activate ml
jupyter kernelspec list

# Dans VSCode
# Ouvrir un .ipynb → Le kernel "Python (ML)" apparaît maintenant ✅
```

---

## 📝 Autres problèmes courants

[À compléter au fur et à mesure...]
```

**Message de commit :**
```
docs: solution conflit versions Jupyter VSCode Remote SSH

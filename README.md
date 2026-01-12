# Mon Serveur Ubuntu sur HP Z800 Workstation

## Objectif
Transformer une vieille station de travail HP Z800 en serveur Ubuntu fonctionnel avec :
- Connexion Wi-Fi stable (adaptateur USB Realtek RTL8192EU)
- Accès distant via SSH
- Headless (sans écran/clavier/souris après configuration)

## Matériel
- **Modèle** : HP Z800 Workstation (2009-2010)
- **CPU** : 2 × Intel Xeon E5640 @ 2.67 GHz (8 cœurs / 8 threads)
- **RAM** : ~12 GB DDR3 ECC (utilisable ~4 GB)
- **GPU** : NVIDIA Quadro P4000 (8 GB)
- **Wi-Fi** : Adaptateur USB Realtek RTL8192EU (ID 0bda:818b)
- **OS** : Ubuntu Server 22.04 LTS (noyau 6.8.0-40-generic HWE)

## Parcours et problèmes rencontrés
1. Interfaces Ethernet multiples
   
2. **Wi-Fi non détecté**  
   Le pilote intégré (`rtl8xxxu`) ne fonctionnait pas → pas d'interface.

3. **Tentatives avec pilote tiers**  
   - Installation du driver Mange (`rtl8192eu-linux-driver`) via DKMS.
   - Compilation réussie, mais interface absente ou instable (NO-CARRIER, timeout DHCP).

4. **Solutions testées**  
   - Blacklist `rtl8xxxu`
   - Désactivation power management : `rtw_power_mgnt=0 rtw_enusbss=0`
   - Firmware Realtek installé (`firmware-realtek`)
   - Plusieurs forks testés (Mange → clnhub)

5. **Succès final**  
   - Pilote Mange compilé et chargé correctement.
   - Interface `wlx001ea63024db` détectée.
   - Scan Wi-Fi fonctionnel (réseau BravoTelecom_G27 visible).
   - Connexion établie via netplan.

## Configuration finale

### Netplan (Wi-Fi)
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
        "B********_G**":
          password: "**********"

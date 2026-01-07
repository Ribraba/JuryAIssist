#!/usr/bin/env python3
"""
Script de Test - Détection et Analyse de la Pédale Olympus RS-31

Ce script permet de :
1. Détecter la pédale Olympus connectée
2. Identifier le Vendor ID et Product ID
3. Capturer les événements bruts de chaque bouton
4. Analyser les patterns pour le reverse engineering

Usage:
    python test_pedale.py
"""

import hid
import time
import sys
from typing import Optional, Dict, List


# ============================================================================
# CONFIGURATION
# ============================================================================

# Vendor ID connus pour Olympus
OLYMPUS_VENDOR_IDS = [
    0x07B4,  # Olympus Imaging Corp.
]

# Product IDs connus pour pédales Olympus
KNOWN_PEDAL_PRODUCT_IDS = {
    0x0203: "RS-28 (3 pédales)",
    0x0204: "RS-31H (3 pédales + boutons)",
    0x020D: "RS-31 (4 boutons)",
}


# ============================================================================
# FONCTIONS DE DÉTECTION
# ============================================================================

def list_all_hid_devices() -> None:
    """Liste tous les périphériques HID connectés"""
    print("\n" + "="*70)
    print("LISTE DE TOUS LES PÉRIPHÉRIQUES HID CONNECTÉS")
    print("="*70)
    
    devices = hid.enumerate()
    
    if not devices:
        print("⚠️  Aucun périphérique HID détecté")
        return
    
    for i, device in enumerate(devices, 1):
        print(f"\n[Device {i}]")
        print(f"  Vendor ID:       0x{device['vendor_id']:04x}")
        print(f"  Product ID:      0x{device['product_id']:04x}")
        print(f"  Manufacturer:    {device['manufacturer_string']}")
        print(f"  Product:         {device['product_string']}")
        print(f"  Serial:          {device['serial_number']}")
        print(f"  Path:            {device['path']}")


def find_olympus_pedal() -> Optional[Dict]:
    """
    Recherche spécifiquement une pédale Olympus
    
    Returns:
        Informations du device si trouvé, None sinon
    """
    print("\n" + "="*70)
    print("RECHERCHE DE PÉDALE OLYMPUS")
    print("="*70)
    
    devices = hid.enumerate()
    
    for device in devices:
        vendor_id = device['vendor_id']
        product_id = device['product_id']
        
        # Vérifier si c'est un device Olympus
        if vendor_id in OLYMPUS_VENDOR_IDS:
            print(f"\n✅ Pédale Olympus détectée!")
            print(f"  Vendor ID:       0x{vendor_id:04x}")
            print(f"  Product ID:      0x{product_id:04x}")
            
            # Identifier le modèle si connu
            if product_id in KNOWN_PEDAL_PRODUCT_IDS:
                model = KNOWN_PEDAL_PRODUCT_IDS[product_id]
                print(f"  Modèle:          {model}")
            else:
                print(f"  Modèle:          Inconnu (nouveau modèle?)")
            
            print(f"  Manufacturer:    {device['manufacturer_string']}")
            print(f"  Product:         {device['product_string']}")
            print(f"  Path:            {device['path']}")
            
            return device
    
    print("\n❌ Aucune pédale Olympus détectée")
    print("\nVérifiez que:")
    print("  1. La pédale est branchée")
    print("  2. Les drivers sont installés")
    print("  3. Vous avez les permissions d'accès USB")
    
    return None


# ============================================================================
# CAPTURE D'ÉVÉNEMENTS
# ============================================================================

def capture_pedal_events(vendor_id: int, product_id: int, duration: int = 60) -> None:
    """
    Capture les événements bruts de la pédale
    
    Args:
        vendor_id: Vendor ID du device
        product_id: Product ID du device
        duration: Durée de capture en secondes (défaut: 60s)
    """
    print("\n" + "="*70)
    print("CAPTURE D'ÉVÉNEMENTS (REVERSE ENGINEERING)")
    print("="*70)
    print(f"\nDurée de capture: {duration} secondes")
    print("\nInstructions:")
    print("  1. Appuyez sur BOUTON 1 puis relâchez")
    print("  2. Appuyez sur BOUTON 2 puis relâchez")
    print("  3. Appuyez sur BOUTON 3 puis relâchez")
    print("  4. Appuyez sur BOUTON 4 puis relâchez")
    print("  5. Testez des appuis simultanés si possible")
    print("\nFormat des événements: [byte1, byte2, byte3, ...]")
    print("\nAppuyez sur Ctrl+C pour arrêter\n")
    
    try:
        device = hid.device()
        device.open(vendor_id, product_id)
        device.set_nonblocking(False)  # Mode bloquant
        
        print("✅ Connexion établie avec la pédale")
        print("📊 Début de la capture...\n")
        
        start_time = time.time()
        event_count = 0
        last_data = None
        
        while time.time() - start_time < duration:
            # Lecture des données (timeout 100ms)
            data = device.read(64, timeout_ms=100)
            
            if data and data != last_data:  # Afficher seulement si changement
                event_count += 1
                timestamp = time.time() - start_time
                
                # Convertir en liste pour affichage
                data_list = list(data)
                
                # Affichage formaté
                print(f"[{timestamp:6.2f}s] Event #{event_count:3d}: {data_list[:8]}")
                
                # Analyse basique
                if all(b == 0 for b in data_list):
                    print("           └─> Tous les boutons relâchés")
                else:
                    active_bytes = [i for i, b in enumerate(data_list[:8]) if b != 0]
                    print(f"           └─> Bytes actifs: {active_bytes}")
                
                last_data = data
        
        print(f"\n✅ Capture terminée: {event_count} événements enregistrés")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Capture interrompue par l'utilisateur")
        print(f"📊 Événements capturés: {event_count}")
    
    except Exception as e:
        print(f"\n❌ Erreur lors de la capture: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            device.close()
            print("🔌 Connexion fermée")
        except:
            pass


def interactive_test(vendor_id: int, product_id: int) -> None:
    """
    Test interactif avec affichage en temps réel
    
    Args:
        vendor_id: Vendor ID du device
        product_id: Product ID du device
    """
    print("\n" + "="*70)
    print("TEST INTERACTIF")
    print("="*70)
    print("\nAppuyez sur les boutons de la pédale.")
    print("Les événements s'afficheront en temps réel.")
    print("Appuyez sur Ctrl+C pour quitter.\n")
    
    try:
        device = hid.device()
        device.open(vendor_id, product_id)
        device.set_nonblocking(True)  # Mode non-bloquant
        
        print("✅ Connexion établie - En attente d'événements...\n")
        
        last_data = None
        
        while True:
            data = device.read(64)
            
            if data and data != last_data:
                data_list = list(data)
                
                # Détection de changement
                if last_data is None:
                    print(f"🔵 État initial: {data_list[:8]}")
                else:
                    # Comparer avec état précédent
                    changes = []
                    for i, (old, new) in enumerate(zip(last_data, data)):
                        if old != new:
                            changes.append(f"Byte[{i}]: {old} → {new}")
                    
                    if changes:
                        print(f"🟢 Changement détecté:")
                        for change in changes:
                            print(f"     {change}")
                        print(f"   État complet: {data_list[:8]}")
                
                last_data = data
            
            time.sleep(0.01)  # 10ms entre lectures
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu")
    
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            device.close()
            print("\n🔌 Connexion fermée")
        except:
            pass


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def main():
    """Fonction principale avec menu interactif"""
    print("="*70)
    print(" OUTIL DE TEST - PÉDALE OLYMPUS RS-31")
    print("="*70)
    
    while True:
        print("\n" + "─"*70)
        print("MENU PRINCIPAL")
        print("─"*70)
        print("\n[1] Lister tous les périphériques HID")
        print("[2] Rechercher une pédale Olympus")
        print("[3] Capturer les événements (reverse engineering)")
        print("[4] Test interactif (temps réel)")
        print("[0] Quitter")
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == "1":
            list_all_hid_devices()
        
        elif choice == "2":
            pedal = find_olympus_pedal()
            if pedal:
                print(f"\n💡 Pour tester cette pédale, utilisez:")
                print(f"   Vendor ID:  0x{pedal['vendor_id']:04x}")
                print(f"   Product ID: 0x{pedal['product_id']:04x}")
        
        elif choice == "3":
            pedal = find_olympus_pedal()
            if pedal:
                duration = input("\nDurée de capture (secondes, défaut 60): ").strip()
                duration = int(duration) if duration.isdigit() else 60
                capture_pedal_events(pedal['vendor_id'], pedal['product_id'], duration)
            else:
                print("\n❌ Pédale non trouvée. Connectez-la d'abord.")
        
        elif choice == "4":
            pedal = find_olympus_pedal()
            if pedal:
                interactive_test(pedal['vendor_id'], pedal['product_id'])
            else:
                print("\n❌ Pédale non trouvée. Connectez-la d'abord.")
        
        elif choice == "0":
            print("\n👋 Au revoir!")
            sys.exit(0)
        
        else:
            print("\n❌ Choix invalide")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

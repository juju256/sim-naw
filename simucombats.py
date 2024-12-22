import re


class Unit:
    """Classe de base pour toutes les unités de combat."""
    def __init__(self, name, level, health, attack, defense, unit_count=0):
        self.name = name
        self.level = level
        self.health = health
        self.attack = attack
        self.defense = defense
        self.unit_count = unit_count

    def effective_stats(self, mandibule_lvl, carapace_lvl, dome_lvl, loge_lvl, environment):
        """
        Calcule les statistiques effectives en fonction des bonus de ressources et de l'environnement.
        
        Environnements :
        - "dome" : bonus de dôme actif.
        - "loge" : bonus de loge actif.
        - "terrain" : aucun bonus.
        """
        # Bonus de base
        attack_bonus = 1 + (mandibule_lvl * 0.05)
        defense_bonus = 1 + (mandibule_lvl * 0.05)
        health_bonus = 1 + (carapace_lvl * 0.05)

        # Bonus spécifiques à l'environnement
        if environment == "dome":
            health_bonus += (dome_lvl * 0.025)  # 2.5% par niveau de dôme
            health_bonus += 0.05  # +5% supplémentaire en attaque
        elif environment == "loge":
            health_bonus += (loge_lvl * 0.05)  # 5% par niveau de loge
            health_bonus += 0.10  # +10% supplémentaire en attaque

        # Calcul des statistiques effectives
        effective_health = self.health * health_bonus
        effective_attack = self.attack * attack_bonus
        effective_defense = self.defense * defense_bonus

        return {
            "health": effective_health,
            "attack": effective_attack,
            "defense": effective_defense
        }

    def __repr__(self):
        return (f"{self.name} (Niveau {self.level}) : Vie={self.health}, "
                f"Attaque={self.attack}, Défense={self.defense}, "
                f"Quantité={self.unit_count}")


# Définition des classes d'unités spécifiques
class Esclave(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Esclave", 1, 4, 4, 3, unit_count)


class MaitreEsclave(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Maître esclave", 2, 6, 6, 4, unit_count)


class JeuneSoldate(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Jeune soldate", 1, 16, 8, 7, unit_count)


class Soldate(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Soldate", 2, 20, 11, 10, unit_count)


class SoldateElite(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Soldate d'élite", 3, 26, 17, 14, unit_count)


class Gardienne(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Gardienne", 1, 25, 1, 27, unit_count)


class GardienneElite(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Gardienne d'élite", 2, 32, 1, 35, unit_count)


class Tirailleuse(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Tirailleuse", 1, 12, 32, 10, unit_count)


class TirailleuseElite(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Tirailleuse d'élite", 2, 15, 40, 12, unit_count)


class JeuneLegionnaire(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Jeune légionnaire", 1, 40, 45, 35, unit_count)


class Legionnaire(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Légionnaire", 2, 55, 60, 45, unit_count)


class LegionnaireElite(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Légionnaire d'élite", 3, 60, 65, 50, unit_count)


class JeuneTank(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Jeune tank", 1, 40, 80, 1, unit_count)


class Tank(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Tank", 2, 70, 140, 1, unit_count)


class TankElite(Unit):
    def __init__(self, unit_count=0):
        super().__init__("Tank d'élite", 3, 80, 160, 1, unit_count)


class Joueur:
    """Classe représentant un joueur avec des unités et des ressources."""
    def __init__(self, name):
        self.name = name
        self.units = {}
        self.mandibule = 0
        self.carapace = 0
        self.dome = 0
        self.loge = 0

    def ajouter_unite(self, unit_class, unit_count):
        """
        Ajoute ou met à jour une unité spécifique.
        Si l'unité existe déjà, elle incrémente le nombre d'unités.
        """
        if unit_class in self.units:
            self.units[unit_class].unit_count = unit_count
        else:
            self.units[unit_class] = unit_class(unit_count)


    def importer_unites_depuis_texte(self, texte):
        """
        Analyse le texte pour extraire les unités et leurs quantités.
        Gère les grands nombres avec espaces comme séparateurs.
        """
        import re

        # Regex pour capturer les quantités et noms des unités
        pattern = r"([\d\s]+)\s+([\w\s'êé]+),?"
        matches = re.findall(pattern, texte)

        # Mapping des noms d'unités aux classes
        unit_map = {
            "Esclaves": Esclave,
            "Maîtres esclaves": MaitreEsclave,
            "Jeunes soldates": JeuneSoldate,
            "Soldates": Soldate,
            "Soldates d'élite": SoldateElite,
            "Gardiennes": Gardienne,
            "Gardiennes d'élite": GardienneElite,
            "Tirailleuses": Tirailleuse,
            "Tirailleuses d'élite": TirailleuseElite,
            "Jeunes légionnaires": JeuneLegionnaire,
            "Légionnaires": Legionnaire,
            "Jeunes tanks": JeuneTank,
            "Tanks": Tank,
        }

        # Parcours des correspondances
        for match in matches:
            # Nettoyage et conversion de la quantité
            quantity = int(match[0].replace(" ", ""))
            # Nettoyage du nom de l'unité
            unit_name = match[1].strip()
            # Ajout ou mise à jour de l'unité si reconnue
            if unit_name in unit_map:
                self.ajouter_unite(unit_map[unit_name], quantity)
            else:
                raise ValueError(f"Unité non reconnue : '{unit_name}'")


    def stats_effectives(self, environment="terrain"):
        """
        Calcule les statistiques effectives pour toutes les unités du joueur.
        Environnement par défaut : terrain de chasse (pas de bonus).
        """
        resultats = {}
        for unit_class, unit in self.units.items():
            stats = unit.effective_stats(
                self.mandibule, self.carapace, self.dome, self.loge, environment
            )
            resultats[unit.name] = stats
        return resultats

    def __repr__(self):
        """Représentation des unités et ressources du joueur."""
        units_repr = "\n".join(f"{unit.name} : {unit.unit_count}" for unit in self.units.values())
        return (f"Joueur : {self.name}\n"
                f"Mandibule : {self.mandibule}\n"
                f"Carapace : {self.carapace}\n"
                f"Dôme : {self.dome}\n"
                f"Loge : {self.loge}\n"
                f"Unités :\n{units_repr}")


def calcul_stat(joueur, stat, environment):
    stats = 0
    for unit_class, unit in joueur.units.items():
        if unit.unit_count > 0:  # Ne compte que les unités encore vivantes
            stats_ = unit.effective_stats(
                joueur.mandibule,
                joueur.carapace,
                joueur.dome,
                joueur.loge,
                environment
            )
            stats_unit = stats_[stat] * unit.unit_count
            stats += stats_unit
    return stats

def appliquer_degats(attaquant, defenseur, degats_attaque_effectif, degats_defenseur_effectif, environment):
    # Appliquer les dégâts à l'armée du défenseur
    for unit_class, unit in defenseur.units.items():
        vie = unit.effective_stats(
            defenseur.mandibule,
            defenseur.carapace,
            defenseur.dome,
            defenseur.loge,
            environment
            )["health"]
        while degats_attaque_effectif > 0 and unit.unit_count > 0:
            if degats_attaque_effectif >= vie:
                # Si les dégâts sont supérieurs à la vie de l'unité, on la tue
                degats_attaque_effectif -= vie
                unit.unit_count -= 1  # Une unité détruite
            else:
                degats_attaque_effectif = 0

    # Appliquer les dégâts à l'armée de l'attaquant
    for unit_class, unit in attaquant.units.items():
        vie = unit.effective_stats(
            defenseur.mandibule,
            defenseur.carapace,
            defenseur.dome,
            defenseur.loge,
            None
            )["health"]
        # Calculer combien d'unités doivent être éliminées
        while degats_defenseur_effectif > 0 and unit.unit_count > 0:
            if degats_defenseur_effectif >= vie:
                # Si les dégâts sont supérieurs à la vie de l'unité, on la tue
                degats_defenseur_effectif -= vie
                unit.unit_count -= 1  # Une unité détruite
            else:
                degats_defenseur_effectif = 0


def combat(joueur_attaquant, joueur_defenseur, environment="terrain"):
    """
    Permet à deux joueurs de se combattre tour par tour.
    Les morts sont appliqués uniquement à la fin de chaque tour.
    Si le joueur attaquant tue toutes les unités ennemies, les dégâts de riposte sont réduits de moitié.
    Retourne un rapport détaillé du combat.
    """
    rapport = []

    rapport.append("\n--- État des unités ---")
    rapport.append(f"Attaquant ({joueur_attaquant.name}):")
    rapport.append("")
    for unit in joueur_attaquant.units.values():
        rapport.append(f"  {unit.name} : {unit.unit_count} unités")
    
    rapport.append("")

    rapport.append(f"Défenseur ({joueur_defenseur.name}):")
    for unit in joueur_defenseur.units.values():
        rapport.append(f"  {unit.name} : {unit.unit_count} unités")
        
    rapport.append("")


    tour = 1

    while tour < 20:
        rapport.append(f"\n=== Tour {tour} ===")
        # Calcul des dégâts pour ce tour
        degats_attaquant = calcul_stat(joueur_attaquant, "attack", None)
        degats_defenseur = calcul_stat(joueur_defenseur, "defense", environment)

        vie_att = calcul_stat(joueur_attaquant, "health", None)
        vie_def = calcul_stat(joueur_defenseur, "health", environment)

        rapport.append(f"Dégâts infligés par l'attaquant : {degats_attaquant}")
        rapport.append(f"Vie de l'attaquant : {vie_att}")
        rapport.append(f"Dégâts infligés par le défenseur : {degats_defenseur}")
        rapport.append(f"Vie du défenseur : {vie_def}")
        
        if degats_attaquant >= vie_def:
            rapport.append("Attaque trop forte degats de la defense divisé par 2.")
            degats_defenseur /= 2
        
        appliquer_degats(joueur_attaquant, joueur_defenseur, degats_attaquant, degats_defenseur, environment)


        # Ajout d'un résumé de l'état des unités
        rapport.append("\n--- État des unités ---")
        rapport.append(f"Attaquant ({joueur_attaquant.name}):")
        rapport.append("")
        for unit in joueur_attaquant.units.values():
            rapport.append(f"  {unit.name} : {unit.unit_count} unités restantes")
        
        rapport.append("")

        rapport.append(f"Défenseur ({joueur_defenseur.name}):")
        for unit in joueur_defenseur.units.values():
            rapport.append(f"  {unit.name} : {unit.unit_count} unités restantes")
            
        rapport.append("")
        
        
        # Vérification si toutes les unités des deux joueurs sont détruites
        if all(unit.unit_count == 0 for unit in joueur_defenseur.units.values()) and \
           all(unit.unit_count == 0 for unit in joueur_attaquant.units.values()):
            rapport.append("Toutes les unités des deux joueurs ont été détruites. Match nul.")
            break

        # Vérification si toutes les unités du defenseur sont détruites
        if all(unit.unit_count == 0 for unit in joueur_defenseur.units.values()):
            rapport.append("Toutes les unités du defenseur ont été détruites. Fin du combat.")
            break
        
        # Vérification si toutes les unités de l'attaquant sont détruites
        if all(unit.unit_count == 0 for unit in joueur_attaquant.units.values()):
            rapport.append("Toutes les unités de l'attaquant ont été détruites. Fin du combat.")
            break

        # Augmenter le numéro du tour
        tour += 1

    return rapport


import tkinter as tk
from tkinter import messagebox, ttk


class CombatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulateur de Combat")
        
        # Joueurs
        self.joueur1 = Joueur("Joueur 1")
        self.joueur2 = Joueur("Joueur 2")

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Zone de configuration des joueurs
        frame_joueurs = tk.Frame(self.root)
        frame_joueurs.pack(pady=10)

        tk.Label(frame_joueurs, text="Joueur 1:").grid(row=0, column=0, padx=5, pady=5)
        self.joueur1_entry = tk.Entry(frame_joueurs, width=50)
        self.joueur1_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_joueurs, text="Joueur 2:").grid(row=1, column=0, padx=5, pady=5)
        self.joueur2_entry = tk.Entry(frame_joueurs, width=50)
        self.joueur2_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame_joueurs, text="Configurer Joueurs", command=self.configurer_joueurs).grid(row=2, column=0, columnspan=2, pady=10)

        # Zone de configuration des bonus
        frame_bonus = tk.Frame(self.root)
        frame_bonus.pack(pady=10)

        tk.Label(frame_bonus, text="Joueur").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame_bonus, text="Mandibule").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_bonus, text="Carapace").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame_bonus, text="Dôme").grid(row=0, column=3, padx=5, pady=5)
        tk.Label(frame_bonus, text="Loge").grid(row=0, column=4, padx=5, pady=5)

        # Joueur 1
        tk.Label(frame_bonus, text="Joueur 1").grid(row=1, column=0, padx=5, pady=5)
        self.joueur1_mandibule = tk.Entry(frame_bonus, width=5)
        self.joueur1_mandibule.grid(row=1, column=1, padx=5, pady=5)
        self.joueur1_carapace = tk.Entry(frame_bonus, width=5)
        self.joueur1_carapace.grid(row=1, column=2, padx=5, pady=5)
        self.joueur1_dome = tk.Entry(frame_bonus, width=5)
        self.joueur1_dome.grid(row=1, column=3, padx=5, pady=5)
        self.joueur1_loge = tk.Entry(frame_bonus, width=5)
        self.joueur1_loge.grid(row=1, column=4, padx=5, pady=5)

        # Joueur 2
        tk.Label(frame_bonus, text="Joueur 2").grid(row=2, column=0, padx=5, pady=5)
        self.joueur2_mandibule = tk.Entry(frame_bonus, width=5)
        self.joueur2_mandibule.grid(row=2, column=1, padx=5, pady=5)
        self.joueur2_carapace = tk.Entry(frame_bonus, width=5)
        self.joueur2_carapace.grid(row=2, column=2, padx=5, pady=5)
        self.joueur2_dome = tk.Entry(frame_bonus, width=5)
        self.joueur2_dome.grid(row=2, column=3, padx=5, pady=5)
        self.joueur2_loge = tk.Entry(frame_bonus, width=5)
        self.joueur2_loge.grid(row=2, column=4, padx=5, pady=5)

        tk.Button(frame_bonus, text="Configurer Bonus", command=self.configurer_bonus).grid(row=3, column=0, columnspan=5, pady=10)

        # Zone de simulation
        frame_simulation = tk.Frame(self.root)
        frame_simulation.pack(pady=10)

        tk.Label(frame_simulation, text="Environnement:").grid(row=0, column=0, padx=5, pady=5)
        self.environment_combobox = ttk.Combobox(frame_simulation, values=["terrain", "dome", "loge"], state="readonly")
        self.environment_combobox.set("terrain")
        self.environment_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_simulation, text="Lancer Combat", command=self.lancer_combat).grid(row=1, column=0, columnspan=2, pady=10)

        # Zone d'affichage des résultats
        self.result_text = tk.Text(self.root, height=20, width=80)
        self.result_text.pack(pady=10)

    def configurer_joueurs(self):
        """Configure les joueurs à partir des entrées."""
        try:
            self.joueur1.importer_unites_depuis_texte(self.joueur1_entry.get())
            self.joueur2.importer_unites_depuis_texte(self.joueur2_entry.get())
            messagebox.showinfo("Succès", "Joueurs configurés avec succès !")
            self.afficher_armee()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de configuration : {e}")

    def configurer_bonus(self):
        """Configure les bonus pour chaque joueur."""
        try:
            self.joueur1.mandibule = int(self.joueur1_mandibule.get() or 0)
            self.joueur1.carapace = int(self.joueur1_carapace.get() or 0)
            self.joueur1.dome = int(self.joueur1_dome.get() or 0)
            self.joueur1.loge = int(self.joueur1_loge.get() or 0)

            self.joueur2.mandibule = int(self.joueur2_mandibule.get() or 0)
            self.joueur2.carapace = int(self.joueur2_carapace.get() or 0)
            self.joueur2.dome = int(self.joueur2_dome.get() or 0)
            self.joueur2.loge = int(self.joueur2_loge.get() or 0)

            messagebox.showinfo("Succès", "Bonus configurés avec succès !")
            self.afficher_armee()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de configuration des bonus : {e}")

    def afficher_armee(self):
        """Affiche l'armée finale des deux joueurs."""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Armée du Joueur 1 ({self.joueur1.name}):\n")
        for unit in self.joueur1.units.values():
            self.result_text.insert(tk.END, f"  {unit.name} : {unit.unit_count} unités\n")
        
        self.result_text.insert(tk.END, f"\nArmée du Joueur 2 ({self.joueur2.name}):\n")
        for unit in self.joueur2.units.values():
            self.result_text.insert(tk.END, f"  {unit.name} : {unit.unit_count} unités\n")

    def lancer_combat(self):
        """Lance un combat entre les deux joueurs."""
        environment = self.environment_combobox.get()
        rapport = "\n".join(combat(self.joueur1, self.joueur2, environment))
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, rapport)


# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CombatApp(root)
    root.mainloop()

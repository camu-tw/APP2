from données.APP_datasets import avions, AVIONS_INITIAL, avions_diplomatic_50, avions_medical_50
#importer les données des 24 avions de l'exemple de l'APP
import random
import time
import sys
import tkinter as tk
from copy import deepcopy
from tkinter import ttk, messagebox

# =============================================================================
# 1. FONCTIONS UTILITAIRES POUR LA VÉRIFICATION ET LE SCORING DES DONNÉES
# =============================================================================

def verification_donnees(listes_avion):
    """
    Vérifie la cohérence des données des avions (clés, types, valeurs).
    Retourne une liste d'erreurs si des incohérences sont détectées.
    """
    erreurs = []

    #si la liste est vide :
    if not listes_avion:
        erreurs.append({"erreur n°": "global", "erreur": "La liste des avions est vide"})
        return erreurs

    #si les id ne sont pas correctes 
    for idx, avion in enumerate(listes_avion):
        # Vérification de l'id
        if "id" not in avion:
            erreurs.append({"erreur n°": idx, "erreur": "La clé 'id' est manquante"})
        else:
            id_avion = avion.get("id")
            if not isinstance(id_avion, str):
                erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'id' doit être une chaîne de caractères"})
            else:
                id_avion = id_avion.strip()
                if len(id_avion) < 2 or len(id_avion) > 40:
                    erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'id' est trop courte ou trop longue"})
                elif not all(c.isalnum() for c in id_avion):
                    erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'id' contient des caractères invalides"})
                elif not any(c.isalpha() for c in id_avion):
                    erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'id' doit contenir au moins une lettre"})

        # Vérification du carburant (fuel)
        if "fuel" not in avion:
            erreurs.append({"erreur n°": idx, "erreur": "La clé 'fuel' est manquante"})
        else:
            if not isinstance(avion.get("fuel"), (int, float)):
                erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'fuel' doit être un nombre"})
            elif avion.get("fuel") < 0:
                erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'fuel' doit être positive"})

        # Vérification des booléens (medical, technical_issue)
        for key in ["medical", "technical_issue"]:
            if key not in avion:
                erreurs.append({"erreur n°": idx, "erreur": f"La clé '{key}' est manquante"})
            else:
                if not isinstance(avion.get(key), bool):
                    erreurs.append({"erreur n°": idx, "erreur": f"La valeur de '{key}' doit être un booléen"})

        # Vérification du niveau diplomatique
        if "diplomatic_level" not in avion:
            erreurs.append({"erreur n°": idx, "erreur": "La clé 'diplomatic_level' est manquante"})
        else:
            if not isinstance(avion.get("diplomatic_level"), int):
                erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'diplomatic_level' doit être un entier"})
            elif avion.get("diplomatic_level") < 1 or avion.get("diplomatic_level") > 5:
                erreurs.append({"erreur n°": idx, "erreur": "La valeur de 'diplomatic_level' doit être entre 1 et 5"})

    return erreurs
#erreurs étant la liste de toutes les erreurs trouvées après avoir tout analyser

# -----------------------------------------------------------------------------

def avions_scoring(liste_avions):
    """
    Calcule un score pour chaque avion en fonction de ses caractéristiques.
    Le score est utilisé pour prioriser les atterrissages.
    """
    copie = []
    for avion in liste_avions:
        scoring = 0
        scoring += 5 if avion.get("medical", False) else 1
        scoring += 5 if avion.get("technical_issue", False) else 1
        diplomatic_level = avion.get("diplomatic_level", 1)
        scoring += 5 if diplomatic_level >= 4 else 3 if diplomatic_level >= 2 else 1
        fuel = avion.get("fuel", 0)
        scoring += 5 if fuel < 10 else 3 if fuel < 20 else 1
        avion_copie = avion.copy()
        avion_copie["scoring"] = scoring
        copie.append(avion_copie)
    return copie

def verifier_crashes(liste_avions):
    """
    Sépare les avions en deux listes : ceux qui ont crashé (fuel <= 0) et ceux qui sont encore en vol.
    """
    avions_crashes = [avion for avion in liste_avions if avion["fuel"] <= 0]
    avions_sains = [avion for avion in liste_avions if avion["fuel"] > 0]
    return avions_crashes, avions_sains

# =============================================================================
# 2. GÉNÉRATION DE TRAFIC ALÉATOIRE
# =============================================================================

def generate_random_traffic(n=10, scenario="normal"):
    """
    Génère une liste de n avions avec des caractéristiques aléatoires.
    Scénarios possibles : normal, medical_crisis, technical_failure, fuel_crisis, diplomatic_summit.
    """
    avions = []
    for i in range(n):
        fuel = random.randint(5, 50)
        medical = False
        technical_issue = False
        diplomatic_level = random.randint(1, 5)

        #les critères ont été définit de manière arbitraire (0.3 ,0.25 ,...)
        if scenario == "medical_crisis":
            medical = random.random() < 0.3
        elif scenario == "technical_failure":
            technical_issue = random.random() < 0.25
        elif scenario == "fuel_crisis":
            fuel = random.randint(5, 15)
        elif scenario == "diplomatic_summit":
            diplomatic_level = random.randint(3, 5)

        avions.append({
            "id": f"FL{i:03}",
            "fuel": fuel,
            "medical": medical,
            "technical_issue": technical_issue,
            "diplomatic_level": diplomatic_level,
            "arrival_time": round(19.40 + i * 0.01, 2)
        })
    return avions

# =============================================================================
# 3. POLITIQUES DES POLICIES
# =============================================================================

# Poids par défaut pour chaque critère (le fuel a toujours la priorité maximale car si l'avion n'a plus de fuel alors il crashe))
POIDS = {
    "fuel": 4,      # Priorité absolue
    "medical": 3,   # À ajuster par l'utilisateur
    "technical": 2,
    "diplomatic": 1
}

def policy_fuel(avion):
    """Priorité au carburant le plus bas (toujours priorité maximale)."""
    return avion["fuel"] * POIDS["fuel"]

def policy_medical(avion):
    """Priorité aux urgences médicales (pondéré)."""
    return (5 if avion["medical"] else 0) * POIDS["medical"]
#si la valeur de 'avion["médical"] est True alors on multiplie par 5 le score medical de l'avion, sinon par 0

#on fait pareil pour la suite
def policy_diplomatic(avion):
    """Priorité au niveau diplomatique (pondéré)."""
    return (5 if avion["diplomatic_level"] else 0) * POIDS["diplomatic"]

def policy_technical(avion):
    """Priorité aux incidents techniques (pondéré)."""
    return (5 if avion["technical_issue"] else 0) * POIDS["technical"]

def policy_combined(avion):
    """
    Politique combinée : priorité absolue au fuel, puis aux autres critères.
    Retourne un tuple pour un tri lexicographique.
    """
    return (
        avion["fuel"] * POIDS["fuel"],
        (5 if avion["medical"] else 0) * POIDS["medical"],
        (5 if avion["technical_issue"] else 0) * POIDS["technical"],
        avion["diplomatic_level"] * POIDS["diplomatic"]
    )

def policy_scoring(avion):
    """Priorité selon le score calculé par avions_scoring()."""
    return avion.get("scoring", 0)

# =============================================================================
# 4. ALGORITHMES DE TRI
# =============================================================================

def insertion_tri_score(L, policy):
    """
    Trie une liste de dictionnaires selon une politique donnée.
    Retourne la liste triée et le nombre de comparaisons effectuées.
    """

    #On évite un bug si la liste est vide : 
    if not L:
        return L, 0

    #Pour une liste non-vide : 
    n = len(L)
    comparaisons = 0
    for i in range(1, n):
        key = L[i]
        j = i - 1
        while j >= 0 and policy(L[j]) > policy(key):
            L[j + 1] = L[j]
            j -= 1
            comparaisons += 1
        L[j + 1] = key
    return L, comparaisons

def selection_sort(L, policy):
    """
    Trie une liste de dictionnaires selon une politique donnée (version sélection).
    Retourne la liste triée et le nombre de comparaisons effectuées.
    """

    #pareil, on évite les liste vides
    if not L:
        return L, 0

    n = len(L)
    comparaisons = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if policy(L[j]) < policy(L[min_idx]):
                min_idx = j
            comparaisons += 1
        L[i], L[min_idx] = L[min_idx], L[i]
    return L, comparaisons

# =============================================================================
# 5. SIMULATION AVEC L'UTILISATEUR
# =============================================================================

def defragmenter_carburant(liste_avions, minutes_ecoulees=3):
    """Réduit le carburant de chaque avion en fonction du temps écoulé (en minutes)."""
    for avion in liste_avions:
        avion["fuel"] -= minutes_ecoulees  # 1 unité de carburant par minute
        if avion["fuel"] < 0:
            avion["fuel"] = 0
    return liste_avions

def simuler_tour(liste_avions, policy, dernier_atterrissage=0):
    """
    Simule un tour d'atterrissage :
    1. Trie les avions selon la politique.
    2. Un seul avion atterrit toutes les 3 minutes.
    3. Réduit le carburant des autres.
    4. Vérifie les crashes.
    """
    liste_triee, _ = insertion_tri_score(liste_avions.copy(), policy)

    # Un seul avion peut atterrir par tour (toutes les 3 minutes)
    if liste_triee:
        avion_atterri = liste_triee.pop(0)
    else:
        avion_atterri = None

    # Réduit le carburant des autres avions (3 minutes écoulées)
    defragmenter_carburant(liste_triee, minutes_ecoulees=3)

    # Vérifie les crashes
    avions_crashes, avions_en_attente = verifier_crashes(liste_triee)

    # Retourne les résultats + le temps actuel pour le prochain tour
    if avion_atterri:
        avion_atterri["temps_atterrissage"] = dernier_atterrissage + 3  # Heure d'atterrissage en minutes
        return [avion_atterri], avions_crashes, avions_en_attente, dernier_atterrissage + 3
    else:
        return [], avions_crashes, avions_en_attente, dernier_atterrissage + 3

def simulation_complete(liste_avions, policy, tours_max=100):
    """
    Simule l'atterrissage de tous les avions selon une politique,
    en respectant un intervalle de 3 minutes entre chaque atterrissage.
    """
    avions_atterris = []
    avions_crashes = []
    avions_en_attente = liste_avions.copy()
    dernier_atterrissage = 0  # Temps initial (en minutes)

    tours = 0
    while avions_en_attente and tours < tours_max:
        tours += 1
        atterris, crashes, en_attente, dernier_atterrissage = simuler_tour(
            avions_en_attente, policy, dernier_atterrissage
        )
        avions_atterris.extend(atterris)
        avions_crashes.extend(crashes)
        avions_en_attente = en_attente

    if avions_en_attente:
        print(f"Avertissement : {len(avions_en_attente)} avions n'ont pas pu atterrir en {tours_max} tours.")
    return avions_atterris, avions_crashes, tours


def convert_arrival_time_to_minutes(arrival_time):
    """Convertit une heure de type 19.42 en minutes absolues (ex: 1182)."""
    heures = int(arrival_time)
    minutes = int(round((arrival_time - heures) * 100))
    return heures * 60 + minutes


def format_minutes_to_clock(total_minutes):
    """Transforme un nombre de minutes absolues en HH:MM."""
    heures = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{heures:02d}:{minutes:02d}"


class SimulationAppGUI:
    """Interface graphique de simulation du trafic aerien."""

    def __init__(self, root):
        self.root = root
        self.root.title("APP2 - Controle des avions en approche")
        self.root.geometry("1280x760")
        self.root.minsize(1080, 680)

        self.running = False
        self.last_tick = time.time()
        self.sim_minutes = 0.0
        self.next_landing_time = 0.0
        self.base_arrival_min = 0

        self.pending_arrivals = []
        self.active_planes = []
        self.landed_planes = []
        self.crashed_planes = []

        self.dataset_var = tk.StringVar(value="initial_24")
        self.nb_avions_var = tk.IntVar(value=24)
        self.policy_var = tk.StringVar(value="combined")
        self.time_speed_var = tk.DoubleVar(value=1.0)
        self.interval_var = tk.DoubleVar(value=3.0)
        self.weight_medical_var = tk.IntVar(value=3)
        self.weight_technical_var = tk.IntVar(value=2)
        self.weight_diplomatic_var = tk.IntVar(value=1)

        self._build_layout()
        self._draw_static_scene()
        self.reset_simulation()

    def _build_layout(self):
        self.root.configure(bg="#10253f")

        container = tk.Frame(self.root, bg="#10253f")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        left_panel = tk.Frame(container, bg="#10253f")
        left_panel.pack(side="left", fill="both", expand=True)

        right_panel = tk.Frame(container, bg="#142d4d", width=350)
        right_panel.pack(side="right", fill="y", padx=(12, 0))
        right_panel.pack_propagate(False)

        self.canvas = tk.Canvas(
            left_panel,
            bg="#0b1c31",
            highlightthickness=1,
            highlightbackground="#355a85",
            height=450,
        )
        self.canvas.pack(fill="both", expand=False)

        info_row = tk.Frame(left_panel, bg="#10253f")
        info_row.pack(fill="x", pady=(8, 0))

        self.clock_label = tk.Label(
            info_row,
            text="Heure simulee: 19:40",
            fg="#f8f8f8",
            bg="#10253f",
            font=("Segoe UI", 12, "bold"),
        )
        self.clock_label.pack(side="left")

        self.status_label = tk.Label(
            info_row,
            text="En attente",
            fg="#ffd166",
            bg="#10253f",
            font=("Segoe UI", 11),
        )
        self.status_label.pack(side="right")

        table_frame = tk.LabelFrame(
            left_panel,
            text="Colonne des temps d'arrivee",
            bg="#10253f",
            fg="#ffffff",
            bd=1,
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=8,
        )
        table_frame.pack(fill="both", expand=True, pady=(8, 0))

        self.arrivals_tree = ttk.Treeview(
            table_frame,
            columns=("id", "arrivee", "fuel", "signal", "etat"),
            show="headings",
            height=10,
        )
        self.arrivals_tree.heading("id", text="Avion")
        self.arrivals_tree.heading("arrivee", text="Arrivee")
        self.arrivals_tree.heading("fuel", text="Fuel")
        self.arrivals_tree.heading("signal", text="Signal")
        self.arrivals_tree.heading("etat", text="Etat")

        self.arrivals_tree.column("id", width=90, anchor="center")
        self.arrivals_tree.column("arrivee", width=90, anchor="center")
        self.arrivals_tree.column("fuel", width=70, anchor="center")
        self.arrivals_tree.column("signal", width=90, anchor="center")
        self.arrivals_tree.column("etat", width=120, anchor="center")

        self.arrivals_tree.tag_configure("urgent", background="#ffdddd")
        self.arrivals_tree.tag_configure("warning", background="#fff1cc")
        self.arrivals_tree.tag_configure("normal", background="#ddf5e3")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.arrivals_tree.yview)
        self.arrivals_tree.configure(yscrollcommand=scrollbar.set)
        self.arrivals_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        control_title = tk.Label(
            right_panel,
            text="Parametres de simulation",
            fg="#ffffff",
            bg="#142d4d",
            font=("Segoe UI", 13, "bold"),
        )
        control_title.pack(anchor="w", padx=10, pady=(10, 8))

        self._add_dataset_controls(right_panel)
        self._add_priority_controls(right_panel)
        self._add_time_controls(right_panel)
        self._add_action_controls(right_panel)

    def _add_dataset_controls(self, parent):
        section = tk.LabelFrame(parent, text="Scenario", bg="#142d4d", fg="#ffffff", padx=8, pady=8)
        section.pack(fill="x", padx=10, pady=6)

        options = [
            ("Initial 24 avions", "initial_24"),
            ("Diplomatique 50", "diplomatic_50"),
            ("Medical 50", "medical_50"),
            ("Aleatoire", "random"),
        ]
        for label, value in options:
            tk.Radiobutton(
                section,
                text=label,
                variable=self.dataset_var,
                value=value,
                bg="#142d4d",
                fg="#ffffff",
                selectcolor="#1c3a5f",
                activebackground="#142d4d",
                activeforeground="#ffffff",
            ).pack(anchor="w")

        row = tk.Frame(section, bg="#142d4d")
        row.pack(fill="x", pady=(6, 0))
        tk.Label(row, text="Nb avions (aleatoire):", bg="#142d4d", fg="#ffffff").pack(side="left")
        tk.Spinbox(row, from_=5, to=120, textvariable=self.nb_avions_var, width=6).pack(side="right")

    def _add_priority_controls(self, parent):
        section = tk.LabelFrame(parent, text="Politique et poids", bg="#142d4d", fg="#ffffff", padx=8, pady=8)
        section.pack(fill="x", padx=10, pady=6)

        policy_menu = ttk.Combobox(
            section,
            textvariable=self.policy_var,
            values=["fuel", "combined", "scoring"],
            state="readonly",
        )
        policy_menu.pack(fill="x", pady=(0, 8))

        self._slider(section, "Poids medical", self.weight_medical_var, 0, 5)
        self._slider(section, "Poids technique", self.weight_technical_var, 0, 5)
        self._slider(section, "Poids diplomatique", self.weight_diplomatic_var, 0, 5)

    def _add_time_controls(self, parent):
        section = tk.LabelFrame(parent, text="Temps", bg="#142d4d", fg="#ffffff", padx=8, pady=8)
        section.pack(fill="x", padx=10, pady=6)

        tk.Label(section, text="Vitesse du temps", bg="#142d4d", fg="#ffffff").pack(anchor="w")
        tk.Scale(
            section,
            from_=0.2,
            to=4.0,
            resolution=0.2,
            orient="horizontal",
            variable=self.time_speed_var,
            bg="#142d4d",
            fg="#ffffff",
            highlightthickness=0,
        ).pack(fill="x")

        tk.Label(section, text="Intervalle entre atterrissages (minutes)", bg="#142d4d", fg="#ffffff").pack(anchor="w")
        tk.Scale(
            section,
            from_=1.0,
            to=8.0,
            resolution=0.5,
            orient="horizontal",
            variable=self.interval_var,
            bg="#142d4d",
            fg="#ffffff",
            highlightthickness=0,
        ).pack(fill="x")

    def _add_action_controls(self, parent):
        section = tk.Frame(parent, bg="#142d4d")
        section.pack(fill="x", padx=10, pady=8)

        self.start_btn = tk.Button(section, text="Demarrer", command=self.start_simulation, bg="#1d9a6c", fg="#ffffff")
        self.start_btn.pack(fill="x", pady=3)

        self.pause_btn = tk.Button(section, text="Pause", command=self.toggle_pause, bg="#e59f00", fg="#ffffff")
        self.pause_btn.pack(fill="x", pady=3)

        reset_btn = tk.Button(section, text="Recharger les parametres", command=self.reset_simulation, bg="#315b8c", fg="#ffffff")
        reset_btn.pack(fill="x", pady=3)

        legend = tk.LabelFrame(parent, text="Signal lumineux", bg="#142d4d", fg="#ffffff", padx=8, pady=8)
        legend.pack(fill="x", padx=10, pady=6)

        tk.Label(legend, text="Rouge : urgence (fuel <= 8 ou alerte)", bg="#142d4d", fg="#ffb3b3").pack(anchor="w")
        tk.Label(legend, text="Orange : surveillance (fuel <= 15)", bg="#142d4d", fg="#ffd57a").pack(anchor="w")
        tk.Label(legend, text="Vert : normal", bg="#142d4d", fg="#9be0ad").pack(anchor="w")

    def _slider(self, parent, label, variable, min_val, max_val):
        tk.Label(parent, text=label, bg="#142d4d", fg="#ffffff").pack(anchor="w")
        tk.Scale(
            parent,
            from_=min_val,
            to=max_val,
            orient="horizontal",
            variable=variable,
            bg="#142d4d",
            fg="#ffffff",
            highlightthickness=0,
        ).pack(fill="x")

    def _draw_static_scene(self):
        self.canvas.delete("static")
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 2 else 900
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 2 else 450

        self.canvas.create_rectangle(0, 0, w, h, fill="#0b1c31", outline="", tags="static")
        self.canvas.create_rectangle(70, h - 120, w - 70, h - 50, fill="#2f3440", outline="#808a99", width=2, tags="static")

        for x in range(90, w - 90, 70):
            self.canvas.create_line(x, h - 85, x + 35, h - 85, fill="#ffffff", width=3, tags="static")

        self.canvas.create_text(95, h - 133, text="PISTE UNIQUE", fill="#d6e4ff", anchor="w", font=("Segoe UI", 11, "bold"), tags="static")
        self.canvas.create_text(w - 100, h - 133, text="Zone atterrissage", fill="#d6e4ff", anchor="e", font=("Segoe UI", 10), tags="static")

    def reset_simulation(self):
        try:
            planes = self._create_dataset()
            erreurs = verification_donnees(planes)
            if erreurs:
                messagebox.showerror("Donnees invalides", f"{len(erreurs)} erreur(s) detectee(s).")
                return

            self.running = False
            self.pause_btn.config(text="Pause")
            self.status_label.config(text="Pret a demarrer", fg="#7cd1ff")

            self.pending_arrivals = []
            self.active_planes = []
            self.landed_planes = []
            self.crashed_planes = []
            self.sim_minutes = 0.0
            self.next_landing_time = 0.0

            plane_copies = []
            for index, p in enumerate(deepcopy(planes)):
                p.setdefault("arrival_time", round(19.40 + index * 0.01, 2))
                p["arrival_minutes_abs"] = convert_arrival_time_to_minutes(p["arrival_time"])
                p["initial_fuel"] = float(p["fuel"])
                p["remaining_fuel"] = float(p["fuel"])
                p["x"] = 980 + (index % 6) * 50
                p["y"] = 90 + (index % 5) * 48
                plane_copies.append(p)

            plane_copies.sort(key=lambda p: p["arrival_minutes_abs"])
            self.base_arrival_min = plane_copies[0]["arrival_minutes_abs"] if plane_copies else convert_arrival_time_to_minutes(19.40)

            for p in plane_copies:
                p["arrival_relative"] = p["arrival_minutes_abs"] - self.base_arrival_min
                self.pending_arrivals.append(p)

            self._draw_static_scene()
            self._render_dynamic_scene(0.0)
            self._refresh_table()
            self._refresh_clock()
        except Exception as exc:
            messagebox.showerror("Erreur", f"Impossible de charger la simulation: {exc}")

    def _create_dataset(self):
        mode = self.dataset_var.get()
        if mode == "initial_24":
            return deepcopy(AVIONS_INITIAL)
        if mode == "diplomatic_50":
            return deepcopy(avions_diplomatic_50)
        if mode == "medical_50":
            return deepcopy(avions_medical_50)

        n = max(5, int(self.nb_avions_var.get()))
        return generate_random_traffic(n=n, scenario="fuel_crisis")

    def start_simulation(self):
        if self.running:
            return
        self.running = True
        self.last_tick = time.time()
        self.status_label.config(text="Simulation en cours", fg="#7fffb5")
        self._tick()

    def toggle_pause(self):
        if not self.running:
            self.start_simulation()
            self.pause_btn.config(text="Pause")
            return

        self.running = False
        self.status_label.config(text="Simulation en pause", fg="#ffd166")
        self.pause_btn.config(text="Reprendre")

    def _tick(self):
        if not self.running:
            return

        now = time.time()
        dt_real = now - self.last_tick
        self.last_tick = now

        speed_factor = float(self.time_speed_var.get())
        dt_sim = dt_real * speed_factor * 6.0
        self.sim_minutes += dt_sim

        self._inject_arrivals()
        self._consume_fuel(dt_sim)
        self._process_landings()

        self._render_dynamic_scene(dt_real)
        self._refresh_table()
        self._refresh_clock()

        if not self.pending_arrivals and not self.active_planes:
            self.running = False
            self.status_label.config(
                text=f"Terminee | Atterris: {len(self.landed_planes)} | Crashes: {len(self.crashed_planes)}",
                fg="#ffffff",
            )
            self.pause_btn.config(text="Pause")
            return

        self.root.after(40, self._tick)

    def _inject_arrivals(self):
        while self.pending_arrivals and self.pending_arrivals[0]["arrival_relative"] <= self.sim_minutes:
            incoming = self.pending_arrivals.pop(0)
            incoming["x"] = 980
            self.active_planes.append(incoming)

    def _consume_fuel(self, dt_sim):
        survivors = []
        for plane in self.active_planes:
            plane["remaining_fuel"] = max(0.0, plane["remaining_fuel"] - dt_sim)
            if plane["remaining_fuel"] <= 0:
                plane["status"] = "crashe"
                self.crashed_planes.append(plane)
            else:
                survivors.append(plane)
        self.active_planes = survivors

    def _process_landings(self):
        interval = float(self.interval_var.get())
        if interval <= 0:
            interval = 3.0

        while self.active_planes and self.sim_minutes >= self.next_landing_time:
            candidate = self._select_next_plane()
            if candidate is None:
                break

            self.active_planes.remove(candidate)
            candidate["status"] = "atterri"
            candidate["landing_minutes_abs"] = self.base_arrival_min + self.sim_minutes
            self.landed_planes.append(candidate)
            self.next_landing_time += interval

        if self.next_landing_time < self.sim_minutes and not self.landed_planes:
            self.next_landing_time = self.sim_minutes + interval

    def _select_next_plane(self):
        if not self.active_planes:
            return None

        policy = self.policy_var.get()
        if policy == "fuel":
            return min(self.active_planes, key=lambda p: p["remaining_fuel"])
        if policy == "scoring":
            return max(self.active_planes, key=self._score_plane)

        return min(self.active_planes, key=self._combined_priority)

    def _score_plane(self, plane):
        wm = self.weight_medical_var.get()
        wt = self.weight_technical_var.get()
        wd = self.weight_diplomatic_var.get()
        score = 0
        score += 50 if plane["remaining_fuel"] <= 8 else 20 if plane["remaining_fuel"] <= 15 else 5
        score += 40 * wm if plane["medical"] else 0
        score += 35 * wt if plane["technical_issue"] else 0
        score += 8 * wd * plane["diplomatic_level"]
        return score

    def _combined_priority(self, plane):
        wm = self.weight_medical_var.get()
        wt = self.weight_technical_var.get()
        wd = self.weight_diplomatic_var.get()
        return (
            plane["remaining_fuel"] * 4,
            -(1 if plane["medical"] else 0) * wm,
            -(1 if plane["technical_issue"] else 0) * wt,
            -plane["diplomatic_level"] * wd,
        )

    def _signal_level(self, plane):
        if plane["remaining_fuel"] <= 8 or plane["medical"] or plane["technical_issue"]:
            return "ROUGE", "#ff4d4d", "urgent"
        if plane["remaining_fuel"] <= 15:
            return "ORANGE", "#ffb347", "warning"
        return "VERT", "#42c96d", "normal"

    def _render_dynamic_scene(self, dt_real):
        self.canvas.delete("plane")
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 2 else 450
        speed = max(0.2, float(self.time_speed_var.get()))

        priority_sorted = sorted(self.active_planes, key=lambda p: p["remaining_fuel"])
        for idx, plane in enumerate(priority_sorted):
            target_x = 180 + idx * 95
            plane["x"] = max(target_x, plane.get("x", 980) - (85 * speed * dt_real))
            lane = idx % 5
            plane["y"] = 80 + lane * 48

            signal_text, signal_color, _ = self._signal_level(plane)
            fuel_ratio = 0 if plane["initial_fuel"] == 0 else plane["remaining_fuel"] / plane["initial_fuel"]
            fuel_len = int(42 * fuel_ratio)

            x = plane["x"]
            y = plane["y"]

            self.canvas.create_polygon(
                x, y,
                x + 26, y - 8,
                x + 52, y,
                x + 26, y + 8,
                fill="#dce7f7",
                outline="#b0c4de",
                width=1,
                tags="plane",
            )
            self.canvas.create_text(x + 26, y - 15, text=plane["id"], fill="#ffffff", font=("Segoe UI", 8, "bold"), tags="plane")
            self.canvas.create_rectangle(x + 6, y + 12, x + 48, y + 18, outline="#9ca9b8", fill="#1d2b3a", tags="plane")
            self.canvas.create_rectangle(x + 6, y + 12, x + 6 + fuel_len, y + 18, outline="", fill="#42c96d" if fuel_ratio > 0.35 else "#ff8f66", tags="plane")
            self.canvas.create_oval(x + 54, y - 4, x + 62, y + 4, fill=signal_color, outline="", tags="plane")
            self.canvas.create_text(x + 72, y, text=signal_text, fill=signal_color, anchor="w", font=("Segoe UI", 8, "bold"), tags="plane")

        self.canvas.create_text(
            14,
            h - 20,
            text=f"Approche: {len(self.active_planes)} | Atterris: {len(self.landed_planes)} | Crashes: {len(self.crashed_planes)}",
            fill="#e6f0ff",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            tags="plane",
        )

    def _refresh_table(self):
        for item in self.arrivals_tree.get_children():
            self.arrivals_tree.delete(item)

        display_rows = []
        for plane in self.active_planes:
            signal_text, _, tag = self._signal_level(plane)
            display_rows.append((
                plane["id"],
                format_minutes_to_clock(plane["arrival_minutes_abs"]),
                f"{plane['remaining_fuel']:.1f}",
                signal_text,
                "en approche",
                tag,
            ))

        for plane in self.pending_arrivals[:20]:
            signal_text, _, tag = self._signal_level(plane)
            display_rows.append((
                plane["id"],
                format_minutes_to_clock(plane["arrival_minutes_abs"]),
                f"{plane['remaining_fuel']:.1f}",
                signal_text,
                "en attente",
                tag,
            ))

        display_rows.sort(key=lambda row: row[1])
        for row in display_rows[:30]:
            self.arrivals_tree.insert("", "end", values=row[:-1], tags=(row[-1],))

    def _refresh_clock(self):
        current_abs_minutes = self.base_arrival_min + self.sim_minutes
        self.clock_label.config(text=f"Heure simulee: {format_minutes_to_clock(current_abs_minutes)}")


def lancer_affichage_graphique():
    """Point d'entree de l'interface graphique utilisateur."""
    try:
        root = tk.Tk()
    except KeyboardInterrupt as exc:
        raise RuntimeError("Initialisation Tkinter interrompue.") from exc
    except tk.TclError as exc:
        raise RuntimeError(f"Tkinter indisponible: {exc}") from exc

    app = SimulationAppGUI(root)
    root.mainloop()

# =============================================================================
# 6. FONCTION PRINCIPALE (MAIN)
# =============================================================================

def main():
    """
    Fonction principale du programme.
    Elle guide l'utilisateur à travers les étapes de la simulation.
    """
    # =========================================================================
    # BIENVENUE ET CHOIX DES DONNÉES
    # =========================================================================
    print("=" * 70)
    print("SIMULATION D'ATTERRISSAGE - AÉROPORT DE ROISSY (Tempête Exceptionnelle)")
    print("=" * 70)
    print("\nSITUATION CRITIQUE : 19h42")
    print("   - 2 pistes fermées")
    print("   - 1 seule piste opérationnelle")
    print("   - Multiple avions en approche\n")

    # Choix du jeu de données
    print("Choisissez le jeu de données à utiliser :")
    print("   0 - Liste prédéfinie de 24 avions")
    print("   1 - Générateur de trafic aléatoire (10 avions)")
    print("   2 - Générateur personnalisé (nombre d'avions à préciser)")

    choix = None
    while choix is None:
        try:
            choix = int(input("\nVotre choix (0, 1 ou 2) : "))
            if choix not in [0, 1, 2]:
                print("Erreur : Veuillez entrer 0, 1 ou 2.")
                choix = None
        except ValueError:
            print("Erreur : Veuillez entrer un nombre entier valide.")

    # Chargement des données
    if choix == 0:
        avions = AVIONS_INITIAL
        print(f"\n   ✓ {len(avions)} avions chargés (liste prédéfinie)")
    elif choix == 1:
        avions = generate_random_traffic(10, scenario="fuel_crisis")
        print(f"\n   ✓ 10 avions générés aléatoirement (scénario : crise de carburant)")
    else:
        while True:
            try:
                n = int(input("\nNombre d'avions à générer : "))
                if n > 0:
                    scenario = input("Scénario (normal/medical_crisis/technical_failure/fuel_crisis/diplomatic_summit) : ")
                    avions = generate_random_traffic(n, scenario=scenario)
                    print(f"\n   ✓ {n} avions générés (scénario : {scenario})")
                    break
                else:
                    print("Erreur : Veuillez entrer un nombre positif.")
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier valide.")

    # =========================================================================
    # VÉRIFICATION DES DONNÉES
    # =========================================================================
    print("\n Vérification de la cohérence des données...")
    erreurs = verification_donnees(avions)

    if erreurs:
        print(f"   ❌ {len(erreurs)} erreur(s) détectée(s) :")
        for erreur in erreurs:
            print(f"      - {erreur['erreur']}")
        return
    else:
        print("   ✓ Toutes les données sont valides")

    # Affichage d'un exemple d'avion
    print("\nExemple d'avion dans le dataset :")
    premier_avion = avions[0]
    print(f"   ID : {premier_avion['id']}")
    print(f"   Carburant restant : {premier_avion['fuel']} minutes")
    print(f"   Urgence médicale : {'Oui' if premier_avion['medical'] else 'Non'}")
    print(f"   Incident technique : {'Oui' if premier_avion['technical_issue'] else 'Non'}")
    print(f"   Importance diplomatique : {premier_avion['diplomatic_level']}/5")
    print(f"   Heure d'arrivée prévue : {premier_avion['arrival_time']}")

    # =========================================================================
    # DÉFINITION DES PRIORITÉS (POIDS DES POLITIQUES)
    # =========================================================================
    print("\nDéfinissez les priorités pour les critères secondaires :")
    print("   Le carburant a toujours la priorité maximale (poids = 4).")
    print("   Classez les 3 autres critères par ordre d'importance (3 = plus important, 1 = moins important) :")

    priorites = {}
    while True:
        try:
            print("\n   1 - Urgences médicales")
            print("   2 - Incidents techniques")
            print("   3 - Niveau diplomatique")

            priorites["medical"] = int(input("\nPriorité pour les urgences médicales (1, 2 ou 3) : "))
            priorites["technical"] = int(input("Priorité pour les incidents techniques (1, 2 ou 3) : "))
            priorites["diplomatic"] = int(input("Priorité pour le niveau diplomatique (1, 2 ou 3) : "))

            valeurs_priorites = sorted(priorites.values())
            if valeurs_priorites == [1, 2, 3]:
                break
            else:
                print("Erreur : Les priorités doivent être 1, 2 et 3 sans répétition.")
        except ValueError:
            print("Erreur : Veuillez entrer des nombres valides (1, 2 ou 3).")

    # Attribution des poids
    POIDS["medical"] = 4 - priorites["medical"]
    POIDS["technical"] = 4 - priorites["technical"]
    POIDS["diplomatic"] = 4 - priorites["diplomatic"]

    print(f"\nPoids attribués :")
    print(f"   Fuel : {POIDS['fuel']} (priorité absolue)")
    print(f"   Medical : {POIDS['medical']}")
    print(f"   Technical : {POIDS['technical']}")
    print(f"   Diplomatic : {POIDS['diplomatic']}")

    # =========================================================================
    # CHOIX DE LA POLITIQUE DE TRI
    # =========================================================================
    print("\nChoisissez la politique de tri :")
    print("   1 - Priorité carburant seule")
    print("   2 - Priorité combinée (fuel + medical + technical + diplomatic)")
    print("   3 - Scoring personnalisé")

    choix_policy = None
    while choix_policy is None:
        try:
            choix_policy = int(input("\nVotre choix (1, 2 ou 3) : "))
            if choix_policy not in [1, 2, 3]:
                print("Erreur : Veuillez entrer 1, 2 ou 3.")
                choix_policy = None
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")

    # Sélection de la politique
    if choix_policy == 1:
        policy = policy_fuel
        print("\nPolitique sélectionnée : Priorité carburant seule")
    elif choix_policy == 2:
        policy = policy_combined
        print("\nPolitique sélectionnée : Priorité combinée")
    else:
        policy = policy_scoring
        print("\nPolitique sélectionnée : Scoring personnalisé")

    # =========================================================================
    # SIMULATION ET RÉSULTATS
    # =========================================================================
    print("\nLancement de la simulation...")
    avions_atterris, avions_crashes, tours = simulation_complete(avions, policy=policy)
    print(f"\nTemps total de la simulation : {tours * 3} minutes")
    print("\n" + "-" * 70)
    print("RÉSULTATS DE LA SIMULATION")
    print("-" * 70)
    print(f"\nTemps total de la simulation : {tours * 3} minutes")
    print(f"Avions atterris : {len(avions_atterris)}")
    print(f"Avions crashés : {len(avions_crashes)}")

    # =========================================================================
    # AFFICHAGE DÉTAILLÉ DES AVIONS ATTERRIS
    # =========================================================================
    if avions_atterris:
        print("\n Liste complète des avions atterris (par ordre d'atterrissage) :")
        print("-" * 70)
        for i, avion in enumerate(avions_atterris, 1):
            print(f"{i:2d}. {avion['id']:6} | Atterrissage: {avion.get('temps_atterrissage', 0):2d} min | "
                f"Fuel restant: {avion['fuel']:2d} min | Médical: {'OUI' if avion['medical'] else 'NON':3}")
            print("-" * 70)

    # =========================================================================
    # AFFICHAGE DÉTAILLÉ DES AVIONS CRASHÉS (SI EXISTANTS)
    # =========================================================================
    if avions_crashes:
        print("\nListe complète des avions crashés :")
        print("-" * 50)
        for i, avion in enumerate(avions_crashes, 1):
            print(f"{i:2d}. {avion['id']:6} | Fuel restant: {avion['fuel']:2d} min | "
                f"Médical: {'OUI' if avion['medical'] else 'NON':3} | "
                f"Technique: {'OUI' if avion['technical_issue'] else 'NON':3} | "
                f"Diplomatie: {avion['diplomatic_level']}/5")
        print("-" * 50)
    else:
        print("\nAucun avion n'a crashé.")

    # =========================================================================
    # COMPARAISON DES ALGORITHMES DE TRI
    # =========================================================================
    print("\nComparaison des algorithmes de tri :")
    liste_test = avions.copy()
    _, comp_insertion = insertion_tri_score(liste_test.copy(), policy)
    _, comp_selection = selection_sort(liste_test.copy(), policy)
    print(f"   Tri par insertion : {comp_insertion} comparaisons")
    print(f"   Tri par sélection : {comp_selection} comparaisons")

    print("\n" + "=" * 70)
    print("FIN DE LA SIMULATION")
    print("=" * 70)
# =============================================================================
# POINT D'ENTRÉE DU PROGRAMME
# =============================================================================
if __name__ == "__main__":
    force_console = "--console" in sys.argv

    if force_console:
        print("Mode console force avec --console")
        main()
    else:
        try:
            lancer_affichage_graphique()
        except Exception as exc:
            print(f"Impossible de lancer l'interface graphique ({exc}).")
            print("Bascule automatique vers le mode console.")
            main()
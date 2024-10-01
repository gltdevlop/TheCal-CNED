import tkinter as tk
from tkinter import ttk, filedialog, Menu, messagebox
import json
import os
import ctypes

# Créer la fenêtre principale
root = tk.Tk()
root.title("Calendrier des devoirs")

# Vérifier et créer le fichier de configuration si ce n'est pas encore fait
config_file_path = "json-files/config.json"
if not os.path.exists(config_file_path):
    with open(config_file_path, "w", encoding="utf-8") as config_file:
        json.dump({"dark_mode": False}, config_file)

# Charger la configuration
with open(config_file_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Numéros de semaine (de 36 à 22)
semaines = list(range(36, 53)) + list(range(1, 23))

# Charger la liste des matières et la planification depuis les fichiers JSON
def charger_matieres():
    print("Json matières chargé")
    with open("json-files/matieres.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def charger_devoirs():
    print("Json devoirs chargé")
    with open("json-files/devoirs.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)

# Charger les données
matieres = charger_matieres()
devoirs = charger_devoirs()

# Créer une liste pour stocker les variables des cases cochées
checkbox_vars = []
# Variable pour stocker le chemin du fichier chargé
fichier_charge = None

# Fonction pour charger l'état des cases cochées depuis un fichier JSON
def charger():
    global fichier_charge
    filepath = filedialog.askopenfilename(
        title="Charger un fichier JSON",
        filetypes=(("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*"))
    )

    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as json_file:
                etat_devoirs = json.load(json_file)

            if etat_devoirs.get("file-state") != 1:
                raise ValueError("Le fichier ne contient pas un état valide.")

            for i, matiere in enumerate(matieres.keys()):
                for j, semaine in enumerate(semaines):
                    checkbox_vars[i][j].set(etat_devoirs.get(matiere, {}).get(str(semaine), 0))

            root.title(f"Calendrier des devoirs - {filepath}")
            fichier_charge = filepath
            print(f"État chargé depuis '{filepath}'.")
        except (json.JSONDecodeError, FileNotFoundError):
            messagebox.showerror("Erreur", "Erreur lors du chargement du fichier.")
            print("Erreur lors du chargement du fichier.")
        except ValueError as ve:
            ctypes.windll.user32.MessageBoxW(0, str(ve), "Erreur de fichier", 1)
            print(str(ve))
    else:
        print("Aucun fichier sélectionné ou fichier introuvable.")

# Fonction pour sauvegarder manuellement l'état des cases cochées dans un fichier JSON
def sauvegarder(filepath=None):
    etat_devoirs = {"file-state": 1}
    for i, matiere in enumerate(matieres.keys()):
        etat_devoirs[matiere] = {}
        for j, semaine in enumerate(semaines):
            etat_devoirs[matiere][semaine] = checkbox_vars[i][j].get()

    if not filepath:
        filepath = filedialog.asksaveasfilename(
            title="Sauvegarder le fichier JSON",
            defaultextension=".json",
            filetypes=(("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")),
            initialfile="etat_devoirs.json"
        )

    if filepath:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(etat_devoirs, json_file, ensure_ascii=False, indent=4)
        global fichier_charge
        fichier_charge = filepath
        print(f"État sauvegardé dans '{filepath}'.")
        charger_fichier(filepath)

# Fonction pour "Enregistrer sous"
def enregistrer_sous():
    sauvegarder()

# Fonction pour charger un fichier et mettre à jour l'état des cases
def charger_fichier(filepath):
    global fichier_charge
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as json_file:
                etat_devoirs = json.load(json_file)

            if etat_devoirs.get("file-state") != 1:
                raise ValueError("Le fichier ne contient pas un état valide.")

            for i, matiere in enumerate(matieres.keys()):
                for j, semaine in enumerate(semaines):
                    checkbox_vars[i][j].set(etat_devoirs.get(matiere, {}).get(str(semaine), 0))

            root.title(f"Calendrier des devoirs - {filepath}")
            fichier_charge = filepath

        except (json.JSONDecodeError, FileNotFoundError):
            messagebox.showerror("Erreur", "Erreur lors du chargement du fichier.")
            print("Erreur lors du chargement du fichier.")
        except ValueError as ve:
            ctypes.windll.user32.MessageBoxW(0, str(ve), "Erreur de fichier", 1)
            print(str(ve))

# Fonction pour afficher les informations
def afficher_informations():
    info_window = tk.Toplevel(root)
    info_window.title("Informations")

    with open(config_file_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    # Ajouter les informations sur le logiciel
    version_label = tk.Label(info_window, text="Version " + config.get("version"))
    version_label.pack(pady=10)

    developer_label = tk.Label(info_window, text="Développé par: gltdevlop")
    developer_label.pack(pady=10)

    close_button = tk.Button(info_window, text="Fermer", command=info_window.destroy)
    close_button.pack(pady=10)


# Fonction pour sauvegarder les devoirs après modification
def sauvegarder_devoirs(devoirs):
    with open("json-files/devoirs.json", "w", encoding="utf-8") as f:
        json.dump(devoirs, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Succès", "Les devoirs ont été mis à jour.")


# Fonction pour modifier les matières
# Fonction pour modifier les matières avec une scrollbar verticale
def modifier_matieres():
    matiere_window = tk.Toplevel(root)
    matiere_window.title("Modifier les matières")

    # Frame pour le canvas et la scrollbar
    frame_canvas = tk.Frame(matiere_window)
    frame_canvas.pack(fill="both", expand=True)

    # Canvas pour les matières
    matiere_canvas = tk.Canvas(frame_canvas)
    matiere_canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar verticale
    scrollbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=matiere_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    matiere_canvas.configure(yscrollcommand=scrollbar.set)

    # Frame pour les matières dans le canvas
    matiere_frame = tk.Frame(matiere_canvas)
    matiere_canvas.create_window((0, 0), window=matiere_frame, anchor="nw")

    # Charger les matières prédéfinies et sélectionnées
    with open("json-files/predefined_matieres.json", "r", encoding="utf-8") as f:
        predefined_matieres = json.load(f)

    with open("json-files/matieres.json", "r", encoding="utf-8") as f:
        selected_matieres = json.load(f)

    checkbox_vars = {}

    # Fonction pour sauvegarder les matières modifiées
    def sauvegarder_matieres():
        nouvelles_matieres = {}
        nouvelles_matieres_devoirs = {}

        for matiere_id, var in checkbox_vars.items():
            if var.get() == 1:
                nouvelles_matieres[matiere_id] = predefined_matieres[matiere_id]
                if matiere_id not in devoirs:
                    nouvelles_matieres_devoirs[matiere_id] = {}
            elif matiere_id in devoirs:
                devoirs.pop(matiere_id)

        with open("json-files/matieres.json", "w", encoding="utf-8") as f:
            json.dump(nouvelles_matieres, f, ensure_ascii=False, indent=4)

        devoirs.update(nouvelles_matieres_devoirs)
        sauvegarder_devoirs(devoirs)
        charger_matieres()
        charger_devoirs()
        messagebox.showinfo("Succès", "Les matières ont été mises à jour.")
        matiere_window.destroy()

    # Afficher les matières à cocher
    for matiere_id, matiere_nom in predefined_matieres.items():
        var = tk.IntVar()
        if matiere_id in selected_matieres:
            var.set(1)
        checkbox = tk.Checkbutton(matiere_frame, text=matiere_nom, variable=var)
        checkbox.pack(anchor='w')
        checkbox_vars[matiere_id] = var

    # Boutons Enregistrer et Annuler
    save_button = tk.Button(matiere_window, text="Enregistrer", command=sauvegarder_matieres)
    save_button.pack(pady=10)

    close_button = tk.Button(matiere_window, text="Annuler", command=matiere_window.destroy)
    close_button.pack(pady=5)

    # Mise à jour de la scrollbar
    matiere_frame.update_idletasks()
    matiere_canvas.configure(scrollregion=matiere_canvas.bbox("all"))
# Fonction pour modifier les devoirs avec des scrollbars verticale et horizontale
def modifier_devoirs():
    devoir_window = tk.Toplevel(root)
    devoir_window.title("Modifier les devoirs")

    # Frame pour le canvas et les scrollbars
    frame_canvas = tk.Frame(devoir_window)
    frame_canvas.pack(fill="both", expand=True)

    # Canvas pour les devoirs
    devoir_canvas = tk.Canvas(frame_canvas)
    devoir_canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar verticale
    v_scrollbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=devoir_canvas.yview)
    v_scrollbar.pack(side="right", fill="y")

    # Scrollbar horizontale
    h_scrollbar = ttk.Scrollbar(devoir_window, orient="horizontal", command=devoir_canvas.xview)
    h_scrollbar.pack(side="bottom", fill="x")

    devoir_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Frame pour les devoirs dans le canvas
    devoir_frame = tk.Frame(devoir_canvas)
    devoir_canvas.create_window((0, 0), window=devoir_frame, anchor="nw")

    # Charger les matières et les devoirs
    with open("json-files/matieres.json", "r", encoding="utf-8") as f:
        selected_matieres = json.load(f)

    with open("json-files/devoirs.json", "r", encoding="utf-8") as f:
        devoirs = json.load(f)

    devoir_vars = {}

    # Fonction pour sauvegarder les devoirs modifiés
    def sauvegarder_devoirs_modifies():
        for matiere_id, semaine_vars in devoir_vars.items():
            for semaine, var in semaine_vars.items():
                if var.get() == 1:
                    devoirs[matiere_id][semaine] = f"Devoir {len(devoirs[matiere_id]) + 1}"
                elif semaine in devoirs[matiere_id]:
                    devoirs[matiere_id].pop(semaine)

        sauvegarder_devoirs(devoirs)
        charger_matieres()
        charger_devoirs()
        devoir_window.destroy()

    # Afficher les cases à cocher pour les semaines de chaque matière
    for matiere_id, matiere_nom in selected_matieres.items():
        label = tk.Label(devoir_frame, text=f"{matiere_nom} :")
        label.pack(anchor='w')

        semaine_vars = {}
        week_frame = tk.Frame(devoir_frame)
        week_frame.pack(anchor='w')

        for semaine in semaines:
            var = tk.IntVar()
            if str(semaine) in devoirs.get(matiere_id, {}):
                var.set(1)
            checkbox = tk.Checkbutton(week_frame, text=f"S{semaine}", variable=var)
            checkbox.pack(side='left')
            semaine_vars[semaine] = var

        devoir_vars[matiere_id] = semaine_vars

    # Bouton pour sauvegarder
    save_button = tk.Button(devoir_window, text="Enregistrer", command=sauvegarder_devoirs_modifies)
    save_button.pack(pady=10)

    # Bouton pour annuler
    close_button = tk.Button(devoir_window, text="Annuler", command=devoir_window.destroy)
    close_button.pack(pady=5)

    # Mise à jour de la scrollbar
    devoir_frame.update_idletasks()
    devoir_canvas.configure(scrollregion=devoir_canvas.bbox("all"))


# Fonction appelée lors de la fermeture de l'application
def on_closing():
    if messagebox.askyesnocancel("Confirmation", "Voulez-vous enregistrer vos modifications avant de quitter ?"):
        sauvegarder(filepath=fichier_charge)
        root.destroy()
    elif messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir quitter sans enregistrer ?"):
        root.destroy()

# Créer un canvas avec une barre de défilement
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar.set)

# Créer un frame à l'intérieur du canvas pour contenir le tableau
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Créer les en-têtes des colonnes (numéros de semaines)
for j, semaine in enumerate(semaines):
    header_label = tk.Label(frame, text=f"S{semaine}", font=("Arial", 12, "bold"))
    header_label.grid(row=0, column=j * 2 + 2, padx=2, pady=2, sticky="nsew")

    # Ajouter une ligne de séparation horizontale
    tk.Frame(frame, height=2, bg="black").grid(row=1, columnspan=len(semaines) * 2 + 2, sticky="ew")

    # Ajouter une ligne verticale après chaque colonne
    if j < len(semaines) - 1:
        tk.Frame(frame, width=2, bg="black").grid(row=0, column=j * 2 + 3, rowspan=len(matieres) * 2 + 2, sticky="ns")

# Créer les en-têtes des lignes (noms des matières)
for i, (matiere_code, matiere_nom) in enumerate(matieres.items()):
    tk.Label(frame, text=matiere_nom, font=("Arial", 12)).grid(row=i * 2 + 2, column=0, padx=2, pady=2, sticky="nsew")

    row_vars = []
    for j, semaine in enumerate(semaines):
        var = tk.IntVar()
        # Créer un style personnalisé pour les cases à cocher plus grandes
        style = ttk.Style()
        style.configure('Large.TCheckbutton', padding=10)
        checkbox = ttk.Checkbutton(frame, variable=var, style='Large.TCheckbutton')
        checkbox.grid(row=i * 2 + 2, column=j * 2 + 2, padx=2, pady=2)
        row_vars.append(var)

        # Ajouter une description sous chaque case à cocher
        if matiere_code in devoirs and str(semaine) in devoirs[matiere_code]:
            description_devoir = devoirs[matiere_code][str(semaine)]
            tk.Label(frame, text=description_devoir, font=("Arial", 10)).grid(row=i * 2 + 3, column=j * 2 + 2, padx=2, pady=2, sticky="nsew")

    checkbox_vars.append(row_vars)

# Mettre à jour la taille de la fenêtre et du canvas pour s'adapter au contenu
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))
canvas.pack(side="top", fill="both", expand=True)
scrollbar.pack(side="bottom", fill="x")

# Ajouter une barre de menus
menu_bar = Menu(root)

# Menu Fichier
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Charger (Ctrl + O)", command=charger)
file_menu.add_command(label="Sauvegarder (Ctrl + S)", command=lambda: sauvegarder(fichier_charge))
file_menu.add_command(label="Enregistrer sous (Ctrl + Shift + S)", command=enregistrer_sous)
file_menu.add_separator()
file_menu.add_command(label="Quitter", command=on_closing)
menu_bar.add_cascade(label="Fichier", menu=file_menu)

# Menu Options
opt_menu = Menu(menu_bar, tearoff=0)
opt_menu.add_command(label="Modifier les matières", command=modifier_matieres)
opt_menu.add_command(label="Modifier les devoirs", command=modifier_devoirs)
menu_bar.add_cascade(label="Options", menu=opt_menu)

# Menu Aide
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="À propos", command=afficher_informations)
menu_bar.add_cascade(label="Aide", menu=help_menu)

root.config(menu=menu_bar)

# Ajouter les raccourcis clavier
root.bind("<Control-s>", lambda event: sauvegarder(fichier_charge))
root.bind("<Control-S>", lambda event: sauvegarder(fichier_charge))  # Pour majuscule
root.bind("<Control-Shift-s>", lambda event: enregistrer_sous())
root.bind("<Control-o>", lambda event: charger())

# Lier la fonction de fermeture de fenêtre personnalisée
root.protocol("WM_DELETE_WINDOW", on_closing)

# Lancer l'application
root.geometry('1000x600')
root.mainloop()

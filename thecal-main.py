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

# Fonction pour modifier les matières (le contenu sera ajouté plus tard)
def modifier_matieres():
    # Ici, on ajoutera le contenu pour gérer la modification des matières
    messagebox.showinfo("Modifier les matières", "Fonctionnalité à implémenter.")

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
root.mainloop()

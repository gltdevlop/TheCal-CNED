import tkinter as tk
from tkinter import ttk, filedialog, Menu, messagebox
import json
import os
import ctypes  # Importer le module ctypes pour afficher des boîtes de dialogue

# Créer la fenêtre principale
root = tk.Tk()
root.title("Calendrier des devoirs")

# Vérifier et créer le fichier de configuration si ce n'est pas encore fait
config_file_path = "config.json"
if not os.path.exists(config_file_path):
    with open(config_file_path, "w", encoding="utf-8") as config_file:
        json.dump({"dark_mode": False}, config_file)  # Écrire un état par défaut pour le mode sombre

# Charger la configuration
with open(config_file_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

# Numéros de semaine (de 36 à 22)
semaines = list(range(36, 53)) + list(range(1, 23))

# Charger la liste des matières et la planification depuis les fichiers JSON
def charger_matieres():
    print("Json matières chargé")
    with open("matieres.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def charger_devoirs():
    print("Json devoirs chargé")
    with open("devoirs.json", "r", encoding="utf-8") as json_file:
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
    global fichier_charge  # Rendre la variable globale
    # Utiliser un sélecteur de fichiers pour charger un fichier JSON
    filepath = filedialog.askopenfilename(
        title="Charger un fichier JSON",
        filetypes=(("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*"))
    )

    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as json_file:
                etat_devoirs = json.load(json_file)

            # Vérifier si le fichier contient "file-state" avec la valeur 1
            if etat_devoirs.get("file-state") != 1:
                raise ValueError("Le fichier ne contient pas un état valide.")

            # Mettre à jour l'état des checkboxes
            for i, matiere in enumerate(matieres.keys()):
                for j, semaine in enumerate(semaines):
                    checkbox_vars[i][j].set(etat_devoirs.get(matiere, {}).get(str(semaine), 0))

            # Mettre à jour le titre de la fenêtre avec le chemin du fichier chargé
            root.title(f"Calendrier des devoirs - {filepath}")
            fichier_charge = filepath  # Mettez à jour le fichier chargé
            print(f"État chargé depuis '{filepath}'.")
        except (json.JSONDecodeError, FileNotFoundError):
            # Afficher une boîte de dialogue d'erreur
            messagebox.showerror("Erreur", "Erreur lors du chargement du fichier.")
            print("Erreur lors du chargement du fichier.")
        except ValueError as ve:
            # Utiliser ctypes pour afficher l'erreur
            ctypes.windll.user32.MessageBoxW(0, str(ve), "Erreur de fichier", 1)
            print(str(ve))
    else:
        print("Aucun fichier sélectionné ou fichier introuvable.")

# Fonction pour sauvegarder manuellement l'état des cases cochées dans un fichier JSON
def sauvegarder(filepath=None):
    etat_devoirs = {"file-state": 1}  # Ajouter la variable "file-state" avec la valeur 1
    for i, matiere in enumerate(matieres.keys()):
        etat_devoirs[matiere] = {}
        for j, semaine in enumerate(semaines):
            etat_devoirs[matiere][semaine] = checkbox_vars[i][j].get()

    # Si aucun chemin n'est fourni, utiliser un sélecteur de fichiers
    if not filepath:
        filepath = filedialog.asksaveasfilename(
            title="Sauvegarder le fichier JSON",
            defaultextension=".json",
            filetypes=(("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")),
            initialfile="etat_devoirs.json"
        )

    if filepath:  # Sauvegarder uniquement si un chemin a été sélectionné
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(etat_devoirs, json_file, ensure_ascii=False, indent=4)
        global fichier_charge  # Mettez à jour le fichier chargé
        fichier_charge = filepath  # Enregistrer le chemin du fichier
        print(f"État sauvegardé dans '{filepath}'.")

        # Charger automatiquement le fichier sauvegardé
        charger_fichier(filepath)

# Fonction pour "Enregistrer sous"
def enregistrer_sous():
    # Appeler la fonction sauvegarder qui va également charger le fichier
    sauvegarder()

# Fonction pour charger un fichier et mettre à jour l'état des cases
def charger_fichier(filepath):
    global fichier_charge  # Rendre la variable globale
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as json_file:
                etat_devoirs = json.load(json_file)

            # Vérifier si le fichier contient "file-state" avec la valeur 1
            if etat_devoirs.get("file-state") != 1:
                raise ValueError("Le fichier ne contient pas un état valide.")

            # Mettre à jour l'état des checkboxes
            for i, matiere in enumerate(matieres.keys()):
                for j, semaine in enumerate(semaines):
                    checkbox_vars[i][j].set(etat_devoirs.get(matiere, {}).get(str(semaine), 0))

            # Mettre à jour le titre de la fenêtre avec le chemin du fichier chargé
            root.title(f"Calendrier des devoirs - {filepath}")
            fichier_charge = filepath  # Mettez à jour le fichier chargé

            # Ne pas afficher la popup de succès ici
        except (json.JSONDecodeError, FileNotFoundError):
            # Afficher une boîte de dialogue d'erreur
            messagebox.showerror("Erreur", "Erreur lors du chargement du fichier.")
            print("Erreur lors du chargement du fichier.")
        except ValueError as ve:
            # Utiliser ctypes pour afficher l'erreur
            ctypes.windll.user32.MessageBoxW(0, str(ve), "Erreur de fichier", 1)
            print(str(ve))

# Fonction pour afficher les informations
def afficher_informations():
    # Créer une nouvelle fenêtre pour afficher les informations
    info_window = tk.Toplevel(root)
    info_window.title("Informations")

    with open(config_file_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

            # Ajouter les informations sur le logiciel
    version_label = tk.Label(info_window, text="Version " + config.get("version"))
    version_label.pack(pady=10)

    developer_label = tk.Label(info_window, text="Développé par: gltdevlop")
    developer_label.pack(pady=10)

    # Ajouter un bouton pour fermer la fenêtre
    close_button = tk.Button(info_window, text="Fermer", command=info_window.destroy)
    close_button.pack(pady=10)

# Fonction appelée lors de la fermeture de l'application
def on_closing():
    if messagebox.askyesnocancel("Confirmation", "Voulez-vous enregistrer vos modifications avant de quitter ?"):
        sauvegarder(filepath=fichier_charge)
        root.destroy()  # Ferme l'application après sauvegarde
    elif messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir quitter sans enregistrer ?"):
        root.destroy()  # Ferme l'application sans sauvegarder
    # Si l'utilisateur choisit 'Annuler', ne rien faire

# Créer un canvas avec une barre de défilement
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar.set)

# Créer un frame à l'intérieur du canvas pour contenir le tableau
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Créer les en-têtes des colonnes (numéros de semaines)
for j, semaine in enumerate(semaines):
    header_label = tk.Label(frame, text=f"S{semaine}", font=("Arial", 10, "bold"))
    header_label.grid(row=0, column=j + 2, padx=1, pady=1, sticky="nsew")

    # Ajouter une ligne de séparation horizontale
    tk.Frame(frame, height=2, bg="black").grid(row=1, column=j + 2, sticky="ew")

# Créer les en-têtes des lignes (noms des matières)
for i, (matiere_code, matiere_nom) in enumerate(matieres.items()):
    tk.Label(frame, text=matiere_nom, font=("Arial", 10)).grid(row=i * 2 + 2, column=1, padx=1, pady=1, sticky="nsew")

    row_vars = []
    for j, semaine in enumerate(semaines):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(frame, variable=var)
        checkbox.grid(row=i * 2 + 2, column=j + 2, padx=1, pady=1)
        row_vars.append(var)

        # Ajouter une description sous chaque case à cocher
        if matiere_code in devoirs and str(semaine) in devoirs[matiere_code]:
            description_devoir = devoirs[matiere_code][str(semaine)]
            tk.Label(frame, text=description_devoir).grid(row=i * 2 + 3, column=j + 2, padx=1, pady=1)

    checkbox_vars.append(row_vars)

    # Ajouter une ligne de séparation horizontale après chaque matière
    tk.Frame(frame, height=2, bg="black").grid(row=i * 2 + 4, columnspan=len(semaines) + 2, sticky="ew")

# Configurer le canvas pour avoir une barre de défilement
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def left():
    quit()


frame.bind("<Configure>", on_frame_configure)

# Ajouter le canvas et la barre de défilement à la fenêtre principale
canvas.pack(side="top", fill="both", expand=True)
scrollbar.pack(side="bottom", fill="x")

# Créer un menu avec les options "Charger", "Sauvegarder", "Informations"
menu = Menu(root)
root.config(menu=menu)

# Menu Fichier
file_menu = Menu(menu, tearoff=0)  # Retirer le menu flottant
menu.add_cascade(label="Fichier", menu=file_menu)
file_menu.add_command(label="Charger (Ctrl + O)", command=charger)
file_menu.add_command(label="Enregistrer (Ctrl + S)", command=lambda: sauvegarder(filepath=fichier_charge))
file_menu.add_command(label="Enregistrer sous (Ctrl + Maj + S)", command=enregistrer_sous)
file_menu.add_command(label="Informations", command=afficher_informations)

opt_menu = Menu(menu, tearoff=0)  # Retirer le menu flottant
menu.add_cascade(label="Options", menu=opt_menu)
opt_menu.add_command(label="Quitter", command=left)

# Raccourcis clavier
root.bind('<Control-o>', lambda event: charger())
root.bind('<Control-s>', lambda event: sauvegarder(filepath=fichier_charge))
root.bind('<Control-S>', lambda event: enregistrer_sous())
root.bind('<Control-Shift-S>', lambda event: enregistrer_sous())
root.geometry('1000x600')

# Associer la fonction on_closing à la fermeture de la fenêtre
root.protocol("WM_DELETE_WINDOW", on_closing)

# Démarrer la boucle principale de l'application
root.mainloop()

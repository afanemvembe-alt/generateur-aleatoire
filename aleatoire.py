import secrets
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    fruit = fruit_entry.get().strip()
    animal = animal_entry.get().strip()
    date = date_entry.get().strip()
    
    # 1. Vérification de la longueur entré par l'utilisateur
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur de saisie", "La longueur doit être un nombre entier supérieur à 0.")
        return

    # 2. Collecte des critères personnalisés
    criteria = [x for x in [fruit, animal, date] if x]
    base = "".join(criteria)
    
    if not base:
        messagebox.showwarning("Champs vides", "Veuillez remplir au moins un critère personnalisé (fruit, animal ou date).")
        return

    if length < len(base):
        messagebox.showwarning(
            "Longueur insuffisante", 
            f"La longueur totale demandée ({length}) est trop courte pour contenir vos mots personnalisés (longueur requise minimale : {len(base)})."
        )
        return

    # 3. Génération sécurisée de la partie aléatoire (utilisation de secrets)
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    remaining_length = length - len(base)
    random_part = ''.join(secrets.choice(characters) for _ in range(remaining_length))
    
    # 4. Mélange sécurisé des caractères
    password_list = list(base + random_part)
    secrets.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)

    # 5. Affichage du résultat dans le champ protégé
    result_entry.config(state="normal")
    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)
    result_entry.config(state="readonly")

def copy_password():
    password = result_entry.get()
    if not password:
        messagebox.showwarning("Presse-papier", "Il n'y a aucun mot de passe généré à copier.")
        return
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Succès", "Le mot de passe a été copié dans le presse-papier.")

# --- Fonctions de design pour l'effet au survol des boutons ---
def on_enter_generate(e):
    btn_generate.config(bg="#2980b9")

def on_leave_generate(e):
    btn_generate.config(bg="#3498db")

def on_enter_copy(e):
    btn_copy.config(bg="#27ae60")

def on_leave_copy(e):
    btn_copy.config(bg="#2ecc71")


# ---- Fenêtre principale ----
root = tk.Tk()
root.title("Générateur de Mot de Passe Sécurisé")

# Configuration de la taille et centrage automatique sur l'écran
window_width = 450
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.configure(bg="#f8fafc")

# Titre principal
title_label = tk.Label(root, text="Générateur de Mot de Passe", font=("Helvetica", 16, "bold"), bg="#f8fafc", fg="#1e293b")
title_label.pack(pady=20)

# Grille d'alignement pour les formulaires
frame_inputs = tk.Frame(root, bg="#f8fafc")
frame_inputs.pack(pady=10)

# Labels et Champs de texte
label_style = {"font": ("Helvetica", 11), "bg": "#f8fafc", "fg": "#475569"}
entry_style = {"font": ("Helvetica", 11), "bd": 1, "relief": "solid"}

tk.Label(frame_inputs, text="Fruit préféré :", **label_style).grid(row=0, column=0, sticky="e", padx=8, pady=6)
fruit_entry = tk.Entry(frame_inputs, **entry_style)
fruit_entry.grid(row=0, column=1, padx=8, pady=6, ipady=3)

tk.Label(frame_inputs, text="Animal préféré :", **label_style).grid(row=1, column=0, sticky="e", padx=8, pady=6)
animal_entry = tk.Entry(frame_inputs, **entry_style)
animal_entry.grid(row=1, column=1, padx=8, pady=6, ipady=3)

tk.Label(frame_inputs, text="Date de naissance :", **label_style).grid(row=2, column=0, sticky="e", padx=8, pady=6)
date_entry = tk.Entry(frame_inputs, **entry_style)
date_entry.grid(row=2, column=1, padx=8, pady=6, ipady=3)

tk.Label(frame_inputs, text="Longueur totale :", **label_style).grid(row=3, column=0, sticky="e", padx=8, pady=6)
length_entry = tk.Entry(frame_inputs, **entry_style)
length_entry.insert(0, "12")  # Valeur par défaut recommandée
length_entry.grid(row=3, column=1, padx=8, pady=6, ipady=3)

# Bouton de génération
btn_generate = tk.Button(root, text="Générer le mot de passe", command=generate_password,
                         bg="#3498db", fg="white", font=("Helvetica", 11, "bold"), 
                         bd=0, cursor="hand2", activebackground="#2980b9", activeforeground="white")
btn_generate.pack(pady=20, ipadx=15, ipady=6)
btn_generate.bind("<Enter>", on_enter_generate)
btn_generate.bind("<Leave>", on_leave_generate)

# Section d'affichage du résultat
result_frame = tk.Frame(root, bg="#f8fafc")
result_frame.pack(pady=10)

result_entry = tk.Entry(result_frame, font=("Consolas", 13, "bold"), width=22, justify="center", bd=1, relief="solid")
result_entry.pack(side="left", padx=5, ipady=4)
result_entry.config(state="readonly")

# Bouton de copie
btn_copy = tk.Button(result_frame, text="Copier", command=copy_password,
                     bg="#2ecc71", fg="white", font=("Helvetica", 11, "bold"), 
                     bd=0, cursor="hand2", activebackground="#27ae60", activeforeground="white")
btn_copy.pack(side="left", padx=5, ipadx=10, ipady=4)
btn_copy.bind("<Enter>", on_enter_copy)
btn_copy.bind("<Leave>", on_leave_copy)

root.mainloop()

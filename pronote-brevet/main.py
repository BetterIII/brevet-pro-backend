#!/usr/bin/env python3
"""Brevet Pro - calculateur et simulateur d'examen."""

import json
import threading
import uuid
import webbrowser
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from examens import MATIERES, SUJETS, note_matiere

DOSSIER = Path(__file__).parent
CREDENTIALS = DOSSIER / "credentials.json"
SETTINGS = DOSSIER / "settings.json"
HISTORY = DOSSIER / "history.json"
APP_UUID = "brevet-pro-" + uuid.uuid4().hex[:8]

THEMES = {
    "dark": {
        "bg": "#0f172a",
        "sidebar": "#1e293b",
        "card": "#1e293b",
        "card_border": "#334155",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "accent": "#3b82f6",
        "accent_hover": "#2563eb",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "input": "#334155",
    },
    "light": {
        "bg": "#f8fafc",
        "sidebar": "#ffffff",
        "card": "#ffffff",
        "card_border": "#e2e8f0",
        "text": "#0f172a",
        "muted": "#64748b",
        "accent": "#2563eb",
        "accent_hover": "#1d4ed8",
        "success": "#16a34a",
        "warning": "#d97706",
        "danger": "#dc2626",
        "input": "#f1f5f9",
    },
}


def charger_json(chemin, default=None):
    if chemin.exists():
        try:
            return json.loads(chemin.read_text(encoding="utf-8"))
        except Exception:
            pass
    return default if default is not None else {}


def sauver_json(chemin, data):
    chemin.write_text(json.dumps(data, indent=2), encoding="utf-8")


def lire_note(texte):
    try:
        n = float(str(texte).strip().replace(",", "."))
        return n if 0 <= n <= 20 else None
    except ValueError:
        return None


def mention_brevet(finale):
    if finale >= 18:
        return "Tres bien avec felicitations du jury"
    if finale >= 16:
        return "Tres bien"
    if finale >= 14:
        return "Bien"
    if finale >= 12:
        return "Assez bien"
    if finale >= 10:
        return "Admis sans mention"
    return None


def calculer_brevet(moyenne_cc, note_epreuves):
    finale = round(moyenne_cc * 0.4 + note_epreuves * 0.6, 2)
    mention = mention_brevet(finale)
    if mention:
        verdict = f"BREVET OBTENU\nMention : {mention}"
    else:
        verdict = f"BREVET NON OBTENU\nIl te manque {round(10 - finale, 2)} pt(s) sur 20"
    return finale, verdict, mention


# --- Pronote ---

def decoder_qr_image(chemin):
    import cv2

    img = cv2.imread(str(chemin))
    if img is None:
        raise Exception("Image illisible.")
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    if not data:
        raise Exception("Aucun QR code trouve.")
    return json.loads(data)


def type_client(url):
    import pronotepy

    return pronotepy.ParentClient if "parent" in url else pronotepy.Client


def lier_compte(qr_data, pin):
    from pronotepy import MFAError

    client_class = type_client(qr_data.get("url", ""))
    cfg = charger_json(CREDENTIALS) or {}
    app_uuid = cfg.get("uuid", APP_UUID)
    try:
        client = client_class.qrcode_login(qr_data, pin, app_uuid, device_name="Brevet Pro")
    except MFAError:
        code = simpledialog.askstring("Securite", "Code PIN de ton compte Pronote :")
        client = client_class.qrcode_login(
            qr_data, pin, app_uuid, account_pin=code, device_name="Brevet Pro"
        )
    if not client.logged_in:
        raise Exception("Liaison refusee.")
    creds = client.export_credentials()
    creds["uuid"] = app_uuid
    sauver_json(CREDENTIALS, creds)
    return client


def reconnecter():
    creds = charger_json(CREDENTIALS)
    if not creds:
        return None
    import pronotepy

    client_class = type_client(creds.get("pronote_url", ""))
    try:
        kwargs = {
            "pronote_url": creds["pronote_url"],
            "username": creds["username"],
            "password": creds["password"],
            "uuid": creds.get("uuid", APP_UUID),
        }
        if creds.get("client_identifier"):
            kwargs["client_identifier"] = creds["client_identifier"]
        client = client_class.token_login(**kwargs)
        if not client.logged_in:
            return None
        sauver_json(CREDENTIALS, {**client.export_credentials(), "uuid": creds.get("uuid", APP_UUID)})
        return client
    except Exception:
        return None


def moyenne_pronote(client):
    notes, periodes = [], []
    for periode in client.periods:
        periodes.append(periode.name)
        for m in periode.averages:
            try:
                n = float(str(m.student).replace(",", "."))
                if 0 <= n <= 20:
                    notes.append(n)
            except ValueError:
                pass
    if not notes:
        raise Exception("Aucune note trouvee.")
    return round(sum(notes) / len(notes), 2), periodes


class StyledButton(tk.Button):
    def __init__(self, master, theme, kind="primary", **kw):
        colors = {
            "primary": (theme["accent"], "white", theme["accent_hover"]),
            "success": (theme["success"], "white", theme["success"]),
            "ghost": (theme["card"], theme["text"], theme["card_border"]),
            "danger": (theme["danger"], "white", theme["danger"]),
        }
        bg, fg, active = colors.get(kind, colors["primary"])
        super().__init__(
            master,
            bg=bg,
            fg=fg,
            activebackground=active,
            activeforeground=fg,
            relief="flat",
            cursor="hand2",
            font=kw.pop("font", ("Segoe UI", 10, "bold")),
            padx=kw.pop("padx", 20),
            pady=kw.pop("pady", 8),
            **kw,
        )
        self.bind("<Enter>", lambda e: self.config(bg=active))
        self.bind("<Leave>", lambda e: self.config(bg=bg))


class DialogLiaison(tk.Toplevel):
    def __init__(self, parent, theme, on_success):
        super().__init__(parent)
        self.title("Lier Pronote")
        self.geometry("440x400")
        self.configure(bg=theme["bg"])
        self.on_success = on_success
        self.transient(parent)
        self.grab_set()

        tk.Label(
            self, text="Lier ton compte Pronote", font=("Segoe UI", 16, "bold"),
            bg=theme["bg"], fg=theme["text"],
        ).pack(pady=(20, 12))

        instructions = (
            "📱 1. Ouvre l'app Pronote sur ton téléphone\n"
            "📋 2. Menu → QR code → Afficher mon QR code\n"
            "🔢 3. Note le code PIN à 4 chiffres\n"
            "📸 4. Capture le QR code"
        )
        tk.Label(
            self,
            text=instructions,
            justify="left", bg=theme["bg"], fg=theme["muted"],
            font=("Segoe UI", 10),
        ).pack(padx=20, anchor="w", pady=(0, 16))

        frame = tk.Frame(self, bg=theme["card"], highlightbackground=theme["card_border"], highlightthickness=1)
        frame.pack(fill="x", padx=20, pady=8)
        tk.Label(frame, text="PIN Pronote (4 chiffres) :", bg=theme["card"], fg=theme["text"], font=("Segoe UI", 10, "bold")).pack(side="left", padx=12, pady=12)
        self.pin = tk.Entry(frame, width=8, font=("Segoe UI", 14, "bold"), justify="center", bg=theme["input"], fg=theme["text"], relief="flat")
        self.pin.pack(side="left", padx=8, pady=12)

        StyledButton(self, theme, text="📸 Importer capture QR", command=self.importer).pack(fill="x", padx=20, pady=6)
        StyledButton(self, theme, kind="ghost", text="📋 Coller texte QR", command=self.coller).pack(fill="x", padx=20, pady=(0, 8))
        self.status = tk.Label(self, text="", bg=theme["bg"], fg=theme["accent"], font=("Segoe UI", 10, "bold"))
        self.status.pack(pady=8)

    def pin_ok(self):
        p = self.pin.get().strip()
        return p if len(p) == 4 and p.isdigit() else None

    def finaliser(self, qr_data):
        pin = self.pin_ok()
        if not pin:
            messagebox.showwarning("PIN", "Entre 4 chiffres.")
            return
        self.status.config(text="Connexion...")

        def task():
            try:
                client = lier_compte(qr_data, pin)
                moy, periodes = moyenne_pronote(client)
                nom = client.info.name if client.info else "Eleve"
                self.after(0, lambda: self.on_success(moy, periodes, nom))
                self.after(0, self.destroy)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erreur", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def importer(self):
        if not self.pin_ok():
            return
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            try:
                self.finaliser(decoder_qr_image(path))
            except Exception as e:
                messagebox.showerror("QR", str(e))

    def coller(self):
        if not self.pin_ok():
            return
        try:
            self.finaliser(json.loads(self.clipboard_get().strip()))
        except Exception:
            messagebox.showerror("Erreur", "Presse-papier invalide.")


class ExamSimulator(tk.Frame):
    """Simulateur brevet - progression sans retour arriere."""

    def __init__(self, master, app):
        super().__init__(master, bg=app.theme["bg"])
        self.app = app
        self.idx = 0
        self.reponses = {}  # cle matiere -> list indices
        self.notes_matiere = {}  # cle matiere -> note /20
        self.var_choices = []
        self.termine = False
        self.build_start()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def build_start(self):
        self.clear()
        t = self.app.theme
        card = tk.Frame(self, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(
            card, text="🎓 Simulateur Brevet Blanc", font=("Segoe UI", 20, "bold"),
            bg=t["card"], fg=t["text"],
        ).pack(pady=(28, 12))
        tk.Label(
            card,
            text="✓ 7 matières au programme\n✓ Sujets types des sessions précédentes\n✓ Pas de retour en arrière\n✓ Résultats détaillés à la fin",
            bg=t["card"], fg=t["muted"], justify="center", font=("Segoe UI", 11),
        ).pack(pady=8)

        tk.Label(card, text="📚 Matières au programme :", bg=t["card"], fg=t["text"], font=("Segoe UI", 11, "bold")).pack(pady=(20, 8))
        matieres_frame = tk.Frame(card, bg=t["card"])
        matieres_frame.pack(pady=8)
        for i, (nom, _) in enumerate(MATIERES):
            tk.Label(matieres_frame, text=f"• {nom}", bg=t["card"], fg=t["muted"], font=("Segoe UI", 10)).pack(anchor="w", padx=40, pady=2)

        StyledButton(
            card, t, kind="success", text="COMMENCER LE BREVET BLANC",
            command=self.demarrer, font=("Segoe UI", 12, "bold"),
        ).pack(fill="x", padx=40, pady=24, ipady=10)

    def demarrer(self):
        self.idx = 0
        self.reponses = {}
        self.notes_matiere = {}
        self.termine = False
        self.afficher_matiere()

    def afficher_matiere(self):
        self.clear()
        t = self.app.theme
        nom, cle = MATIERES[self.idx]
        questions = SUJETS[cle]
        self.var_choices = [tk.IntVar(value=-1) for _ in questions]

        # Barre progression
        prog = tk.Frame(self, bg=t["sidebar"], height=8)
        prog.pack(fill="x")
        pct = self.idx / len(MATIERES)
        tk.Frame(prog, bg=t["accent"], width=int(700 * pct), height=8).pack(side="left")

        header = tk.Frame(self, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        header.pack(fill="x", padx=8, pady=8)
        tk.Label(
            header,
            text=f"📖 {nom} ({self.idx + 1}/{len(MATIERES)})",
            font=("Segoe UI", 15, "bold"), bg=t["card"], fg=t["text"],
        ).pack(side="left", padx=16, pady=14)
        if self.app.settings.get("chrono"):
            tk.Label(header, text="⏱ Chrono actif", bg=t["card"], fg=t["warning"], font=("Segoe UI", 10, "bold")).pack(side="right", padx=16)

        canvas = tk.Canvas(self, bg=t["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=t["bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(8, 0))
        scroll.pack(side="right", fill="y")

        for i, q in enumerate(questions):
            qf = tk.Frame(inner, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
            qf.pack(fill="x", pady=8, padx=4)
            
            # Question header
            q_header = tk.Frame(qf, bg=t["accent"])
            q_header.pack(fill="x")
            tk.Label(
                q_header, text=f" Question {i+1} ", font=("Segoe UI", 9, "bold"),
                bg=t["accent"], fg="white",
            ).pack(side="left", padx=8, pady=4)
            tk.Label(
                q_header, text=f"Session {q['annee']}", font=("Segoe UI", 8),
                bg=t["accent"], fg=t["muted"],
            ).pack(side="right", padx=8, pady=4)
            
            tk.Label(
                qf, text=q["question"], font=("Segoe UI", 11, "bold"), wraplength=620,
                bg=t["card"], fg=t["text"], justify="left",
            ).pack(anchor="w", padx=12, pady=(10, 8))
            for j, choix in enumerate(q["choices"]):
                rb = tk.Radiobutton(
                    qf, text=f"  {choix}", variable=self.var_choices[i], value=j,
                    bg=t["card"], fg=t["text"], selectcolor=t["input"],
                    activebackground=t["card"], font=("Segoe UI", 10),
                    anchor="w", wraplength=580, justify="left", indicatoron=0,
                    padx=12, pady=6, relief="flat",
                )
                rb.pack(anchor="w", padx=12, pady=3, fill="x")
                rb.bind("<Enter>", lambda e, b=rb: b.config(bg=t["input"]))
                rb.bind("<Leave>", lambda e, b=rb: b.config(bg=t["card"]))
            tk.Frame(qf, height=12, bg=t["card"]).pack()

        footer = tk.Frame(self, bg=t["sidebar"])
        footer.pack(fill="x", side="bottom")
        label_btn = "PASSER A LA MATIERE SUIVANTE →" if self.idx < len(MATIERES) - 1 else "TERMINER LE BREVET BLANC"
        StyledButton(
            footer, t, kind="success", text=label_btn,
            command=self.matiere_suivante, font=("Segoe UI", 11, "bold"),
        ).pack(fill="x", padx=16, pady=12, ipady=8)

    def matiere_suivante(self):
        nom, cle = MATIERES[self.idx]
        questions = SUJETS[cle]
        reps = []
        for i, var in enumerate(self.var_choices):
            if var.get() == -1:
                messagebox.showwarning("Incomplete", f"Reponds a toutes les questions de {nom}.")
                return
            reps.append(var.get())

        derniere = self.idx >= len(MATIERES) - 1
        msg = (
            f"{nom} sera validee.\n\nTu ne pourras plus revenir en arriere.\n\nTerminer le brevet blanc ?"
            if derniere
            else f"{nom} sera validee.\n\nTu ne pourras plus revenir en arriere.\n\nPasser a la matiere suivante ?"
        )
        if not messagebox.askokcancel("Confirmer", msg):
            return

        self.reponses[cle] = reps
        self.notes_matiere[cle] = note_matiere(reps, questions)
        self.idx += 1

        if self.idx >= len(MATIERES):
            self.termine = True
            self.sauver_historique()
            self.afficher_fin()
        else:
            self.afficher_matiere()

    def sauver_historique(self):
        history = charger_json(HISTORY, [])
        from datetime import datetime
        
        moy_ep = round(sum(self.notes_matiere.values()) / len(self.notes_matiere), 2)
        cc = self.cc_moyenne()
        finale, verdict, mention = calculer_brevet(cc, moy_ep)
        
        entry = {
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "notes_matiere": self.notes_matiere.copy(),
            "moyenne_epreuves": moy_ep,
            "moyenne_cc": cc,
            "moyenne_finale": finale,
            "mention": mention,
            "verdict": verdict,
        }
        history.insert(0, entry)
        if len(history) > 50:
            history = history[:50]
        sauver_json(HISTORY, history)

    def afficher_fin(self):
        self.clear()
        t = self.app.theme
        card = tk.Frame(self, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(
            card, text="🎉 Brevet blanc terminé !", font=("Segoe UI", 22, "bold"),
            bg=t["card"], fg=t["success"],
        ).pack(pady=(40, 12))
        tk.Label(
            card,
            text="Toutes les matières sont terminées.\nTes notes ont été calculées avec succès.",
            bg=t["card"], fg=t["muted"], justify="center", font=("Segoe UI", 11),
        ).pack(pady=8)

        StyledButton(
            card, t, kind="primary", text="📊 VOIR MES RÉSULTATS",
            command=self.afficher_resultats, font=("Segoe UI", 13, "bold"),
        ).pack(fill="x", padx=60, pady=30, ipady=12)

    def cc_moyenne(self):
        if self.app.moyenne_pronote is not None:
            return self.app.moyenne_pronote
        manuelle = lire_note(self.app.settings.get("cc_manuel", ""))
        if manuelle is not None:
            return manuelle
        rep = simpledialog.askstring(
            "Controle continu",
            "Entre ta moyenne de controle continu /20\n(ou lie Pronote dans Accueil) :",
        )
        if rep and lire_note(rep) is not None:
            self.app.settings["cc_manuel"] = rep
            sauver_json(SETTINGS, self.app.settings)
            return lire_note(rep)
        return 10.0

    def afficher_resultats(self):
        t = self.app.theme
        self.clear()

        moy_ep = round(sum(self.notes_matiere.values()) / len(self.notes_matiere), 2)
        cc = self.cc_moyenne()
        finale, verdict, mention = calculer_brevet(cc, moy_ep)

        canvas = tk.Canvas(self, bg=t["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=t["bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(
            inner, text="📊 Résultats du brevet blanc", font=("Segoe UI", 18, "bold"),
            bg=t["bg"], fg=t["text"],
        ).pack(pady=(8, 16))

        # Notes par matiere
        grid = tk.Frame(inner, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        grid.pack(fill="x", padx=8, pady=4)
        
        # Header
        header_row = tk.Frame(grid, bg=t["sidebar"])
        header_row.pack(fill="x")
        tk.Label(header_row, text="Matière", font=("Segoe UI", 10, "bold"), bg=t["sidebar"], fg=t["text"], width=24, anchor="w").pack(side="left", padx=12, pady=8)
        tk.Label(header_row, text="Note /20", font=("Segoe UI", 10, "bold"), bg=t["sidebar"], fg=t["text"], width=12).pack(side="left", pady=8)
        tk.Label(header_row, text="Statut", font=("Segoe UI", 10, "bold"), bg=t["sidebar"], fg=t["text"], width=10).pack(side="left", pady=8)
        
        for r, (nom, cle) in enumerate(MATIERES):
            note = self.notes_matiere.get(cle, 0)
            color = t["success"] if note >= 10 else t["danger"]
            statut = "✓ Réussi" if note >= 10 else "✗ À améliorer"
            row = tk.Frame(grid, bg=t["card"] if r % 2 == 0 else t["bg"])
            row.pack(fill="x")
            tk.Label(row, text=nom, bg=row["bg"], fg=t["text"], anchor="w", font=("Segoe UI", 10)).pack(side="left", padx=12, pady=8, fill="x", expand=True)
            tk.Label(row, text=f"{note}/20", bg=row["bg"], fg=color, font=("Segoe UI", 11, "bold"), width=12).pack(side="left", pady=8)
            tk.Label(row, text=statut, bg=row["bg"], fg=color, font=("Segoe UI", 9, "bold"), width=10).pack(side="left", pady=8)

        # Synthese
        syn = tk.Frame(inner, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        syn.pack(fill="x", padx=8, pady=12)
        lignes = [
            ("Moyenne epreuves (7 matieres)", f"{moy_ep}/20"),
            ("Controle continu Pronote (40%)", f"{cc}/20"),
            ("─" * 28, ""),
            ("MOYENNE FINALE BREVET", f"{finale}/20"),
        ]
        for i, (label, val) in enumerate(lignes):
            fg = t["accent"] if "FINALE" in label else t["text"]
            fw = "bold" if "FINALE" in label else "normal"
            tk.Label(syn, text=label, bg=t["card"], fg=t["muted"] if not val else fg, font=("Segoe UI", 11, fw)).pack(anchor="w", padx=16, pady=2)
            if val:
                tk.Label(syn, text=val, bg=t["card"], fg=fg, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=16, pady=(0, 8))

        res = tk.Frame(inner, bg=t["success"] if finale >= 10 else t["danger"])
        res.pack(fill="x", padx=8, pady=8)
        tk.Label(res, text=verdict.replace("\n", " — "), bg=res["bg"], fg="white", font=("Segoe UI", 12, "bold"), wraplength=640, pady=16).pack()

        btns = tk.Frame(inner, bg=t["bg"])
        btns.pack(fill="x", pady=12)
        StyledButton(btns, t, kind="ghost", text="← Retour accueil", command=lambda: self.app.show_page("home")).pack(side="left", padx=8)
        StyledButton(btns, t, kind="primary", text="📝 Voir les explications", command=self.afficher_explications).pack(side="left", padx=8)
        StyledButton(btns, t, kind="success", text="Recommencer un brevet", command=self.build_start).pack(side="right", padx=8)

    def afficher_explications(self):
        t = self.app.theme
        self.clear()

        canvas = tk.Canvas(self, bg=t["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=t["bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(
            inner, text="📝 Explications détaillées", font=("Segoe UI", 18, "bold"),
            bg=t["bg"], fg=t["text"],
        ).pack(pady=(8, 16))

        for nom, cle in MATIERES:
            questions = SUJETS[cle]
            reponses = self.reponses.get(cle, [])
            
            matiere_frame = tk.Frame(inner, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
            matiere_frame.pack(fill="x", padx=8, pady=8)
            
            tk.Label(
                matiere_frame, text=f"📖 {nom}", font=("Segoe UI", 14, "bold"),
                bg=t["card"], fg=t["accent"],
            ).pack(anchor="w", padx=12, pady=10)
            
            for i, q in enumerate(questions):
                reponse_utilisateur = reponses[i] if i < len(reponses) else -1
                bonne_reponse = q["answer"]
                est_correct = reponse_utilisateur == bonne_reponse
                
                q_frame = tk.Frame(matiere_frame, bg=t["bg"] if i % 2 == 0 else t["card"])
                q_frame.pack(fill="x", padx=8, pady=4)
                
                status = "✓" if est_correct else "✗"
                status_color = t["success"] if est_correct else t["danger"]
                
                tk.Label(
                    q_frame, text=f"Q{i+1} {status}", font=("Segoe UI", 10, "bold"),
                    bg=q_frame["bg"], fg=status_color,
                ).pack(anchor="w", padx=8, pady=(6, 2))
                
                tk.Label(
                    q_frame, text=q["question"], font=("Segoe UI", 10),
                    bg=q_frame["bg"], fg=t["text"], wraplength=600,
                ).pack(anchor="w", padx=8, pady=2)
                
                if not est_correct:
                    tk.Label(
                        q_frame, text=f"Ta réponse : {q['choices'][reponse_utilisateur] if reponse_utilisateur >= 0 else 'Aucune'}",
                        bg=q_frame["bg"], fg=t["danger"], font=("Segoe UI", 9),
                    ).pack(anchor="w", padx=8, pady=2)
                
                tk.Label(
                    q_frame, text=f"Bonne réponse : {q['choices'][bonne_reponse]}",
                    bg=q_frame["bg"], fg=t["success"], font=("Segoe UI", 9, "bold"),
                ).pack(anchor="w", padx=8, pady=2)
                
                explication_text = q.get('explication', "Pas d'explication disponible")
                tk.Label(
                    q_frame, text=f"💡 {explication_text}",
                    bg=q_frame["bg"], fg=t["muted"], font=("Segoe UI", 9), wraplength=600,
                ).pack(anchor="w", padx=8, pady=(2, 6))

        btns = tk.Frame(inner, bg=t["bg"])
        btns.pack(fill="x", pady=12)
        StyledButton(btns, t, kind="ghost", text="← Retour résultats", command=self.afficher_resultats).pack(side="left", padx=8)
        StyledButton(btns, t, kind="success", text="Recommencer un brevet", command=self.build_start).pack(side="right", padx=8)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Brevet Pro")
        self.geometry("760x640")
        self.minsize(720, 580)

        self.settings = charger_json(SETTINGS, {"theme": "dark", "chrono": False, "cc_manuel": ""})
        self.theme = THEMES[self.settings.get("theme", "dark")]
        self.configure(bg=self.theme["bg"])

        self.moyenne_pronote = None
        self.nom_eleve = None
        self.pages = {}
        self.current_page = None

        self.build_layout()
        self.show_page("home")
        self.after(400, self.auto_connecter)

    def apply_theme(self):
        self.theme = THEMES[self.settings.get("theme", "dark")]
        self.configure(bg=self.theme["bg"])
        for w in [self.sidebar, self.header, self.content]:
            w.destroy()
        self.build_layout()
        if self.current_page:
            self.show_page(self.current_page)

    def build_layout(self):
        t = self.theme

        self.header = tk.Frame(self, bg=t["sidebar"], height=52)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        tk.Label(
            self.header, text="🎓  Brevet Pro", font=("Segoe UI", 15, "bold"),
            bg=t["sidebar"], fg=t["text"],
        ).pack(side="left", padx=16, pady=10)
        self.header_status = tk.Label(self.header, text="Non connecte", bg=t["sidebar"], fg=t["muted"])
        self.header_status.pack(side="right", padx=16)

        body = tk.Frame(self, bg=t["bg"])
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(body, bg=t["sidebar"], width=180)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        nav = [
            ("home", "Accueil"),
            ("exam", "Brevet blanc"),
            ("calc", "Calcul rapide"),
            ("history", "Historique"),
            ("settings", "Parametres"),
        ]
        for key, label in nav:
            btn = tk.Button(
                self.sidebar, text=label, anchor="w", padx=16,
                bg=t["sidebar"], fg=t["text"], activebackground=t["accent"],
                activeforeground="white", relief="flat", cursor="hand2",
                font=("Segoe UI", 10),
                command=lambda k=key: self.show_page(k),
            )
            btn.pack(fill="x", pady=2, padx=8, ipady=8)

        self.content = tk.Frame(body, bg=t["bg"])
        self.content.pack(side="left", fill="both", expand=True)

        self.pages["exam"] = ExamSimulator(self.content, self)

    def clear_content(self):
        for w in self.content.winfo_children():
            if w != self.pages.get("exam"):
                w.destroy()

    def show_page(self, name):
        self.current_page = name
        self.clear_content()
        t = self.theme

        if name == "home":
            self.page_home()
        elif name == "exam":
            self.pages["exam"].pack(fill="both", expand=True)
        elif name == "calc":
            self.page_calc()
        elif name == "history":
            self.page_history()
        elif name == "settings":
            self.page_settings()
        else:
            self.pages["exam"].pack_forget()

        if name != "exam":
            self.pages["exam"].pack_forget()

    def page_home(self):
        t = self.theme
        f = tk.Frame(self.content, bg=t["bg"])
        f.pack(fill="both", expand=True, padx=12, pady=12)

        card = tk.Frame(f, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        card.pack(fill="x", pady=8)
        tk.Label(card, text="🔗 Mon compte Pronote", font=("Segoe UI", 14, "bold"), bg=t["card"], fg=t["text"]).pack(anchor="w", padx=16, pady=(16, 8))
        tk.Label(
            card,
            text="Lie ton compte pour récupérer automatiquement ta moyenne de contrôle continu.",
            bg=t["card"], fg=t["muted"], wraplength=520, justify="left", font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16)
        StyledButton(card, t, text="🔐 LIER MON COMPTE PRONOTE", command=self.ouvrir_liaison).pack(fill="x", padx=16, pady=12, ipady=8)

        if self.moyenne_pronote:
            info = tk.Frame(f, bg=t["success"])
            info.pack(fill="x", pady=8)
            tk.Label(
                info,
                text=f"  {self.nom_eleve}  ·  Moyenne CC : {self.moyenne_pronote}/20",
                bg=t["success"], fg="white", font=("Segoe UI", 11, "bold"), pady=10,
            ).pack(anchor="w")

        card2 = tk.Frame(f, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        card2.pack(fill="x", pady=8)
        tk.Label(card2, text="🎓 Brevet blanc complet", font=("Segoe UI", 14, "bold"), bg=t["card"], fg=t["text"]).pack(anchor="w", padx=16, pady=(16, 8))
        tk.Label(card2, text="7 matières · Sujets types · Résultats avec mentions", bg=t["card"], fg=t["muted"], font=("Segoe UI", 10)).pack(anchor="w", padx=16)
        StyledButton(card2, t, kind="success", text="✏️ PASSER MON BREVET BLANC", command=self.start_exam).pack(fill="x", padx=16, pady=12, ipady=8)

        self.result_box = tk.Text(f, height=10, font=("Segoe UI", 10), bg=t["input"], fg=t["text"], relief="flat", padx=12, pady=12, wrap="word")
        self.result_box.pack(fill="both", expand=True, pady=8)
        self.result_box.insert("1.0", "👋 Bienvenue dans Brevet Pro !\n\n📌 Pour commencer :\n• Lie ton compte Pronote pour récupérer ta moyenne automatiquement\n• Passe un brevet blanc pour t'entraîner\n• Utilise le calcul rapide pour estimer ta note")
        self.result_box.config(state="disabled")

    def page_calc(self):
        t = self.theme
        f = tk.Frame(self.content, bg=t["bg"])
        f.pack(fill="both", expand=True, padx=12, pady=12)

        card = tk.Frame(f, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        card.pack(fill="x")
        tk.Label(card, text="⚡ Calcul rapide", font=("Segoe UI", 14, "bold"), bg=t["card"], fg=t["text"]).pack(anchor="w", padx=16, pady=(16, 12))

        row = tk.Frame(card, bg=t["card"])
        row.pack(fill="x", padx=16, pady=8)
        tk.Label(row, text="Note épreuves /20 :", bg=t["card"], fg=t["text"], font=("Segoe UI", 11)).pack(side="left", padx=(0, 12))
        self.note_ep = tk.Entry(row, width=10, font=("Segoe UI", 12, "bold"), bg=t["input"], fg=t["text"], relief="flat", justify="center")
        self.note_ep.insert(0, "0")
        self.note_ep.pack(side="right")

        StyledButton(card, t, kind="success", text="🧮 CALCULER MA NOTE", command=self.on_calculer).pack(fill="x", padx=16, pady=16, ipady=8)

        self.calc_result = tk.Text(f, height=12, font=("Consolas", 11), bg=t["input"], fg=t["text"], relief="flat", padx=10, pady=10)
        self.calc_result.pack(fill="both", expand=True, pady=8)

    def page_history(self):
        t = self.theme
        f = tk.Frame(self.content, bg=t["bg"])
        f.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(f, text="📜 Historique des examens", font=("Segoe UI", 16, "bold"), bg=t["bg"], fg=t["text"]).pack(pady=(8, 12))

        history = charger_json(HISTORY, [])
        
        if not history:
            tk.Label(f, text="Aucun examen passé pour le moment.", bg=t["bg"], fg=t["muted"], font=("Segoe UI", 11)).pack(pady=20)
            return

        canvas = tk.Canvas(f, bg=t["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(f, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=t["bg"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for entry in history:
            card = tk.Frame(inner, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
            card.pack(fill="x", padx=8, pady=6)
            
            color = t["success"] if entry["moyenne_finale"] >= 10 else t["danger"]
            tk.Label(card, text=f"📅 {entry['date']}", bg=t["card"], fg=t["muted"], font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(8, 2))
            tk.Label(card, text=f"Note finale : {entry['moyenne_finale']}/20", bg=t["card"], fg=color, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=2)
            tk.Label(card, text=f"Mention : {entry.get('mention', 'Aucune')}", bg=t["card"], fg=t["text"], font=("Segoe UI", 10)).pack(anchor="w", padx=12, pady=(2, 8))

    def page_settings(self):
        t = self.theme
        f = tk.Frame(self.content, bg=t["bg"])
        f.pack(fill="both", expand=True, padx=12, pady=12)

        card = tk.Frame(f, bg=t["card"], highlightbackground=t["card_border"], highlightthickness=1)
        card.pack(fill="x")

        tk.Label(card, text="Apparence", font=("Segoe UI", 12, "bold"), bg=t["card"], fg=t["text"]).pack(anchor="w", padx=16, pady=(12, 4))
        self.var_theme = tk.StringVar(value=self.settings.get("theme", "dark"))
        for val, lbl in [("dark", "Theme sombre"), ("light", "Theme clair")]:
            tk.Radiobutton(
                card, text=lbl, variable=self.var_theme, value=val,
                bg=t["card"], fg=t["text"], selectcolor=t["input"],
            ).pack(anchor="w", padx=24)

        tk.Label(card, text="Examen", font=("Segoe UI", 12, "bold"), bg=t["card"], fg=t["text"]).pack(anchor="w", padx=16, pady=(16, 4))
        self.var_chrono = tk.BooleanVar(value=self.settings.get("chrono", False))
        tk.Checkbutton(
            card, text="Afficher indicateur chrono (bientot)", variable=self.var_chrono,
            bg=t["card"], fg=t["text"], selectcolor=t["input"],
        ).pack(anchor="w", padx=24)

        tk.Label(card, text="Controle continu manuel (si Pronote non lie)", font=("Segoe UI", 12, "bold"), bg=t["card"], fg=t["text"]).pack(anchor="w", padx=16, pady=(16, 4))
        self.cc_entry = tk.Entry(card, width=10, font=("Segoe UI", 11), bg=t["input"], fg=t["text"], relief="flat")
        self.cc_entry.insert(0, self.settings.get("cc_manuel", ""))
        self.cc_entry.pack(anchor="w", padx=24, pady=4)

        StyledButton(card, t, text="Enregistrer", command=self.save_settings).pack(fill="x", padx=16, pady=16, ipady=6)

        StyledButton(
            f, t, kind="danger", text="Deconnecter Pronote",
            command=self.deconnecter,
        ).pack(fill="x", pady=12, ipady=6)

    def save_settings(self):
        ancien_theme = self.settings.get("theme", "dark")
        self.settings["theme"] = self.var_theme.get()
        self.settings["chrono"] = self.var_chrono.get()
        self.settings["cc_manuel"] = self.cc_entry.get().strip()
        sauver_json(SETTINGS, self.settings)
        if self.settings["theme"] != ancien_theme:
            self.apply_theme()
        messagebox.showinfo("OK", "Parametres enregistres.")

    def deconnecter(self):
        if CREDENTIALS.exists():
            CREDENTIALS.unlink()
        self.moyenne_pronote = None
        self.nom_eleve = None
        self.header_status.config(text="Non connecte", fg=self.theme["muted"])
        messagebox.showinfo("OK", "Compte Pronote deconnecte.")

    def on_connecte(self, moyenne, periodes, nom):
        self.moyenne_pronote = moyenne
        self.nom_eleve = nom
        self.header_status.config(text=f"{nom} · CC {moyenne}/20", fg=self.theme["success"])
        if self.current_page == "home" and hasattr(self, "result_box"):
            self.result_box.config(state="normal")
            self.result_box.delete("1.0", "end")
            self.result_box.insert("1.0", f"Connecte : {nom}\nMoyenne CC : {moyenne}/20\n\nPeriodes :\n" + "\n".join(f"  - {p}" for p in periodes))
            self.result_box.config(state="disabled")
        self.show_page("home")

    def auto_connecter(self):
        if not CREDENTIALS.exists():
            return
        self.header_status.config(text="Connexion...", fg=self.theme["accent"])

        def task():
            try:
                client = reconnecter()
                if client:
                    moy, periodes = moyenne_pronote(client)
                    nom = client.info.name if client.info else "Eleve"
                    self.after(0, lambda: self.on_connecte(moy, periodes, nom))
                else:
                    self.after(0, lambda: self.header_status.config(text="Session expiree", fg=self.theme["warning"]))
            except Exception:
                pass

        threading.Thread(target=task, daemon=True).start()

    def start_exam(self):
        self.pages["exam"].build_start()
        self.show_page("exam")

    def ouvrir_liaison(self):
        try:
            import pronotepy  # noqa: F401
            import cv2  # noqa: F401
        except ImportError:
            messagebox.showerror("Manquant", "Lance lancer.bat pour installer les dependances.")
            return
        DialogLiaison(self, self.theme, self.on_connecte)

    def on_calculer(self):
        note = lire_note(self.note_ep.get())
        if note is None:
            messagebox.showwarning("Note", "Entre un nombre entre 0 et 20.")
            return
        cc = self.moyenne_pronote or lire_note(self.settings.get("cc_manuel", ""))
        if cc is None:
            messagebox.showinfo("CC manquant", "Lie Pronote ou entre ta moyenne CC dans Parametres.")
            return
        finale, verdict, _ = calculer_brevet(cc, note)
        self.calc_result.delete("1.0", "end")
        self.calc_result.insert(
            "1.0",
            f"Controle continu : {cc}/20  (40%)\nEpreuves        : {note}/20  (60%)\n{'='*32}\n"
            f"MOYENNE FINALE   : {finale}/20\n{'='*32}\n\n{verdict}",
        )


if __name__ == "__main__":
    App().mainloop()

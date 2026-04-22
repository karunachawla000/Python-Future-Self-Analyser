"""
Future Self Analyzer
A professional career readiness assessment tool.
Requires: customtkinter, matplotlib, numpy
Install: pip install customtkinter matplotlib numpy
"""

import customtkinter as ctk
from tkinter import messagebox
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import sqlite3
import datetime

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Matplotlib dark style
rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#0f3460",
    "axes.labelcolor": "#e0e0e0",
    "xtick.color": "#a0a0b0",
    "ytick.color": "#a0a0b0",
    "text.color": "#e0e0e0",
    "grid.color": "#0f3460",
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "font.family": "DejaVu Sans",
})

# ── Database ────────────────────────────────────────────────────────────────────
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    field TEXT,
    score REAL,
    date TEXT
)
""")
conn.commit()

# ── Data Maps ──────────────────────────────────────────────────────────────────
skills_map = {
    "Data Science":     ["Python", "Statistics", "Machine Learning", "Data Analysis", "Visualization"],
    "Web Development":  ["HTML/CSS", "JavaScript", "React", "Backend", "Database"],
    "AI/ML":            ["Python", "ML Algorithms", "Deep Learning", "Math", "Projects"],
    "Cyber Security":   ["Networking", "Security Basics", "Ethical Hacking", "Linux", "Cryptography"],
    "App Development":  ["Java/Kotlin", "UI Design", "API Handling", "Database", "Debugging"],
    "Cloud Computing":  ["AWS/Azure", "Linux", "Networking", "Docker", "Security"],
    "Game Development": ["Unity/Unreal", "C++/C#", "Game Design", "Physics", "Animation"],
    "UI/UX Design":     ["Figma", "User Research", "Wireframing", "Prototyping", "Creativity"],
}

role_map = {
    "Data Science":     "Data Scientist",
    "Web Development":  "Web Developer",
    "AI/ML":            "ML Engineer",
    "Cyber Security":   "Cyber Security Expert",
    "App Development":  "App Developer",
    "Cloud Computing":  "Cloud Engineer",
    "Game Development": "Game Developer",
    "UI/UX Design":     "UI/UX Designer",
}

weights_map = {
    "Data Science":     [0.30, 0.20, 0.30, 0.10, 0.10],
    "Web Development":  [0.10, 0.30, 0.25, 0.20, 0.15],
    "AI/ML":            [0.25, 0.25, 0.20, 0.15, 0.15],
    "Cyber Security":   [0.25, 0.20, 0.20, 0.20, 0.15],
    "App Development":  [0.30, 0.20, 0.20, 0.15, 0.15],
    "Cloud Computing":  [0.30, 0.20, 0.20, 0.15, 0.15],
    "Game Development": [0.30, 0.25, 0.15, 0.15, 0.15],
    "UI/UX Design":     [0.30, 0.20, 0.20, 0.15, 0.15],
}

ACCENT   = "#4f8ef7"
SUCCESS  = "#2ecc71"
WARNING  = "#f39c12"
DANGER   = "#e74c3c"
BG_DARK  = "#0d1117"
BG_CARD  = "#161b22"
BG_INPUT = "#21262d"
TEXT_PRI = "#e6edf3"
TEXT_SEC = "#8b949e"


# ── Graph ───────────────────────────────────────────────────────────────────────
def show_graph(performance, skills):
    ideal = [8] * 5
    x = np.arange(len(performance))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#161b22")

    bars1 = ax.bar(x - width / 2, performance, width,
                   color=ACCENT, alpha=0.85, label="Your Level",
                   zorder=3, linewidth=0)
    bars2 = ax.bar(x + width / 2, ideal, width,
                   color="#2ecc71", alpha=0.55, label="Target Level",
                   zorder=3, linewidth=0)

    # Value labels on bars
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.15,
                f"{h:.0f}", ha="center", va="bottom",
                fontsize=9, color=TEXT_PRI, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(skills, rotation=20, ha="right", fontsize=10)
    ax.set_ylabel("Skill Level (1–10)", fontsize=11)
    ax.set_ylim(0, 11)
    ax.set_title("Skill Assessment vs Target", fontsize=14,
                 fontweight="bold", color=TEXT_PRI, pad=14)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)

    p1 = mpatches.Patch(color=ACCENT, alpha=0.85, label="Your Level")
    p2 = mpatches.Patch(color="#2ecc71", alpha=0.55, label="Target Level")
    ax.legend(handles=[p1, p2], framealpha=0.2, edgecolor="#30363d",
              labelcolor=TEXT_PRI, fontsize=10)

    for spine in ax.spines.values():
        spine.set_edgecolor("#30363d")

    plt.tight_layout()
    plt.show(block=True)


# ── Main App ────────────────────────────────────────────────────────────────────
class FutureSelfApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Future Self Analyzer")
        self.geometry("720x860")
        self.configure(fg_color=BG_DARK)
        self.resizable(False, False)

        self.skill_entries = []
        self.skill_labels  = []

        self._build_ui()

    # ── UI Builder ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ─────────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⚡  Future Self Analyzer",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=ACCENT,
        ).place(relx=0.5, rely=0.5, anchor="center")

        # ── Scrollable body ────────────────────────────────────────────────────
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG_DARK, corner_radius=0
        )
        self.scroll.pack(fill="both", expand=True, padx=0, pady=0)

        pad = {"padx": 28, "pady": (10, 0)}

        # ── Identity card ──────────────────────────────────────────────────────
        card1 = self._card(self.scroll, "👤  Identity")
        card1.pack(fill="x", **pad)

        self._label(card1, "Full Name")
        self.name_entry = self._entry(card1, "Enter your name")

        self._label(card1, "Career Path")
        self.field_var = ctk.StringVar(value="Data Science")
        self.field_menu = ctk.CTkOptionMenu(
            card1,
            variable=self.field_var,
            values=list(skills_map.keys()),
            command=self._update_fields,
            fg_color=BG_INPUT,
            button_color=ACCENT,
            button_hover_color="#3a7bd5",
            text_color=TEXT_PRI,
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=8,
            width=380,
        )
        self.field_menu.pack(anchor="w", pady=(0, 8))

        # ── Habits card ────────────────────────────────────────────────────────
        card2 = self._card(self.scroll, "📋  Daily Habits")
        card2.pack(fill="x", **pad)

        row = ctk.CTkFrame(card2, fg_color="transparent")
        row.pack(fill="x")

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._label(left, "Study Hours / Day  (1–10)")
        self.study_entry = self._entry(left, "e.g. 4")

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="left", fill="x", expand=True)
        self._label(right, "Consistency Score  (1–10)")
        self.consistency_entry = self._entry(right, "e.g. 7")

        # ── Skills card ────────────────────────────────────────────────────────
        self.skills_card = self._card(self.scroll, "🎯  Skill Ratings  (1–10 each)")
        self.skills_card.pack(fill="x", **pad)
        self._build_skill_rows()

        # ── Buttons ────────────────────────────────────────────────────────────
        btn_row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        btn_row.pack(fill="x", padx=28, pady=(16, 0))

        ctk.CTkButton(
            btn_row,
            text="  Analyze  →",
            command=self._analyze,
            fg_color=ACCENT,
            hover_color="#3a7bd5",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=46,
            corner_radius=10,
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            btn_row,
            text="  View Records",
            command=self._view_records,
            fg_color=BG_CARD,
            hover_color="#21262d",
            border_color="#30363d",
            border_width=1,
            font=ctk.CTkFont(size=14),
            height=46,
            corner_radius=10,
            text_color=TEXT_SEC,
        ).pack(side="left", fill="x", expand=True)

        # ── Result card ────────────────────────────────────────────────────────
        self.result_card = self._card(self.scroll, "📊  Result")
        self.result_card.pack(fill="x", padx=28, pady=(16, 28))

        self.score_label = ctk.CTkLabel(
            self.result_card,
            text="—",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=ACCENT,
        )
        self.score_label.pack(pady=(4, 0))

        self.result_label = ctk.CTkLabel(
            self.result_card,
            text="Run an analysis to see your career readiness score.",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SEC,
            wraplength=600,
        )
        self.result_label.pack(pady=(2, 10))

        self.level_badge = ctk.CTkLabel(
            self.result_card,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=6,
            fg_color="transparent",
            text_color=TEXT_PRI,
            padx=14, pady=4,
        )
        self.level_badge.pack(pady=(0, 8))

    # ── Helpers ─────────────────────────────────────────────────────────────────
    def _card(self, parent, title):
        outer = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        ctk.CTkLabel(
            outer,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SEC,
        ).pack(anchor="w", padx=18, pady=(12, 4))
        ctk.CTkFrame(outer, height=1, fg_color="#30363d").pack(
            fill="x", padx=18, pady=(0, 10)
        )
        return outer

    def _label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SEC,
        ).pack(anchor="w", padx=18, pady=(4, 2))

    def _entry(self, parent, placeholder):
        e = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            fg_color=BG_INPUT,
            border_color="#30363d",
            text_color=TEXT_PRI,
            placeholder_text_color="#484f58",
            font=ctk.CTkFont(size=13),
            height=40,
            corner_radius=8,
            width=380,
        )
        e.pack(anchor="w", padx=18, pady=(0, 8))
        return e

    def _build_skill_rows(self):
        for w in self.skills_card.winfo_children()[2:]:
            w.destroy()
        self.skill_entries.clear()
        self.skill_labels.clear()

        field = self.field_var.get()
        skills = skills_map[field]
        weights = weights_map[field]

        for i in range(0, 5, 2):
            row = ctk.CTkFrame(self.skills_card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=2)
            for j in range(2):
                idx = i + j
                if idx >= 5:
                    break
                col = ctk.CTkFrame(row, fg_color="transparent")
                col.pack(side="left", fill="x", expand=True, padx=4)

                lbl_text = f"{skills[idx]}  ×{weights[idx]:.0%}"
                lbl = ctk.CTkLabel(
                    col,
                    text=lbl_text,
                    font=ctk.CTkFont(size=12),
                    text_color=TEXT_SEC,
                )
                lbl.pack(anchor="w", pady=(2, 1))
                self.skill_labels.append(lbl)

                ent = ctk.CTkEntry(
                    col,
                    placeholder_text="1–10",
                    fg_color=BG_INPUT,
                    border_color="#30363d",
                    text_color=TEXT_PRI,
                    placeholder_text_color="#484f58",
                    font=ctk.CTkFont(size=13),
                    height=38,
                    corner_radius=8,
                )
                ent.pack(fill="x", pady=(0, 6))
                self.skill_entries.append(ent)

    def _update_fields(self, _=None):
        self._build_skill_rows()

    # ── Analysis Logic ──────────────────────────────────────────────────────────
    def _analyze(self):
        name  = self.name_entry.get().strip()
        field = self.field_var.get()
        role  = role_map[field]

        if not name:
            messagebox.showerror("Missing Name", "Please enter the student name.")
            return

        try:
            study       = float(self.study_entry.get())
            consistency = float(self.consistency_entry.get())
            skills      = [float(e.get()) for e in self.skill_entries]
        except ValueError:
            messagebox.showerror("Invalid Input", "All fields must be numbers between 1 and 10.")
            return

        for val in [study, consistency] + skills:
            if not (1 <= val <= 10):
                messagebox.showerror("Out of Range", "All values must be between 1 and 10.")
                return

        weights = weights_map[field]
        current_skills = skills_map[field]

        weighted_skill_score = sum(skills[i] * weights[i] for i in range(5))
        bonus  = (study * 0.1) + (consistency * 0.1)
        score  = (weighted_skill_score * 8) + (bonus * 10)
        score  = min(score, 100)

        if score > 75:
            result_text  = f"Strong profile for {role}"
            level        = "ADVANCED"
            badge_color  = SUCCESS
        elif score > 50:
            result_text  = f"You are on track to becoming a {role}"
            level        = "GROWING"
            badge_color  = WARNING
        else:
            result_text  = f"Keep building to become a {role}"
            level        = "BEGINNER"
            badge_color  = DANGER

        # DB
        date = str(datetime.datetime.now())
        cursor.execute("SELECT id FROM records WHERE name=?", (name,))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE records SET field=?, score=?, date=? WHERE name=?",
                (field, score, date, name),
            )
        else:
            cursor.execute(
                "INSERT INTO records(name, field, score, date) VALUES(?,?,?,?)",
                (name, field, score, date),
            )
        conn.commit()

        # Suggestions
        suggestions = []
        if study < 6:
            suggestions.append(f"📚  Increase study by {6-study:.1f} hrs/day")
        else:
            suggestions.append("📚  Study routine is solid")

        if consistency < 6:
            suggestions.append(f"⏱   Improve consistency by {6-consistency:.1f} pts")
        else:
            suggestions.append("⏱   Consistency looks strong")

        weak = [current_skills[i] for i, v in enumerate(skills) if v < 7]
        if weak:
            suggestions.append(f"🔧  Work on: {', '.join(weak)}")
        else:
            suggestions.append("✅  Core skills are solid — ship real projects")

        top_skills = sorted(
            zip(current_skills, weights), key=lambda x: x[1], reverse=True
        )[:2]
        priority = ", ".join(s for s, _ in top_skills)
        suggestions.append(f"🎯  Prioritize: {priority}")
        suggestions.append("🚀  30–45 days of focused practice = career-ready")

        gap = max(0, 80 - score)
        power_msg = (
            f"\n⚡  POWER BOOST\n\n"
            f"Level: {level}  |  Gap to goal: {gap:.1f} pts\n"
            f"Stay consistent and you can become a {role}.\n"
            f"High-weight skills give the fastest score boost."
        )

        messagebox.showinfo("Analysis Complete", "\n".join(suggestions) + power_msg)

        # Update result card
        self.score_label.configure(text=f"{score:.1f} / 100")
        self.result_label.configure(text=result_text, text_color=TEXT_PRI)
        self.level_badge.configure(
            text=f"  {level}  ",
            fg_color=badge_color,
            text_color="#ffffff",
        )

        show_graph(skills, current_skills)

    # ── View Records ────────────────────────────────────────────────────────────
    def _view_records(self):
        win = ctk.CTkToplevel(self)
        win.title("Student Records")
        win.geometry("680x420")
        win.configure(fg_color=BG_DARK)
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="📁  Student Records",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=ACCENT,
        ).pack(pady=(18, 6))

        frame = ctk.CTkScrollableFrame(win, fg_color=BG_CARD, corner_radius=12)
        frame.frame_scrollbar_fg_color = BG_CARD
        frame.pack(fill="both", expand=True, padx=20, pady=(4, 20))

        headers = ["ID", "Name", "Career Path", "Score", "Date"]
        col_widths = [40, 140, 160, 80, 220]

        # Header row
        hrow = ctk.CTkFrame(frame, fg_color="#21262d", corner_radius=6)
        hrow.pack(fill="x", padx=8, pady=(8, 4))
        for h, w in zip(headers, col_widths):
            ctk.CTkLabel(
                hrow, text=h, width=w,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TEXT_SEC,
            ).pack(side="left", padx=6, pady=6)

        cursor.execute("SELECT * FROM records ORDER BY id DESC")
        rows = cursor.fetchall()

        if not rows:
            ctk.CTkLabel(
                frame,
                text="No records yet.",
                text_color=TEXT_SEC,
                font=ctk.CTkFont(size=13),
            ).pack(pady=30)
        else:
            for row in rows:
                drow = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0)
                drow.pack(fill="x", padx=8, pady=1)
                formatted = [
                    str(row[0]),
                    row[1],
                    row[2],
                    f"{row[3]:.1f}",
                    row[4][:19],
                ]
                for val, w in zip(formatted, col_widths):
                    ctk.CTkLabel(
                        drow, text=val, width=w,
                        font=ctk.CTkFont(size=12),
                        text_color=TEXT_PRI,
                        anchor="w",
                    ).pack(side="left", padx=6, pady=5)
                ctk.CTkFrame(frame, height=1, fg_color="#21262d").pack(
                    fill="x", padx=8
                )


# ── Run ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FutureSelfApp()
    app.mainloop()

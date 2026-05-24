# ============================================================
#  AURA DRIVE — dashboard/analytics.py
#  6-chart session analytics dashboard (dark-themed matplotlib)
# ============================================================

import matplotlib
matplotlib.use("Agg")          # non-interactive backend (safe for Colab)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# ── Color palette ────────────────────────────────────────────
BG      = "#0d0d0d"
PANEL   = "#1a1a1a"
GREEN   = "#00dc50"
YELLOW  = "#ffc800"
RED     = "#dd2828"
ORANGE  = "#c88200"
CYAN    = "#00dcff"
WHITE   = "#ffffff"
GRAY    = "#888888"


def generate_dashboard(tracker, save_path="aura_drive_dashboard.png"):
    """
    Generate a 6-chart analytics dashboard from a completed AuraTracker session.
    Saves the PNG to `save_path` and returns the figure.
    """
    df = tracker.to_dataframe()
    if df.empty:
        print("No session data to plot.")
        return

    frames = df["frame"].tolist()

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.patch.set_facecolor(BG)
    fig.suptitle("🚗  AURA DRIVE — Session Analytics Dashboard",
                 color=WHITE, fontsize=16, fontweight="bold", y=0.98)

    def _style(ax, title, xlabel="Frame", ylabel=""):
        ax.set_facecolor(PANEL)
        ax.set_title(title, color=WHITE, fontsize=11, pad=8)
        ax.set_xlabel(xlabel, color=GRAY, fontsize=9)
        ax.set_ylabel(ylabel, color=GRAY, fontsize=9)
        ax.tick_params(colors=GRAY)
        for spine in ax.spines.values():
            spine.set_edgecolor("#333333")
        ax.grid(color="#2a2a2a", linestyle="--", linewidth=0.6)

    # ── 1. EAR over time ────────────────────────────────────
    ax = axes[0, 0]
    ax.plot(frames, df["ear"], color=CYAN, linewidth=1.5, label="EAR")
    ax.axhline(0.22, color=RED, linestyle="--", linewidth=1, label="Threshold 0.22")
    ax.fill_between(frames, df["ear"], 0.22,
                    where=[v < 0.22 for v in df["ear"]],
                    alpha=0.25, color=RED)
    ax.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=8)
    _style(ax, "👁  Eye Aspect Ratio (EAR)", ylabel="EAR")

    # ── 2. MAR over time ────────────────────────────────────
    ax = axes[0, 1]
    ax.plot(frames, df["mar"], color=YELLOW, linewidth=1.5, label="MAR")
    ax.axhline(0.55, color=ORANGE, linestyle="--", linewidth=1, label="Yawn Threshold 0.55")
    ax.fill_between(frames, df["mar"], 0.55,
                    where=[v > 0.55 for v in df["mar"]],
                    alpha=0.25, color=ORANGE)
    ax.legend(facecolor=PANEL, labelcolor=WHITE, fontsize=8)
    _style(ax, "👄  Mouth Aspect Ratio (MAR)", ylabel="MAR")

    # ── 3. Attention score ──────────────────────────────────
    ax = axes[0, 2]
    ax.plot(frames, df["attention"], color=GREEN, linewidth=2)
    ax.fill_between(frames, df["attention"], alpha=0.15, color=GREEN)
    ax.set_ylim(0, 105)
    _style(ax, "🎯  Attention Score", ylabel="Score (0–100)")

    # ── 4. Fatigue level ────────────────────────────────────
    ax = axes[1, 0]
    ax.plot(frames, df["fatigue"], color=ORANGE, linewidth=2)
    ax.fill_between(frames, df["fatigue"], alpha=0.15, color=ORANGE)
    ax.set_ylim(0, 105)
    _style(ax, "😴  Fatigue Level", ylabel="Level (0–100)")

    # ── 5. Risk score (colour-coded bars) ───────────────────
    ax = axes[1, 1]
    bar_colors = []
    for r in df["risk"]:
        if r < 25:    bar_colors.append(GREEN)
        elif r < 50:  bar_colors.append(YELLOW)
        elif r < 75:  bar_colors.append(ORANGE)
        else:         bar_colors.append(RED)
    ax.bar(frames, df["risk"], color=bar_colors, width=0.8)
    ax.set_ylim(0, 105)
    patches = [
        mpatches.Patch(color=GREEN,  label="Safe (<25)"),
        mpatches.Patch(color=YELLOW, label="Caution (25–50)"),
        mpatches.Patch(color=ORANGE, label="Warning (50–75)"),
        mpatches.Patch(color=RED,    label="Emergency (≥75)"),
    ]
    ax.legend(handles=patches, facecolor=PANEL, labelcolor=WHITE, fontsize=7)
    _style(ax, "🚨  Risk Score per Frame", ylabel="Risk (0–100)")

    # ── 6. Emotion distribution (pie) ───────────────────────
    ax = axes[1, 2]
    emotion_counts = df["emotion"].value_counts()
    emotion_colors = {
        "CALM":    GREEN,
        "FOCUSED": CYAN,
        "STRESSED":ORANGE,
        "TIRED":   YELLOW,
        "YAWNING": RED,
    }
    colors = [emotion_colors.get(e, GRAY) for e in emotion_counts.index]
    wedges, texts, autotexts = ax.pie(
        emotion_counts.values,
        labels=emotion_counts.index,
        colors=colors,
        autopct="%1.0f%%",
        startangle=140,
        textprops={"color": WHITE, "fontsize": 9},
    )
    for at in autotexts:
        at.set_color(BG)
        at.set_fontweight("bold")
    ax.set_facecolor(PANEL)
    ax.set_title("😌  Emotion Distribution", color=WHITE, fontsize=11, pad=8)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=BG)
    print(f"Dashboard saved → {save_path}")
    return fig

"""Build the Module 3 graphs from the CSV exports in results/.

Usage: python make_charts.py   (writes PNGs to graphs/)
"""
import csv
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
GRAPHS = ROOT / "graphs"
RELEASE = date(2018, 6, 2)
BEFORE_COLOR = "#4C72B0"
AFTER_COLOR = "#DD8452"


def read_csv(name):
    with open(RESULTS / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mark_release(ax):
    ax.axvline(RELEASE, color="black", linestyle="--", linewidth=1)
    ax.annotate("Kanban Board released\n2018-06-02", xy=(RELEASE, 1), xycoords=("data", "axes fraction"),
                xytext=(6, -6), textcoords="offset points", va="top", fontsize=9)


def format_date_axis(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.tick_params(axis="x", rotation=45)


def dau_chart():
    rows = read_csv("dau_by_day.csv")
    averages = read_csv("avg_dau_before_after.csv")

    fig, (ax, ax_avg) = plt.subplots(1, 2, figsize=(15, 5.5), gridspec_kw={"width_ratios": [3, 1]})

    for label, color in (("Before", BEFORE_COLOR), ("After", AFTER_COLOR)):
        part = [r for r in rows if r["period"].startswith(label)]
        days = [date.fromisoformat(r["day"]) for r in part]
        users = [int(r["daily_active_users"]) for r in part]
        avg = next(float(a["avg_daily_active_users"]) for a in averages if a["period"].startswith(label))
        ax.plot(days, users, marker=".", linewidth=1, color=color, label=f"{label} feature change")
        ax.hlines(avg, days[0], days[-1], colors=color, linestyles=":", linewidth=2,
                  label=f"{label} average ({avg:.2f})")

    mark_release(ax)
    format_date_axis(ax)
    ax.set_title("Daily active users")
    ax.set_xlabel("Day")
    ax.set_ylabel("Distinct users who logged in")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", bbox_to_anchor=(0, 0.88))

    labels = [a["period"].replace(" Feature Change", "") for a in averages]
    values = [float(a["avg_daily_active_users"]) for a in averages]
    bars = ax_avg.bar(labels, values, color=[BEFORE_COLOR, AFTER_COLOR])
    ax_avg.bar_label(bars, fmt="%.2f")
    ax_avg.set_title("Average daily active users")
    ax_avg.set_ylabel("Users per day")
    ax_avg.set_xlabel("Feature change")
    ax_avg.set_ylim(0, max(values) * 1.2)

    fig.suptitle("Daily active users before and after the Kanban Board release", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAPHS / "dau_before_after.png", dpi=150)
    plt.close(fig)


def status_chart(top_n=15):
    by_day = read_csv("status_changes_by_day.csv")
    by_card = read_csv("status_changes_by_card.csv")[:top_n]

    fig, (ax, ax_card) = plt.subplots(2, 1, figsize=(13, 11))

    days = [date.fromisoformat(r["day"]) for r in by_day]
    counts = [int(r["status_changes"]) for r in by_day]
    colors = [BEFORE_COLOR if d < RELEASE else AFTER_COLOR for d in days]
    ax.bar(days, counts, color=colors, width=1.0)
    if days[0] < RELEASE < days[-1]:
        mark_release(ax)
    format_date_axis(ax)
    ax.set_title(f"Card status changes per day (total: {sum(counts)})")
    ax.set_xlabel("Day")
    ax.set_ylabel("Status changes")
    ax.grid(axis="y", alpha=0.3)

    names = [r["card_name"] for r in by_card][::-1]
    values = [int(r["status_changes"]) for r in by_card][::-1]
    bars = ax_card.barh(names, values, color=AFTER_COLOR)
    ax_card.bar_label(bars, padding=3)
    ax_card.set_title(f"Top {top_n} cards by number of status changes")
    ax_card.set_xlabel("Status changes")
    ax_card.xaxis.get_major_locator().set_params(integer=True)

    fig.suptitle("Number of status changes by card", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(GRAPHS / "status_changes.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    GRAPHS.mkdir(exist_ok=True)
    dau_chart()
    status_chart()
    print("Saved graphs/dau_before_after.png and graphs/status_changes.png")

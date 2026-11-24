"""
Visualization module (Member B)
讀取 expenses.csv，依類別加總金額並畫出圓餅圖。
"""
import argparse
import csv
import os
import sys
from collections import defaultdict

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

DEFAULT_FILE = "expenses.csv"


def setup_chinese_font():
    """讓圖表能顯示中文類別名稱（依作業系統挑可用字型）。"""
    candidates = ["Microsoft JhengHei", "PingFang TC", "Heiti TC",
                  "Noto Sans CJK TC", "Noto Sans TC", "SimHei"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def load_expenses(path, month=None):
    """讀取 CSV，回傳 {類別: 總金額}。month 格式 YYYY-MM，可只統計某個月。"""
    if not os.path.exists(path):
        sys.exit(f"找不到資料檔：{path}，請先用輸入模組新增支出。")

    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            try:
                if month and not row["date"].startswith(month):
                    continue
                amount = float(row["amount"])
                category = row["category"].strip() or "未分類"
            except (KeyError, ValueError):
                print(f"略過第 {line_no} 行（格式錯誤）：{row}")
                continue
            if amount > 0:
                totals[category] += amount
    return dict(totals)


def draw_pie(totals, output, title, show=True):
    """畫圓餅圖並存成圖片。"""
    if not totals:
        sys.exit("沒有可以畫的資料。")

    items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    labels = [k for k, _ in items]
    values = [v for _, v in items]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, _, autotexts = ax.pie(
        values,
        autopct=lambda p: f"{p:.1f}%\n(${p * total / 100:,.0f})",
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        pctdistance=0.75,
    )
    for t in autotexts:
        t.set_fontsize(9)

    ax.legend(wedges, [f"{l}：${v:,.0f}" for l, v in items],
              title="類別", loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title(f"{title}（總計 ${total:,.0f}）")
    ax.axis("equal")
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    print(f"圓餅圖已存到 {output}")
    if show:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="依類別產生支出圓餅圖")
    parser.add_argument("-f", "--file", default=DEFAULT_FILE, help="資料檔路徑（預設 expenses.csv）")
    parser.add_argument("-o", "--output", default="pie_chart.png", help="輸出圖片檔名")
    parser.add_argument("-m", "--month", help="只統計某個月，例如 2026-11")
    parser.add_argument("--no-show", action="store_true", help="只存檔不開視窗")
    args = parser.parse_args()

    setup_chinese_font()
    totals = load_expenses(args.file, args.month)

    print("各類別支出：")
    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {amt:,.0f}")

    title = f"{args.month} 支出分布" if args.month else "支出類別分布"
    draw_pie(totals, args.output, title, show=not args.no_show)


if __name__ == "__main__":
    main()
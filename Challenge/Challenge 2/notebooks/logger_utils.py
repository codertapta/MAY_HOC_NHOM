"""
Ghi nhật ký thí nghiệm (experiment log) cho Challenge 2.

Mỗi lần chạy một notebook, gọi:

    log = ExperimentLogger(runner="Nguyen Van A", stage="02_EDA", notebook="02_EDA.ipynb",
                           log_dir="<...>/Challenge 2/logs", goal="Mục tiêu của lần chạy")
    log.step("Tên bước", key1=value1, key2=value2)     # ghi lại từng bước / kết quả
    log.save(notes="Nhận xét của bạn")                 # ghi ra file

Kết quả:
    logs/experiment_log.csv                          -> mỗi lần chạy = 1 dòng (mở bằng Excel được)
    logs/<stage>_<ngày>_<giờ>_<người chạy>.md        -> báo cáo chi tiết của lần chạy đó
"""
from __future__ import annotations

import csv
import json
import platform
import re
import sys
import time
from datetime import datetime
from pathlib import Path

PLACEHOLDER_RUNNERS = {"", "TEN_CUA_BAN"}

CSV_COLUMNS = [
    "run_id", "date", "time", "runner", "stage", "notebook", "goal",
    "steps", "duration_sec", "python", "platform", "notes",
]


def _slug(text: str) -> str:
    return re.sub(r"[^\w]+", "-", text.strip(), flags=re.UNICODE).strip("-") or "unknown"


def _fmt(v):
    """Chuyển giá trị bất kỳ (tuple, numpy, list...) thành chuỗi dễ đọc."""
    if isinstance(v, float):
        return f"{v:.4g}"
    if hasattr(v, "item") and callable(v.item):          # numpy scalar
        try:
            return _fmt(v.item())
        except Exception:
            pass
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    return str(v)


class ExperimentLogger:
    def __init__(self, runner: str, stage: str, notebook: str, log_dir, goal: str = ""):
        if runner.strip() in PLACEHOLDER_RUNNERS:
            print("⚠️  Bạn chưa điền tên người chạy (biến RUNNER). "
                  "Hãy sửa RUNNER rồi chạy lại để nhật ký có tên bạn.")
        self.runner = runner.strip() or "UNKNOWN"
        self.stage = stage
        self.notebook = notebook
        self.goal = goal
        self.log_dir = Path(log_dir)
        self.start = datetime.now()
        self._t0 = time.perf_counter()
        self.steps: list[tuple[str, dict]] = []

    # ------------------------------------------------------------------ ghi từng bước
    def step(self, name: str, **info):
        self.steps.append((name, {k: _fmt(v) for k, v in info.items()}))

    # ------------------------------------------------------------------ lưu ra file
    def save(self, notes: str = ""):
        self.log_dir.mkdir(parents=True, exist_ok=True)
        end = datetime.now()
        duration = round(time.perf_counter() - self._t0, 1)
        run_id = f"{self.stage}_{self.start:%Y%m%d_%H%M%S}"

        # 1) báo cáo chi tiết .md
        md_path = self.log_dir / f"{run_id}_{_slug(self.runner)}.md"
        lines = [
            f"# Nhật ký thí nghiệm – {self.stage}",
            "",
            "| Mục | Giá trị |",
            "|---|---|",
            f"| Người chạy | {self.runner} |",
            f"| Ngày chạy | {self.start:%d/%m/%Y} |",
            f"| Giờ bắt đầu – kết thúc | {self.start:%H:%M:%S} – {end:%H:%M:%S} ({duration} giây) |",
            f"| Notebook | `{self.notebook}` |",
            f"| Mục tiêu | {self.goal or '-'} |",
            f"| Môi trường | Python {platform.python_version()} · {platform.system()} {platform.release()} |",
            "",
            "## Các bước & kết quả",
            "",
        ]
        for i, (name, info) in enumerate(self.steps, 1):
            lines.append(f"{i}. **{name}**")
            for k, v in info.items():
                lines.append(f"   - {k}: {v}")
        lines += ["", "## Nhận xét", "", notes or "(chưa có)", ""]
        md_path.write_text("\n".join(lines), encoding="utf-8")

        # 2) thêm 1 dòng vào experiment_log.csv
        csv_path = self.log_dir / "experiment_log.csv"
        new_file = not csv_path.exists()
        steps_text = " | ".join(
            f"{n}: " + ", ".join(f"{k}={v}" for k, v in info.items()) for n, info in self.steps
        )
        row = {
            "run_id": run_id,
            "date": f"{self.start:%Y-%m-%d}",
            "time": f"{self.start:%H:%M:%S}",
            "runner": self.runner,
            "stage": self.stage,
            "notebook": self.notebook,
            "goal": self.goal,
            "steps": steps_text,
            "duration_sec": duration,
            "python": platform.python_version(),
            "platform": f"{platform.system()} {platform.release()}",
            "notes": notes,
        }
        with open(csv_path, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            if new_file:
                w.writeheader()
            w.writerow(row)

        print(f"✅ Đã ghi nhật ký: {csv_path.name} (thêm 1 dòng) và {md_path.name}")
        return md_path

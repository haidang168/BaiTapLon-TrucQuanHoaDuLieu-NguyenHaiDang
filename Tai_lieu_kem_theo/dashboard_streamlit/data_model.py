"""Read and aggregate the supplied customer dataset without changing it."""
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pandas as pd

PRODUCTS = {
    "MntWines": "Rượu vang",
    "MntMeatProducts": "Thịt",
    "MntGoldProds": "Gold (nhãn nguồn)",
    "MntFishProducts": "Cá",
    "MntSweetProducts": "Đồ ngọt",
    "MntFruits": "Trái cây",
}
GROUPS = ["Chi tiêu thấp", "Chi tiêu trung bình", "Chi tiêu cao"]
NUMERIC = ["ID", "Age", "Income", "Is_Parent", "Spent", "Response", *PRODUCTS]
REQUIRED = [*NUMERIC, "Spending_Group"]


@dataclass
class Snapshot:
    frame: pd.DataFrame
    digest: str
    read_at: datetime
    modified_at: datetime


def read_snapshot(path: Path) -> Snapshot:
    try:
        before = path.stat()
        contents = path.read_bytes()
        after = path.stat()
    except OSError as exc:
        raise ValueError("Chưa đọc được CSV nguồn. Kiểm tra file rồi chờ lần cập nhật tiếp theo.") from exc
    if (before.st_mtime_ns, before.st_size) != (after.st_mtime_ns, after.st_size):
        raise ValueError("CSV đang được ghi lại. Dashboard sẽ thử đọc ở lần cập nhật tiếp theo.")
    try:
        frame = pd.read_csv(BytesIO(contents), encoding="utf-8-sig")
    except (ValueError, UnicodeError, pd.errors.ParserError) as exc:
        raise ValueError("CSV chưa đọc được đúng định dạng. Dùng bản CSV sạch UTF-8.") from exc
    missing = sorted(set(REQUIRED) - set(frame.columns))
    if missing:
        raise ValueError("CSV thiếu cột: " + ", ".join(missing))
    if frame.empty:
        raise ValueError("CSV nguồn chưa có hồ sơ khách hàng.")
    for name in NUMERIC:
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
    if frame[REQUIRED].isna().any().any():
        raise ValueError("CSV có ô thiếu hoặc giá trị số không hợp lệ trong các cột cần dùng.")
    if frame["ID"].duplicated().any():
        raise ValueError("CSV có ID trùng. Kiểm tra bản dữ liệu sạch trước khi sử dụng.")
    if not frame["Is_Parent"].isin([0, 1]).all() or not frame["Response"].isin([0, 1]).all():
        raise ValueError("Is_Parent và Response cần có giá trị 0 hoặc 1.")
    if not frame["Spending_Group"].isin(GROUPS).all():
        raise ValueError("Tên nhóm chi tiêu cần là: thấp, trung bình hoặc cao như CSV sạch hiện có.")
    if not frame["Age"].between(18, 89).all():
        raise ValueError("Tuổi nằm ngoài khoảng 18–89 của quy trình làm sạch hiện tại.")
    if (frame[["Income", "Spent", *PRODUCTS]] < 0).any().any():
        raise ValueError("Thu nhập và chi tiêu cần là số không âm.")
    return Snapshot(frame, sha256(contents).hexdigest(), datetime.now().astimezone(),
                    datetime.fromtimestamp(after.st_mtime).astimezone())


def filter_customers(frame, ages, parent):
    selected = frame[frame["Age"].between(*ages)]
    if parent is not None:
        selected = selected[selected["Is_Parent"].eq(parent)]
    return selected


def statistics(frame):
    return {
        "customers": len(frame),
        "spent": float(frame["Spent"].sum()),
        "income": float(frame["Income"].mean()) if len(frame) else None,
        "response": float(frame["Response"].mean() * 100) if len(frame) else None,
    }


def product_totals(frame):
    return pd.DataFrame({"Sản phẩm": list(PRODUCTS.values()),
                         "Chi tiêu": [float(frame[name].sum()) for name in PRODUCTS]})\
        .sort_values("Chi tiêu", ascending=False)


def response_groups(frame):
    groups = frame.groupby("Spending_Group", observed=True)["Response"].agg(["mean", "count"])
    groups = groups.reindex(GROUPS)
    return pd.DataFrame({"Nhóm": GROUPS, "Tỷ lệ": groups["mean"].to_numpy() * 100,
                         "Khách hàng": groups["count"].fillna(0).astype(int).to_numpy()})


def vi_number(value, decimals=0):
    if value is None or pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")

import pandas as pd
import glob
import warnings
warnings.filterwarnings("ignore")

cost_df = pd.read_csv("cost_ym.csv")

total_revenue = 0
total_commission = 0
total_cost = 0
total_orders = 0
monthly = []

# Буст продаж — реальные расходы из ЛК YM (все с твоего счёта, бонусов 0)
BOOST_TOTAL = 20067.66

def find_col(df, *keywords):
    for c in df.columns:
        cs = str(c)
        if all(k in cs for k in keywords):
            return c
    return None

def parse_services(f):
    xls = pd.ExcelFile(f)
    total = 0
    details = {}
    for sheet in xls.sheet_names:
        if "汇总" in sheet or "Сводка" in sheet:
            continue
        try:
            raw = pd.read_excel(f, sheet_name=sheet, header=None)
            hdr = None
            for i in range(min(20, len(raw))):
                vals = [str(v) for v in raw.iloc[i].values if pd.notna(v)]
                if any("SKU" in v for v in vals):
                    hdr = i
                    break
            if hdr is None:
                continue
            df = pd.read_excel(f, sheet_name=sheet, header=hdr)
            cost_col = None
            for c in df.columns:
                if "服务费用" in str(c):
                    cost_col = c
                    break
            if cost_col is None:
                for c in df.columns:
                    if "服务价格" in str(c):
                        cost_col = c
                        break
            if cost_col is None:
                continue
            df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce").fillna(0)
            first_col = df.columns[0]
            df = df[~df[first_col].astype(str).str.contains("总计|Итого", na=False)]
            sheet_total = df[cost_col].sum()
            if sheet_total > 0:
                details[sheet] = sheet_total
                total += sheet_total
        except:
            pass
    return total, details

print("=" * 60)
print("АНАЛИЗ YM (себес: закупка + FF + YCT/Inf)")
print("=" * 60)

# === REALIZATION ===
real_files = sorted(glob.glob("ym_realization_*.xlsx"))
print(f"\nОтчётов о реализации: {len(real_files)}")

for f in real_files:
    month_label = f.replace("ym_realization_", "").replace(".xlsx", "")
    print(f"\n--- {month_label} ---")
    
    try:
        raw = pd.read_excel(f, sheet_name="产品已配送", header=None)
        hdr = None
        for i in range(min(25, len(raw))):
            vals = [str(v) for v in raw.iloc[i].values if pd.notna(v)]
            if any("SKU" in v for v in vals):
                hdr = i
                break
        
        df = pd.read_excel(f, sheet_name="产品已配送", header=hdr)
        sku_col = find_col(df, "SKU")
        qty_col = find_col(df, "已配送")
        revenue_col = find_col(df, "所有交付件", "包括所有折扣") or find_col(df, "Стоимость", "скидок")
        
        df = df[df[sku_col].notna()]
        df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0)
        if qty_col:
            df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)
        
        revenue = df[revenue_col].sum()
        count = int(df[qty_col].sum()) if qty_col else len(df)
        
        merged = pd.merge(df, cost_df, left_on=sku_col, right_on="supplierArticle", how="left")
        merged["cost_cny"] = merged["cost_cny"].fillna(0)
        if qty_col:
            merged["total_cost"] = merged["cost_cny"] * merged[qty_col]
        else:
            merged["total_cost"] = merged["cost_cny"]
        cost = merged["total_cost"].sum()
        
        print(f"  Заказов:                     {len(df)}")
        print(f"  Доставлено, шт.:             {count}")
        print(f"  Выручка:                    {revenue:>10,.2f} ¥")
        print(f"  Себес (закуп+FF+YCT):      -{cost:>10,.2f} ¥")
        
        total_revenue += revenue
        total_cost += cost
        total_orders += len(df)
        
        monthly.append({
            "month": month_label,
            "orders": len(df),
            "revenue": revenue,
            "cost": cost,
            "commission": 0,
        })
    except Exception as e:
        print(f"  Ошибка: {e}")

# === SERVICES (комиссии YM) ===
serv_files = sorted(glob.glob("ym_services_*.xlsx"))
print(f"\n\nОтчётов о стоимости услуг: {len(serv_files)}")

for f in serv_files:
    month_label = f.replace("ym_services_", "").replace(".xlsx", "")
    print(f"\n--- {month_label} ---")
    total, details = parse_services(f)
    for sheet, amount in details.items():
        print(f"  {sheet}: {amount:>10,.2f} ¥")
    print(f"  === Комиссии YM:             {total:>10,.2f} ¥")
    total_commission += total
    for m in monthly:
        if m["month"] == month_label:
            m["commission"] = total
            break

# === ИТОГИ ===
print("\n")
print("=" * 60)
print("ИТОГ (CNY)")
print("=" * 60)
print(f"Заказов:              {total_orders:>10,}")
print(f"Выручка:              {total_revenue:>10,.2f} ¥")
print(f"Себес:               -{total_cost:>10,.2f} ¥")
print(f"Комиссии YM:         -{total_commission:>10,.2f} ¥")
print(f"Буст продаж:         -{BOOST_TOTAL:>10,.2f} ¥")
print("-" * 40)
net_profit = total_revenue - total_cost - total_commission - BOOST_TOTAL
print(f"ЧИСТАЯ ПРИБЫЛЬ:       {net_profit:>10,.2f} ¥")
if monthly:
    print(f"В месяц:              {net_profit/len(monthly):>10,.2f} ¥")
print(f"Маржа:                {net_profit / total_revenue * 100:>10,.2f} %")

print("\n" + "=" * 60)
print("ПО МЕСЯЦАМ (CNY)")
print("=" * 60)
mdf = pd.DataFrame(monthly)
mdf["profit"] = mdf["revenue"] - mdf["cost"] - mdf["commission"]
print(mdf.round(2).to_string(index=False))

print("\n" + "=" * 60)
print("ПО МЕСЯЦАМ (с распределённым бустом)")
print("=" * 60)

mdf = pd.DataFrame(monthly)
mdf["boost"] = (mdf["revenue"] / mdf["revenue"].sum()) * BOOST_TOTAL
mdf["profit_with_boost"] = mdf["revenue"] - mdf["cost"] - mdf["commission"] - mdf["boost"]
mdf["margin_%"] = (mdf["profit_with_boost"] / mdf["revenue"] * 100).round(1)
print(mdf.round(2).to_string(index=False))
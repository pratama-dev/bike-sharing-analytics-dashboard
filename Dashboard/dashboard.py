import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY   = "#2563EB"
SECONDARY = "#10B981"
ACCENT    = "#F59E0B"
DANGER    = "#EF4444"
NEUTRAL   = "#64748B"
MINT      = "#8fd9b6"

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family"       : "DejaVu Sans",
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.titleweight"  : "bold",
    "axes.titlesize"    : 12,
    "axes.labelsize"    : 10,
    "xtick.labelsize"   : 8.5,
    "ytick.labelsize"   : 8.5,
    "figure.facecolor"  : "white",
    "axes.facecolor"    : "white",
})

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #F1F5F9; }
[data-testid="stSidebar"]          { background-color: #1E3A5F; }
[data-testid="stSidebar"] *        { color: #E2E8F0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: #CBD5E1 !important; font-size: 0.83rem; }

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    border-left: 4px solid var(--accent-color, #2563EB);
    margin-bottom: 8px;
}
.metric-label {
    font-size: 0.78rem; color: #64748B; font-weight: 600;
    text-transform: uppercase; letter-spacing: .05em;
}
.metric-value { font-size: 1.9rem; font-weight: 800; color: #1E293B; line-height: 1.2; }
.metric-delta { font-size: 0.78rem; margin-top: 2px; }

.section-title {
    font-size: 1.05rem; font-weight: 700; color: #1E293B;
    border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; margin-bottom: 16px;
}
.question-badge {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
    border: 1px solid #BFDBFE;
}
.chart-card {
    background: white; border-radius: 12px;
    padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); margin-bottom: 16px;
}
.insight-box {
    background: #F0FDF4;
    border-left: 4px solid #10B981;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 8px;
    font-size: 0.83rem;
    color: #1E293B;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    day_df  = pd.read_csv("dashboard/day.csv",  parse_dates=["dteday"])
    hour_df = pd.read_csv("dashboard/hour.csv", parse_dates=["dteday"])

    season_map  = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Cerah/Berawan",
        2: "Kabut/Mendung",
        3: "Hujan/Salju Ringan",
        4: "Cuaca Ekstrem",
    }
    weekday_map = {0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
    month_map   = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


    for df in [day_df, hour_df]:
        df["season_name"]  = df["season"].map(season_map)
        df["weather_name"] = df["weathersit"].map(weather_map)
        df["weekday_name"] = df["weekday"].map(weekday_map)
        df["month_name"]   = df["mnth"].map(month_map)
        df["year_label"]   = df["yr"].map({0: "2011", 1: "2012"})
        df["temp_c"]       = df["temp"] * 41
        df["hum_pct"]      = df["hum"] * 100
        df["wind_kmh"]     = df["windspeed"] * 67


    bins   = [0, 0.3, 0.6, 1]
    labels = ["Cold", "Moderate", "Hot"]
    day_df["temp_category"] = pd.cut(day_df["atemp"], bins=bins, labels=labels)


    return day_df, hour_df


day_df, hour_df = load_data()

with st.sidebar:
    st.markdown("## 🚲 Bike Sharing")
    st.markdown("Capital Bikeshare · Washington D.C.")
    st.divider()

    st.markdown("**Filter Data**")
    selected_years = st.multiselect(
        "Tahun", options=["2011", "2012"], default=["2011", "2012"]
    )
    selected_seasons = st.multiselect(
        "Musim", options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )
    selected_weather = st.multiselect(
        "Kondisi Cuaca",
        options=["Cerah/Berawan", "Kabut/Mendung", "Hujan/Salju Ringan", "Cuaca Ekstrem"],
        default=["Cerah/Berawan", "Kabut/Mendung", "Hujan/Salju Ringan", "Cuaca Ekstrem"],
    )
    st.divider()
    st.caption("Dataset: UCI Bike Sharing Dataset\nPeriode: Jan 2011 – Des 2012")

day_f  = day_df[
    day_df["year_label"].isin(selected_years) &
    day_df["season_name"].isin(selected_seasons) &
    day_df["weather_name"].isin(selected_weather)
].copy()

hour_f = hour_df[
    hour_df["year_label"].isin(selected_years) &
    hour_df["season_name"].isin(selected_seasons) &
    hour_df["weather_name"].isin(selected_weather)
].copy()


def metric_card(label, value, delta=None, color=PRIMARY):
    delta_html = ""
    if delta is not None:
        arrow = "▲" if delta >= 0 else "▼"
        clr   = SECONDARY if delta >= 0 else DANGER
        delta_html = f'<div class="metric-delta" style="color:{clr}">{arrow} {abs(delta):.1f}% vs 2011</div>'
    st.markdown(f"""
    <div class="metric-card" style="--accent-color:{color}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def chart_card(fig):
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)


def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def question_badge(text):
    st.markdown(f'<div class="question-badge">{text}</div>', unsafe_allow_html=True)


def insight_box(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)


st.markdown("""
<div style="background:linear-gradient(135deg,#1E3A5F,#2563EB);
            border-radius:14px;padding:24px 30px;margin-bottom:24px;color:white;">
  <h1 style="margin:0;font-size:1.7rem;font-weight:800;">🚲 Bike Sharing Analytics Dashboard</h1>
  <p style="margin:6px 0 0;opacity:.8;font-size:.9rem;">
    Analisis pola peminjaman sepeda Capital Bikeshare · Washington D.C. · 2011–2012
  </p>
</div>
""", unsafe_allow_html=True)


section("📊 Ringkasan Statistik")
k1, k2, k3, k4 = st.columns(4)

total_rentals  = day_f["cnt"].sum()
avg_daily      = day_f["cnt"].mean()
peak_day       = day_f["cnt"].max()
registered_pct = (day_f["registered"].sum() / day_f["cnt"].sum() * 100
                  if day_f["cnt"].sum() > 0 else 0)

yoy_delta = None
if {"2011", "2012"}.issubset(set(selected_years)):
    t11 = day_df[day_df["year_label"] == "2011"]["cnt"].sum()
    t12 = day_df[day_df["year_label"] == "2012"]["cnt"].sum()
    yoy_delta = (t12 - t11) / t11 * 100 if t11 > 0 else None

with k1:
    metric_card("Total Peminjaman", f"{total_rentals:,.0f}",
                delta=yoy_delta, color=PRIMARY)
with k2:
    metric_card("Rata-rata / Hari", f"{avg_daily:,.0f}", color=SECONDARY)
with k3:
    metric_card("Puncak Harian", f"{peak_day:,}", color=ACCENT)
with k4:
    metric_card("Pengguna Registered", f"{registered_pct:.1f}%", color=NEUTRAL)

st.markdown("<br>", unsafe_allow_html=True)


section("📈 Tren Peminjaman Sepanjang Waktu")
col1, col2 = st.columns([3, 2])

with col1:
    monthly = (
        day_f.groupby(["yr", "mnth"])["cnt"]
        .sum()
        .reset_index()
    )
    month_labels = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                    7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

    fig, ax = plt.subplots(figsize=(7, 3.8))
    colors_yr = {0: PRIMARY, 1: SECONDARY}
    labels_yr = {0: "2011", 1: "2012"}
    for yr_val, grp in monthly.groupby("yr"):
        ax.plot(
            grp["mnth"], grp["cnt"] / 1000,
            marker="o", markersize=5, linewidth=2,
            color=colors_yr.get(yr_val, NEUTRAL),
            label=labels_yr.get(yr_val, str(yr_val))
        )
        ax.fill_between(grp["mnth"], grp["cnt"] / 1000, alpha=0.08,
                        color=colors_yr.get(yr_val, NEUTRAL))

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([month_labels[m] for m in range(1, 13)])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}K"))
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Total Peminjaman Sepeda per Bulan", fontweight="bold")
    ax.legend(title="Tahun", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    chart_card(fig)

with col2:
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    season_data = (
        day_f.groupby("season_name")["cnt"]
        .mean()
        .reindex(season_order)
        .dropna()
    )
    bar_colors = [PRIMARY if val == season_data.max() else MINT
                  for val in season_data.values]

    fig, ax = plt.subplots(figsize=(4.5, 3.8))
    bars = ax.barh(season_data.index, season_data.values,
                   color=bar_colors, height=0.6, edgecolor="white")
    for bar, val in zip(bars, season_data.values):
        ax.text(bar.get_width() + 100,
                bar.get_y() + bar.get_height() / 2,
                f"{val:,.0f}", va="center", fontsize=10,
                fontweight="bold", color="#2c3e50")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_xlabel("Rata-rata Peminjaman per Hari", fontsize=11)
    ax.set_title("Rata-rata Peminjaman per Musim (2011-2012)",
                 fontweight="bold", fontsize=12, pad=16)
    ax.set_xlim(0, season_data.max() * 1.15)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    fig.tight_layout()
    chart_card(fig)

st.markdown("<br>", unsafe_allow_html=True)

question_badge("Pertanyaan Bisnis 1")
st.markdown(
    "**Bagaimana perbedaan tren rata-rata jumlah peminjaman sepeda per jam antara "
    "hari kerja dan hari libur untuk menentukan jam puncak (*rush hour*) "
    "masing-masing tipe hari?**"
)
section("⏱️ Pola Peminjaman per Jam: Hari Kerja vs Akhir Pekan")

col3, col4 = st.columns([3, 2])

with col3:
    hourly = (
        hour_f.groupby(["hr", "workingday"])["cnt"]
        .mean()
        .reset_index()
    )
    wd_colors = {1: PRIMARY, 0: ACCENT}
    wd_labels = {1: "Hari Kerja", 0: "Akhir Pekan / Libur"}

    fig, ax = plt.subplots(figsize=(8, 4))
    for wd, grp in hourly.groupby("workingday"):
        ax.plot(
            grp["hr"], grp["cnt"],
            marker="o", markersize=4, linewidth=2,
            color=wd_colors[wd], label=wd_labels[wd]
        )
        ax.fill_between(grp["hr"], grp["cnt"], alpha=0.07, color=wd_colors[wd])

    ax.set_xticks(range(0, 24))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24)],
                       rotation=45, fontsize=7.5)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Peminjaman")
    ax.set_title("Pola Peminjaman per Jam: Hari Kerja vs Akhir Pekan",
                 fontweight="bold")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    chart_card(fig)

with col4:
    pivot = (
        hour_f.groupby(["weekday", "hr"])["cnt"]
        .mean()
        .unstack(level=0)
    )
    pivot.columns = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    pivot = pivot[["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]]
    pivot.index = [f"{h:02d}:00" for h in pivot.index]

    tick_idx = [i for i, lbl in enumerate(pivot.index) if int(lbl[:2]) % 2 == 0]

    fig, ax = plt.subplots(figsize=(4.5, 4))
    sns.heatmap(
        pivot.T, ax=ax,
        cmap="YlOrRd", annot=False,
        linewidths=0.3, linecolor="#F1F5F9",
        cbar_kws={"label": "Rata-rata Peminjaman", "shrink": 0.7},
        xticklabels=False,
    )
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([pivot.index[i] for i in tick_idx], rotation=45, fontsize=7)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Hari")
    ax.set_title("Heatmap: Jam × Hari", fontweight="bold")
    ax.tick_params(axis="y", labelsize=8.5, rotation=0)
    fig.tight_layout()
    chart_card(fig)

insight_box(
    "Jam puncak hari kerja jatuh pada pukul <b>08:00</b> (berangkat kerja) dan "
    "<b>17:00</b> (pulang kerja), mencerminkan pola <i>commuting</i>. "
    "Sebaliknya, puncak akhir pekan terjadi di tengah hari sekitar pukul <b>13:00</b> "
    "yang mengindikasikan aktivitas rekreasi."
)

st.markdown("<br>", unsafe_allow_html=True)

question_badge("Pertanyaan Bisnis 2")
st.markdown(
    "**Bagaimana perbandingan rata-rata jumlah peminjaman sepeda harian di antara "
    "berbagai kategori kondisi cuaca untuk mengidentifikasi sejauh mana cuaca "
    "memengaruhi minat pengguna layanan?**"
)
section("🌤️ Dampak Kondisi Cuaca terhadap Peminjaman")

col5, col6 = st.columns([3, 2])

with col5:
    weather_order = [
        "Cerah/Berawan", "Kabut/Mendung",
        "Hujan/Salju Ringan", "Cuaca Ekstrem"
    ]
    wth_data = (
        day_f.groupby("weather_name")["cnt"]
        .mean()
        .reindex([w for w in weather_order if w in day_f["weather_name"].unique()])
        .dropna()
    )
    bar_colors_w = ["#1f77b4" if val == wth_data.max() else MINT
                    for val in wth_data.values]

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x=wth_data.index,
        y=wth_data.values,
        palette=bar_colors_w,
        ax=ax,
    )
    ax.set_title("Dampak Kondisi Cuaca terhadap Rata-rata Peminjaman Sepeda",
                 fontsize=14, fontweight="bold", pad=20)
    ax.set_ylabel("Rata-rata Jumlah Peminjaman", fontsize=12)
    ax.set_xlabel("Kondisi Cuaca", fontsize=12)
    for i, val in enumerate(wth_data.values):
        ax.text(i, val + 80, f"{int(val)}", ha="center",
                fontsize=11, fontweight="bold", color="#2c3e50")
    ax.set_ylim(0, wth_data.max() * 1.15)
    sns.despine(ax=ax)
    fig.tight_layout()
    chart_card(fig)

with col6:
    sample = day_f.sample(min(500, len(day_f)), random_state=42)
    fig, ax = plt.subplots(figsize=(4.5, 4))
    sc = ax.scatter(
        sample["temp_c"], sample["cnt"],
        c=sample["hum_pct"], cmap="RdYlBu_r",
        alpha=0.55, s=30, edgecolors="none"
    )
    m, b   = np.polyfit(day_f["temp_c"], day_f["cnt"], 1)
    x_line = np.linspace(day_f["temp_c"].min(), day_f["temp_c"].max(), 100)
    ax.plot(x_line, m * x_line + b, color=PRIMARY,
            linewidth=2, linestyle="--", label=f"Regresi (slope={m:.0f})")
    cbar = fig.colorbar(sc, ax=ax, shrink=0.85)
    cbar.set_label("Kelembaban (%)", fontsize=9)
    ax.set_xlabel("Suhu (°C)")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Hubungan Suhu dan Jumlah Peminjaman\n(warna = kelembaban)",
                 fontweight="bold")
    ax.legend(frameon=False, fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    chart_card(fig)

insight_box(
    "Cuaca <b>Cerah/Berawan</b> secara konsisten mencatat volume peminjaman tertinggi. "
    "Kondisi buruk seperti hujan/salju ringan menurunkan rata-rata peminjaman secara signifikan, "
    "sementara cuaca ekstrem (badai) hampir menghentikan aktivitas penyewaan sepenuhnya."
)

st.markdown("<br>", unsafe_allow_html=True)

question_badge("Pertanyaan Bisnis 3")
st.markdown(
    "**Bagaimana perbedaan rata-rata jumlah peminjaman sepeda pada setiap kelompok "
    "kategori suhu (Cold, Moderate, Hot) di hari kerja, dan kategori mana yang "
    "memberikan kontribusi penyewaan tertinggi?**"
)
section("🌡️ Klaster Suhu: Cold · Moderate · Hot")

col7, col8 = st.columns([3, 2])

with col7:
    temp_cluster = (
        day_f.groupby("temp_category", observed=True)["cnt"]
        .mean()
        .reset_index()
    )
    cat_order = ["Cold", "Moderate", "Hot"]
    temp_cluster["temp_category"] = pd.Categorical(
        temp_cluster["temp_category"], categories=cat_order, ordered=True
    )
    temp_cluster = temp_cluster.sort_values("temp_category")

    bar_colors_t = ["#1f77b4" if val == temp_cluster["cnt"].max() else MINT
                    for val in temp_cluster["cnt"]]

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        data=temp_cluster,
        x="temp_category",
        y="cnt",
        palette=bar_colors_t,
        ax=ax,
        order=cat_order,
    )
    ax.set_title("Rata-rata Peminjaman Berdasarkan Klaster Suhu (Manual Grouping)",
                 fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Kategori Suhu (atemp)", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Peminjaman", fontsize=12)
    for i, val in enumerate(temp_cluster["cnt"]):
        ax.text(i, val + 80, f"{int(val)}", ha="center",
                fontweight="bold", color="#2c3e50", fontsize=11)
    ax.set_ylim(0, temp_cluster["cnt"].max() * 1.15)
    sns.despine(ax=ax)
    fig.tight_layout()
    chart_card(fig)

with col8:
    cat_colors_map = {"Cold": "#60A5FA", "Moderate": "#2563EB", "Hot": "#F59E0B"}
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("**Ringkasan Rata-rata per Klaster Suhu**")

    for _, row in temp_cluster.iterrows():
        cat   = str(row["temp_category"])
        val   = int(row["cnt"])
        clr   = cat_colors_map.get(cat, NEUTRAL)
        pct   = val / temp_cluster["cnt"].max() * 100
        is_max = (val == temp_cluster["cnt"].max())
        badge = " 🏆" if is_max else ""
        st.markdown(f"""
        <div style="margin-bottom:14px;">
            <div style="font-size:.85rem;font-weight:700;color:{clr};
                        margin-bottom:4px;">{cat}{badge}</div>
            <div style="background:#E2E8F0;border-radius:6px;height:10px;
                        overflow:hidden;margin-bottom:3px;">
                <div style="background:{clr};width:{pct:.1f}%;height:100%;
                            border-radius:6px;"></div>
            </div>
            <div style="font-size:.82rem;color:{NEUTRAL};">
                Rata-rata: <b style="color:#1E293B;">{val:,}</b> peminjaman/hari
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

insight_box(
    "Kategori suhu <b>Moderate</b> mencatat rata-rata peminjaman tertinggi karena "
    "memberikan kenyamanan termal optimal bagi pengguna. Suhu <b>Cold</b> menyebabkan "
    "penurunan permintaan paling drastis — jadikan ini prioritas penjadwalan "
    "perawatan armada saat suhu rendah."
)

st.markdown("<br>", unsafe_allow_html=True)


section("🗓️ Peta Panas Lengkap: Jam × Hari dalam Seminggu")

pivot_full = (
    hour_f.groupby(["weekday", "hr"])["cnt"]
    .mean()
    .unstack(level=0)
)
pivot_full.columns = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
pivot_full = pivot_full[["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]]
pivot_full.index = [f"{h:02d}:00" for h in pivot_full.index]

fig, ax = plt.subplots(figsize=(13, 4.5))
sns.heatmap(
    pivot_full.T, ax=ax,
    cmap="YlOrRd", annot=False,
    linewidths=0.3, linecolor="#F1F5F9",
    cbar_kws={"label": "Rata-rata Peminjaman", "shrink": 0.75}
)
ax.set_xlabel("Jam")
ax.set_ylabel("Hari")
ax.set_title("Heatmap Peminjaman: Jam × Hari dalam Seminggu", fontweight="bold")
ax.tick_params(axis="x", labelsize=7.5, rotation=45)
ax.tick_params(axis="y", labelsize=9, rotation=0)
fig.tight_layout()
chart_card(fig)

st.markdown("<br>", unsafe_allow_html=True)
section("👥 Segmentasi Pengguna: Casual vs Registered")

col9, col10 = st.columns(2)

with col9:
    seg = (
        day_f.groupby(["yr", "mnth"])[["casual", "registered"]]
        .sum()
        .reset_index()
        .sort_values(["yr", "mnth"])
    )
    seg["label"] = seg.apply(
        lambda r: f"{'2011' if r['yr']==0 else '2012'}-{r['mnth']:02d}", axis=1
    )
    fig, ax = plt.subplots(figsize=(6, 3.8))
    x = range(len(seg))
    ax.stackplot(x, seg["casual"] / 1000, seg["registered"] / 1000,
                 labels=["Casual", "Registered"],
                 colors=[ACCENT + "CC", PRIMARY + "CC"], alpha=0.9)
    tick_step = max(1, len(seg) // 10)
    ax.set_xticks(range(0, len(seg), tick_step))
    ax.set_xticklabels(
        [seg["label"].iloc[i] for i in range(0, len(seg), tick_step)],
        rotation=30, ha="right", fontsize=7
    )
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}K"))
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Tren Casual vs Registered per Bulan", fontweight="bold")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    chart_card(fig)

with col10:
    corr_cols   = ["temp_c", "hum_pct", "wind_kmh", "casual", "registered", "cnt"]
    col_labels  = ["Suhu", "Kelembaban", "Kec. Angin", "Casual", "Registered", "Total"]
    corr_matrix = day_f[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(6, 3.8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    sns.heatmap(
        corr_matrix, mask=mask, ax=ax,
        annot=True, fmt=".2f", annot_kws={"size": 8},
        cmap="RdYlBu_r", center=0, vmin=-1, vmax=1,
        xticklabels=col_labels, yticklabels=col_labels,
        linewidths=0.5, linecolor="#E2E8F0",
        cbar_kws={"shrink": 0.75}
    )
    ax.set_title("Matriks Korelasi Variabel Utama", fontweight="bold")
    ax.tick_params(axis="x", labelsize=7.5, rotation=15)
    ax.tick_params(axis="y", labelsize=7.5, rotation=0)
    fig.tight_layout()
    chart_card(fig)

st.markdown("<br>", unsafe_allow_html=True)

section("💡 Temuan Utama")

peak_hour_wd = (
    hour_f[hour_f["workingday"] == 1].groupby("hr")["cnt"].mean().idxmax()
    if len(hour_f[hour_f["workingday"] == 1]) > 0 else 17
)
peak_hour_we = (
    hour_f[hour_f["workingday"] == 0].groupby("hr")["cnt"].mean().idxmax()
    if len(hour_f[hour_f["workingday"] == 0]) > 0 else 13
)
best_season   = day_f.groupby("season_name")["cnt"].mean().idxmax() if len(day_f) > 0 else "Fall"
worst_weather = day_f.groupby("weather_name")["cnt"].mean().idxmin() if len(day_f) > 0 else "Cuaca Ekstrem"

ins1, ins2, ins3, ins4 = st.columns(4)
insights = [
    ("🕗 Jam Puncak Hari Kerja",
     f"{peak_hour_wd:02d}:00 – {peak_hour_wd+1:02d}:00",
     "Pola commuting pagi & sore mendominasi permintaan.", SECONDARY),
    ("🎉 Jam Puncak Akhir Pekan",
     f"{peak_hour_we:02d}:00 – {peak_hour_we+1:02d}:00",
     "Peminjaman rekreasi paling tinggi di tengah hari.", ACCENT),
    ("🍂 Musim Terbaik",
     best_season,
     "Musim ini secara konsisten mencatat peminjaman tertinggi.", PRIMARY),
    ("🌧️ Cuaca Paling Sepi",
     worst_weather,
     "Cuaca buruk secara signifikan menurunkan jumlah peminjaman.", DANGER),
]
for col_ins, (title, val, desc, clr) in zip([ins1, ins2, ins3, ins4], insights):
    with col_ins:
        st.markdown(f"""
        <div class="metric-card" style="--accent-color:{clr}">
            <div class="metric-label">{title}</div>
            <div class="metric-value" style="font-size:1.25rem">{val}</div>
            <div class="metric-delta" style="color:{NEUTRAL};margin-top:6px;
                         font-size:.77rem">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

if {"2011", "2012"}.issubset(set(selected_years)):
    t11 = day_df[day_df["year_label"] == "2011"]["cnt"].sum()
    t12 = day_df[day_df["year_label"] == "2012"]["cnt"].sum()
    yoy_pct = (t12 - t11) / t11 * 100 if t11 > 0 else 0
    arrow = "▲" if yoy_pct > 0 else "▼"
    color = SECONDARY if yoy_pct > 0 else DANGER
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:14px 22px;
                box-shadow:0 1px 4px rgba(0,0,0,.08);margin-top:8px;
                border-left:4px solid {color};">
        <span style="font-size:.85rem;font-weight:600;color:{NEUTRAL}">
            📅 PERTUMBUHAN TAHUN KE TAHUN &nbsp;
        </span>
        <span style="font-size:1.15rem;font-weight:800;color:{color}">
            {arrow} {abs(yoy_pct):.1f}% ({int(t11):,} → {int(t12):,} peminjaman)
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Sumber data: UCI Machine Learning Repository – Bike Sharing Dataset (Fanaee-T & Gama, 2013)")
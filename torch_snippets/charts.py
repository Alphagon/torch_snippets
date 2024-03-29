# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/charts.ipynb.

# %% auto 0
__all__ = ["alt", "Chart", "CM", "radar", "confusion_matrix", "spider"]

# %% ../nbs/charts.ipynb 2
import altair as alt
from altair import Chart

alt = alt
Chart = Chart
from .loader import *

# %% ../nbs/charts.ipynb 5
def confusion_matrix(df=None, truth=None, pred=None, mapping=None, save_to=None):
    if df is None:
        df = pd.DataFrame({"truth": truth, "pred": pred})
        truth = "truth"
        pred = "pred"
    DF = df[[truth, pred]]

    try:
        from sklearn.metrics import classification_report

        print(classification_report(DF[truth], DF[pred]))
    except:
        logger.info("Skipping Report")
    df = DF.pivot_table(index=truth, columns=pred, aggfunc=len).reset_index()
    df = df.melt(id_vars=truth, var_name=pred, value_name="value")
    sz = 450 if len(DF[truth].unique()) > 4 else 250

    base = alt.Chart(df, height=sz, width=sz)
    hm = base.mark_rect().encode(
        x=f"{pred}:O",
        y=f"{truth}:O",
        color=alt.Color("value:Q", scale=alt.Scale(scheme="lightorange"), legend=None),
    )

    tx = base.mark_text(baseline="middle").encode(
        x=f"{pred}:O",
        y=f"{truth}:O",
        text="value:Q",
        color=alt.condition(
            alt.datum.value > 0,
            alt.value("black"),
            alt.value("rgba(0, 0, 0, 0)"),  # Transparent color for value 0
        ),
    )

    if save_to is not None:
        assert str(save_to).endswith("html"), "Can only save in html format"
        (hm + tx).save(save_to, format="html")
        Info(f"Saved chart at {save_to}")
    else:
        return hm + tx


CM = confusion_matrix

# %% ../nbs/charts.ipynb 12
def spider(df, *, id_column, title=None, max_values=None, padding=1.25):
    categories = df.dtypes[(df.dtypes == "float") | (df.dtypes == "int")].index.tolist()
    data = df[categories].to_dict(orient="list")
    ids = df[id_column].tolist()
    if max_values is None:
        max_values = {key: padding * max(value) for key, value in data.items()}
    normalized_data = {
        key: np.array(value) / max_values[key] for key, value in data.items()
    }
    num_vars = len(data.keys())
    tiks = list(data.keys())
    tiks += tiks[:1]
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i, model_name in enumerate(ids):
        values = [normalized_data[key][i] for key in data.keys()]
        actual_values = [data[key][i] for key in data.keys()]
        values += values[:1]  # Close the plot for a better look
        ax.plot(angles, values, label=model_name)
        ax.fill(angles, values, alpha=0.15)
        for _x, _y, t in zip(angles, values, actual_values):
            t = f"{t:.2f}" if isinstance(t, float) else str(t)
            ax.text(_x, _y, t, size="xx-small")

    ax.fill(angles, np.ones(num_vars + 1), alpha=0.05)
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(tiks)
    ax.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
    if title is not None:
        plt.suptitle(title)
    plt.show()


radar = spider

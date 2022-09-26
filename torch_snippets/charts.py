# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/charts.ipynb.

# %% auto 0
__all__ = ['alt', 'Chart', 'CM', 'confusion_matrix']

# %% ../nbs/charts.ipynb 2
import altair as alt
from altair import Chart

alt = alt
Chart = Chart
from .loader import *

# %% ../nbs/charts.ipynb 5
def confusion_matrix(df=None, truth=None, pred=None, mapping=None):
    if df is None:
        df = pd.DataFrame({"truth": truth, "pred": pred})
        truth = "truth"
        pred = "pred"
    threshold = len(df)
    if mapping:
        assert isinstance(mapping, dict), "mapping should be a dictionary"
        df[truth] = df[truth].map(lambda x: mapping[x])
        df[pred] = df[pred].map(lambda x: mapping[x])

    sz = 450 if len(df[truth].unique()) > 4 else 250
    base = (
        Chart(df, height=sz, width=sz)
        .transform_aggregate(num_vals="count()", groupby=[truth, pred])
        .transform_calculate(
            rev_num_vals="-(datum.num_vals) + max(datum.num_vals)",
        )
        .encode(
            alt.Y(f"{truth}:O", scale=alt.Scale(paddingInner=0)),
            alt.X(f"{pred}:O", scale=alt.Scale(paddingInner=0)),
        )
    )

    hm = base.mark_rect().encode(
        color=alt.Color(
            "num_vals:Q", scale=alt.Scale(scheme="lightorange"), legend=None
        )
    )

    tx = base.mark_text(baseline="middle").encode(
        text="num_vals:Q",
        #         color=alt.Color(alt.value('gray'))
        #         color='rev_num_vals:Q'
        #         color=alt.Color(
        #             'num_vals:Q', scale=alt.Scale(scheme="redyellowgreen"),
        #         )
        color=alt.condition(
            alt.datum.num_vals > threshold, alt.value("black"), alt.value("black")
        ),
    )

    try:
        from sklearn.metrics import classification_report

        print(classification_report(df[truth], df[pred]))
    except:
        logger.info("Skipping Report")
    return hm + tx


CM = confusion_matrix

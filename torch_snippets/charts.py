# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/charts.ipynb (unless otherwise specified).

__all__ = ['alt', 'Chart', 'confusion_matrix', 'CM']

# Cell
# export
import altair as alt
from altair import Chart
alt = alt
Chart = Chart
from .loader import *

# Cell
def confusion_matrix(df=None, truth=None, pred=None, threshold=None, mapping=None):
    if df is None:
        df = pd.DataFrame({'truth': truth, 'pred': pred})
        truth = 'truth'
        pred = 'pred'
    if threshold is None:
        threshold = len(df) // 4
    if mapping:
        assert isinstance(mapping, dict), 'mapping should be a dictionary'
        df[truth] = df[truth].map(lambda x: mapping[x])
        df[pred] = df[pred].map(lambda x: mapping[x])
    base = Chart(df).transform_aggregate(
        num_vals='count()',
        groupby=[truth, pred]
    ).encode(
        alt.X(f'{truth}:O', scale=alt.Scale(paddingInner=0)),
        alt.Y(f'{pred}:O', scale=alt.Scale(paddingInner=0)),
    )

    hm = base.mark_rect().encode(
        color=alt.Color('num_vals:Q',
            legend=None # alt.Legend(direction='horizontal')
        )
    )

    tx = base.mark_text(baseline='middle').encode(
        text='num_vals:Q',
        color=alt.condition(
            alt.datum.num_vals > threshold,
            alt.value('white'),
            alt.value('black'))
    )

    try:
        from sklearn.metrics import classification_report
        print(classification_report(df['truth'], df['pred']))
    except:
        ...

    return hm + tx

CM = confusion_matrix
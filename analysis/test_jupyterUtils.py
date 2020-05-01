import pytest

from jupyterUtils import exportPlotlyFigure


def test_fig_export():
    import plotly.graph_objects as go

    import numpy as np
    np.random.seed(1)

    # Generate scatter plot data
    N = 100
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    sz = np.random.rand(N) * 30

    # Build and display figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker={"size": sz,
                "color": colors,
                "opacity": 0.6,
                "colorscale": "Viridis"
                }
    ))

    exportPlotlyFigure(fig=fig, name='testFig')
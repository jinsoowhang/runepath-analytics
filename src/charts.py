import plotly.express as px
import plotly.graph_objects as go


def line_chart(df, x, y, title):
    return px.line(df, x=x, y=y, title=title)


def bar_chart(df, x, y, title):
    return px.bar(df, x=x, y=y, title=title)


def heatmap(z, x, y, z_label="Value", title="Heatmap", color_scale="Blues"):
    """
    Create a heatmap visualization
    
    Args:
        z: 2D array/matrix of values
        x: List of x-axis labels (columns)
        y: List of y-axis labels (rows)
        z_label: Label for the color scale
        title: Chart title
        color_scale: Plotly color scale (Blues, RdYlGn, Viridis, etc.)
    """
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=color_scale,
        text=z,
        texttemplate='%{text:.1f}%',
        textfont={"size": 10},
        colorbar=dict(title=z_label),
        hoverongaps=False
    ))
    
    fig.update_layout(
        title=title,
        height=600
    )
    
    return fig
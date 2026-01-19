import plotly.express as px

def line_chart(df, x, y, title):
    return px.line(df, x=x, y=y, title=title)


def bar_chart(df, x, y, title):
    return px.bar(df, x=x, y=y, title=title)

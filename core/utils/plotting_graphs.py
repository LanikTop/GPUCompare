import plotly.graph_objects as go
import plotly.offline as pyo


def create_top5_best_graph(comparisons, game_name, resolution, settings):
    gpu_names = [c.gpu.name + f" ({c.gpu.memory_gb} Гб)" for c in comparisons]
    fps_values = [c.avg_fps for c in comparisons]
    prices = [c.gpu.price_rub for c in comparisons]
    x_positions = list(range(1, len(comparisons) + 1))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_positions,
        y=fps_values,
        mode='lines+markers+text',
        name='FPS',
        line=dict(
            color='#2E86AB',
            width=4,
            shape='spline',
            smoothing=0.7
        ),
        marker=dict(
            size=15,
            color=fps_values,
            colorscale='Viridis',
            showscale=False,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        text=[f"{fps:.1f} FPS" for fps in fps_values],
        textposition="top center",
        customdata=list(zip(gpu_names, prices)),
        hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Место: <b>%{x}</b><br>" +
                "FPS: <b>%{y:.1f}</b><br>" +
                "Цена: <b>%{customdata[1]}₽</b><br>" +
                "<extra></extra>"
        )
    ))

    for i, (pos, name) in enumerate(zip(x_positions, gpu_names)):
        fig.add_annotation(
            x=pos,
            y=min(fps_values) * 0.8,
            text=f"<b>{name}</b>",
            showarrow=False,
            font=dict(size=15),
            textangle=0,
            yshift=-60
        )

    fig.update_layout(
        title=dict(
            text=f'<b>Топ-5 видеокарт с наивысшим FPS в {game_name}</b><br><span style="font-size:14px">{resolution}, {settings}</span>',
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Место в рейтинге',
            tickmode='array',
            tickvals=x_positions,
            ticktext=[f"#{i}" for i in x_positions],
            range=[0.5, len(x_positions) + 0.5],
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title='Средний FPS',
            gridcolor='lightgray',
            gridwidth=1
        ),
        plot_bgcolor='white',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Arial'
        ),
        showlegend=False,
        height=600,
        margin=dict(l=50, r=50, t=100, b=100)
    )

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    return pyo.plot(fig, output_type='div', include_plotlyjs=False)


def create_top5_optimal_graph(comparisons, game_name, resolution, settings):
    gpu_names = [c.gpu.name + f" ({c.gpu.memory_gb} Гб)" for c in comparisons]
    fps_values = [c.avg_fps for c in comparisons]
    prices = [float(c.gpu.price_rub) for c in comparisons]
    efficiency = [c.efficiency for c in comparisons]
    x_positions = list(range(1, len(comparisons) + 1))
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_positions,
        y=prices,
        mode='lines+markers+text',
        name='FPS',
        line=dict(
            color='#2E86AB',
            width=4,
            shape='spline',
            smoothing=0.7
        ),
        marker=dict(
            size=15,
            color=prices,
            colorscale='Viridis',
            showscale=False,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        text=[f"{price}₽" for price in prices],
        textposition="top center",
        customdata=list(zip(gpu_names, prices, fps_values, efficiency)),
        hovertemplate=(
                "<b>%{customdata[0]}</b><br>" +
                "Место: <b>%{x}</b><br>" +
                "Цена: <b>%{customdata[1]}₽</b><br>" +
                "FPS: <b>%{customdata[2]:.1f}</b><br>" +
                "FPS/1000₽: <b>%{customdata[3]:.5f}</b><br>" +
                "<extra></extra>"
        )
    ))

    for i, (pos, name) in enumerate(zip(x_positions, gpu_names)):
        fig.add_annotation(
            x=pos,
            y=min(prices) * 0.8,
            text=f"<b>{name}</b>",
            showarrow=False,
            font=dict(size=15),
            textangle=0,
            yshift=-40
        )

    fig.update_layout(
        title=dict(
            text=f'<b>Топ-5 оптимальных видеокарт в {game_name}</b><br><span style="font-size:14px">{resolution}, {settings}</span>',
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Место в рейтинге',
            tickmode='array',
            tickvals=x_positions,
            ticktext=[f"#{i}" for i in x_positions],
            range=[0.5, len(x_positions) + 0.5],
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title='Цена, руб',
            gridcolor='lightgray',
            gridwidth=1
        ),
        plot_bgcolor='white',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Arial'
        ),
        showlegend=False,
        height=600,
        margin=dict(l=50, r=50, t=100, b=100)
    )

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    return pyo.plot(fig, output_type='div', include_plotlyjs=False)

def create_top5_budget_graph(comparisons, game_name, resolution, settings):
    gpu_names = [c.gpu.name + f" ({c.gpu.memory_gb} Гб)" for c in comparisons]
    fps_values = [c.avg_fps for c in comparisons]
    prices = [c.gpu.price_rub for c in comparisons]
    x_positions = list(range(1, len(comparisons) + 1))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_positions,
        y=fps_values,
        mode='lines+markers+text',
        name='FPS',
        line=dict(
            color='#2E86AB',
            width=4,
            shape='spline',
            smoothing=0.7
        ),
        marker=dict(
            size=15,
            color=fps_values,
            colorscale='Viridis',
            showscale=False,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        text=[f"{fps:.1f} FPS" for fps in fps_values],
        textposition="top center",
        customdata=list(zip(gpu_names, prices)),
        hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Место: <b>%{x}</b><br>" +
                "FPS: <b>%{y:.1f}</b><br>" +
                "Цена: <b>%{customdata[1]}₽</b><br>" +
                "<extra></extra>"
        )
    ))

    for i, (pos, name) in enumerate(zip(x_positions, gpu_names)):
        fig.add_annotation(
            x=pos,
            y=min(fps_values) * 0.8,
            text=f"<b>{name}</b>",
            showarrow=False,
            font=dict(size=15),
            textangle=0,
            yshift=-60
        )

    fig.update_layout(
        title=dict(
            text=f'<b>Топ-5 бюджетных видеокарт в {game_name}</b><br><span style="font-size:14px">{resolution}, {settings}</span>',
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Место в рейтинге',
            tickmode='array',
            tickvals=x_positions,
            ticktext=[f"#{i}" for i in x_positions],
            range=[0.5, len(x_positions) + 0.5],
            gridcolor='lightgray',
            gridwidth=1
        ),
        yaxis=dict(
            title='Средний FPS',
            gridcolor='lightgray',
            gridwidth=1
        ),
        plot_bgcolor='white',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Arial'
        ),
        showlegend=False,
        height=600,
        margin=dict(l=50, r=50, t=100, b=100)
    )

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    return pyo.plot(fig, output_type='div', include_plotlyjs=False)
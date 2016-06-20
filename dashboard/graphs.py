import json
import plotly
from datetime import datetime


# # Convert the start date in the desired format
# def format_start_date(start_date):
#     return datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
#
# # Convert the end date in the desired format
# def format_end_date(end_date):
#     return datetime.strptime(end_date, '%Y-%m-%d').strftime('%d/%m/%Y')


def generate_graph(data, title, username, start_date, end_date):
    graphs = [
        dict(
            data=[
                dict(
                    x=data.keys(),
                    y=data.values(),
                    type='bar',
                ),
            ],
            layout=dict(
                title=title + ' for ' + username + ' between ' +
                      str(start_date) + ' and ' + str(end_date)
            )
        )
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graph_json


def generate_pie_chart(data, title, username, start_date, end_date):
    graphs = [
        dict(
            data=[
                dict(
                    labels=data.keys(),
                    values=data.values(),
                    type='pie',
                ),
            ],
            layout=dict(
                title=title + ' for ' + username + ' between ' +
                      str(start_date) + ' and ' + str(end_date)
            )
        )
    ]
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graph_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graph_json

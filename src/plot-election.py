from bokeh.models import ColumnDataSource, LabelSet, ranges
from bokeh.plotting import figure, show, output_file

import codecs
import json

def make_others(data):
    sum_share = 0
    sum_votes = 0
    delNums = []
    for i, val in enumerate(data):
        if val['share'] < 1:
            sum_share += val['share']
            sum_votes += val['votes']
            delNums.append(val['number'])
    data.append({'number':111111, 'name': 'Ostatní', 'share': sum_share, 'votes': sum_votes, 'color': '#555', 'short': 'Ostatní'})
    data = list(filter(lambda x: x['number'] not in delNums, data))
    return data

def make_short(name):
    return ''.join( map(lambda x: x[:1], name.split(' ')) )

data = json.load(codecs.open("../data/election.json", 'r', 'utf-8-sig'))
data = sorted(data, key= lambda x: x['votes'], reverse=True)

data = make_others(data)

src = ColumnDataSource( data = {
    'share': list(map(lambda x: x['share'], data)),
    'color': list(map(lambda x: x['color'] if 'color' in x else '#333333', data)),
    'label': list(map(lambda x: x['short'] if 'short' in x else make_short(x['name']), data)),
    'votes': list(map(lambda x: x['votes'] if 'votes' in x else 0, data)),
})
p = figure( plot_width=1000, plot_height=600,
            x_axis_label = 'Strany', y_axis_label = 'Procenta',
            title = 'Volby 2017',
            x_minor_ticks=2,
            x_range=src.data['label'], y_range= ranges.Range1d(start=0,end=40))
labels = LabelSet(x='label', y='share', text='votes', level='glyph',
                  x_offset=-28, y_offset=0, source=src, render_mode='canvas')
p.add_layout(labels)
p.vbar(source = src, x = "label", top = "share", bottom = 0, width = 0.8, color = 'color')

output_file("../data/election2017.html")
show( p )
from cProfile import label
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    if chart_type == '#1':
        #plt.bar(data['date'], data['price'])
        sns.barplot(x='year-month', y='total_price', data=data)
    elif chart_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data=data, x='total_price', labels=labels)
    elif chart_type == '#3':
        plt.plot(data['year-month'], data['total_price'])
    else:
        print('failed to identify the chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart
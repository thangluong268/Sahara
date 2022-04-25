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


def get_key(res_by):
    key = None
    if res_by == '#1':
        key = 'quantity'
    elif res_by == '#2':
        key = 'total_price'
    return key


def get_data(data, res_by):
    dt = None
    if res_by == '#1':
        dt = data.groupby(['year-month', 'product name'], as_index=False)['quantity'].agg('sum')
        dt = dt.sort_values(by=['year-month', 'quantity'], ascending=False)
        dt = dt.drop_duplicates(subset=['year-month'])
        # dt = dt.drop('quantity', axis=1)
    elif res_by == '#2':
        dt = data.groupby('year-month', as_index=False)['total_price'].agg('sum')
    return dt


def get_chart(chart_type, data_df, result_by):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 4))
    key = get_key(result_by)
    dt = get_data(data_df, result_by)

    if chart_type == '#1':
        plt.bar(dt['year-month'], dt[key])
        # sns.barplot(x='year-month', y=key, data=dt)
        for i in range(len(dt[key])):
            if key == 'quantity':
                plt.annotate(xy=(i - 0.4, dt[key].values[i]), text=dt['product name'].values[i])
            else:
                plt.annotate(xy=(i - 0.4, dt[key].values[i]), text=dt[key].values[i])

    elif chart_type == '#2':
        plt.pie(data=dt, x=key, labels=dt['year-month'].values, autopct='%1.2f%%')
        if key == 'quantity':
            plt.legend(dt['product name'], bbox_to_anchor=(-0.8, 1), loc="upper left")
        else:
            plt.legend(dt['total_price'], bbox_to_anchor=(-0.8, 1), loc="upper left")


    elif chart_type == '#3':
        plt.plot(dt['year-month'], dt[key])
        for i in range(len(dt[key])):
            if key == 'quantity':
                plt.annotate(xy=(i, dt[key].values[i]), text=dt['product name'].values[i])
            else:
                plt.annotate(xy=(i, dt[key].values[i]), text=dt[key].values[i])

    else:
        print('failed to identify the chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart

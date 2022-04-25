from math import fabs
from unittest import result
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from store.models.orders import Order
from store.models.product import Product
from store.models.customer import Customer
import pandas as pd
from store.utils import get_chart, get_data

CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)

RESULT_CHOICES = (
    ('#1', 'Product'),
    ('#2', 'Revenue'),
)


class SearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    result_by = forms.ChoiceField(choices=RESULT_CHOICES)


class SearchFormView(View):
    def get(self, request):
        form = SearchForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'report.html', {'context': context})

    def post(self, request):
        form = SearchForm(request.POST or None)
        orders_df = None
        result_df = None
        chart = None

        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_by = request.POST.get('result_by')

        order = Order.get_orders_by_date(date_from, date_to)

        if len(order) > 0:
            orders_df = pd.DataFrame(order.values())

            orders_df['product_id'] = orders_df['product_id'].apply(Product.get_product_by_id)
            orders_df['customer_id'] = orders_df['customer_id'].apply(Customer.get_customer_by_id)
            orders_df = orders_df.rename({'product_id': 'product name', 'customer_id': 'customer', 'id': 'order_id'}, axis=1)
            orders_df = orders_df.drop('status', axis=1)
            orders_df['total_price'] = orders_df['quantity']*orders_df['price']
            orders_df['year-month'] = pd.to_datetime(orders_df['date']).dt.strftime('%Y-%m')
        
            chart = get_chart(chart_type, orders_df, result_by)
            result_df = get_data(orders_df, result_by)

            orders_df = orders_df.to_html()
            result_df = result_df.to_html()

        else:
            print("no data")

        context = {
            'form': form,
            'orders_df': orders_df,
            'chart': chart,
            'result_df': result_df,
        }

        return render(request, 'report.html', {'context': context})

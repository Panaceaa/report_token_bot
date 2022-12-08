import io
import re

import pandas as pd
from fpdf import FPDF, HTMLMixin
import sql_data
import numpy as np
import requests
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates
import pathlib
import get_data

# для винды не нужна
pathlib.WindowsPath = pathlib.PosixPath


font_manager.fontManager.addfont('Fonts/Anonymous_Pro.ttf')
prop = font_manager.FontProperties(fname='Fonts/Anonymous_Pro.ttf')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()


class PDF(FPDF, HTMLMixin):
    def header(self):
        # Rendering logo:
        self.image("https://storage.yandexcloud.net/research.b4b/TokenSets/b4b.png", 250, 8, 20, 12)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("times", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")


def plot_pie(weighted):

    colors = plt.get_cmap('BuGn')(np.linspace(0.2, 0.5, len(weighted['weight'])))

    plt.pie(weighted['weight'],
            labels=weighted['ticker'],
            startangle=90,
            autopct='%1.1f%%',
            textprops={'fontsize': 14}, colors=colors)

    plt.axis('equal')

    fig = plt.gcf()
    fig.set_size_inches(12.5, 7.5)

    comma_fmt = FuncFormatter(lambda x, p: format(int(x), ','))
    plt.gca().yaxis.set_major_formatter(comma_fmt)
    png = io.BytesIO()

    plt.savefig(png, format='png')
    png.seek(0)
    plt.clf()
    plt.close()
    return png


def plot_graph(return_db, bench):
    fig, ax = plt.subplots()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.margins(x=0)
    ax.margins(y=0)
    list_value = return_db[return_db.columns[0]].astype(float).tolist()
    list_value.extend([x * 100 for x in bench.values])
    plt.fill_between(return_db.index, return_db[return_db.columns[0]].astype(float), y2=np.min(list_value), color="#44DAB7", alpha=0.7, label=return_db.columns[0])
    plt.fill_between(return_db.index, [x * 100 for x in bench.astype(float).values], y2=np.min(list_value), color="#000000", alpha=0.2, label='BTC')
    plt.annotate('{:.1f} $'.format(return_db[return_db.columns[0]][-1]), xy=(1, return_db[return_db.columns[0]][-1]), xytext=(8, 0),
                 xycoords=('axes fraction', 'data'), textcoords='offset points', fontsize=16)

    plt.legend(loc="upper left", frameon=False)

    fig = plt.gcf()
    fig.set_size_inches(15.0, 5.0)

    comma_fmt = FuncFormatter(lambda x, p: '{:.1f} $'.format(x))
    x_format = mdates.DateFormatter('%d.%b.%y')
    plt.gca().yaxis.set_major_formatter(comma_fmt)
    plt.gca().xaxis.set_major_formatter(x_format)

    png = io.BytesIO()
    plt.savefig(png, format='png')
    png.seek(0)
    plt.clf()
    plt.close()
    return png


def indent_format(pdf):
    if pdf.get_y() < 20:
        pdf.set_y(20)
    if pdf.get_y() > 180:
        pdf.add_page(orientation='L')
        pdf.set_y(25)


def pdf_creator_structure(graph_png, weighted_png, token):
    today_day = datetime.date.today()
    today = today_day.strftime('%Y%m%d')
    name_file = 'Report'

    pdf = PDF()
    pdf.add_page(orientation='L')
    pdf.add_font('Anonymous_Pro', '', "Fonts/Anonymous_Pro.ttf", uni=True)
    pdf.add_font('Anonymous_Pro', 'B', "Fonts/Anonymous_Pro_B.ttf", uni=True)
    line_height = int(9)

    # report date
    pdf.set_xy(25, 10)
    pdf.set_font("Anonymous_Pro", size=16, style='B')
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.set_x(7)
    pdf.set_fill_color(99, 99, 99)

    pdf.set_xy(25, 17)
    pdf.set_font("Anonymous_Pro", size=11)
    pdf.cell(align='L', w=51, h=6, txt=f'Дата отчета: {today_day.strftime("%Y.%m.%d")}', border=0, fill=True)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_x(10)

    # graph/instruments/classes
    pdf.set_font("Anonymous_Pro", size=11, style='B')
    shift = 100
    pdf.set_x(10)
    pdf.image(graph_png, x=10, y=25, w=270, h=77)
    pdf.set_xy(30, 25)
    pdf.cell(align='L', w=0, txt=f'Динамика токена {token}', border=0)
    pdf.set_y(30 + pdf.font_size + 2 * shift)
    pdf.image(weighted_png, x=0, y=100, w=150, h=90)
    pdf.set_xy(30, 100)
    pdf.cell(align='L', w=0, txt=f'Текущее распределение', border=0)
    pdf.output('output.pdf')
    return_byte_string = pdf.output(dest='S')
    the_file = io.BytesIO(return_byte_string)
    the_file.seek(0)

    the_file.name = f'{token} {today[2:]} {name_file}.pdf'
    return the_file


def file_creator(token):
    oc_prices = pd.DataFrame()
    oc_prices.index.name = 'date'
    perf, bench, weight = get_data.return_full_data(token)
    # return graph
    graph_png = plot_graph(perf, bench)

    # weight
    weighted_png = plot_pie(weight)

    the_file = pdf_creator_structure(graph_png, weighted_png, token)

    return the_file


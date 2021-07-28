import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .forms import ContactForm

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
import numpy as np
def get_plot(x,y, title=None, labels=[], y_lim=()):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    # plt.style.use('fivethirtyeight')
    plt.axhline(y=0, color='k')
    plt.title(title)
    plt.plot(x, y, marker='.')

    plt.xticks(rotation=45)
    # plt.axvline(0.5)
    # plt.axhline(0)
    if labels:
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])

    plt.tight_layout()
    if y_lim:
        plt.ylim(y_lim)
    graph = get_graph()
    return graph

def get_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()

    return form
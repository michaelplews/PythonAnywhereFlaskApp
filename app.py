# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, Response, request
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import scipy.stats as stats
import pandas as pd
import base64

app = Flask(__name__)
app.config["DEBUG"] = True

def monte_carlo_sim(alpha, n1, p1, n2, p2, size):
    A = stats.binom(n1, p1).rvs(size=size)/n1
    B = stats.binom(n2, p2).rvs(size=size)/n2

    data = {
        "A":{
            'mean': A.mean(),
            'UCI': np.quantile(A, q=1-alpha/2),
            'LCI': np.quantile(A, q=alpha/2)
        },
        "B":{
            'mean': B.mean(),
            'UCI': np.quantile(B, q=1-alpha/2),
            'LCI': np.quantile(B, q=alpha/2)
        },
    }
    data = pd.DataFrame(data).T
    data['UCI']-=data['mean']
    data['LCI']-=data['mean']
    
    fig, ax = plt.subplots(dpi=150)
    data[['mean']].plot(kind="bar", rot=0, yerr=[data.UCI, data.LCI], ax=ax)
    ax.legend().set_visible(False)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel('Proportion')
    ax.set_xlabel("Condition")
    return fig, *np.quantile(A-B, q=[alpha/2, 0.5, 1-alpha/2])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("main_page.html")
    elif request.method == "POST":
        # extract variables
        a = request.form.get("alpha", type=float)
        n1 = request.form.get("groupA_trials", type=int)
        p1 = request.form.get("groupA_successes", type=int)/n1
        n2 = request.form.get("groupB_trials", type=int)
        p2 = request.form.get("groupB_successes", type=int)/n2
        size = request.form.get("simulation_size", type=int)
        
        # generate the png image
        fig, d_lci, d_mean, d_uci = monte_carlo_sim(alpha=a, n1=n1, p1=p1, n2=n2, p2=p2, size=size)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        
        # convert to base64
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(output.getvalue()).decode('utf8')

        return render_template("comp_prop.html", 
            result=pngImageB64String,
            n1=n1,
            n2=n2,
            p1=p1,
            p2=p2,
            d_lci="{0:.2f}".format(d_lci),
            d_mean="{0:.2f}".format(d_mean),
            d_uci="{0:.2f}".format(d_uci),
            ci=100*(1-a)
        )
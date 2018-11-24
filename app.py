from flask import Flask, render_template, request, send_from_directory
import os
from script import hydrophobicity as hp
from corrcoef import correlation as cr

app = Flask(__name__, static_url_path='/static')


path = 'Hydropathy_Plot.pdf'

atomic_kernel= None

@app.route('/')
def plot():
    return render_template('plot.html')

@app.route('/correlation/', methods=['GET','POST'])
def plot2():
    return render_template('correlation.html')

@app.route('/generate2/', methods=['GET','POST'])
def getplot2():
    try:
        if request.method=="POST":
            amino_acid_sequence = request.form['sequence']
            window_size = request.form['Wsize']
            menu =request.form['menu']
            # print(amino_acid_sequence)
            # print(window_size)
            # print(menu)
            cof = cr()
            cof.get_coefficient_plot(amino_acid_sequence,window_size,menu)

    except Exception as e:
        print(e)
    return render_template('correlation.html')

@app.route('/generate/', methods=['GET','POST'])
def getplot():
    hydropathy_plot_url = None
    # try:
    #     if request.method=="POST":
    #         amino_acid_sequence = request.form['sequence']
    #         window_size = request.form['Wsize']
    #         h = hp()
    #         hydropathy_plot_url = hp.get_plot(amino_acid_sequence,window_size)

    # except Exception as e:
    #     print(e)

    if request.method=="POST":
            amino_acid_sequence = request.form['sequence']
            window_size = request.form['Wsize']
            h = hp()
            hydropathy_plot_url = hp.get_plot(amino_acid_sequence,window_size)

    return render_template('results.html', hydropathy_plot=hydropathy_plot_url)


@app.route('/pdf/', methods=['GET','POST'])
def pdf():
    # return "hello"
    return send_from_directory('static/pdfs', 'Hydropathy Plot.pdf')


@app.route('/excel/', methods=['GET','POST'])
def excel():
    # return "hello"
    return send_from_directory('static/pdfs', 'Hydrophobicity_scores.xls')


"""
if __name__=='__main__':
	app.run(host='0.0.0.0', port=4141, debug=True, threaded=True)
"""
if __name__=='__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/zenith-voyages')
def zenith_voyages():
    return render_template('zenith_voyages.html')

@app.route('/aether-tech')
def aether_tech():
    return render_template('aether_tech.html')

@app.route('/solaris-ventures')
def solaris_ventures():
    return render_template('solaris_ventures.html')

if __name__ == '__main__':
    app.run(debug=True)
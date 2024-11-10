from flask import Flask, render_template
from py.analises import (criar_grafico_ocorrencias_por_ano, gerar_grafico_local)
app = Flask(__name__)

@app.route('/')
def index():
    # Renderiza o gráfico e passa para o template
    grafico_html = criar_grafico_ocorrencias_por_ano()
    gerar_gr_html = gerar_grafico_local()
    return render_template('index.html', grafico_html=grafico_html, gerar_gr_html=gerar_gr_html) 

if __name__ == '__main__':
    app.run(debug=True)

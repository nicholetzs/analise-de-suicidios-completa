from flask import Flask, render_template
from py.analises import (criar_grafico_ocorrencias_por_ano,
                         gerar_grafico_local, total_suicidios, idade_mais_afetada)
app = Flask(__name__)


@app.route('/inicio')
def inicio():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/graficos')
def graficos():
    # Renderiza o gráfico e passa para o template
    grafico_html = criar_grafico_ocorrencias_por_ano()
    gerar_gr_html = gerar_grafico_local()
    idade, suicidios = idade_mais_afetada()
    return render_template('graficos.html', grafico_html=grafico_html, gerar_gr_html=gerar_gr_html, total_suicidios=total_suicidios(), idade=idade, suicidios=suicidios)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)

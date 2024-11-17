from flask import Flask, render_template
from py.analises import (criar_grafico_ocorrencias_por_ano,
                         gerar_grafico_local, total_suicidios, idade_mais_afetada, local_mais_ocorrencias, gerar_grafico_faixa_etaria, gerar_grafico_suicidios_distribuicao, maior_causa_suicidio)
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
    local, ocorrencias = local_mais_ocorrencias()
    gerar_gr_faixa_etaria_html = gerar_grafico_faixa_etaria()
    gerar_grafico_suicidios_distribuicao_html = gerar_grafico_suicidios_distribuicao()
    causa, qtd = maior_causa_suicidio()

    return render_template('graficos.html', grafico_html=grafico_html, gerar_gr_html=gerar_gr_html, total_suicidios=total_suicidios(),
                           idade=idade, suicidios=suicidios, local=local, ocorrencias=ocorrencias, gerar_gr_faixa_etaria_html=gerar_gr_faixa_etaria_html, gerar_grafico_suicidios_distribuicao_html=gerar_grafico_suicidios_distribuicao_html, causa=causa, qtd=qtd)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)

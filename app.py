from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Certifique-se de que este nome corresponde exatamente ao arquivo

if __name__ == '__main__':
    app.run(debug=True)

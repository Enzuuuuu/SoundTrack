from flask import Flask, render_template
# Cria a aplicação Flask
app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
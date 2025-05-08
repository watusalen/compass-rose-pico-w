import os
from flask import Flask, request, jsonify, render_template_string, make_response
from flask_cors import CORS  # Adicione esta linha

app = Flask(__name__)
CORS(app)  # Adicione esta linha para permitir requisições CORS

# Variável para armazenar a última direção detectada
last_direction = "Norte"
last_x = 2048
last_y = 2048

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rosa dos Ventos</title>
    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #eef2f5;
            --container-bg: #ffffff;
            --accent-color: #2980b9;
            --text-color: #34495e;
            --arrow-color: #e74c3c;
            --font-family: 'Roboto', sans-serif;
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: var(--font-family);
            background: var(--bg-color);
            color: var(--text-color);
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            background: var(--container-bg);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--accent-color);
        }
        .compass {
            position: relative;
            width: 250px;
            height: 250px;
            margin: 1rem auto;
            border: 4px solid var(--text-color);
            border-radius: 50%;
            background: radial-gradient(circle at center, #fdfdfd 70%, #f0f0f0 100%);
        }
        .direction {
            position: absolute;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-color);
            font-size: 0.9rem;
        }
        .north      { top: 8%;  left: 50%; transform: translateX(-50%); }
        .south      { bottom: 8%; left: 50%; transform: translateX(-50%); }
        .east       { top: 50%; right: 8%; transform: translateY(-50%); }
        .west       { top: 50%; left: 8%; transform: translateY(-50%); }
        .northeast  { top: 18%; right: 18%; }
        .northwest  { top: 18%; left: 18%; }
        .southeast  { bottom: 18%; right: 18%; }
        .southwest  { bottom: 18%; left: 18%; }
        .center     { top: 50%; left: 50%; transform: translate(-50%, -50%); 
                       font-size: 1.2rem; color: var(--accent-color); }
        .arrow {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 16px;
            height: 100px;
            background: var(--arrow-color);
            clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            transform-origin: 50% 100%;
            transform: translate(-50%, -100%) rotate(0deg);
            transition: transform 0.4s ease-in-out;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            border-radius: 2px;
        }
        .current-direction {
            font-size: 1.25rem;
            margin: 0.75rem 0;
        }
        .coordinates {
            font-size: 0.95rem;
            color: var(--accent-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Rosa dos Ventos</h1>
        <div class="compass">
            <div class="direction north">N</div>
            <div class="direction northeast">NE</div>
            <div class="direction east">E</div>
            <div class="direction southeast">SE</div>
            <div class="direction south">S</div>
            <div class="direction southwest">SW</div>
            <div class="direction west">W</div>
            <div class="direction northwest">NW</div>
            <div class="direction center">•</div>
            <div class="arrow" id="arrow"></div>
        </div>
        <div class="current-direction">
            Direção atual: <span id="direction">Norte</span>
        </div>
        <div class="coordinates" id="coordinates">
            X: 2048, Y: 2048
        </div>
    </div>

    <script>
        async function updateDirection() {
            try {
                const res = await fetch('/data');
                if (!res.ok) throw new Error('Erro na requisição');
                const data = await res.json();
                document.getElementById('direction').textContent = data.direction;
                document.getElementById('coordinates').textContent = `X: ${data.x}, Y: ${data.y}`;
                const arrow = document.getElementById('arrow');
                const map = {
                    'Norte': 0,'Nordeste':45,'Leste':90,'Sudeste':135,
                    'Sul':180,'Sudoeste':225,'Oeste':270,'Noroeste':315,'Centro':0
                };
                const angle = map[data.direction] || 0;
                arrow.style.transform = `translate(-50%, -100%) rotate(${angle}deg)`;
            } catch(e) {
                console.error(e);
            }
        }
        updateDirection();
        setInterval(updateDirection, 500);
    </script>
</body>
</html>
"""

@app.route("/data", methods=["GET"])
def get_direction():
    global last_direction, last_x, last_y
    
    # Se receber parâmetros, atualiza os valores
    if 'x' in request.args and 'y' in request.args:
        last_x = request.args.get("x", type=int, default=2048)
        last_y = request.args.get("y", type=int, default=2048)
    
    # Lógica para determinar a direção
    ADC_MAX = 4095  # 12-bit ADC
    
    if last_y < ADC_MAX / 4 and last_x < ADC_MAX / 4:
        direction = "Sudoeste"
    elif last_y < ADC_MAX / 4 and last_x > 3 * ADC_MAX / 4:
        direction = "Sudeste"
    elif last_y > 3 * ADC_MAX / 4 and last_x < ADC_MAX / 4:
        direction = "Noroeste"
    elif last_y > 3 * ADC_MAX / 4 and last_x > 3 * ADC_MAX / 4:
        direction = "Nordeste"
    elif last_y < ADC_MAX / 3:
        direction = "Sul"
    elif last_y > 2 * ADC_MAX / 3:
        direction = "Norte"
    elif last_x < ADC_MAX / 3:
        direction = "Oeste"
    elif last_x > 2 * ADC_MAX / 3:
        direction = "Leste"
    else:
        direction = "Centro"
    
    last_direction = direction
    
    # Debug no console do servidor
    print(f"Retornando dados - X: {last_x}, Y: {last_y}, Direção: {direction}")
    
    response = jsonify({
        "direction": direction,
        "x": last_x,
        "y": last_y
    })
    
    # Configura headers para evitar cache
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

@app.route("/", methods=["GET"])
def pagina_inicial():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
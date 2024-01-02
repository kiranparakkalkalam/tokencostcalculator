from flask import Flask, request, jsonify
from tokencost import calculate_prompt_cost, USD_PER_TPU
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

@app.route('/calculate', methods=['POST'])
@cross_origin()
def calculate_token_cost():
    data = request.json
    prompt = data['prompt']
    model = data['model']
    prompt_cost = calculate_prompt_cost(prompt=prompt, model=model)
    prompt_cost_in_usd = float(prompt_cost/USD_PER_TPU)
    prompt_decimal_notation = ("%.17f" % prompt_cost_in_usd).rstrip('0').rstrip('.')
    response_data = {
        'model': model,
        'prompt_cost': prompt_cost,
        'prompt_cost_in_usd': prompt_decimal_notation
    }
    return jsonify(response_data)
    

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, jsonify, request
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert_currency', methods=['POST'])
def convert():
    from_currency = request.form.get('from')
    try:
        amount = float(request.form.get('amount'))
    except TypeError:
        return jsonify({'result': 'Invalid Amount Entered'})
    to_currency = request.form.get('to')
    result_amount = amount

    if from_currency != to_currency:
        result_amount = _currency_convert_api(from_currency, amount, to_currency)

    if result_amount:
        result = '{:.2f} {} is equal to {:.2f} {}'.format(amount, from_currency, result_amount, to_currency)
    else:
        result = 'Something Went Wrong'

    return jsonify({'result': result})


def _currency_convert_api(from_currency, amount, to_currency):
    query_string = '{fromc}_{toc}'.format(fromc=from_currency, toc=to_currency)
    base_url = 'https://free.currencyconverterapi.com/api/v6/convert?q={query_string}&compact=ultra' \
        .format(query_string=query_string)

    converter_response = requests.get(base_url)
    response_text = json.loads(converter_response.text)

    conversion_rate = response_text.get(query_string)

    if conversion_rate:
        return amount * conversion_rate

    return None


if __name__ == '__main__':
    app.run(debug=True)

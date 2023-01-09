from flask import Flask, render_template, request, flash
import requests

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

with open('waluty.csv', 'w', encoding='UTF-8') as mf:

    for item in data[0]['rates']:
        currency=item['currency']
        code=item['code']
        bid=item['bid']
        ask=item['ask']
        mf.write (currency + ';' + code + ';' + str(bid) + ';' + str(ask) +'\n') 

with open ('waluty.csv', encoding='UTF-8') as mf:
    lst=mf.readlines()

output=[]

for item in lst:
    output.append (item.strip().split(';'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route("/kalkulator/", methods=["GET", "POST"])
def form_view():
    if request.method == "POST":
        data=request.form
        print (output)
        code=data['waluty']
        ilosc=int (data ['ilosc'])
        for waluta in output:
            if waluta[1]==code:
                total=ilosc * float(waluta [-1])
        flash(f'Aby kupić {ilosc} {code} potrzebujesz {round (total,2)} PLN', category='info')
    return render_template('kalkulator.html', items=output)

if __name__ == '__main__':
    app.run(debug=True)
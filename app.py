from flask import Flask, render_template, request
from utils import get_salary, get_rating, get_secret_key

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        salary_data = get_salary(
            request.form['first'],
            request.form['last']
            )
        rating_data = get_rating(
            salary_data['full_name'],
            request.form['school']
            )
        return render_template(
            'results.html',
            full_name = salary_data['full_name'],
            salary = "{:,}".format(salary_data['salary']),
			salaryfloat = salary_data['salary'],
            rating = rating_data['rating'],
            num_ratings = rating_data['num_ratings']
            )
    return render_template('index.html')

if __name__ == "__main__":
   app.debug = True
   app.secret_key = get_secret_key()
   app.run(host="0.0.0.0", port=8000)

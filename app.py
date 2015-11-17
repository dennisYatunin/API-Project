from flask import Flask, render_template, request
from utils import get_salary, get_name_and_rating, get_rating, get_secret_key, get_photo, get_efficiency

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        salary_data = get_salary(
            request.form['first'],
            request.form['last']
            )
        full_name = salary_data['full_name']
        salary = salary_data['salary']
        # If the NYC Database does not have an entry with the given name,
        # scrape ratemyteachers.com for the teacher with the closest name
        # at the given school, and then attempt to get the salary data again.
        if not salary:
            name_and_rating_data = get_name_and_rating(
                full_name,
                request.form['school']
                )
            subject = name_and_rating_data['subject']
            rating = name_and_rating_data['rating']
            num_ratings = name_and_rating_data['num_ratings']
            salary_data = get_salary(
                name_and_rating_data['first_name'],
                name_and_rating_data['last_name']
                )
            full_name = salary_data['full_name']
            salary = salary_data['salary']
        # Otherwise, only use ratemyteachers.com to get the rating.
        else:
            rating_data = get_rating(
                salary_data['full_name'],
                request.form['school']
                )
            subject = rating_data['subject']
            rating = rating_data['rating']
            num_ratings = rating_data['num_ratings']
        photo = get_photo(full_name, request.form['school'])
        efficiency = get_efficiency(salary, rating)
        return render_template(
            'results.html',
            full_name = full_name,
            subject = subject,
            salary = salary,
            rating = rating,
            num_ratings = num_ratings,
            photo = photo,
            efficiency = efficiency
            )
    return render_template('index.html')

if __name__ == "__main__":
   app.debug = True
   app.secret_key = get_secret_key()
   app.run(host="0.0.0.0", port=8000)

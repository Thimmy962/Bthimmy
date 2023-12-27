from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        'id': 1, 'title': 'Data Analyst', 'location': "Lagos, Nigeria", 'salary': 250000,
    },
    {
        'id': 2, 'title': 'Web Developer', 'location': "Lagos, Nigeria", 'salary': 300000,
    },
    {
        'id': 3, 'title': 'Data Scientist', 'location': "Lagos, Nigeria", 'salary': 250000,
    },
    {
        'id': 4, 'title': 'AI Developer', 'location': "Lagos, Nigeria", 'salary': 500000,
    },
    {
        'id': 5, 'title': 'Frontend Engineer', 'location': "Lagos, Nigeria", 'salary': 200000,
    },
    {
        'id': 6, 'title': 'Backend engineer', 'location': "Lagos, Nigeria", 'salary': 400000,
    }
]


@app.route("/")
def hoome():
    return render_template('homepage.html',
                           jobs = JOBS)


@app.route("/api/jobs")
def list_cars():
    return jsonify(JOBS)


if __name__ == '__main__':
    app.run(debug=True)
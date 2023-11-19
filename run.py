from app.api import app, db, Numbers
from flask import render_template
import config

@app.route('/')
def index():
    numbers = Numbers.query.first()
    if numbers:
        num1 = numbers.num1
        num2 = numbers.num2
        result = num1 + num2
    else:
        num1 = 0
        num2 = 0
        result = 0
    return render_template('index.html', num1=num1, num2=num2, result=result)

if __name__ == '__main__':
    app.run(port=config.PORT)

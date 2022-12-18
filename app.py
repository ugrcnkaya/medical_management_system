from flask import render_template

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



@app.errorhandler(404)
# take 404 error
def not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
# take 500 error
def ser_error(e):
    return render_template("500.html")

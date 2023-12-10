from flask import Flask, render_template, request, redirect
from main import get_google_results, data_cleanup, compare_sentences

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    # get text from form
    text = request.form['text']
    google_results = get_google_results(text, num_results=5)
    # clean up the text
    cleaned_text = data_cleanup(text)
    # compare the sentences
    comparison = compare_sentences(cleaned_text, google_results)

    return render_template(
        'check.html',
        comparison=comparison,
    )


@app.route('/check', methods=['GET'])
def redirectToHome():
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

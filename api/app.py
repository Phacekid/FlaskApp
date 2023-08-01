
from flask import Flask, request, render_template, jsonify, Response
from werkzeug.utils import secure_filename
from api.my_pdf_processor import process_pdf_query, save_pdf_to_tmp
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        pdf_data = file.read()
        tmp_file_path = save_pdf_to_tmp(pdf_data)

        # filename = secure_filename(file.filename)
        # file.save(filename)

        question = request.form['question']
        response = process_pdf_query(tmp_file_path, question)

        return render_template('upload.html', response=response)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
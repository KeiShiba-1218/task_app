from flask import Flask, render_template, session, request, redirect, url_for, send_from_directory, g
import os
import werkzeug
import pandas as pd
from process_csv import preprocess, predict

app = Flask(__name__)
UPLOAD_DIR = './uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 # 100MB
app.config['UPLOAD_DIR'] = UPLOAD_DIR
app.secret_key = 'secret'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        prediction_state
    except NameError:
        prediction_state = session.get('prediction_state', None)
        session['prediction_state'] = 'まだ'
    
    if request.method=='POST':
        if 'file' not in request.files:
            print('ファイルがありません', flush=True)
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            print('ファイルがありません', flush=True)
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            
            return redirect(url_for('process', filename=filename))
        
        if os.path.join(app.config['UPLOAD_DIR'], 'answer.csv'):
            return redirect(url_for('download'))

    return render_template('index.html', prediction_state=prediction_state)

@app.route('/uploads/process/<filename>')
def process(filename):
    x = pd.read_csv(os.path.join(app.config['UPLOAD_DIR'], filename))
    x, train_nums = preprocess(x)
    y = predict(x, train_nums)
    y.to_csv(os.path.join(app.config['UPLOAD_DIR'], 'answer.csv'), index=False)
    session['prediction_state'] = '推論完了'
    
    return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download():
    return send_from_directory(app.config['UPLOAD_DIR'], 'answer.csv', 
                               as_attachment=True, attachment_filename='answer.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
from flask import Blueprint, render_template, redirect, url_for, request, flash
from project.models.model import Model
from project.views.view import View
from project.controllers.controller import Controller
from werkzeug.utils import secure_filename
from pathlib import Path
from flask import current_app as app

from project.models import getData, preprocessing, klasifikasi

ALLOWED_EXTENSIONS = {'dat'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Blueprint Configuration
router_bp = Blueprint('router_bp', __name__,
                    template_folder='templates')

@app.errorhandler(404)
def page_not_found(error):
    return render_template("notfound.html")

@router_bp.route('/', methods=['GET'])
def main():
    return redirect(url_for('router_bp.home'))

@router_bp.route('/home', methods=['GET'])
def home():
    modeln = Model("Masukkan Dua File (.dat) dan (.hea)", "Hasil Akan Ditampilkan disini")
    view = View()
    controller = Controller(modeln, view)
    return controller.update_view()

gloForm = ""
gloAuth = False

@router_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    view = View()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if 'file' in request.files:
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file((file.filename)):
                if len(request.files.getlist('file')) == 2:
                    for f in request.files.getlist('file'):
                        savePath = str(Path(__file__).parent.parent) + '\project/'+app.config['UPLOAD_FOLDER'] + '/' + \
                            secure_filename(f.filename)
                        f.save(savePath)
                elif len(request.files.getlist('file')) != 2:
                    flash('File harus berjumlah 2, format dat dan hea')
                    return redirect(request.url)
                global gloForm
                gloForm = file.filename[:-4]
                modelf = Model(gloForm, "")
                controller = Controller(modelf, view)
                return controller.update_view()
            else:
                flash('File yang dimasukkan Salah, format dat dan hea')
                return redirect(request.url)
    return redirect(url_for('router_bp.home'))

@router_bp.route('/progress', methods=['GET', 'POST'])
def progress_data():
    view = View()
    if request.method == 'POST':
        if 'preproc' in request.form:
            try:
                getData.fileattr(gloForm)
                preprocessing.progreSignal()
                preprocessing.showRes()
            except BaseException as e:
                flash('Error '+str(e))
                return redirect(request.url)
            res = "Berhasil melakukan Preprocessing"
            global gloAuth
            gloAuth = True
            modelf = Model(gloForm, res)
            controller = Controller(modelf, view)
            return controller.update_view()
        if 'clasi' in request.form and gloAuth:
            try:
                # res, acc, preci, recall, fscore = klasifikasi.progreKlasi()
                reskNN, resMkNN = klasifikasi.progreKlasi()
            except BaseException as e:
                flash('Error '+str(e))
                return redirect(request.url)
            modelf = Model(gloForm, reskNN, resMkNN)
            controller = Controller(modelf, view)
            return controller.update_view()
        elif 'clasi' in request.form and not gloAuth:
            flash("Lakukan preprocessing terlebih dahulu")
    return redirect(url_for('router_bp.home'))
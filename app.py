from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

user = 'root'
password = 'root'
host = 'localhost'
port = 3306
dbname = 'surabayapy'

db_uri = 'mysql+mysqldb://%s:%s@%s:%d/%s' % (user, password, host, port, dbname)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


def savedb(data):
    db.session.add(data)
    db.session.commit()

def waktu(data):
    return datetime.strptime(data, '%d %b %Y %H:%M')

daftar_hadir = db.Table('daftar_hadir',
    db.Column('kegiatan',db.Integer, db.ForeignKey('kegiatan.id'), index=True),
    db.Column('peserta',db.Integer, db.ForeignKey('anggota.id'), index=True),
)

class Anggota(db.Model):
    __table_args__ = {'extend_existing': True}  
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telegram = db.Column(db.String(64), unique=True, nullable=False)
    github = db.Column(db.String(15), unique=True, nullable=True)
    key = db.Column(db.String(4), unique=True, nullable=True)
    cari_kerja = db.Column(db.Boolean, nullable=False)
    tanggal_terdaftar = db.Column(db.DateTime, default=datetime.utcnow)
    ikut_serta = db.relationship('Kegiatan', secondary='daftar_hadir', backref=db.backref('peserta', lazy='dynamic'))

    def __repr__(self):
        return '<Anggota %r>' % self.telegram

class Kegiatan(db.Model):
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True)
    tema =  db.Column(db.Text, nullable=False)
    pembicara = db.Column(db.Text,  nullable=False)
    tempat = db.Column(db.Text,  nullable=False)
    maps = db.Column(db.String(80), nullable=True)
    waktu = db.Column(db.DateTime, nullable=False)
    pendaftaran = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Kegiatan %r>' % self.tema

# Belum difungsikan
class Lowongan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pengirim = db.Column(db.String(80), nullable=False)
    judul = db.Column(db.String(80),  nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return '<Lowongan %r>' % self.judul
    
db.create_all()


def registrasi_anggota(nama, email, telegram, github='', cari_kerja=False):
    try:
        anggota_baru = Anggota(nama=nama, email=email, telegram=telegram, github=github, cari_kerja=cari_kerja)
        savedb(anggota_baru)
        
        data= {
            'id' : anggota_baru.id,
            'nama' : anggota_baru.nama,
            'email' : anggota_baru.email,
            'telegram' : anggota_baru.telegram,
            'github' : anggota_baru.github,
            'cari_kerja' : anggota_baru.cari_kerja
        }
        return {'status': 'success', 'data': data}, 201
    
    except:
        db.session.rollback()
        return {'status': 'failed', 'data': 'Username, email, telegram atau github sudah digunakan'}, 400

    
def buat_kegiatan(tema, pembicara, tempat, maps, waktuacara, pendaftaran):
    try:
        kegiatan_baru = Kegiatan(tema = tema, pembicara = pembicara, tempat = tempat, maps = maps, waktu = waktu(waktuacara), pendaftaran = waktu(pendaftaran))
        savedb(kegiatan_baru)
        data= {
            'id' : kegiatan_baru.id,
            'tema' : kegiatan_baru.tema,
            'pembicara' : kegiatan_baru.pembicara,
            'tempat' : kegiatan_baru.tempat,
            'maps' : kegiatan_baru.maps,
            'waktu' : kegiatan_baru.waktu,
            'pendaftaran' : kegiatan_baru.pendaftaran
        }
        
        return {'status': 'success', 'data': data}, 201
    except:
        db.session.rollback()
        return {'status': 'failed', 'data': 'Kegiatan tidak dapat didaftarkan'}, 400


def kegiatan_peserta(anggota_telegram):
    try:
        anggota = Anggota.query.filter_by(telegram=anggota_telegram).first()
        info_anggota =[]
        for kegiatan in anggota.ikut_serta:
            data = {
                'id': kegiatan.id,
                'tema': kegiatan.tema,
                'pembicara': kegiatan.pembicara,
                'tempat': kegiatan.tempat,
                'maps': kegiatan.maps,
                'waktu': kegiatan.waktu
            }
            info_anggota.append(data)
        return {'status': 'success', 'data': info_anggota}, 200
    except:
        return {'status': 'failed', 'data': 'Not found'}, 404

def mendaftar_kegiatan(anggota_telegram, idkegiatan):
    try:
        anggota = Anggota.query.filter_by(telegram=anggota_telegram).first()
        kegiatan = Kegiatan.query.filter_by(id=idkegiatan).first()
        kegiatan.peserta.append(anggota)
        db.session.commit()
        response = kegiatan_peserta(anggota_telegram)
        return response[0], 201
    except:
        return {'status': 'failed', 'data': 'Not found'}, 404


def list_kegiatan(mode, idkegiatan=0):
    try:
        if mode == 'tema':
            daftar_kegiatan = []
            for kegiatan in Kegiatan.query:
                data = {
                    'tema' : kegiatan.tema,
                    'id' : kegiatan.id
                }
                daftar_kegiatan.append(data)
            return {'status': 'success', 'data': daftar_kegiatan}, 200
        
        elif mode == 'peserta':
            kegiatan = Kegiatan.query.filter_by(id=idkegiatan).first()
            daftar_peserta = []
            for peserta in kegiatan.peserta:
                daftar_peserta.append(peserta.telegram)
            return {'status': 'success', 'data': daftar_peserta}, 200
        
    except:
        return {'status': 'failed', 'data': 'Not found'}, 404

@app.route('/api/daftar-anggota/', methods=['POST'])
def api_daftar_anggota():
    if request.method == 'POST':
        parameter = ['nama', 'email', 'telegram', 'github']
        if not request.json or not set(parameter).issubset(request.json):
            response = {'status': 'failed', 'data': 'Bad Request'}, 400
        else:
            content = request.json
            response = registrasi_anggota(content["nama"], content["email"], content["telegram"], content["github"])
    return jsonify(response[0]), response[1]
    

@app.route('/api/buat-kegiatan/', methods=['POST'])
def api_buat_kegiatan():
    if request.method == 'POST':
        parameter = ['tema', 'pembicara', 'tempat', 'maps', 'waktu', 'pendaftaran']
        if not request.json or not set(parameter).issubset(request.json):
            response = {'status': 'failed', 'data': 'Bad Request'}, 400
        else:
            content = request.json
            response = buat_kegiatan(content["tema"], content["pembicara"], content["tempat"], content["maps"], content["waktu"], content["pendaftaran"])
    return jsonify(response[0]), response[1]
    

@app.route('/api/mendaftar-kegiatan/', methods=['POST'])
def api_mendaftar_kegiatan():
    if request.method == 'POST':
        parameter = ['anggota_telegram', 'idkegiatan']
        if not request.json or not set(parameter).issubset(request.json):
            response = {'status': 'failed', 'data': 'Bad Request'}, 400
        else:
            content = request.json
            response = mendaftar_kegiatan(content["anggota_telegram"], content["idkegiatan"])
    return jsonify(response[0]), response[1]
     

@app.route('/api/daftar-kegiatan/', methods=['GET'])
def api_kegiatan():
    if request.method == 'GET':
        response = list_kegiatan('tema')
    return jsonify(response[0]), response[1]
     

@app.route('/api/peserta-kegiatan/<int:idkegiatan>/', methods=['GET'])
def api_peserta_kegiatan(idkegiatan):
    if request.method == 'GET':
        response = list_kegiatan('peserta', idkegiatan)
    return jsonify(response[0]), response[1]
     

@app.route('/api/kegiatan/<idtelegram>/', methods=['GET'])
def api_kegiatan_idtelegram(idtelegram):
    if request.method == 'GET':
        response = kegiatan_peserta(idtelegram)
    return jsonify(response[0]), response[1]
     

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not  Found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Requesst'}), 404)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=False)


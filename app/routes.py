from app import app
from flask import jsonify
from flask import render_template, request, flash, redirect, url_for
from app.models import *
from app.forms import *
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import func
import json
from flask import render_template, request, flash, redirect, url_for, jsonify


@app.route("/")
def index():
    return render_template("index.html")


# ------------ signUpForm --------------
@app.route("/signUp_form", methods=["GET", "POST"])
def signUp_form():
    """form đăng kí"""
    form = signUpForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        full_name = form.full_name.data
        password = form.password.data
        NewUser = USER(user_name=user_name, full_name=full_name, password=password)
        NewUser.set_password(form.password.data)
        db.session.add(NewUser)
        db.session.commit()
        flash('Đăng kí thành công!')
        return redirect(url_for('index'))
    return render_template("signUp_form.html", form=form)


# ---------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = USER.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Tên đăng nhập hoặc mật khẩu không đúng!')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


# ---------- logout ----------------
@app.route('/logout')
def logout():
    """Đăng xuất"""
    logout_user()
    return redirect(url_for('index'))


# ------------ setAdmin --------------
@app.route('/setAdmin')
@login_required
def setAdmin():
    """Xét admin"""
    if current_user.is_admin == 1:
        users = USER.query.all()
        return render_template('setAdmin.html', users=users)
    else:
        flash('Bạn không có quyền truy cập!')
    return render_template("index.html")


@app.route('/setAdmin_s2/<int:id>')
def setAdmin_s2(id):
    user = USER.query.get(id)
    return render_template('setAdmin_s2.html', user=user)


@app.route('/setAdmin_s3', methods=['GET', 'POST'])
def setAdmin_s3():
    id = request.form.get('id')
    is_admin = request.form.get('is_admin')
    user = USER.query.get(id)
    user.is_admin = is_admin
    db.session.commit()
    message = "Xét Admin thành công!"
    return render_template('succes.html', message=message)


# -------------------addSHOP-----------------
@app.route("/insertCayXang_s1", methods=["GET"])
def insertCayXang_s1():
    """choose place to add Cay xang"""
    form = addCayXangForm()
    return render_template("insertCayXang_s1.html", form=form)


@app.route("/insertCayXang_result", methods=["POST"])
def insertCayXang_result():
    """add new cay xang"""
    # Get form information.
    name = request.form.get("name")
    img = request.form.get("img")
    time = request.form.get("time")
    address = request.form.get("address")
    geomInput = 'Point(' + request.form.get("lng") + " " + request.form.get("lat") + ")"
    newCayXang = CAYXANGPOINT(name=name, address=address, time=time, img=img, geom=func.ST_GeomFromText(geomInput, 4326))
    db.session.add(newCayXang)
    db.session.commit()
    message = "Thêm địa điểm thành công!"
    return render_template("succes.html", message=message)


@app.route("/api/v1/cayXangPoints")
def cayXangPoints_get_API():
    """Return feature in point table"""
    cayXangs = db.session.query(CAYXANGPOINT.id, CAYXANGPOINT.name, CAYXANGPOINT.time, CAYXANGPOINT.address, CAYXANGPOINT.img, \
    func.ST_AsGeoJSON(CAYXANGPOINT.geom).label('geometry')).all()
    # Get all daily flights.
    cayXangFeatures = []  # store all shop
    for cayXang in cayXangs:  # generate geojson for each shop
        cayXang_temp = {}
        cayXang_temp["type"] = "Feature"
        cayXang_temp["properties"] = {
            "id": cayXang.id,
            "name": cayXang.name,
            "time": cayXang.time,
            "img": cayXang.img,
            "address": cayXang.address,
        }
        cayXang_temp["geometry"] = json.loads(cayXang.geometry)
        cayXangFeatures.append(cayXang_temp)  # add shop geojson to list

    return jsonify({  # convert to geojson format
            "features": cayXangFeatures
        })


@app.route("/deleteCayXang", methods=['POST'])
def deleteCayXang():
    id = request.form.get('id')
    cayXang = CAYXANGPOINT.query.get(id)
    db.session.delete(cayXang)
    db.session.commit()
    message = "Xóa thành công!"
    return render_template("succes.html", message=message)


@app.route("/api/v1/CAYXANG/<int:id>")
def updateCayXang_s1(id):
    cayXang = db.session.query(CAYXANGPOINT.id, CAYXANGPOINT.name, CAYXANGPOINT.address, CAYXANGPOINT.time, CAYXANGPOINT.img, \
    func.ST_AsGeoJSON(CAYXANGPOINT.geom).label('geometry')).filter_by(id=id).first()
    cayXangFeatures = []
    cayXang_temp = {}
    cayXang_temp["type"] = "Feature"
    cayXang_temp["properties"] = {
        "id": cayXang.id,
        "name": cayXang.name,
        "time": cayXang.time,
        "img": cayXang.img,
        "address": cayXang.address,
    }
    cayXang_temp["geometry"] = json.loads(cayXang.geometry)
    cayXangFeatures.append(cayXang_temp)  # add shop geojson to list

    return jsonify({  # convert to geojson format
            "features": cayXangFeatures
        })


@app.route("/updateCayXang_s2", methods=['POST'])
def updateCayXang_s2():
    id = request.form.get('id')
    return render_template("updateCayXang.html", id=id)


@app.route("/updateCayXang_s3", methods=['POST'])
def updateCayXang_s3():
    id = request.form.get('id')
    address = request.form.get('address')
    name = request.form.get('name')
    time = request.form.get('time')
    img = request.form.get('img')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    geomInput = 'Point(' + request.form.get("lng") + " " + request.form.get("lat") + ")"
    cayXang = CAYXANGPOINT.query.get(id)
    cayXang.address = address
    cayXang.name = name
    cayXang.time = time
    cayXang.img = img
    cayXang.geom = func.ST_GeomFromText(geomInput, 4326)
    db.session.commit()
    message = "Cập nhật thành công!"
    return render_template("succes.html", message=message)


# @app.route("/api/v1/District")
# def get_api_District():
#     Districts = db.session.query(BOUNDARY.id, BOUNDARY.name, \
#     func.ST_AsGeoJSON(BOUNDARY.geom).label('geometry')).all()
#     DistrictFeatures = []  # store all shop
#     for District in Districts:  # generate geojson for each shop
#         District_temp = {}
#         District_temp["type"] = "Feature"
#         District_temp["properties"] = {
#             "id": District.id,
#             "name": District.name,
#         }
#         District_temp["geometry"] = json.loads(District.geometry)
#         DistrictFeatures.append(District_temp)  # add shop geojson to list

#     return jsonify({  # convert to geojson format
#             "features": DistrictFeatures
#         })

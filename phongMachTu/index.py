from flask import render_template, request, flash, redirect, session, jsonify
import dao, utils
from phongMachTu.models import UserRoleEnum
from phongMachTu import app, login
from flask_login import login_user, logout_user



@app.route("/")
def home():
    return render_template('index.html', vaiTro = None, userRole = None)



@app.route("/user-login", methods=["POST", "GET"])
def user_login():
    if request.method.__eq__("POST"):
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        user = dao.auth_user(username=uname, password=pwd)
        if user:
            login_user(user)
            if user.vaiTro == UserRoleEnum.DOCTOR:
                return redirect("/doctor") #trả về trang doctor
            elif user.vaiTro == UserRoleEnum.NURSE :
                return redirect("/") #trả về trang nurse
            elif user.vaiTro == UserRoleEnum.STAFF :
                return redirect("/") #trả về trang staff
        else:
            flash("Sai tên đăng nhập / mật khẩu", category="error")
    return render_template("login.html")


@app.route("/user-logout", methods=["POST", "GET"])
def sign_out():
        logout_user()
        return redirect("/")


@app.route("/lap-phieu-kham", methods = ['post', 'get'])
def lap_phieu_kham():
    thuocs = []
    session['thuoc'] ={}
    for t in dao.get_thuoc():
        thuocs.append(t.ten)
    if request.method.__eq__('POST'):
        for i in range(request.form.getlist('cachDung').__len__()):
            dao.add_phieu_kham(hoTen=request.form.get('hoTen'), ngayKham=request.form.get('ngayKham')
                               , trieuChung=request.form.get('trieuChung'), duDoanBenh=request.form.get('duDoan')
                               , tenThuoc=request.form.getlist('tenThuoc')[i], soLuong=request.form.getlist('soLuong')[i]
                               , cachDung=request.form.getlist('cachDung')[i])
    return render_template("lap_phieu_kham.html", vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum
                           ,thuocs = thuocs)


@app.route("/api/lap-phieu-kham", methods=['post'])
def addThuoc():
    data = request.json
    id = str(data['id'])
    ten = []

    for t in dao.get_thuoc():
        ten.append(t.ten)

    # ten = data['ten']
    # donVi = data['donVi']
    thuoc = session.get('thuoc')


    thuoc[id] = {
        "id": id,
        "ten": ten,
    }

    session['thuoc'] = thuoc
    print(session["thuoc"])
    return jsonify()



@app.route("/api/lap-phieu-kham/<thuoc_id>", methods=['delete'])
def delete_cart(thuoc_id):
    thuoc = session.get('thuoc')
    if thuoc and thuoc_id in thuoc:
        del thuoc[thuoc_id]

    session['thuoc'] = thuoc
    return jsonify()


@app.route("/doctor")
def doctor():
    # session.pop('thuoc', default=None)
    return render_template("doctor.html", vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum)


@app.route("/tra-cuu-thuoc")
def tra_cuu_thuoc():
    return render_template("tra_cuu_thuoc.html",vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum)


@login.user_loader
def load_user(user_id):
    return dao.get_nguoiDung_by_id(user_id)


@app.route("/admin/login", methods=["post"])
def login_admin():
    username = request.form.get("admname")
    password = request.form.get("admpwd")
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)
    return redirect("/admin")





if __name__ == '__main__':
    from phongMachTu import admin
    app.run(debug=True)
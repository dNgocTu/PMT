from flask import render_template, request, flash, redirect, session, jsonify
import dao
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
        session.clear()
        return redirect("/")


@app.route("/lap-phieu-kham", methods = ['post', 'get'])
def lap_phieu_kham():
    if session.get('thuoc') is None:
        session['thuoc'] = {}
    if session.get('id') is None:
        session['id'] = 1
    thuocs = []
    for t in dao.get_thuoc():
        thuocs.append(t.ten)
    if request.method.__eq__('POST'):
        if dao.get_benhNhan_by_ten(request.form.get('hoTen')):
            try:
                for i in range(request.form.getlist('cachDung').__len__()):
                    dao.add_phieu_kham(hoTen=request.form.get('hoTen'), ngayKham=request.form.get('ngayKham')
                                       , trieuChung=request.form.get('trieuChung'), duDoanBenh=request.form.get('duDoan')
                                       , nguoiDung_id=request.form.get("doctorID"), tenThuoc=request.form.getlist('tenThuoc')[i]
                                       , soLuong=request.form.getlist('soLuong')[i], cachDung=request.form.getlist('cachDung')[i])
                    if session.get('thuoc'):
                        session['thuoc'].clear()
                    if session.get('id'):
                        session.pop('id')
            except Exception as ex:
                err_msg = str(ex)
                flash(err_msg, category="error")
            else:
                flash("Lưu thành công", category="success")
        else:
            flash("Lưu thất bại", category="error")
    return render_template("lap_phieu_kham.html", vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum
                           ,thuocs = thuocs)


@app.route("/api/lap-phieu-kham", methods=['post'])
def addThuoc():
    thuoc = session.get('thuoc')
    id = session.get('id')
    data = request.json

    ten = []

    for t in dao.get_thuoc():
        ten.append(t.ten)

    thuoc[str(id)] = {
        "id": str(id),
        "ten": ten,
    }

    session['thuoc'] = thuoc
    session['id'] = id + 1
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
    if session.get('thuoc'):
        session['thuoc'].clear()
    if session.get('id'):
        session.pop('id')
    return render_template("doctor.html", vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum)


@app.route("/tra-cuu-thuoc")
def tra_cuu_thuoc():
    if session.get('thuoc'):
        session['thuoc'].clear()
    if session.get('id'):
        session.pop('id')
    kw = request.args.get("kw")
    thuoc = dao.search_thuoc_by_name(kw)
    donViThuoc = dao.get_donViThuoc()
    return render_template("tra_cuu_thuoc.html",vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum
                           , thuoc = thuoc, donViThuoc=donViThuoc)


@app.route("/xem-lich-su-benh")
def xem_lich_su_benh():
    kw = request.args.get("kw")
    benhNhan = dao.get_benhNhan_thuoc_by_tenBenhNhan(kw)

    return render_template("xem_lich_su_benh.html",vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum
                           , benhNhan=benhNhan)


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
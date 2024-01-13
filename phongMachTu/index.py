import math
from datetime import datetime, date

from flask import render_template, request, flash, redirect, session, jsonify
import dao
from phongMachTu.models import UserRoleEnum
from phongMachTu import app, login
from flask_login import login_user, logout_user
from sqlalchemy.sql.expression import false


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
                return redirect("/nurse") #trả về trang nurse
            elif user.vaiTro == UserRoleEnum.STAFF :
                return redirect("/staff") #trả về trang staff
        else:
            flash("Sai tên đăng nhập / mật khẩu", category="error")
    return render_template("login.html")


@app.route("/user-logout", methods=["POST", "GET"])
def sign_out():
        logout_user()
        session.clear()
        return redirect("/")


@app.route("/doctor")
def doctor():
    if session.get('thuoc'):
        session['thuoc'].clear()
    if session.get('id'):
        session.pop('id')
    return render_template("doctor.html", vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum)


@app.route("/doctor/lap-phieu-kham", methods=['post', 'get'])
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
                    dao.add_phieuKham_info(hoTen=request.form.get('hoTen'), ngayKham=request.form.get('ngayKham')
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


@app.route("/api/doctor/lap-phieu-kham", methods=['post'])
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
    # print(session["thuoc"])
    return jsonify()



@app.route("/api/doctor/lap-phieu-kham/<thuoc_id>", methods=['delete'])
def delete_cart(thuoc_id):
    thuoc = session.get('thuoc')
    if thuoc and thuoc_id in thuoc:
        del thuoc[thuoc_id]

    session['thuoc'] = thuoc
    return jsonify()


@app.route("/doctor/tra-cuu-thuoc", methods=['get'])
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


@app.route("/doctor/xem-lich-su-benh", methods=['get'])
def xem_lich_su_benh():
    kw = request.args.get("kw")
    # Lấy danh sach join giữa benhNhan Va phieukhambenh
    lichSuBenh = dao.get_lich_su_benh(kw)
    return render_template("xem_lich_su_benh.html",vaiTro = UserRoleEnum.DOCTOR, userRole = UserRoleEnum
                           , lichSuBenh=lichSuBenh)


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


@app.route("/staff", methods=['get', 'post'])
def staff():
    kw = request.args.get("kw")
    page = request.args.get("page")
    page_size = app.config["PAGE_SIZE"]
    if kw == "" or kw is None:
        if page == None:
            page = 1
        hoaDonChuaThanhToan = dao.get_hoaDon_by_state(kw, page, "False")
    else:
        page = None
        hoaDonChuaThanhToan = dao.get_hoaDon_by_state(kw, page, "False")
    num = dao.count_hoaDon_by_state("False")

    return render_template("staff.html", vaiTro=UserRoleEnum.STAFF, userRole = UserRoleEnum
                           , hoaDons=hoaDonChuaThanhToan, pages=math.ceil(num / page_size), kw=kw)


@app.route("/api/staff/thanh-toan-hoa-don/<hoaDon_id>", methods=["put"])
def add_to_cart(hoaDon_id):
    try:
        dao.set_trangThai_hoaDon(hoaDon_id, True)
    except:
        return jsonify({'status': 500, 'err_msg': "Something wrong"})
    else:
        return jsonify({'status': 200})


@app.route("/staff/hoa-don-da-thanh-toan")
def hoa_don_da_thanh_toan():
    kw = request.args.get("kw")
    page = request.args.get("page")
    page_size = app.config["PAGE_SIZE"]
    if page == None:
        page = 1
    hoaDonDaThanhToan = dao.get_hoaDon_by_state(kw, page, "True")
    num = dao.count_hoaDon_by_state("True")

    return render_template("hoa_don_da_thanh_toan.html", vaiTro=UserRoleEnum.STAFF, userRole=UserRoleEnum
                           , hoaDons=hoaDonDaThanhToan, pages=math.ceil(num / page_size))


@app.route('/nurse', methods=['GET', 'POST'])
def book_form():
    err_msg = ""
    dskb = dao.get_danhSachKhamBenh()
    nguoiDung_id = session.get('user_id')
    if request.method == 'POST':
        ten = request.form.get('hoTen')
        gioiTinh = request.form.get('gioiTinh')
        namSinh = request.form.get('namSinh')
        diaChi = request.form.get('diaChi')
        sdt = request.form.get('SDT')
        kb_id = request.form.get('dskb')
        ngayDangKy = dao.get_ngayKham_by_id(kb_id)
        soLuongBenhNhan = dao.check_so_luong_kham(kb_id)

        if soLuongBenhNhan < int(dao.get_quyDinh_by_ten("So luong benh nhan mot ngay").giaTri):
            dao.add_lichKham(ten=ten, gioiTinh=gioiTinh, namSinh=namSinh, ngayDangKy=ngayDangKy
                             , sdt=sdt, nguoiDung_id=nguoiDung_id, kb_id=kb_id)
            dao.add_benhNhan(ten=ten, gioiTinh=gioiTinh, namSinh=namSinh, diaChi=diaChi, sdt=sdt)
            return render_template('nurse.html',vaiTro=UserRoleEnum.NURSE, userRole = UserRoleEnum
                                   , soLuongBenhNhan=soLuongBenhNhan, kb_id=kb_id)
        else:
            err_msg = "Danh sách khám này đã đầy"

    return render_template('nurse.html', vaiTro=UserRoleEnum.NURSE, userRole = UserRoleEnum
                           , dskb=dskb, err_msg=err_msg, )

@app.route('/nurse/tao-lich-kham', methods=['GET', 'POST'])
def tao_lichKham():
    err_msg = ""
    dskb = dao.get_danhSachKhamBenh()
    flat = True
    if request.method == 'POST':
        ngayKham = request.form.get('ngayKham')
        for ds in dskb:
            if ds.ngayKham.strftime('%Y-%m-%d') == ngayKham:
                flat = False
                break

        if flat:
            dao.add_danhSachKham(ngayKham)

            return render_template('tao_lich_kham.html', vaiTro=UserRoleEnum.NURSE, userRole=UserRoleEnum)
        else:
            err_msg = "Lịch ngày khám " + datetime.strptime(ngayKham, '%Y-%m-%d').strftime('%d-%m-%Y') + " này đã tồn tại, vui lòng tạo lịch với 1 ngày khác"

    return render_template('tao_lich_kham.html', vaiTro=UserRoleEnum.NURSE, userRole = UserRoleEnum
                           , err_msg=err_msg)



if __name__ == '__main__':
    from phongMachTu import admin
    app.run(debug=True)
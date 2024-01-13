from flask import session
from sqlalchemy import func

from phongMachTu.models import *
from phongMachTu import app, db
import hashlib
from sqlalchemy.sql.expression import false, true

def get_thuoc():
    return Thuoc.query.all()

def search_thuoc_by_name(thuoc_ten):
    thuocs = get_Thuoc_by_ten(thuoc_ten)
    if thuoc_ten:
        thuocs = Thuoc.query.filter(Thuoc.ten.contains(thuoc_ten)).all()
    return thuocs


def get_donViThuoc():
    return DonViThuoc.query.all()


def get_nguoiDung_by_id(user_id):
    return NguoiDung.query.filter(NguoiDung.id.__eq__(user_id)).first()


def get_benhNhan_by_id(benhNhan_id):
    return BenhNhan.query.filter(BenhNhan.id.__eq__(benhNhan_id)).first()


def get_benhNhan_by_ten(benhNhan_ten):
    return BenhNhan.query.filter(BenhNhan.ten.__eq__(benhNhan_ten)).first()


def get_Thuoc_by_ten(thuoc_ten):
    return Thuoc.query.filter(Thuoc.ten.__eq__(thuoc_ten)).first()


def get_benhNhan():
    return BenhNhan.query.all()


def get_benhNhan_thuoc_by_tenBenhNhan(ten_benh_nhan):
    return db.session.query(BenhNhan.ten.label("tenBenhNhan")
                            , BenhNhan.namSinh.label("namSinh")
                            , BenhNhan.gioiTinh.label("gioiTinh")
                            , BenhNhan.sdt.label("sdt")
                            , PhieuKhamBenh.ngayLap.label("ngayKham")
                            , Thuoc.ten.label("tenThuoc"))\
            .join(PhieuKhamBenh, PhieuKhamBenh.benhNhan_id.__eq__(BenhNhan.id))\
            .join(ChiTietToaThuoc, ChiTietToaThuoc.phieuKhamBenh_id.__eq__(PhieuKhamBenh.id))\
            .join(Thuoc, ChiTietToaThuoc.thuoc_id.__eq__(Thuoc.id))\
            .filter(BenhNhan.ten.__eq__(ten_benh_nhan))\
            .all()


def get_phieuKhamBenh_by_id(phieuKhamBenh_id):
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.id.__eq__(phieuKhamBenh_id)).first()


def get_quyDinh_by_ten(quyDinh_ten):
    quyDinh = None
    if quyDinh_ten:
        quyDinh = QuyDinh.query.filter(QuyDinh.ten.contains(quyDinh_ten)).first()
    return quyDinh


def add_phieuKham_info(hoTen, ngayKham, trieuChung, duDoanBenh, nguoiDung_id, tenThuoc, soLuong, cachDung):
    phieuKham = PhieuKhamBenh(ten="PhieuKham " + ngayKham + " " + hoTen, ngayLap=ngayKham
                               , trieuChung=trieuChung, duDoanBenh=duDoanBenh
                               , nguoiDung_id=nguoiDung_id, benhNhan_id=get_benhNhan_by_ten(hoTen).id)
    db.session.add(phieuKham)
    db.session.commit()
    chiTietToaThuoc = ChiTietToaThuoc(cachDung=cachDung, soLuong=soLuong
                                    , thuoc_id=get_Thuoc_by_ten(tenThuoc).id, phieuKhamBenh_id=phieuKham.id)
    db.session.add(chiTietToaThuoc)
    db.session.commit()
    # Join thì trước khi so sánh phải kết nối với bảng đó trước
    thuoc_phieuKham = (db.session.query(Thuoc.donGia.label("donGia"), ChiTietToaThuoc.soLuong.label("soLuong"))
                       .join(ChiTietToaThuoc, ChiTietToaThuoc.thuoc_id.__eq__(Thuoc.id))
                       .join(PhieuKhamBenh, ChiTietToaThuoc.phieuKhamBenh_id.__eq__(PhieuKhamBenh.id))
                       .filter(PhieuKhamBenh.id.__eq__(phieuKham.id))).all()
    tienThuoc = 0
    for tp in thuoc_phieuKham:
        tienThuoc += tp.donGia * int(tp.soLuong)
    add_hoaDon(ngayKham=ngayKham, tienThuoc=tienThuoc, nguoiDung_id=nguoiDung_id, phieuKhamBenh_id=phieuKham.id)


def add_hoaDon(ngayKham, tienThuoc, nguoiDung_id, phieuKhamBenh_id):
    trangThai = False
    baoHiem = False
    benhNhan_id = get_phieuKhamBenh_by_id(phieuKhamBenh_id).benhNhan_id
    tienKham = float(get_quyDinh_by_ten("tien kham").giaTri)
    ten = "HoaDon " + ngayKham + " " + get_benhNhan_by_id(benhNhan_id).ten

    hoaDon = HoaDon(ten=ten, ngayKham=ngayKham, tienThuoc=tienThuoc, tienKham=tienKham, baoHiem=baoHiem
                    , trangThai=trangThai, nguoiDung_id=nguoiDung_id, phieuKhamBenh_id=phieuKhamBenh_id)
    db.session.add(hoaDon)
    db.session.commit()


def get_lich_su_benh(tenBenhNhan):
    lsb = (db.session.query(BenhNhan.ten.label('tenBenhNhan')
                            , BenhNhan.gioiTinh.label('gioiTinh')
                            , BenhNhan.namSinh.label('namSinh')
                            , BenhNhan.sdt.label('sdt')
                            , PhieuKhamBenh.ngayLap.label('ngayKham')
                            , PhieuKhamBenh.duDoanBenh.label('duDoanBenh'))
           .join(PhieuKhamBenh, PhieuKhamBenh.benhNhan_id.__eq__(BenhNhan.id))
           .distinct()
           .filter(BenhNhan.ten.__eq__(tenBenhNhan))
           .all())
    return lsb


def count_hoaDon():
    return HoaDon.query.count()


def count_hoaDon_by_state(state):
    hoaDons = HoaDon.query
    if state == "False":
        hoaDons = hoaDons.filter(HoaDon.trangThai.__eq__(false()))
    else: # Nếu state = True
        hoaDons = hoaDons.filter(HoaDon.trangThai.__eq__(true()))

    return hoaDons.count()

def get_hoaDon_by_id(hoaDon_id):
    return HoaDon.query.filter(HoaDon.id.__eq__(hoaDon_id)).first()


def get_hoaDon_by_state(kw,  page, state):
    hoaDons = HoaDon.query
    if kw:
        hoaDons = hoaDons.filter(HoaDon.ten.contains(kw))
    if state == "False":
        hoaDons = hoaDons.filter(HoaDon.trangThai.__eq__(false()))
    else: # Nếu state = True
        hoaDons = hoaDons.filter(HoaDon.trangThai.__eq__(true()))
    if page:
        page = int(page)
    else:
        return hoaDons.all()
    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size

    return hoaDons.slice(start, start + page_size)


def set_trangThai_hoaDon(hoaDon_id, trangThai):
    get_hoaDon_by_id(hoaDon_id).trangThai = trangThai
    db.session.commit()


def get_danhSachKhamBenh():
    return DanhSachKhamBenh.query.all()

def get_ngayKham_by_id(id):
    return DanhSachKhamBenh.query.filter(DanhSachKhamBenh.id.__eq__(id)).first().ngayKham


def check_so_luong_kham(id):
    patient_count = db.session.query(func.count(DanhSachDangKy.id)). \
        join(DanhSachKhamBenh, DanhSachDangKy.danhSachKhamBenh_id == DanhSachKhamBenh.id). \
        filter(DanhSachKhamBenh.id == id).scalar()

    return patient_count


def add_lichKham(ten, gioiTinh, namSinh, ngayDangKy, sdt, nguoiDung_id, kb_id):
    dsdk = DanhSachDangKy(ten=ten, gioiTinh=gioiTinh, namSinh=namSinh, sdt=sdt
                          , ngayDangKy=ngayDangKy, nguoiDung_id=nguoiDung_id, danhSachKhamBenh_id=kb_id)
    db.session.add(dsdk)
    db.session.commit()


def add_benhNhan(ten, gioiTinh, namSinh, diaChi, sdt):
    benhNhan = BenhNhan(ten=ten, gioiTinh=gioiTinh, namSinh=namSinh, diaChi=diaChi, sdt=sdt)
    db.session.add(benhNhan)
    db.session.commit()


def add_danhSachKham(ngayKham):
    danhSachKham = DanhSachKhamBenh(ngayKham=ngayKham)
    db.session.add(danhSachKham)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    return NguoiDung.query.filter(NguoiDung.taiKhoan.__eq__(username),
                                  NguoiDung.matKhau.__eq__(password)).first()


if __name__ == "__main__":
    with app.app_context():
        print()
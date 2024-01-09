from flask import session

from phongMachTu.models import *
from phongMachTu import app, db
import hashlib


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
    return NguoiDung.query.get(user_id)


def get_benhNhan_by_id(benhNhan_id):
    return BenhNhan.query.get(benhNhan_id)



def get_benhNhan_by_ten(benhNhan_ten):
    return BenhNhan.query.filter(BenhNhan.ten.__eq__(benhNhan_ten)).first()


def get_Thuoc_by_ten(thuoc_ten):
    return Thuoc.query.filter(Thuoc.ten.__eq__(thuoc_ten)).first()


def get_benhNhan_thuoc_by_tenBenhNhan(ten_benh_nhan):
    return db.session.query(BenhNhan.ten.label("tenBenhNhan")
                            , BenhNhan.namSinh.label("namSinh")
                            , BenhNhan.gioiTinh.label("gioiTinh")
                            , PhieuKhamBenh.ngayLap.label("ngayKham")
                            , Thuoc.ten.label("tenThuoc"))\
            .join(PhieuKhamBenh, PhieuKhamBenh.benhNhan_id.__eq__(BenhNhan.id))\
            .join(ChiTietToaThuoc, ChiTietToaThuoc.phieuKhamBenh_id.__eq__(PhieuKhamBenh.id))\
            .join(Thuoc, ChiTietToaThuoc.thuoc_id.__eq__(Thuoc.id))\
            .filter(BenhNhan.ten.__eq__(ten_benh_nhan))\
            .all()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    return NguoiDung.query.filter(NguoiDung.taiKhoan.__eq__(username),
                             NguoiDung.matKhau.__eq__(password)).first()



def add_phieu_kham(hoTen, ngayKham, trieuChung, duDoanBenh, nguoiDung_id, tenThuoc, soLuong, cachDung):
    phieuKham1 = PhieuKhamBenh(ten="PhieuKham" + ngayKham, ngayLap=ngayKham
                               , trieuChung=trieuChung, duDoanBenh=duDoanBenh
                               , nguoiDung_id=nguoiDung_id, benhNhan_id=get_benhNhan_by_ten(hoTen).id)
    db.session.add(phieuKham1)
    db.session.commit()
    chiTietToaThuoc = ChiTietToaThuoc(cachDung=cachDung, soLuong=soLuong
                                       , thuoc_id=get_Thuoc_by_ten(tenThuoc).id, phieuKhamBenh_id=phieuKham1.id)
    db.session.add(chiTietToaThuoc)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        print(get_benhNhan_thuoc_by_tenBenhNhan("Nguyen Van B"))
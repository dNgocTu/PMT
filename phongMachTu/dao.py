from phongMachTu.models import *
from phongMachTu import app, db
import hashlib


def get_thuoc():
    return Thuoc.query.all()

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

def get_tenDonViThuoc_by_id(donVi_id):
    return DonViThuoc.query.get(donVi_id).donVi

def auth_user(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    return NguoiDung.query.filter(NguoiDung.taiKhoan.__eq__(username),
                             NguoiDung.matKhau.__eq__(password)).first()



def add_phieu_kham(hoTen, ngayKham, trieuChung, duDoanBenh, tenThuoc, soLuong, cachDung):
    phieuKham1 = PhieuKhamBenh(ten="PhieuKham1", ngayLap=ngayKham, trieuChung=trieuChung, duDoanBenh=duDoanBenh
                               ,benhNhan_id=get_benhNhan_by_ten(hoTen).id)
    phieuKham1_id = phieuKham1.id
    chiTietToaThuoc1 = ChiTietToaThuoc(cachDung=cachDung, soLuong=soLuong, thuoc_id = get_Thuoc_by_ten(tenThuoc).id
                                       , phieuKhamBenh_id=phieuKham1_id)


    db.session.add_all([phieuKham1, chiTietToaThuoc1])
    db.session.commit()

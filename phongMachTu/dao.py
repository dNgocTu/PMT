from flask import session

from phongMachTu.models import *
from phongMachTu import app, db
import hashlib
from sqlalchemy import func


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


def get_phieuKhamBenh_by_date(phieuKham_date):
    phieuKham_date = datetime.strptime(phieuKham_date, "%Y-%m-%d")
    return PhieuKhamBenh.query.filter(PhieuKhamBenh.ngayLap.__eq__(phieuKham_date)).first()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    return NguoiDung.query.filter(NguoiDung.taiKhoan.__eq__(username),
                                  NguoiDung.matKhau.__eq__(password)).first()


def add_phieu_kham(hoTen, ngayKham, trieuChung, duDoanBenh, tenThuoc, soLuong, cachDung):
    phieu = get_phieuKhamBenh_by_date(ngayKham)
    phieuKham1 = phieu
    if get_benhNhan_by_ten(hoTen):
        if phieu == None or phieu.benhNhan_id != get_benhNhan_by_ten(hoTen).id:
            phieuKham1 = PhieuKhamBenh(ten="PhieuKham" + ngayKham, ngayLap=ngayKham
                                       , trieuChung=trieuChung, duDoanBenh=duDoanBenh
                                       , benhNhan_id=get_benhNhan_by_ten(hoTen).id)
            db.session.add(phieuKham1)
            db.session.commit()
        chiTietToaThuoc = ChiTietToaThuoc(cachDung=cachDung, soLuong=soLuong
                                          , thuoc_id=get_Thuoc_by_ten(tenThuoc).id, phieuKhamBenh_id=phieuKham1.id)
        db.session.add(chiTietToaThuoc)
        db.session.commit()


# Thống kê theo tháng
def thong_ke_01(thang=None):
    ket_qua = (HoaDon.query
               .join(PhieuKhamBenh, HoaDon.phieuKhamBenh_id == PhieuKhamBenh.id)
               .join(BenhNhan, PhieuKhamBenh.benhNhan_id == BenhNhan.id)
               .with_entities(
        # Đổi tên cột cho rõ ràng
        func.date(PhieuKhamBenh.ngayLap).label('ngayKham'),
        func.count(BenhNhan.id).label('SoBenhNhan'),
        func.sum(HoaDon.tienThuoc + HoaDon.tienKham).label('doanhThu'),
    ).group_by(PhieuKhamBenh.ngayLap).all())

    if thang:
        ket_qua = (HoaDon.query
                   .join(PhieuKhamBenh, HoaDon.phieuKhamBenh_id == PhieuKhamBenh.id)
                   .join(BenhNhan, PhieuKhamBenh.benhNhan_id == BenhNhan.id)
                   .filter(func.extract('month', PhieuKhamBenh.ngayLap) == thang)
                   .with_entities(
            # Đổi tên cột cho rõ ràng
            func.date(PhieuKhamBenh.ngayLap).label('ngayKham'),
            func.count(BenhNhan.id).label('SoBenhNhan'),
            func.sum(HoaDon.tienThuoc + HoaDon.tienKham).label('doanhThu'),
        ).group_by(PhieuKhamBenh.ngayLap).all())

    return ket_qua


def thong_ke_02(thang=None):
    result = db.session.query(
        Thuoc.id.label('thuoc_id'),
        Thuoc.ten.label('tenThuoc'),
        DonViThuoc.donVi.label('tenDonViTinh'),
        func.sum(Thuoc.soLuong).label('soLuongThuoc')
    ).join(
        Thuoc, Thuoc.donVi_id == DonViThuoc.id
    ).group_by(
        Thuoc.id, Thuoc.soLuong, Thuoc.ten
    ).all()

    return result


if __name__ == '__main__':
    with app.app_context():
        print(thong_ke_02())
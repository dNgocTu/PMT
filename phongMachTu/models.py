from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from phongMachTu import db, app
from flask_login import UserMixin
from datetime import datetime
import enum, hashlib


class UserRoleEnum(enum.Enum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    STAFF = 4


class QuyDinh(db.Model):
    ma = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    giaTri = Column(String(50), nullable=True)



class NguoiDung(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    ngaySinh = Column(DateTime, default=datetime(1890, 1, 1, 18, 23))  # yyyy-mm-dd hh-mm
    taiKhoan = Column(String(50), nullable=False, unique=True)
    matKhau = Column(String(150), nullable=False)
    vaiTro = Column(Enum(UserRoleEnum))
    danhSachDangKy = relationship("DanhSachDangKy", backref="nguoiDung", lazy=True)
    phieuKhamBenh = relationship("PhieuKhamBenh", backref="nguoiDung", lazy=True)
    hoaDon = relationship("HoaDon", backref="nguoiDung", lazy=True)

class DanhSachKhamBenh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(DateTime, default=datetime.now())  # yyyy-mm-dd
    danhSachDangKy = relationship("DanhSachDangKy", backref="danhSachKhamBenh", lazy=True)


class DanhSachDangKy(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    gioiTinh = Column(String(10), nullable=True)
    namSinh = Column(DateTime, default=datetime(1890, 1, 1, 18, 23))# yyyy-mm-dd hh-mm
    sdt = Column(String(20), nullable=True)
    ngayDangKy = Column(DateTime, default=datetime.now())
    danhSachKhamBenh_id = Column(Integer, ForeignKey(DanhSachKhamBenh.id), nullable=True)
    nguoiDung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=True)


class BenhNhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    gioiTinh = Column(String(10), nullable=True)
    namSinh = Column(DateTime, default=datetime(1890, 1, 1, 18, 23))#  yyyy-mm-dd hh-mm
    diaChi = Column(String(100), nullable=True)
    sdt = Column(String(20), nullable=True)
    phieuKhamBenh = relationship("PhieuKhamBenh", backref="benhNhan", lazy=True)


class PhieuKhamBenh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    ngayLap = Column(DateTime, default=datetime.now())# yyyy-mm-dd
    trieuChung = Column(String(100), nullable=True)
    duDoanBenh = Column(String(200), nullable=True)
    nguoiDung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=True)
    benhNhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=True)
    hoaDon = relationship("HoaDon", backref="phieuKhamBenh", lazy=True)
    chiTietToaThuoc = relationship("ChiTietToaThuoc", backref="phieuKhamBenh", lazy=True  )


class HoaDon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    ngayKham = Column(DateTime, default=datetime.now())# yyyy-mm-dd
    tienThuoc = Column(Float, nullable=True)
    tienKham = Column(Float, nullable=True)
    baoHiem = Column(String(50), nullable=True)
    trangThai = Column(Boolean, default=False)
    nguoiDung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=True)
    phieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=True)


class DonViThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    donVi = Column(String(50), nullable=True)
    thuoc = relationship("Thuoc", backref="don_vi_thuoc", lazy=True)
    def __str__(self):
        return self.donVi




class ChiTietToaThuoc(db.Model):
    __tablename__ = 'chi_tiet_toa_thuoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cachDung = Column(String(100), nullable=True)
    soLuong = Column(Integer, nullable=True)
    thuoc_id = Column(Integer, ForeignKey('thuoc.id', ondelete='CASCADE'), nullable=False)
    phieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id, ondelete='CASCADE'), nullable=False)



#Thuoc_LoaiThuoc
class ChiTietLoaiThuoc(db.Model):
    __tablename__ = 'chi_tiet_loai_thuoc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    thuoc_id = Column(Integer, ForeignKey('thuoc.id', ondelete='CASCADE'), nullable=False)
    loaiThuoc_id = Column(Integer, ForeignKey("loai_thuoc.id", ondelete='CASCADE'), nullable=False)



class LoaiThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    chiTietLoaiThuoc = relationship("ChiTietLoaiThuoc", backref="loai_thuoc", lazy=True  )



class Thuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    donGia = Column(Float, nullable=True)
    soLuong = Column(Integer, nullable=True)
    ngaySX = Column(DateTime)  # yyyy-mm-dd
    hanSD = Column(DateTime)  # yyyy-mm-dd
    image =  Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
    comments = relationship('Comment', backref='thuoc', lazy=True)
    donVi_id = Column(Integer, ForeignKey(DonViThuoc.id), nullable=True)
    chiTietLoaiThuoc = relationship("ChiTietLoaiThuoc", backref="thuoc", lazy=True )
    chiTietToaThuoc = relationship("ChiTietToaThuoc", backref="thuoc", lazy=True )

    def __str__(self):
        return self.ten


class Comment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=True)

if __name__ == "__main__":

     with app.app_context():

        db.create_all()
        #
        # adm1 = NguoiDung(ten="Admin 1", ngaySinh="2003-05-21",
        #                  taiKhoan="adm1", matKhau=str(hashlib.md5("adm1".encode("utf-8")).hexdigest()),
        #                  vaiTro=UserRoleEnum.ADMIN)
        # bs1 = NguoiDung(ten="Bac Si 1", ngaySinh="2003-01-01",
        #                 taiKhoan="bs1", matKhau=str(hashlib.md5("bs1".encode("utf-8")).hexdigest())
        #                 , vaiTro=UserRoleEnum.DOCTOR)
        # bs2 = NguoiDung(ten="Bac Si 2", ngaySinh="2003-12-01",
        #                 taiKhoan="bs2", matKhau=str(hashlib.md5("bs2".encode("utf-8")).hexdigest())
        #                 , vaiTro=UserRoleEnum.DOCTOR)
        # yt1 = NguoiDung(ten="Y ta 1", ngaySinh="2003-12-11",
        #                 taiKhoan="yt1", matKhau=str(hashlib.md5("yt1".encode("utf-8")).hexdigest())
        #                 , vaiTro=UserRoleEnum.NURSE)
        # yt2 = NguoiDung(ten="Y ta 2", ngaySinh="2004-12-01",
        #                 taiKhoan="yt2", matKhau=str(hashlib.md5("yt2".encode("utf-8")).hexdigest())
        #                 , vaiTro=UserRoleEnum.NURSE)
        # tn1 = NguoiDung(ten="Thu ngan 1", ngaySinh="2003-05-01",
        #                 taiKhoan="tn1", matKhau=str(hashlib.md5("tn1".encode("utf-8")).hexdigest())
        #                 , vaiTro=UserRoleEnum.STAFF)
        # tn2 = NguoiDung(ten="Thu ngan 2", ngaySinh="2003-01-31",
        #                 taiKhoan="tn2", matKhau=str(hashlib.md5("tn2".encode("utf-8")).hexdigest())
        #                 , vaiTro=UserRoleEnum.STAFF)
        # qd1 = QuyDinh(ten="Số lượng bệnh nhân một ngày", giaTri=int(40))
        # qd2 = QuyDinh(ten="Số tiền khám", giaTri=float(100000))
        # db.session.add_all([qd1, qd2])
        # db.session.commit()
        # db.session.add_all([adm1, bs1, bs2, yt1, yt2, tn1, tn2])
        # db.session.commit()
        #
        #
        # bn1 = BenhNhan(ten="Nguyen Van A", gioiTinh="Nam",namSinh="2003-11-21")
        # bn2 = BenhNhan(ten="Nguyen Van B", gioiTinh="Nu", namSinh="2002-05-22")
        # db.session.add_all([bn1, bn2])
        # db.session.commit()
        #
        # dv1=DonViThuoc(donVi = "Chai")
        # dv2=DonViThuoc(donVi = "Sỉ")
        # dv3=DonViThuoc(donVi = "Viên")
        # db.session.add_all([dv1, dv2, dv3])
        # db.session.commit()
        #
        # t1 = Thuoc(ten="Thuoc 1", donGia=100000, soLuong=25, ngaySX="1999-01-01",  hanSD="2020-01-01", donVi_id = 1)
        # t2 = Thuoc(ten="Thuoc 2", donGia=500000, soLuong=25, ngaySX="1989-01-01",  hanSD="2023-01-01", donVi_id = 2)
        # db.session.add_all([t1, t2])
        # db.session.commit()

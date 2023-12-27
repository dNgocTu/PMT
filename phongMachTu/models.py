from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from phongMachTu import db, app
from flask_login import UserMixin
from datetime import datetime
import enum

class UserRoleEnum(enum.Enum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    CASHIER = 4

class NguoiDung(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    ngaySinh = Column(DateTime, default="1890-01-01")  # yyyy-mm-dd
    taiKhoan = Column(String(50), nullable=False, unique=True)
    matKhau = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg")
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
    namSinh = Column(DateTime, default="1890-01-01")
    sdt = Column(String(20), nullable=True)
    ngayDangKy = Column(DateTime, default=datetime.now())
    danhSachKhamBenh_id = Column(Integer, ForeignKey(DanhSachKhamBenh.id), nullable=False)
    nguoiDung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)

class BenhNhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    gioiTinh = Column(String(10), nullable=True)
    namSinh = Column(DateTime, default="1890-01-01")# yyyy-mm-dd
    diaChi = Column(String(100), nullable=True)
    sdt = Column(String(20), nullable=True)
    phieuKhamBenh = relationship("PhieuKhamBenh", backref="benhNhan", lazy=True)


class PhieuKhamBenh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    ngayLap = Column(DateTime, default=datetime.now())# yyyy-mm-dd
    trieuChung = Column(String(100), nullable=True)
    duDoanBenh = Column(String(200), nullable=True)
    nguoiDung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    benhNhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    hoaDon = relationship("HoaDon", backref="phieuKhamBenh", lazy=True)

class HoaDon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(100), nullable=True)
    ngayKham = Column(DateTime, default=datetime.now())# yyyy-mm-dd
    tienThuoc = Column(Float, nullable=True)
    tienKham = Column(Float, nullable=True)
    baoHiem = Column(String(50), nullable=True)
    trangThai = Column(Boolean, default=False)
    nguoiDung_id = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    phieuKhamBenh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)

# Chi tiet toa thuoc, thuoc, don vi, chi tiet loai thuoc, loai thuoc


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # import hashlib
        # u1 = User(name="Admin", username="admin", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
        #         user_role=UserRoleEnum.ADMIN)
        # db.session.add(u1)
        # db.session.commit()
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Tablet")
        # c3 = Category(name="Desktop")
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.commit()
        # p1 = Product(name='iPhone 13', price=21000000, category_id=1)
        # p2 = Product(name='iPad Pro 2023', price=21000000, category_id=2)
        # p3 = Product(name='Galaxy Tab S9', price=24000000, category_id=2)
        # p4 = Product(name='Galaxy S23', price=29000000, category_id=1)
        # p5 = Product(name='iPhone 15 Pro Max', price=25000000, category_id=1)
        # db.session.add_all([p1, p2, p3, p4, p5])
        # db.session.commit()
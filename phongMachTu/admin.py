from phongMachTu.models import *
from phongMachTu import app, db, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request


class AuthenicatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == UserRoleEnum.ADMIN


class AuthenicatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyQuyDinhView(AuthenicatedAdmin):
    column_list = ["ten", "giaTri"]
    column_editable_list = ["giaTri"]
    details_modal = True


class MyThuocView(AuthenicatedAdmin):
    form_columns = ['ten', 'donGia', 'soLuong', 'ngaySX', 'hanSD', 'donVi_id']
    column_list = ['ten', 'donGia', 'soLuong', 'ngaySX', 'hanSD']


class MyLoaiThuocView(AuthenicatedAdmin):
    column_list = ["ten"]
    details_modal = True


class MyDonViThuocView(AuthenicatedAdmin):
    column_list = ["donVi"]
    details_modal = True


class MyNguoiDungView(AuthenicatedAdmin):
    column_list = ["ten", "vaiTro"]


class StatsView(AuthenicatedUser):
    @expose('/')
    def index(self):
        tongDoanhThu = 0
        tongBenhNhan = 0
        thang = request.args.get('thang01')
        thang02 = request.args.get('thang02')
        thong_ke_01 = dao.thong_ke_01(thang)
        thong_ke_02 = dao.thong_ke_02(thang02)
        for row in thong_ke_01:
            tongDoanhThu += row.doanhThu
            tongBenhNhan += row.SoBenhNhan
        return self.render("admin/stats.html",
                           thong_ke_01=thong_ke_01,
                           tongDoanhThu=tongDoanhThu,
                           tongBenhNhan=tongBenhNhan,
                           thong_ke_02=thong_ke_02
                           )


class LogoutView(AuthenicatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


admin = Admin(app=app, name="Phòng mạch tư", template_mode="bootstrap4")
admin.add_view(MyQuyDinhView(QuyDinh, db.session, "Quy định"))
admin.add_view(MyThuocView(Thuoc, db.session, "Thuốc"))
admin.add_view(MyLoaiThuocView(LoaiThuoc, db.session, "Loại thuốc"))
admin.add_view(MyDonViThuocView(DonViThuoc, db.session, "Đơn vị thuốc"))
admin.add_view(MyNguoiDungView(NguoiDung, db.session, "User"))

admin.add_view(StatsView(name="Thống kê báo cáo"))
admin.add_view(LogoutView(name="Đăng xuất"))

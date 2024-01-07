from phongMachTu.models import *
from phongMachTu import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect
class AuthenicatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == UserRoleEnum.ADMIN

class AuthenicatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyQuyDinhView(AuthenicatedAdmin):
    column_list = ["ten","giaTri"]
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
    @expose("/")
    def index(self):
        return self.render("admin/stats.html")

class LogoutView(AuthenicatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")



admin = Admin(app=app, name="Phòng mạch tư", template_mode="bootstrap4" )
admin.add_view(MyQuyDinhView(QuyDinh, db.session, "Quy định"))
admin.add_view(MyThuocView(Thuoc, db.session, "Thuốc"))
admin.add_view(MyLoaiThuocView(LoaiThuoc, db.session, "Loại thuốc"))
admin.add_view(MyDonViThuocView(DonViThuoc, db.session, "Đơn vị thuốc"))
admin.add_view(MyNguoiDungView(NguoiDung, db.session, "User"))

admin.add_view(StatsView(name="Thống kê báo cáo"))
admin.add_view(LogoutView(name="Đăng xuất"))


from edc_model_admin.admin_site import EdcAdminSite


class AdminSite(EdcAdminSite):
    site_header = "Edc Reference"
    site_title = "Edc Reference"
    index_title = "Edc Reference"


edc_reference_admin = AdminSite(name="edc_reference_admin")

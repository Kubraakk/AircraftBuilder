from core.utils import get_current_user


class AuditService:
    def __init__(self, instance):
        self.instance = instance
        self.user = get_current_user()

    def set_audit_fields(self):
        if not self.instance.pk:
            self.instance.created_by = self.user
        self.instance.updated_by = self.user

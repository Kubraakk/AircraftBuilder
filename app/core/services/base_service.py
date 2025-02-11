from django.core.exceptions import ObjectDoesNotExist


class BaseService:
    """
    Generic service class for handling common database operations
    """

    def __init__(self, model):
        self.model = model

    def get(self, **kwargs):
        try:
            return self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def get_all(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, pk, **kwargs):
        try:
            obj = self.get(pk=pk)
            for attr, value in kwargs.items():
                setattr(obj, attr, value)
            obj.save()
        except ObjectDoesNotExist:
            return None
        else:
            return obj

    def update_all(self, filter_kwargs, update_kwargs):
        return self.model.objects.filter(**filter_kwargs).update(
            **update_kwargs
        )

    def delete(self, pk):
        try:
            obj = self.get(pk=pk)
            obj.delete()
        except ObjectDoesNotExist:
            return False
        else:
            return True

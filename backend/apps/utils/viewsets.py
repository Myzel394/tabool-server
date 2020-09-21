from django.db.models import QuerySet


class ReferencedModelViewSet:
    field_name: str = "id"
    request_field_name: str = "id"
    model_field_name: str
    
    def get_field_value(self):
        return self.request.data[self.request_field_name]
    
    def get_referenced_queryset(self) -> QuerySet:
        raise NotImplementedError()
    
    def get_referenced_object(self):
        referenced_queryset = self.get_referenced_queryset()
        
        return referenced_queryset.get(
            **{
                self.field_name: self.get_field_value()
            }
        )
    
    def get_queryset(self):
        obj = self.get_referenced_queryset()
        
        return getattr(obj, self.model_field_name).all()

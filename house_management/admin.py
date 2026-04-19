from django.contrib import admin
from django.contrib.auth.models import Group
from .models import House, Member
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX  
from import_export.widgets import ForeignKeyWidget

class HouseResource(resources.ModelResource):
    class Meta:
        model = House

        fields = (
            'house_no',
            'house_name',
            'house_owner',
            'place',
            'contact_number',
            'no_of_members',
            'remarks',
            'added_by',
            'created_at',
            'updated_at',
        )

class MemberResource(resources.ModelResource):
    class Meta:
        model = Member
        fields = (
            'first_name',
            'last_name',
            'full_name',
            'age',
            'sex',
            'education',
            'marital_status',
            'occupation',
            'house__house_no',
            'house__house_name',
            'remarks',
            'remarks_description',
            'added_by',
            'created_at',
        )
        export_order = fields

class AgeRangeFilter(admin.SimpleListFilter):
    title = _('Age range')
    parameter_name = 'age_range'

    def lookups(self, request, model_admin):
        return (
            ('0-18', '0-18'),
            ('19-30', '19-30'),
            ('31-45', '31-45'),
            ('46-60', '46-60'),
            ('61+', '61+'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-18':
            return queryset.filter(age__lte=18)
        elif self.value() == '19-30':
            return queryset.filter(age__gte=19, age__lte=30)
        elif self.value() == '31-45':
            return queryset.filter(age__gte=31, age__lte=45)
        elif self.value() == '46-60':
            return queryset.filter(age__gte=46, age__lte=60)
        elif self.value() == '61+':
            return queryset.filter(age__gte=61)
        return queryset

admin.site.unregister(Group)

class MemberInline(admin.StackedInline):
    model = Member
    extra = 1

class HouseAdmin(ImportExportModelAdmin):  
    resource_class = HouseResource  
    inlines = [MemberInline]
    list_filter = ['place']
    search_fields = ['house_no', 'house_name', 'house_owner', 'place']
    list_display = ['house_no', 'house_name', 'house_owner', 'place', 'contact_number']

    def get_export_queryset(self, request):
        # Order by house_no (or any other field you prefer)
        return super().get_export_queryset(request).order_by('house_no')
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        for formset in formsets:
            if formset.total_form_count() > 0:  
                for form in formset.forms:
                    member = form.instance
                    if isinstance(member, Member):
                        if not member.house_id:  
                            member.house = formset.instance  
                        if not member.added_by:
                            member.added_by = request.user
                        member.save()


    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  
        return formats
    
    class Media:
        css = {
            'all': ('css/custom_admin.css',) 
        }

class MemberAdmin(ImportExportModelAdmin):  
    resource_class = MemberResource  
    list_display = ['first_name', 'age', 'marital_status', 'education', 'occupation', 'house', 'house__house_name', 'added_by']
    search_fields = ['first_name', 'last_name', 'age', 'education']
    list_filter = ['sex', 'marital_status', AgeRangeFilter, 'remarks', 'house__place']
 
    actions = ['export_admin_action']
    
    

    def save_model(self, request, obj, form, change):
        if not obj.added_by:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(XLSX)  
        return formats
    
    def get_search_results(self, request, queryset, search_term):
        if search_term:
            try:
                house_id = int(search_term)
                queryset = queryset.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(age__icontains=search_term) |
                    Q(house__house_name__icontains=search_term) |
                    Q(house__house_no__icontains=search_term) |
                    Q(house__id=house_id)  
                )
            except ValueError:
                queryset = queryset.filter(
                    Q(first_name__icontains=search_term) |
                    Q(last_name__icontains=search_term) |
                    Q(age__icontains=search_term) |
                    Q(house__house_name__icontains=search_term) |
                    Q(house__house_no__icontains=search_term)
                )
        return queryset, False


admin.site.register(House, HouseAdmin)
admin.site.register(Member, MemberAdmin)

from django.contrib import admin

from .models import Player, Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "specialist")
    list_filter = ("specialist",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "age", "position_list")
    search_fields = ("firstName", "lastName")
    list_filter = ("positions",)
    filter_horizontal = ("positions",)       # nice two-box picker for the many-to-many

    @admin.display(description="Positions")
    def position_list(self, obj):
        return ", ".join(p.name for p in obj.positions.all())

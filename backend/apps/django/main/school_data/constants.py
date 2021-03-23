from django.utils.translation import gettext_lazy as _

__all__ = [
    "APP_LABEL", "SUBJECT_NAMES_MAPPING", "SUBJECT_COLORS_MAPPING",
]

APP_LABEL = "school_data"
SUBJECT_NAMES_MAPPING = {
    "m": _("Mathe"),
    "d": _("Deutsch"),
    
    "e": _("Englisch"),
    "f": _("Französisch"),
    "l": _("Latein"),
    "s": _("Spanisch"),
    
    "in": _("Informatik"),
    
    "ch": _("Chemie"),
    "ph": _("Physik"),
    "bi": _("Biologie"),
    "nawi": _("Naturwissenschaften"),
    
    "skek": _("Sozialkunde-Erdkunde"),
    "sk": _("Sozialkunde"),
    "ek": _("Erdkunde"),
    "g": _("Geschichte"),
    
    "kr": _("Katholische Religion"),
    "et": _("Ethik"),
    "er": _("Evangelische Religion"),
    "mr": _("Mennonitische Religion"),
    
    "mu": _("Musik"),
    "ds": _("Darstellendes Spiel"),
    "bk": _("Kunst"),
    
    "sp": _("Sport"),
    "spk": _("Sport"),
    "spko": _("Sport"),
}
SUBJECT_COLORS_MAPPING = {
    "m": "#FF4834",
    "d": "#2072FF",
    
    "e": "#14A5FF",
    "f": "#FFDA28",
    "l": "#73FFF2",
    "s": "#EAFF00",
    
    "in": "#1E67FF",
    
    "ch": "#F2FF06",
    "ph": "#2FD0FF",
    "bi": "#86FF49",
    "nawi": "#24eda3",
    
    "skek": "#BE10FF",
    "sk": "#FF0021",
    "ek": "#CE8F24",
    
    "g": "#FF6E37",
    
    "kr": "#D70AFF",
    "et": "#D70AFF",
    "er": "#D70AFF",
    "mr": "#D70AFF",
    
    "mu": "#FFFB00",
    "ds": "#48FFF7",
    "bk": "#5645FF",
    
    "sp": "#39D8FF",
    "spk": "#39D8FF",
    "spko": "#39D8FF",
}

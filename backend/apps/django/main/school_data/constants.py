from django.utils.translation import gettext_lazy as _
from pydicti import dicti

APP_LABEL = "school_data"
SUBJECT_NAMES_MAPPING = dicti(
    E=_("Englisch"),
    M=_("Mathe"),
    D=_("Deutsch"),
    F=_("Französisch"),
    L=_("Latein"),
    S=_("Spanisch"),
    
    iN=_("Informatik"),
    
    ch=_("Chemie"),
    ph=_("Physik"),
    bi=_("Biologie"),
    
    skek=_("Sozialkunde-Erdkunde"),
    sk=_("Sozialkunde"),
    ek=_("Erdkunde"),
    
    kr=_("Katholische Religion"),
    et=_("Ethik"),
    er=_("Evangelische Religion"),
    
    mu=_("Musik"),
    ds=_("Darstellendes Spiel"),
    
    spk=_("Sport"),
    g=_("Geschichte"),
    bk=_("Kunst"),
)
SUBJECT_COLORS_MAPPING = dicti(
    E="#14A5FF",
    M="#FF4834",
    D="#2072FF",
    F="#FFDA28",
    L="#73FFF2",
    S="#EAFF00",
    
    iN="#1E67FF",
    
    ch="#F2FF06",
    ph="#2FD0FF",
    bi="#86FF49",
    
    skek="#BE10FF",
    sk="#FF0021",
    ek="#CE8F24",
    
    kr="#D70AFF",
    et="#D70AFF",
    er="#D70AFF",
    
    mu="#FFFB00",
    ds="#48FFF7",
    
    spk="#39D8FF",
    g="#FF6E37",
    bk="#5645FF"
)

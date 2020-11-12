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
    englisch="#14A5FF",
    mathe="#FF4834",
    deutsch="#2072FF",
    französisch="#FFDA28",
    latein="#73FFF2",
    spanisch="#EAFF00",
    
    informatik="#1E67FF",
    
    chemie="#F2FF06",
    physik="#2FD0FF",
    biologie="#86FF49",
    
    sozialkunde_erdkunde="#BE10FF",
    sozialkunde="#FF0021",
    eerdunde="#CE8F24",
    
    katholische_religion="#D70AFF",
    ethik="#D70AFF",
    evangelische_religion="#D70AFF",
    
    musik="#FFFB00",
    darstellendes_spiel="#48FFF7",
    
    sport="#39D8FF",
    geschichte="#FF6E37",
    kunst="#5645FF"
)

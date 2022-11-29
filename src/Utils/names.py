# specific Values
V_DTNAIS_NULL = "0000-00-00"
V_MTREV_NULL = 0  # 0 -> val manquante?
V_RANGADH_NULL = None  # !!! Utiliser la méthode "is_equal_to" de dataExploration
V_DATE_NULL = "0000-00-00"
V_DATE_ODD = "1900-01-00"
V_DTDEM_NO_DEM = "31/12/1900"


V_DTNAIS_INCORRECT = ""

# Columns String names
CS_DTNAIS = "DTNAIS"  # Date de naissance
CS_DTADH = "DTADH"  # Date d’adhésion à l’organisme bancaire
CS_DTDEM = "DTDEM"  # Date de démission
CS_ANNEEDEM = "ANNEEDEM"  # Année de démission
CS_RANGDEM = "RANGDEM"  # Date de la démission au format N AAAA (code puis année)


# Columns Categorical String names

CCS_CDMOTDEM = "CDMOTDEM"  # Motif de la démission (catégorie)


# Columns Numeric names

CN_ID = "ID"  # Identifiant unique (dans ce fichier)
CN_MTREV = "MTREV"  # Montant des revenus
CN_NBENF = "NBENF"  # Nombre d’enfants
CN_AGEAD = "AGEAD"  # Âge du client à l’adhésion, en années
CN_AGEDEM = "AGEDEM"  # Âge du client à la démission, en années
CN_ADH = "ADH"  # Durée de la période d’adhésion, en années

LIST_KEPT_NUM_COLS = [CN_MTREV, CN_NBENF, CN_AGEAD, CN_ADH]


# Columns Categorical (numerical) names

CCN_CDSEXE = "CDSEXE"  # Code relatif au sexe {1,2,3,4}
CCN_CDSITFAM = "CDSITFAM"  # Situation familiale
CCN_CDTMT = "CDTMT"  # Code représentant le statut du sociétaire (catégorie)
CCN_CDDEM = "CDDEM"  # Code de démission
CCN_CDCATCL = "CDCATCL"  # Type de client (catégorie)
CCN_RANGAGEAD = "RANGAGEAD"  # Tranche d’âge du client à l’adhésion
CCN_RANGAGEDEM = "RANGAGEDEM"  # Tranche d’âge du client à la démission
CCN_RANGADH = "RANGADH"  # Tranche de la durée de la période d’adhésion
CCN_ISDEM = "ISDEM"  # Démissionnaire ou non

LIST_KEPT_CAT_COLS = [CCN_CDSEXE, CCN_CDSITFAM, CCN_CDTMT, CCN_CDCATCL]  # CCN_ISDEM ? (label)



# Keys

TRAIN = "TRAIN"
VALID = "VALID"
TEST = "TEST"
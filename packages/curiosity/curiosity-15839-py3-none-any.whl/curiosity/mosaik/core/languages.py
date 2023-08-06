from enum import IntEnum
from typing import Dict, Set


class Language(IntEnum):
    Abkhazian = 0
    Afar = 1
    Afrikaans = 2
    Albanian = 3
    Amharic = 4
    Arabic = 5
    Aragonese = 6
    Armenian = 7
    Assamese = 8
    Avestan = 9
    Aymara = 10
    Azerbaijani = 11
    Bashkir = 12
    Basque = 13
    Belarusian = 14
    Bengali = 15
    Bihari = 16
    Bislama = 17
    Bosnian = 18
    Breton = 19
    Bulgarian = 20
    Burmese = 21
    Catalan = 22
    Chamorro = 23
    Chechen = 24
    Chinese = 25
    Church_Slavic_Slavonic_Old_Bulgarian = 26
    Chuvash = 27
    Cornish = 28
    Corsican = 29
    Croatian = 30
    Czech = 31
    Danish = 32
    Divehi_Dhivehi_Maldivian = 33
    Dutch = 34
    Dzongkha = 35
    English = 36
    Esperanto = 37
    Estonian = 38
    Faroese = 39
    Fijian = 40
    Finnish = 41
    French = 42
    Gaelic_Scottish_Gaelic = 43
    Galician = 44
    Georgian = 45
    German = 46
    Greek_Modern = 47
    Guarani = 48
    Gujarati = 49
    Haitian_Haitian_Creole = 50
    Hausa = 51
    Hebrew = 52
    Herero = 53
    Hindi = 54
    Hiri_Motu = 55
    Hungarian = 56
    Icelandic = 57
    Ido = 58
    Indonesian = 59
    Interlingua = 60
    Interlingue = 61
    Inuktitut = 62
    Inupiaq = 63
    Irish = 64
    Italian = 65
    Japanese = 66
    Javanese = 67
    Kalaallisut = 68
    Kannada = 69
    Kashmiri = 70
    Kazakh = 71
    Khmer = 72
    Kikuyu_Gikuyu = 73
    Kinyarwanda = 74
    Kirghiz = 75
    Komi = 76
    Korean = 77
    Kuanyama_Kwanyama = 78
    Kurdish = 79
    Lao = 80
    Latin = 81
    Latvian = 82
    Limburgan_Limburger_Limburgish = 83
    Lingala = 84
    Lithuanian = 85
    Luxembourgish_Letzeburgesch = 86
    Macedonian = 87
    Malagasy = 88
    Malay = 89
    Malayalam = 90
    Maltese = 91
    Manx = 92
    Maori = 93
    Marathi = 94
    Marshallese = 95
    Moldavian = 96
    Mongolian = 97
    Nauru = 98
    Navaho_Navajo = 99
    Ndebele_North = 100
    Ndebele_South = 101
    Ndonga = 102
    Nepali = 103
    Northern_Sami = 104
    Norwegian = 105
    Norwegian_Bokmal = 106
    Norwegian_Nynorsk = 107
    Nyanja_Chichewa_Chewa = 108
    Occitan_Provencal = 109
    Oriya = 110
    Oromo = 111
    Ossetian_Ossetic = 112
    Pali = 113
    Panjabi = 114
    Persian = 115
    Polish = 116
    Portuguese = 117
    Pushto = 118
    Quechua = 119
    Raeto_Romance = 120
    Romanian = 121
    Rundi = 122
    Russian = 123
    Samoan = 124
    Sango = 125
    Sanskrit = 126
    Sardinian = 127
    Serbian = 128
    Shona = 129
    Sichuan_Yi = 130
    Sindhi = 131
    Sinhala_Sinhalese = 132
    Slovak = 133
    Slovenian = 134
    Somali = 135
    Sotho_Southern = 136
    Spanish = 137
    Sundanese = 138
    Swahili = 139
    Swati = 140
    Swedish = 141
    Tagalog = 142
    Tahitian = 143
    Tajik = 144
    Tamil = 145
    Tatar = 146
    Telugu = 147
    Thai = 148
    Tibetan = 149
    Tigrinya = 150
    Tonga = 151
    Tsonga = 152
    Tswana = 153
    Turkish = 154
    Turkmen = 155
    Twi = 156
    Uighur = 157
    Ukrainian = 158
    Urdu = 159
    Uzbek = 160
    Vietnamese = 161
    Volapuk = 162
    Walloon = 163
    Welsh = 164
    Western_Frisian = 165
    Wolof = 166
    Xhosa = 167
    Yiddish = 168
    Yoruba = 169
    Zhuang_Chuang = 170
    Zulu = 171
    Unknown = 172
    Any = 173


class Languages:
    valid_3_letter_codes: Set[str] = {
        "aar",
        "abk",
        "afr",
        "sqi",
        "amh",
        "ara",
        "arg",
        "hye",
        "asm",
        "ave",
        "aym",
        "aze",
        "bak",
        "eus",
        "bel",
        "ben",
        "bih",
        "bis",
        "bod",
        "bos",
        "bre",
        "bul",
        "mya",
        "cat",
        "ces",
        "cha",
        "che",
        "zho",
        "chu",
        "chv",
        "cor",
        "cos",
        "cym",
        "dan",
        "deu",
        "div",
        "nld",
        "dzo",
        "ell",
        "eng",
        "epo",
        "est",
        "fao",
        "fas",
        "fij",
        "fin",
        "fra",
        "fry",
        "kat",
        "gla",
        "gle",
        "glg",
        "glv",
        "grn",
        "guj",
        "hat",
        "hau",
        "heb",
        "her",
        "hin",
        "hmo",
        "hrv",
        "hun",
        "isl",
        "ido",
        "iii",
        "iku",
        "ile",
        "ina",
        "ind",
        "ipk",
        "ita",
        "jav",
        "jpn",
        "kal",
        "kan",
        "kas",
        "kaz",
        "khm",
        "kik",
        "kin",
        "kir",
        "kom",
        "kor",
        "kua",
        "kur",
        "lao",
        "lat",
        "lav",
        "lim",
        "lin",
        "lit",
        "ltz",
        "mkd",
        "mah",
        "mal",
        "mri",
        "mar",
        "msa",
        "mlg",
        "mlt",
        "mon",
        "nau",
        "nav",
        "nbl",
        "nde",
        "ndo",
        "nep",
        "nno",
        "nob",
        "nor",
        "nya",
        "oci",
        "ori",
        "orm",
        "oss",
        "pan",
        "pli",
        "pol",
        "por",
        "pus",
        "que",
        "roh",
        "ron",
        "run",
        "rus",
        "sag",
        "san",
        "sin",
        "slk",
        "slv",
        "sme",
        "smo",
        "sna",
        "snd",
        "som",
        "sot",
        "spa",
        "srd",
        "srp",
        "ssw",
        "sun",
        "swa",
        "swe",
        "tah",
        "tam",
        "tat",
        "tel",
        "tgk",
        "tgl",
        "tha",
        "tir",
        "ton",
        "tsn",
        "tso",
        "tuk",
        "tur",
        "twi",
        "uig",
        "ukr",
        "urd",
        "uzb",
        "vie",
        "vol",
        "wln",
        "wol",
        "xho",
        "yid",
        "yor",
        "zha",
        "zul"}

    _three_letter_to_two_letter: Dict[str, str] = {
        "aar": "aa",
        "abk": "ab",
        "afr": "af",
        "amh": "am",
        "ara": "ar",
        "arg": "an",
        "asm": "as",
        "ave": "ae",
        "aym": "ay",
        "aze": "az",
        "bak": "ba",
        "bel": "be",
        "ben": "bn",
        "bih": "bh",
        "bis": "bi",
        "bod": "bo",
        "bos": "bs",
        "bre": "br",
        "bul": "bg",
        "cat": "ca",
        "ces": "cs",
        "cha": "ch",
        "che": "ce",
        "chu": "cu",
        "chv": "cv",
        "cor": "kw",
        "cos": "co",
        "cym": "cy",
        "dan": "da",
        "deu": "de",
        "div": "dv",
        "dzo": "dz",
        "ell": "el",
        "eng": "en",
        "epo": "eo",
        "est": "et",
        "eus": "eu",
        "fao": "fo",
        "fas": "fa",
        "fij": "fj",
        "fin": "fi",
        "fra": "fr",
        "fry": "fy",
        "gla": "gd",
        "gle": "ga",
        "glg": "gl",
        "glv": "gv",
        "grn": "gn",
        "guj": "gu",
        "hat": "ht",
        "hau": "ha",
        "heb": "he",
        "her": "hz",
        "hin": "hi",
        "hmo": "ho",
        "hrv": "hr",
        "hun": "hu",
        "hye": "hy",
        "ido": "io",
        "iii": "ii",
        "iku": "iu",
        "ile": "ie",
        "ina": "ia",
        "ind": "id",
        "ipk": "ik",
        "isl": "is",
        "ita": "it",
        "jav": "jv",
        "jpn": "ja",
        "kal": "kl",
        "kan": "kn",
        "kas": "ks",
        "kat": "ka",
        "kaz": "kk",
        "khm": "km",
        "kik": "ki",
        "kin": "rw",
        "kir": "ky",
        "kom": "kv",
        "kor": "ko",
        "kua": "kj",
        "kur": "ku",
        "lao": "lo",
        "lat": "la",
        "lav": "lv",
        "lim": "li",
        "lin": "ln",
        "lit": "lt",
        "ltz": "lb",
        "mah": "mh",
        "mal": "ml",
        "mar": "mr",
        "mkd": "mk",
        "mlg": "mg",
        "mlt": "mt",
        "mon": "mn",
        "mri": "mi",
        "msa": "ms",
        "mya": "my",
        "nau": "na",
        "nav": "nv",
        "nbl": "nr",
        "nde": "nd",
        "ndo": "ng",
        "nep": "ne",
        "nld": "nl",
        "nno": "nn",
        "nob": "nb",
        "nor": "no",
        "nya": "ny",
        "oci": "oc",
        "ori": "or",
        "orm": "om",
        "oss": "os",
        "pan": "pa",
        "pli": "pi",
        "pol": "pl",
        "por": "pt",
        "pus": "ps",
        "que": "qu",
        "roh": "rm",
        "ron": "ro",
        "run": "rn",
        "rus": "ru",
        "sag": "sg",
        "san": "sa",
        "sin": "si",
        "slk": "sk",
        "slv": "sl",
        "sme": "se",
        "smo": "sm",
        "sna": "sn",
        "snd": "sd",
        "som": "so",
        "sot": "st",
        "spa": "es",
        "sqi": "sq",
        "srd": "sc",
        "srp": "sr",
        "ssw": "ss",
        "sun": "su",
        "swa": "sw",
        "swe": "sv",
        "tah": "ty",
        "tam": "ta",
        "tat": "tt",
        "tel": "te",
        "tgk": "tg",
        "tgl": "tl",
        "tha": "th",
        "tir": "ti",
        "ton": "to",
        "tsn": "tn",
        "tso": "ts",
        "tuk": "tk",
        "tur": "tr",
        "twi": "tw",
        "uig": "ug",
        "ukr": "uk",
        "urd": "ur",
        "uzb": "uz",
        "vie": "vi",
        "vol": "vo",
        "wln": "wa",
        "wol": "wo",
        "xho": "xh",
        "yid": "yi",
        "yor": "yo",
        "zha": "za",
        "zho": "zh",
        "zul": "zu"}
    _code_to_enum: Dict[str, Language] = {
        "--": Language.Any,
        "??": Language.Unknown,
        "ab": Language.Abkhazian,
        "aa": Language.Afar,
        "af": Language.Afrikaans,
        "sq": Language.Albanian,
        "am": Language.Amharic,
        "ar": Language.Arabic,
        "an": Language.Aragonese,
        "hy": Language.Armenian,
        "as": Language.Assamese,
        "ae": Language.Avestan,
        "ay": Language.Aymara,
        "az": Language.Azerbaijani,
        "ba": Language.Bashkir,
        "eu": Language.Basque,
        "be": Language.Belarusian,
        "bn": Language.Bengali,
        "bh": Language.Bihari,
        "bi": Language.Bislama,
        "bs": Language.Bosnian,
        "br": Language.Breton,
        "bg": Language.Bulgarian,
        "my": Language.Burmese,
        "ca": Language.Catalan,
        "ch": Language.Chamorro,
        "ce": Language.Chechen,
        "zh": Language.Chinese,
        "cu": Language.Church_Slavic_Slavonic_Old_Bulgarian,
        "cv": Language.Chuvash,
        "kw": Language.Cornish,
        "co": Language.Corsican,
        "hr": Language.Croatian,
        "cs": Language.Czech,
        "da": Language.Danish,
        "dv": Language.Divehi_Dhivehi_Maldivian,
        "nl": Language.Dutch,
        "dz": Language.Dzongkha,
        "en": Language.English,
        "eo": Language.Esperanto,
        "et": Language.Estonian,
        "fo": Language.Faroese,
        "fj": Language.Fijian,
        "fi": Language.Finnish,
        "fr": Language.French,
        "gd": Language.Gaelic_Scottish_Gaelic,
        "gl": Language.Galician,
        "ka": Language.Georgian,
        "de": Language.German,
        "el": Language.Greek_Modern,
        "gn": Language.Guarani,
        "gu": Language.Gujarati,
        "ht": Language.Haitian_Haitian_Creole,
        "ha": Language.Hausa,
        "he": Language.Hebrew,
        "hz": Language.Herero,
        "hi": Language.Hindi,
        "ho": Language.Hiri_Motu,
        "hu": Language.Hungarian,
        "is": Language.Icelandic,
        "io": Language.Ido,
        "id": Language.Indonesian,
        "ia": Language.Interlingua,
        "ie": Language.Interlingue,
        "iu": Language.Inuktitut,
        "ik": Language.Inupiaq,
        "ga": Language.Irish,
        "it": Language.Italian,
        "ja": Language.Japanese,
        "jv": Language.Javanese,
        "kl": Language.Kalaallisut,
        "kn": Language.Kannada,
        "ks": Language.Kashmiri,
        "kk": Language.Kazakh,
        "km": Language.Khmer,
        "ki": Language.Kikuyu_Gikuyu,
        "rw": Language.Kinyarwanda,
        "ky": Language.Kirghiz,
        "kv": Language.Komi,
        "ko": Language.Korean,
        "kj": Language.Kuanyama_Kwanyama,
        "ku": Language.Kurdish,
        "lo": Language.Lao,
        "la": Language.Latin,
        "lv": Language.Latvian,
        "li": Language.Limburgan_Limburger_Limburgish,
        "ln": Language.Lingala,
        "lt": Language.Lithuanian,
        "lb": Language.Luxembourgish_Letzeburgesch,
        "mk": Language.Macedonian,
        "mg": Language.Malagasy,
        "ms": Language.Malay,
        "ml": Language.Malayalam,
        "mt": Language.Maltese,
        "gv": Language.Manx,
        "mi": Language.Maori,
        "mr": Language.Marathi,
        "mh": Language.Marshallese,
        "mo": Language.Moldavian,
        "mn": Language.Mongolian,
        "na": Language.Nauru,
        "nv": Language.Navaho_Navajo,
        "nd": Language.Ndebele_North,
        "nr": Language.Ndebele_South,
        "ng": Language.Ndonga,
        "ne": Language.Nepali,
        "se": Language.Northern_Sami,
        "no": Language.Norwegian,
        "nb": Language.Norwegian_Bokmal,
        "nn": Language.Norwegian_Nynorsk,
        "ny": Language.Nyanja_Chichewa_Chewa,
        "oc": Language.Occitan_Provencal,
        "or": Language.Oriya,
        "om": Language.Oromo,
        "os": Language.Ossetian_Ossetic,
        "pi": Language.Pali,
        "pa": Language.Panjabi,
        "fa": Language.Persian,
        "pl": Language.Polish,
        "pt": Language.Portuguese,
        "ps": Language.Pushto,
        "qu": Language.Quechua,
        "rm": Language.Raeto_Romance,
        "ro": Language.Romanian,
        "rn": Language.Rundi,
        "ru": Language.Russian,
        "sm": Language.Samoan,
        "sg": Language.Sango,
        "sa": Language.Sanskrit,
        "sc": Language.Sardinian,
        "sr": Language.Serbian,
        "sn": Language.Shona,
        "ii": Language.Sichuan_Yi,
        "sd": Language.Sindhi,
        "si": Language.Sinhala_Sinhalese,
        "sk": Language.Slovak,
        "sl": Language.Slovenian,
        "so": Language.Somali,
        "st": Language.Sotho_Southern,
        "es": Language.Spanish,
        "su": Language.Sundanese,
        "sw": Language.Swahili,
        "ss": Language.Swati,
        "sv": Language.Swedish,
        "tl": Language.Tagalog,
        "ty": Language.Tahitian,
        "tg": Language.Tajik,
        "ta": Language.Tamil,
        "tt": Language.Tatar,
        "te": Language.Telugu,
        "th": Language.Thai,
        "bo": Language.Tibetan,
        "ti": Language.Tigrinya,
        "to": Language.Tonga,
        "ts": Language.Tsonga,
        "tn": Language.Tswana,
        "tr": Language.Turkish,
        "tk": Language.Turkmen,
        "tw": Language.Twi,
        "ug": Language.Uighur,
        "uk": Language.Ukrainian,
        "ur": Language.Urdu,
        "uz": Language.Uzbek,
        "vi": Language.Vietnamese,
        "vo": Language.Volapuk,
        "wa": Language.Walloon,
        "cy": Language.Welsh,
        "fy": Language.Western_Frisian,
        "wo": Language.Wolof,
        "xh": Language.Xhosa,
        "yi": Language.Yiddish,
        "yo": Language.Yoruba,
        "za": Language.Zhuang_Chuang,
        "zu": Language.Zulu,
    }

    _enum_to_code: Dict[Language, str] = {
        Language.Any:                                  "--",
        Language.Unknown:                              "??",
        Language.Abkhazian:                            "ab",
        Language.Afar:                                 "aa",
        Language.Afrikaans:                            "af",
        Language.Albanian:                             "sq",
        Language.Amharic:                              "am",
        Language.Arabic:                               "ar",
        Language.Aragonese:                            "an",
        Language.Armenian:                             "hy",
        Language.Assamese:                             "as",
        Language.Avestan:                              "ae",
        Language.Aymara:                               "ay",
        Language.Azerbaijani:                          "az",
        Language.Bashkir:                              "ba",
        Language.Basque:                               "eu",
        Language.Belarusian:                           "be",
        Language.Bengali:                              "bn",
        Language.Bihari:                               "bh",
        Language.Bislama:                              "bi",
        Language.Bosnian:                              "bs",
        Language.Breton:                               "br",
        Language.Bulgarian:                            "bg",
        Language.Burmese:                              "my",
        Language.Catalan:                              "ca",
        Language.Chamorro:                             "ch",
        Language.Chechen:                              "ce",
        Language.Chinese:                              "zh",
        Language.Church_Slavic_Slavonic_Old_Bulgarian: "cu",
        Language.Chuvash:                              "cv",
        Language.Cornish:                              "kw",
        Language.Corsican:                             "co",
        Language.Croatian:                             "hr",
        Language.Czech:                                "cs",
        Language.Danish:                               "da",
        Language.Divehi_Dhivehi_Maldivian:             "dv",
        Language.Dutch:                                "nl",
        Language.Dzongkha:                             "dz",
        Language.English:                              "en",
        Language.Esperanto:                            "eo",
        Language.Estonian:                             "et",
        Language.Faroese:                              "fo",
        Language.Fijian:                               "fj",
        Language.Finnish:                              "fi",
        Language.French:                               "fr",
        Language.Gaelic_Scottish_Gaelic:               "gd",
        Language.Galician:                             "gl",
        Language.Georgian:                             "ka",
        Language.German:                               "de",
        Language.Greek_Modern:                         "el",
        Language.Guarani:                              "gn",
        Language.Gujarati:                             "gu",
        Language.Haitian_Haitian_Creole:               "ht",
        Language.Hausa:                                "ha",
        Language.Hebrew:                               "he",
        Language.Herero:                               "hz",
        Language.Hindi:                                "hi",
        Language.Hiri_Motu:                            "ho",
        Language.Hungarian:                            "hu",
        Language.Icelandic:                            "is",
        Language.Ido:                                  "io",
        Language.Indonesian:                           "id",
        Language.Interlingua:                          "ia",
        Language.Interlingue:                          "ie",
        Language.Inuktitut:                            "iu",
        Language.Inupiaq:                              "ik",
        Language.Irish:                                "ga",
        Language.Italian:                              "it",
        Language.Japanese:                             "ja",
        Language.Javanese:                             "jv",
        Language.Kalaallisut:                          "kl",
        Language.Kannada:                              "kn",
        Language.Kashmiri:                             "ks",
        Language.Kazakh:                               "kk",
        Language.Khmer:                                "km",
        Language.Kikuyu_Gikuyu:                        "ki",
        Language.Kinyarwanda:                          "rw",
        Language.Kirghiz:                              "ky",
        Language.Komi:                                 "kv",
        Language.Korean:                               "ko",
        Language.Kuanyama_Kwanyama:                    "kj",
        Language.Kurdish:                              "ku",
        Language.Lao:                                  "lo",
        Language.Latin:                                "la",
        Language.Latvian:                              "lv",
        Language.Limburgan_Limburger_Limburgish:       "li",
        Language.Lingala:                              "ln",
        Language.Lithuanian:                           "lt",
        Language.Luxembourgish_Letzeburgesch:          "lb",
        Language.Macedonian:                           "mk",
        Language.Malagasy:                             "mg",
        Language.Malay:                                "ms",
        Language.Malayalam:                            "ml",
        Language.Maltese:                              "mt",
        Language.Manx:                                 "gv",
        Language.Maori:                                "mi",
        Language.Marathi:                              "mr",
        Language.Marshallese:                          "mh",
        Language.Moldavian:                            "mo",
        Language.Mongolian:                            "mn",
        Language.Nauru:                                "na",
        Language.Navaho_Navajo:                        "nv",
        Language.Ndebele_North:                        "nd",
        Language.Ndebele_South:                        "nr",
        Language.Ndonga:                               "ng",
        Language.Nepali:                               "ne",
        Language.Northern_Sami:                        "se",
        Language.Norwegian:                            "no",
        Language.Norwegian_Bokmal:                     "nb",
        Language.Norwegian_Nynorsk:                    "nn",
        Language.Nyanja_Chichewa_Chewa:                "ny",
        Language.Occitan_Provencal:                    "oc",
        Language.Oriya:                                "or",
        Language.Oromo:                                "om",
        Language.Ossetian_Ossetic:                     "os",
        Language.Pali:                                 "pi",
        Language.Panjabi:                              "pa",
        Language.Persian:                              "fa",
        Language.Polish:                               "pl",
        Language.Portuguese:                           "pt",
        Language.Pushto:                               "ps",
        Language.Quechua:                              "qu",
        Language.Raeto_Romance:                        "rm",
        Language.Romanian:                             "ro",
        Language.Rundi:                                "rn",
        Language.Russian:                              "ru",
        Language.Samoan:                               "sm",
        Language.Sango:                                "sg",
        Language.Sanskrit:                             "sa",
        Language.Sardinian:                            "sc",
        Language.Serbian:                              "sr",
        Language.Shona:                                "sn",
        Language.Sichuan_Yi:                           "ii",
        Language.Sindhi:                               "sd",
        Language.Sinhala_Sinhalese:                    "si",
        Language.Slovak:                               "sk",
        Language.Slovenian:                            "sl",
        Language.Somali:                               "so",
        Language.Sotho_Southern:                       "st",
        Language.Spanish:                              "es",
        Language.Sundanese:                            "su",
        Language.Swahili:                              "sw",
        Language.Swati:                                "ss",
        Language.Swedish:                              "sv",
        Language.Tagalog:                              "tl",
        Language.Tahitian:                             "ty",
        Language.Tajik:                                "tg",
        Language.Tamil:                                "ta",
        Language.Tatar:                                "tt",
        Language.Telugu:                               "te",
        Language.Thai:                                 "th",
        Language.Tibetan:                              "bo",
        Language.Tigrinya:                             "ti",
        Language.Tonga:                                "to",
        Language.Tsonga:                               "ts",
        Language.Tswana:                               "tn",
        Language.Turkish:                              "tr",
        Language.Turkmen:                              "tk",
        Language.Twi:                                  "tw",
        Language.Uighur:                               "ug",
        Language.Ukrainian:                            "uk",
        Language.Urdu:                                 "ur",
        Language.Uzbek:                                "uz",
        Language.Vietnamese:                           "vi",
        Language.Volapuk:                              "vo",
        Language.Walloon:                              "wa",
        Language.Welsh:                                "cy",
        Language.Western_Frisian:                      "fy",
        Language.Wolof:                                "wo",
        Language.Xhosa:                                "xh",
        Language.Yiddish:                              "yi",
        Language.Yoruba:                               "yo",
        Language.Zhuang_Chuang:                        "za",
        Language.Zulu:                                 "zu"}

    @staticmethod
    def is_valid_3_letter_codes(input_: str) -> bool:
        return input_ in Languages.valid_3_letter_codes

    @staticmethod
    def three_letter_code_to_enum(input_: str) -> Language:
        input_ = input_.lower()

        if input_ in Languages._three_letter_to_two_letter:
            return Languages.code_to_enum(Languages._three_letter_to_two_letter[input_])
        else:
            raise ValueError(f"Invalid language code '{input_}'")

    @staticmethod
    def code_to_enum(input_: str) -> Language:

        if input_ in Languages._code_to_enum:
            return Languages._code_to_enum[input_]
        else:
            raise ValueError(f"Invalid language code '{input_}'")

    @staticmethod
    def enum_to_code(input_: Language) -> str:

        if input_ in Languages._enum_to_code:
            return Languages._enum_to_code[input_]
        else:
            raise ValueError(f"Invalid language '{input_}'")

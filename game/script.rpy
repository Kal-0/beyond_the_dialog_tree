# ==============================================================
# SCRIPT PRINCIPAL - PONTO DE ENTRADA DO JOGO
# ==============================================================

init:
    # Ajeita a Leitura dos Menus e Textos sobre fundos confusos
    style default:
        outlines [(0.1, "#333333aa", 0, 0)]
    style choice_button_text:
        outlines [(0.1, "#333333aa", 0, 0)]
        color "#ffffff"
        hover_color "#ffd700"

# Forçar Modo Desenvolvedor para atalhos (Shift+R, Shift+O) funcionarem:
define config.developer = False

# Variáveis Globais (Estado do Jogador e Mundo)
default dialog_mode = "predef" # "predef", "livre" ou "hibrido"
default eldrin_trust = 0
default has_wand = False
default has_potion = False
default secret_passage_open = False
default cauldron_water = False
default cauldron_fire = False
default read_mural = False

# ==============================================================
label start:
    scene black

    # Seleção de Modo de Diálogo
    menu select_mode:
        "Bem-vindo à Torre de Aethra.\nEscolha o Modo de Diálogo para este teste:"

        "1. Modo Pré-Definido (Opções Fixas / Clássico)":
            $ dialog_mode = "predef"
            jump intro_predef

        "2. Modo Livre (Input Texto para a IA)":
            "O Modo Livre ainda está em desenvolvimento."
            jump select_mode

        "3. Modo Híbrido (Intenções + IA)":
            "O Modo Híbrido ainda está em desenvolvimento."
            jump select_mode

    return

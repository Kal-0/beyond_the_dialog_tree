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
default player_email = ""
default dialog_mode = "predef" # "predef", "livre" ou "hibrido"
default senha_porta = "verdade"
default eldrin_trust = 0
default has_wand = False
default has_potion = False
default secret_passage_open = False
default cauldron_water = False
default cauldron_fire = False
default read_mural = False
default eldrin_revealed_password = False
default knows_porta_needs_password = False
default has_ingredients = False
default potion_ready_for_lumos = False

# Variável p/ controle de sala e estado mágico:
default current_room = ""
default wand_active = False

# Awareness & Gating Flags
default met_eldrin = False
default met_skulla = False
default met_nekrons = False
default met_aurelium = False

default brute_force_count = 0
default examined_porta = False
default examined_estante_porta = False
default asked_if_testing = False
default seen_choices_set = set()
default asked_magia = False
default asked_encarando = False

# Mural Reaction Flags (Modo Livre — cada NPC reage 1 vez ao mural)
default eldrin_reacted_mural = False
default skulla_reacted_mural = False
default nekrons_reacted_mural = False
default aurelium_reacted_mural = False

default knows_oficina = False
default knows_observatorio = False
default knows_biblioteca = False
default knows_invocation_secret = False
default knows_vision_potion = False
default knows_secret = False

default has_key_biblioteca = False
default has_key_oficina = False
default has_key_observatorio = False

# Histórico de chat isolado por NPC (Modo Livre)
default eldrin_chat_history = [
    {"role": "user", "content": "(O jogador desperta no chão de pedra fria, confuso.)"},
    {"role": "assistant", "content": "Finalmente acordou. Não se mova rápido demais, forasteiro. Seus sentidos ainda não se ajustaram a este lugar. Você está na Torre de Aethra. Um santuário de memórias esquecidas... Não me pergunte como veio parar aqui. Esta torre atrai almas por razões que fogem até à minha compreensão. Eu sou Eldrin. Guardião deste lugar, ou o que sobrou de um. Vejo confusão nos seus olhos. Não, você não pode simplesmente sair. A porta atrás de mim está selada e não responde à pressa. Se pretende tocar em qualquer coisa aqui, faça isso com cuidado. Explore, observe, e talvez... talvez eu decida que vale a pena ajudá-lo."}
]
default skulla_chat_history = []
default nekrons_chat_history = []
default aurelium_chat_history = []

# ==============================================================
label start:
    scene black
    
    # --- Coleta de email para métricas acadêmicas ---
    "Este jogo faz parte de um Trabalho de Conclusão de Curso (TCC)."
    "Métricas anônimas de gameplay serão coletadas para fins acadêmicos."
    "Por favor, informe seu email para identificação:"
    
    python:
        _email = renpy.input("Seu email:", length=60)
        player_email = _email.strip()
    
    # Iniciar timer de métricas
    $ game_metrics.start_timer()
    
    # Seleção de Modo de Diálogo
    menu select_mode:
        "Bem-vindo à Torre de Aethra.\nEscolha o Modo de Diálogo para este teste:"

        "1. Modo Pré-Definido (Opções Fixas / Clássico)":
            $ dialog_mode = "predef"
            jump show_tutorial

        "2. Modo Livre (Input Texto para a IA)":
            $ dialog_mode = "livre"
            jump show_tutorial

        "3. Modo Híbrido (Opções + Texto Livre)":
            $ dialog_mode = "hibrido"
            jump show_tutorial

label show_tutorial:
    scene black
    "Antes de começarmos, algumas instruções importantes:"
    "Este é um jogo Point-and-Click de exploração e mistério."
    "Sua principal ferramenta para progredir, descobrir segredos e entender o que fazer é o DIÁLOGO."
    "Explore os cenários clicando nos elementos, mas, acima de tudo, CONVERSE com os personagens."
    "Eles detêm as chaves para o seu progresso."
    jump intro_predef

    return

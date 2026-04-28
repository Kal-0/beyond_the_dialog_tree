# ==============================================================
# MODO PRÉ-DEFINIDO (Loops Centrais, Hub e Motor Mágico)
# ==============================================================

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
default asked_veritas = False
default asked_encarando = False

default knows_oficina = False
default knows_observatorio = False

default has_key_biblioteca = False
default has_key_oficina = False
default has_key_observatorio = False

init python:
    def log_event(text):
        store.custom_log.append(text)
        
    def check_potion_ingredients(i1, i2, i3):
        ing_str = (i1 + " " + i2 + " " + i3).lower()
        return "cristal" in ing_str and "folha" in ing_str and "raiz" in ing_str

label intro_predef:
    scene black
    "Há lugares que não foram abandonados. Foram esquecidos."
    
    scene bg porta_selada with fade
    "Você desperta no chão de pedra fria. A cabeça dói. Há um zumbido arcano no ar."
    "À sua frente, uma grande porta selada por runas pulsa com luz fraca. Estantes de livros ocupam as paredes laterais."
    
    show eldrin normal at center with dissolve
    eldrin "Finalmente acordou. Você está na Torre de Aethra. E, antes que pergunte, sim... ainda há magia aqui."
    $ log_event("Eldrin: Finalmente acordou. Você está na Torre de Aethra.")

    menu dialog_intro:
        "Onde estou?":
            $ log_event("Player: Onde estou?")
            eldrin "Uma torre esquecida. Um lugar onde o que foi apagado ainda insiste em permanecer."
            $ log_event("Eldrin: Uma torre esquecida. Um lugar onde o que foi apagado ainda insiste em permanecer.")
        
        "Quem é você?":
            $ log_event("Player: Quem é você?")
            eldrin "Meu nome é Eldrin. Guardião desta torre. Ou o que restou dela."
            $ log_event("Eldrin: Meu nome é Eldrin. Guardião desta torre. Ou o que restou dela.")
        
        "Quero sair daqui.":
            $ log_event("Player: Quero sair daqui.")
            eldrin "Então terá de fazer mais do que desejar isso. A porta não responde à pressa."
            $ log_event("Eldrin: Então terá de fazer mais do que desejar isso. A porta não responde à pressa.")

    eldrin "Se quer sair, primeiro vai precisar entender este lugar. E, se pretende tocar em qualquer coisa aqui, faça isso com cuidado."
    
    hide eldrin normal with dissolve
    
    # Inicia a HUD no topo (Mapa, Log, Varinha)
    show screen in_game_hud
    jump sala_porta

# ==============================================================
# LOOPS DAS SALAS (O Motor Point n' Click Cênico)
# ==============================================================
label sala_porta:
    $ current_room = "porta"
    scene bg porta_selada with dissolve
    
label sala_porta_loop:
    call screen click_sala_porta

label sala_oficina:
    $ current_room = "oficina"
    if has_potion:
        scene bg oficina_caldeirao_pocao with dissolve
    elif cauldron_water and cauldron_fire:
        scene bg oficina_caldeirao_agua_aceso with dissolve
    elif cauldron_water:
        scene bg oficina_caldeirao_agua with dissolve
    elif cauldron_fire:
        scene bg oficina_caldeirao_aceso with dissolve
    else:
        scene bg oficina with dissolve
    
label sala_oficina_loop:
    call screen click_sala_oficina

label sala_observatorio:
    $ current_room = "observatorio"
    if has_wand:
        scene bg observatorio_sem_varinha with dissolve
    else:
        scene bg observatorio with dissolve
    
label sala_observatorio_loop:
    call screen click_sala_observatorio

label sala_biblioteca:
    $ current_room = "biblioteca"
    
    if secret_passage_open:
        scene bg biblioteca_passagem with dissolve
    elif has_potion:
        scene bg biblioteca_revelare with dissolve
    else:
        scene bg biblioteca with dissolve
    
label sala_biblioteca_loop:
    call screen click_sala_biblioteca

label sala_secreta:
    $ current_room = "secreta"
    scene bg sala_secreta with dissolve
    "Você adentra a catacumba esquecida de arquivos proibidos."
    "As paredes da caverna escura exalam solidão e remorso. Você nota algo arranhado adiante."
    
label sala_secreta_loop:
    call screen click_sala_secreta

# Roteador para reaproveitamento limpo:
label router_current_room:
    if current_room == "porta":
        jump sala_porta_loop
    elif current_room == "oficina":
        jump sala_oficina_loop
    elif current_room == "observatorio":
        jump sala_observatorio_loop
    elif current_room == "biblioteca":
        jump sala_biblioteca_loop
    elif current_room == "secreta":
        jump sala_secreta_loop
    jump sala_porta_loop

# ==============================================================
# MOTOR LÓGICO DE FEITIÇOS MANUAIS
# ==============================================================
label handle_wand:
    if not wand_active:
        "A varinha de cristal encontra-se morta e pesada em suas mãos."
        "Você sente que precisa acendê-la com uma centelha de pura luz em um ambiente de contemplação celeste antes de brandir feitiços."
        jump router_current_room

    call screen custom_spell_input
    
    python:
        spell = _return.strip().lower()
        if spell != "":
            log_event("Player encanta: '" + spell + "'")

    if spell != "":
        call cast_spell_logic(spell)
    
    jump router_current_room


label cast_spell_logic(spell):
    
    if "ignis" in spell:
        if current_room == "oficina":
            $ cauldron_fire = True
            "Um fogo caloroso se acende debaixo do caldeirão."
            if cauldron_water:
                scene bg oficina_caldeirao_agua_aceso with dissolve
            else:
                scene bg oficina_caldeirao_aceso with dissolve
        else:
            show nekrons at center with dissolve
            nekrons "Não brinque com faíscas perto de mim."
            hide nekrons with dissolve
            
    elif "aqua" in spell:
        if current_room == "oficina":
            $ cauldron_water = True
            "Um jato límpido enche o caldeirão."
            if cauldron_fire:
                scene bg oficina_caldeirao_agua_aceso with dissolve
            else:
                scene bg oficina_caldeirao_agua with dissolve
        else:
            show aurelium_book at center with dissolve
            aurelium "Guarde seus instintos! Água arruinará minhas páginas imbecil!"
            hide aurelium_book with dissolve
            
    elif "revelare" in spell:
        if current_room == "biblioteca" and has_potion:
            $ secret_passage_open = True
            scene bg biblioteca_passagem with vpunch
            "As pedras tremem e a enorme estante despenca para a lateral, revelando uma tumba poeirenta."
            show aurelium_book at center with dissolve
            aurelium "Você a abriu..."
            hide aurelium_book with dissolve
            $ log_event("Player abriu a Passagem Secreta com Revelare.")
        else:
            "Meras fagulhas sem rumo pingam no chão. Faltou claridade ou lugar propício."
    else:
        "O espaço distorce levemente e depois morre. Nada relevante ocorreu."
        
    return

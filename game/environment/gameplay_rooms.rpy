# ==============================================================
# MODO PRÉ-DEFINIDO (Loops Centrais, Hub e Motor Mágico)
# ==============================================================

# Variáveis movidas para script.rpy para centralização.

init python:
    def log_event(text):
        store.custom_log.append(text)
        # Registrar métrica de gameplay automaticamente
        if hasattr(store, 'game_metrics') and store.game_metrics:
            store.game_metrics.record_gameplay()
        
    def check_potion_ingredients(i1, i2, i3):
        ing_str = (i1 + " " + i2 + " " + i3).lower()
        return store.ingred_1 in ing_str and store.ingred_2 in ing_str and store.ingred_3 in ing_str

label intro_predef:
    scene black
    "Há lugares que não foram abandonados. Foram esquecidos."
    
    scene bg porta_selada with fade
    "*Você desperta no chão de pedra fria, sua cabeça dói.*"
    "Há um zumbido arcano no ar. Você não faz ideia de como chegou aqui, mas sente que deveria ir embora o mais rápido possível."
    "À sua frente, você vê uma grande porta marcada por runas que pulsam com uma luz fraca. Estantes de livros velhos ocupam as paredes laterais."
    
    show eldrin normal at center with dissolve
    eldrin "Finalmente acordou."
    eldrin "Não se mova rápido demais, forasteiro. Seus sentidos ainda não se ajustaram a este lugar."
    eldrin "Você está na Torre de Aethra. Um santuário de memórias esquecidas... Não me pergunte como veio parar aqui. Esta torre atrai almas por razões que fogem até à minha compreensão."
    eldrin "Eu sou Eldrin. Guardião deste lugar, ou o que sobrou de um."
    eldrin "Vejo confusão nos seus olhos. Não, você não pode simplesmente sair. A porta atrás de mim está selada e não responde à pressa."
    eldrin "Se pretende tocar em qualquer coisa aqui, faça isso com cuidado. Explore, observe, e talvez... talvez eu decida que vale a pena ajudá-lo."
    
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
    "As paredes da caverna escura exalam solidão e remorso. Você nota diversos diagramas e escrituras arranhados adiante."
    
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
    $ spell = ""
    call screen custom_spell_input
    $ spell = _return.strip().lower() if _return else ""

    if not wand_active:
        if spell_light in spell:
            with vpunch
            "Ao proferir a palavra, a varinha ressoa com sua intenção. Uma luz prateada percorre o cristal opaco!"
            "A varinha desperta em suas mãos. Agora ela está pronta para canalizar feitiços."
            $ wand_active = True
            $ log_event("Player reativou a varinha com [spell_light].")
        elif spell != "":
            "A varinha de cristal encontra-se fria e pesada. Você tenta canalizar a magia, mas ela permanece inerte."
            "Você sente que precisa reanimá-la antes de brandir feitiços."
        jump router_current_room

    if spell != "":
        $ log_event("Player encanta: '" + spell + "'")
        call cast_spell_logic(spell) from _call_cast_spell_logic
    
    jump router_current_room


label cast_spell_logic(spell):
    
    if spell_fire in spell:
        if current_room == "oficina":
            $ cauldron_fire = True
            "Um fogo caloroso se acende debaixo do caldeirão."
            if cauldron_water:
                scene bg oficina_caldeirao_agua_aceso with dissolve
            else:
                scene bg oficina_caldeirao_aceso with dissolve
        else:
            "(Melhor não. Soltar fogo aqui poderia danificar algo importante.)"
            
    elif spell_water in spell:
        if current_room == "oficina":
            $ cauldron_water = True
            "Um jato límpido enche o caldeirão."
            if cauldron_fire:
                scene bg oficina_caldeirao_agua_aceso with dissolve
            else:
                scene bg oficina_caldeirao_agua with dissolve
        else:
            "(Água mágica aqui? Não parece uma boa ideia, posso arruinar algo.)"
            
    elif spell_light in spell:
        if current_room == "oficina" and potion_ready_for_lumos:
            "A ponta da varinha brilha intensamente. Ao tocar a superfície da mistura, a poção reage e assume um brilho azulado, suave como o luar!"
            "Você a engole em um gole só. Seus olhos ardem e se enchem de luz!"
            $ has_potion = True
            $ potion_ready_for_lumos = False
            $ log_event("Player finalizou e bebeu a Poção de Visão Arcana usando [spell_light].")
            "Você agora tem a {color=#ffd700}Visão Arcana{/color}."
            scene bg oficina_caldeirao_pocao with dissolve
        else:
            "Uma forte luz cinza azulada sai da varinha."
            
    elif "revelare" in spell:
        if current_room == "biblioteca" and has_potion:
            $ secret_passage_open = True
            scene bg biblioteca_passagem with vpunch
            "As pedras tremem e a enorme estante se abre para as laterais, revelando uma passagem oculta."
            show aurelium_book at center with dissolve
            aurelium "Você a abriu..."
            hide aurelium_book with dissolve
            $ log_event("Player abriu a Passagem Secreta com Revelare.")
        elif current_room == "biblioteca" and not has_potion:
            "Você sente uma leve vibração na estante, mas nada acontece. Talvez precise ver algo que seus olhos normais não enxergam..."
        else:
            "Meras fagulhas sem rumo pingam no chão. Não há nada para revelar aqui."
    else:
        "O espaço distorce levemente e depois morre. Nada relevante ocorreu."
        
    return

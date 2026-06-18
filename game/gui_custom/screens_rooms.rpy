# ==============================================================
# TELAS VISUAIS DO MODO PRÉ-DEFINIDO (Overlays e Point n' Click)
# ==============================================================

screen map_overlay():
    zorder 200
    modal True
    key "game_menu" action Hide("map_overlay")
    frame:
        align (0.5, 0.5)
        xpadding 50 ypadding 50
        background Solid("#151515ee")
        vbox:
            spacing 20
            text "MAPA DA TORRE" size 40 bold True color "#d6b55c" xalign 0.5
            null height 15
            textbutton "Porta Selada" action [Hide("map_overlay"), Jump("sala_porta")] xalign 0.5 text_size 30
            if has_key_oficina:
                textbutton "Oficina Alquímica" action [Hide("map_overlay"), Jump("sala_oficina")] xalign 0.5 text_size 30
            if has_key_observatorio:
                textbutton "Observatório" action [Hide("map_overlay"), Jump("sala_observatorio")] xalign 0.5 text_size 30
            if has_key_biblioteca:
                textbutton "Biblioteca Arcana" action [Hide("map_overlay"), Jump("sala_biblioteca")] xalign 0.5 text_size 30
            null height 20
            textbutton "Fechar Mapa" action Hide("map_overlay") xalign 0.5 text_size 25

screen click_sala_porta():
    button:
        xpos 1100 ypos 380 xsize 150 ysize 500
        background Solid("#ff000055" if config.developer else "#00000000")
        action Jump("falar_eldrin_porta")
        tooltip "Conversar com Eldrin"

    button:
        xpos 750 ypos 240 xsize 300 ysize 550
        background Solid("#0000ff55" if config.developer else "#00000000")
        action Jump("interagir_porta_selada")
        tooltip "Examinar a Porta"
        
    button:
        xpos 1430 ypos 200 xsize 300 ysize 600
        background Solid("#00ff0055" if config.developer else "#00000000")
        action Jump("interagir_estante_porta")
        tooltip "Examinar as Estantes Emporeiradas"

screen click_sala_oficina():
    button:
        xpos 1300 ypos 230 xsize 200 ysize 250
        background Solid("#ff000055" if config.developer else "#00000000")
        action Jump("falar_skulla_oficina")
        tooltip "Conversar com Skulla"

    button:
        xpos 920 ypos 500 xsize 380 ysize 400
        background Solid("#0000ff55" if config.developer else "#00000000")
        action Jump("interagir_caldeirao")
        tooltip "Examinar Caldeirão"

    button:
        xpos 200 ypos 450 xsize 600 ysize 300
        background Solid("#00ff0055" if config.developer else "#00000000")
        action Jump("interagir_mesa_ingredientes")
        tooltip "Examinar Mesa de Ingredientes"

screen click_sala_observatorio():
    button:
        xpos 800 ypos 650 xsize 200 ysize 300
        background Solid("#ff000055" if config.developer else "#00000000")
        action Jump("falar_nekrons_obs")
        tooltip "Conversar com Nekrons"

    if not has_wand:
        button:
            xpos 350 ypos 550 xsize 240 ysize 110
            background Solid("#0000ff55" if config.developer else "#00000000")
            action Jump("interagir_mesa_varinha")
            tooltip "Examinar Mesa Central"

screen click_sala_biblioteca():
    # AURELIUM
    button:
        xpos 700 ypos 470 xsize 280 ysize 200
        background Solid("#ff000055" if config.developer else "#00000000")
        action Jump("falar_aurelium_bib")
        tooltip "Conversar com Aurelium"

    # ESTANTE DE LIVROS E PASSAGEM
    button:
        xpos 1350 ypos 150 xsize 300 ysize 600
        background Solid("#00ff0055" if config.developer else "#00000000")
        action Jump("interagir_estante_bib")
        tooltip "Examinar Estante de Livros"

screen click_sala_secreta():
    # MURAL
    button:
        xpos 750 ypos 200 xsize 500 ysize 400
        background Solid("#ff000055" if config.developer else "#00000000")
        action Jump("ler_mural_secreta")
        tooltip "Ler Anotações Sangrentas"

    # SAÍDA
    button:
        xpos 1400 ypos 200 xsize 200 ysize 500
        background Solid("#0000ff55" if config.developer else "#00000000")
        action Jump("sair_sala_secreta")
        tooltip "Retornar à Biblioteca"

screen custom_spell_input():
    zorder 200
    modal True
    default typed_spell = ""
    key "game_menu" action Return("")
    key "K_RETURN" action Return(typed_spell)
    key "K_KP_ENTER" action Return(typed_spell)
    
    frame:
        align (0.5, 0.5)
        xpadding 40 ypadding 40
        background Solid("#1c112edd") 
        vbox:
            spacing 20
            text "Empunhando a Varinha Arcana" size 35 bold True color "#e4baff" xalign 0.5
            text "(Escreva a palavra de poder e clique em Lançar Feitiço)" size 20 xalign 0.5 color "#a3a3a3"
            
            frame:
                background Solid("#000000aa")
                xpadding 20 ypadding 10
                input value ScreenVariableInputValue("typed_spell") length 30 size 35 color "#fff" xalign 0.5
            
            null height 15
            
            hbox:
                xalign 0.5
                spacing 40
                textbutton "Lançar Feitiço" action Return(typed_spell) text_size 25 text_hover_color "#e4baff"
                textbutton "Guardar Varinha (Cancelar)" action Return("") text_size 25 text_hover_color "#ff8888"

screen llm_chat_input(npc_display_name):
    zorder 200
    modal True
    default typed_message = ""
    key "game_menu" action Return("__SAIR__")
    key "K_RETURN" action Return(typed_message)
    key "K_KP_ENTER" action Return(typed_message)
    on "show" action SetScreenVariable("typed_message", "")
    
    frame:
        align (0.5, 0.85)
        xpadding 40 ypadding 30
        xsize 1200
        background Solid("#151520ee")
        vbox:
            spacing 15
            text "Conversando com [npc_display_name]" size 28 bold True color "#d6b55c" xalign 0.5
            text "(Digite o que deseja dizer ou clique em Sair)" size 18 xalign 0.5 color "#888888"
            
            frame:
                background Solid("#000000aa")
                xpadding 20 ypadding 10
                xfill True
                input value ScreenVariableInputValue("typed_message") length 200 size 28 color "#fff"
            
            hbox:
                xalign 0.5
                spacing 40
                textbutton "Enviar" action Return(typed_message) text_size 22 text_hover_color "#88ff88"
                textbutton "Limpar Memória da IA" action Return("__RESET__") text_size 22 text_hover_color "#ffd288"
                textbutton "Sair da Conversa" action Return("__SAIR__") text_size 22 text_hover_color "#ff8888"


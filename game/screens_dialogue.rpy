# ==============================================================
# SCREENS CUSTOMIZADAS PARA SISTEMA DE DIÁLOGOS
# ==============================================================

screen grouped_dialogue_menu(items, group_states=None):
    """
    Screen customizada para menus de diálogo agrupados.
    
    Parametros:
    - items: lista de (label, action) tuples
    - group_states: dict com {group_key: {"exhausted": bool, "has_new": bool}}
    """
    modal True
    zorder 200
    
    vbox:
        xalign 0.5
        yalign 0.8
        spacing 10
        
        for label, action in items:
            button:
                xsize 600
                xysize (600, 50)
                
                # Se a ação é um grupo exaurido, deixar desabilitado
                if isinstance(action, str) and action.startswith("GROUP_"):
                    # Botão de grupo exaurido (cinza/desabilitado)
                    background Frame("gui/button/choice_disabled_background.png", 12, 12)
                    text label:
                        size 18
                        color "#888888"
                        xalign 0.5
                        yalign 0.5
                else:
                    # Botão normal (ativo)
                    background Frame("gui/button/choice_background.png", 12, 12)
                    text label:
                        size 18
                        color "#ffffff"
                        xalign 0.5
                        yalign 0.5
                    action action


screen dialogue_choice_group(group_label, choices):
    """
    Screen para submenu de grupos de diálogo.
    
    Parametros:
    - group_label: nome do grupo
    - choices: lista de (label, action)
    """
    modal True
    zorder 200
    
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 10
        
        text group_label:
            size 24
            xalign 0.5
            color "#ffd700"
        
        null height 20
        
        for label, action in choices:
            button:
                xsize 600
                xysize (600, 50)
                background Frame("gui/button/choice_background.png", 12, 12)
                text label:
                    size 18
                    color "#ffffff"
                    xalign 0.5
                    yalign 0.5
                action action
        
        null height 20
        
        button:
            xsize 200
            xysize (200, 40)
            background Frame("gui/button/choice_background.png", 12, 12)
            text "Voltar":
                size 16
                color "#ffffff"
                xalign 0.5
                yalign 0.5
            action Return("back")

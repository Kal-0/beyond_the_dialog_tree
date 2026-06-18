# ==============================================================
# INTERFACE DE USUÁRIO (HUD) - MAPA, FEITIÇOS E DIÁRIO
# ==============================================================

# Lista para armazenar o diário de conversas
default custom_log = []

# Função auxiliar para o jogador tentar usar a varinha mágica
init python:
    def try_cast_spell():
        spell = renpy.input("Digite as palavras de poder:", length=30)
        spell = spell.strip().lower()
        return spell

# ==============================================================
# SCREEN PRINCIPAL (HUD CONSTANTE)
# ==============================================================
screen in_game_hud():
    zorder 300 # Garante que fique por cima de tudo e dos modais
    
    # Verifica se há conversas ou inputs ativos na tela
    $ in_dialogue = renpy.get_screen("say") or renpy.get_screen("choice") or renpy.get_screen("input")

    # Fundo semi-transparente para organizar os ícones (opcional)
    frame:
        background Solid("#00000088")
        xalign 1.0 yalign 0.0
        xsize 100 ysize 400
        
        vbox:
            spacing 20
            xalign 0.5 yalign 0.1

            # 1. BOTÃO DE MAPA (Navegação)
            imagebutton:
                idle "icon_map"
                hover "icon_map"
                action ToggleScreen("map_overlay")
                tooltip "Mapa da Torre"

            # 2. BOTÃO DE DIÁRIO / LOG
            imagebutton:
                idle "icon_journal"
                hover "icon_journal"
                action ToggleScreen("chat_log_screen")
                tooltip "Diário Arcano"

            # 3. BOTÃO DE VARINHA (Só visível se has_wand for True)
            if has_wand:
                imagebutton:
                    idle "icon_wand"
                    hover "icon_wand"
                    action If(not in_dialogue, Jump("handle_wand"), None)
                    tooltip "Usar Feitiços"

# ==============================================================
# SCREEN DO DIÁRIO (LOG)
# ==============================================================
screen chat_log_screen():
    zorder 400
    modal True # Bloqueia clique fora enquanto aberto
    key "game_menu" action Hide("chat_log_screen") # Fecha com ESC
    key "K_RETURN" action Hide("chat_log_screen") # Fecha com ENTER
    key "K_KP_ENTER" action Hide("chat_log_screen")

    default log_adj = ui.adjustment()

    frame:
        background Solid("#1c1c1ce6") # Escuro e levemente transparente
        xalign 0.5 yalign 0.5
        xsize 800 ysize 600
        
        vbox:
            text "DIÁRIO ARCANO (Log de Conversas)" size 30 xalign 0.5 bold True color "#d6b55c"
            null height 20

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                yfill False
                ymaximum 450
                yinitial 1.0
                
                vbox:
                    spacing 15
                    for entry in custom_log:
                        $ entry_str = str(entry) if entry else ""
                        $ who_str = ""
                        $ what_str = entry_str
                        $ c_color = "#cdd6f4"
                        $ name_color = "#ffffff"
                        
                        if ":" in entry_str:
                            $ parts = entry_str.split(":", 1)
                            $ who_str = parts[0].strip()
                            $ what_str = parts[1].strip()
                            
                            if who_str in ("Player", "Você"):
                                $ name_color = "#a6e3a1" # Verde claro
                                $ c_color = "#e5f4e3"
                            elif who_str == "Narração":
                                $ name_color = "#a3a3a3"
                                $ c_color = "#a3a3a3"
                            elif who_str == "Eldrin":
                                $ name_color = "#a3a3a3"
                            elif who_str == "Skulla":
                                $ name_color = "#e0e0e0"
                            elif who_str == "Nekrons":
                                $ name_color = "#b48ead" # Roxo suave
                            elif who_str == "Aurelium":
                                $ name_color = "#ffd700"
                        
                        if entry_str.startswith("[SISTEMA]") or entry_str.startswith("[ERRO"):
                            $ final_text = "{color=#ff9e9e}{i}" + entry_str + "{/i}{/color}"
                            text final_text size 20 substitute False
                        elif who_str:
                            $ final_text = "{b}{color=" + name_color + "}" + who_str + ":{/color}{/b} {color=" + c_color + "}" + what_str + "{/color}"
                            text final_text size 20 substitute False
                        else:
                            $ final_text = "{color=#cdd6f4}" + entry_str + "{/color}"
                            text final_text size 20 substitute False

            null height 20
            textbutton "Fechar" action Hide("chat_log_screen") xalign 0.5 text_size 25

    on "show" action Function(log_adj.change, log_adj.range)


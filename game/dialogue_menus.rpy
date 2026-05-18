# ==============================================================
# CAMADA 2B: MENUS DINÂMICOS (SHARED)
# ==============================================================

# Esta tela substitui os blocos "menu:" hardcoded do Ren'Py.
# Ela é agnóstica em relação ao NPC, gerando os botões com base
# nas funções da camada CORE e SHARED.

screen npc_dialog_menu(npc_name, active_group=None):
    style_prefix "choice"

    vbox:
        if active_group is None:
            # --------------------------------------------------
            # EXIBIÇÃO DE GRUPOS (TÓPICOS PAIS)
            # --------------------------------------------------
            $ groups = get_available_groups_for_npc(npc_name)
            for g_key in groups:
                $ display_text = get_group_display_label(npc_name, g_key)
                textbutton display_text:
                    # Retorna um comando de string seguro para evitar previsão de tela
                    action Return(f"group_{g_key}")
            
            # Botão padrão de encerramento
            textbutton "Encerrar conversa":
                action Return("end_dialog")
                
        else:
            # --------------------------------------------------
            # EXIBIÇÃO DE TÓPICOS FILHOS
            # --------------------------------------------------
            $ topics = get_topics_by_group(npc_name, active_group)
            for t_key in topics:
                $ display_text = get_topic_display_label(npc_name, t_key)
                textbutton display_text:
                    action Return(f"topic_{t_key}")
            
            textbutton "← Voltar ao menu principal":
                action Return("back_to_main")

# Label auxiliar para chamar o menu em loop estruturado como Árvore
label call_npc_dialog(npc_name, idle_jump_label, start_group=None):
    $ _active_group = start_group
    
    label .menu_loop:
        call screen npc_dialog_menu(npc_name, _active_group)
        
        if _return == "end_dialog":
            jump expression idle_jump_label
            
        elif _return == "back_to_main":
            $ _active_group = None
            jump .menu_loop
            
        elif _return.startswith("group_"):
            $ group_key = _return.replace("group_", "")
            $ mark_topic_seen(npc_name, f"group_{group_key}")
            # Chama a fala introdutória do Tópico Pai
            call expression f"dialog_{npc_name}_group_{group_key}"
            # Após a fala, abre as perguntas filhas deste grupo
            $ _active_group = group_key
            jump .menu_loop
            
        elif _return.startswith("topic_"):
            $ topic_key = _return.replace("topic_", "")
            $ mark_topic_seen(npc_name, topic_key)
            call expression f"dialog_{npc_name}_{topic_key}"
            jump .menu_loop

# ==============================================================
# CAMADA 2A: LÓGICA COMPARTILHADA (SHARED) E FILTROS DE TÓPICOS
# ==============================================================

init python:
    # ----------------------------------------------------------
    # PROCESSAMENTO DE REQUISITOS (GATES)
    # ----------------------------------------------------------
    def is_topic_unlocked(npc, topic_dict):
        """Avalia os requisitos de um tópico baseado no estado do jogo."""
        reqs = topic_dict.get("requires", {})
        
        # Min/Max Trust de Eldrin
        if "min_trust" in reqs and getattr(store, "eldrin_trust", 0) < reqs["min_trust"]:
            return False
        if "max_trust" in reqs and getattr(store, "eldrin_trust", 0) > reqs["max_trust"]:
            return False
            
        # Variáveis globais do script (como has_wand, has_key_biblioteca)
        if "var" in reqs:
            if not getattr(store, reqs["var"], False):
                return False
        if "not_var" in reqs:
            if getattr(store, reqs["not_var"], False):
                return False
                
        # Tópicos já vistos / não vistos
        if "seen" in reqs:
            for t in reqs["seen"]:
                if f"{npc}_{t}" not in story_state["seen_topics"] and f"{npc}_{t}" not in store.seen_choices_set:
                    return False
        if "not_seen" in reqs:
            for t in reqs["not_seen"]:
                if f"{npc}_{t}" in story_state["seen_topics"] or f"{npc}_{t}" in store.seen_choices_set:
                    return False
                    
        return True

    # ----------------------------------------------------------
    # RETORNO DE TÓPICOS PARA MENUS
    # ----------------------------------------------------------
    def get_available_groups_for_npc(npc):
        """Retorna a lista de chaves de grupos que possuem pelo menos 1 tópico destrancado."""
        available_groups = []
        if npc not in NPC_TOPICS:
            return available_groups
            
        groups = NPC_TOPICS[npc]["groups"]
        topics = NPC_TOPICS[npc]["topics"]
        
        for g_key, g_data in groups.items():
            if not is_topic_unlocked(npc, g_data):
                continue
                
            # Verifica se tem algum topico desse grupo liberado
            for t_key, t_data in topics.items():
                if t_data["group"] == g_key and is_topic_unlocked(npc, t_data):
                    available_groups.append(g_key)
                    break
                    
        return available_groups

    def get_topics_by_group(npc, group_key):
        """Retorna a lista de chaves de tópicos de um grupo específico que estão liberados."""
        available_topics = []
        if npc not in NPC_TOPICS:
            return available_topics
            
        topics = NPC_TOPICS[npc]["topics"]
        for t_key, t_data in topics.items():
            if t_data["group"] == group_key and is_topic_unlocked(npc, t_data):
                available_topics.append(t_key)
                
        return available_topics

    # ----------------------------------------------------------
    # LÓGICA DE EXAUSTÃO (DIMMING/ESCURECER OPÇÕES)
    # ----------------------------------------------------------
    def is_group_exhausted(npc, group_key):
        """Um grupo está exaurido se TODOS os tópicos atualmente desbloqueados dentro dele já foram vistos."""
        available_topics = get_topics_by_group(npc, group_key)
        
        if not available_topics:
            return False
            
        for t_key in available_topics:
            if not is_topic_seen(npc, t_key):
                return False
                
        return True

    def get_group_display_label(npc, group_key):
        """Retorna o texto do botão do grupo. Adiciona tag de cor ou texto se exaurido."""
        base_label = NPC_TOPICS[npc]["groups"][group_key]["label"]
        if is_group_exhausted(npc, group_key):
            return f"{{color=#666666}}{base_label}{{/color}}"
            
        if group_key == "a_verdade":
            return f"{{color=#ffcc00}}{base_label}{{/color}}"
            
        return base_label

    def get_topic_display_label(npc, topic_key):
        """Retorna o texto do botão do tópico. Adiciona tag de cor se exaurido."""
        base_label = NPC_TOPICS[npc]["topics"][topic_key]["label"]
        if is_topic_seen(npc, topic_key):
            return f"{{color=#666666}}{base_label}{{/color}}"
            
        if topic_key in ["quebrar_selo", "ir_embora"]:
            return f"{{b}}{{color=#ff5555}}{base_label}{{/color}}{{/b}}"
            
        return base_label

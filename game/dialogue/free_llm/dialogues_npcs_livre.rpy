# ==============================================================
# DIÁLOGOS DOS NPCS - MODO LIVRE (JSON PARSING)
# ==============================================================

init python:
    import llm_api
    import re
    import json

    def split_dialogue_text(text, max_length=180):
        """
        Quebra um texto longo em partes menores para caber nas caixas de diálogo do Ren'Py.
        Prioriza quebras de linha naturais (parágrafos) e, se necessário, pontuações.
        """
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        chunks = []
        for p in paragraphs:
            if len(p) <= max_length:
                chunks.append(p)
            else:
                sentences = re.split(r'(?<=[.!?])\s+', p)
                current_chunk = ""
                for s in sentences:
                    if not current_chunk:
                        current_chunk = s
                    elif len(current_chunk) + len(s) + 1 <= max_length:
                        current_chunk += " " + s
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = s
                if current_chunk:
                    chunks.append(current_chunk.strip())
        return chunks if chunks else ["..."]

    def highlight_keywords(text):
        """
        Aplica a cor dourada automaticamente a palavras-chave no texto do LLM.
        """
        keywords = [
            "Biblioteca Arcana", "Oficina Alquímica", "Observatório das Estrelas",
            "Poção de Visão Arcana", "Veritas manet quod oblivio delet",
            "varinha antiga", "estante de pedra", "Observatório", "Biblioteca", 
            "Oficina", "Poção", "Veritas", "Lumos", "varinha", "estante", "selo", "senha"
        ]
        
        # Cria a regex ignorando caixa alta/baixa, buscando as palavras inteiras (\b)
        pattern = re.compile(r'\b(' + '|'.join(re.escape(kw) for kw in keywords) + r')\b', re.IGNORECASE)
        
        def replace_fn(match):
            return f"{{color=#ffd700}}{match.group(0)}{{/color}}"
            
        return pattern.sub(replace_fn, text)

    def analisar_eventos_do_texto(npc_name, raw_response):
        """
        Recebe a resposta bruta do LLM (que deve ser um JSON), extrai as variáveis
        para a engine do jogo, e retorna apenas o texto do diálogo limpo.
        """
        # LOGGING PARA ARQUIVO (DEBUG PARA O JOGADOR)
        try:
            with open(config.basedir + "/llm_debug_log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{npc_name.upper()}] RAW OUTPUT: {raw_response}\n")
        except:
            pass

        # 1. Tentativa de extrair o bloco JSON da string bruta
        # O Regex busca tudo entre a primeira chave { e a última chave }
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        
        if not match:
            # Fallback se o LLM falhou miseravelmente em retornar JSON
            store.custom_log.append(f"[ERRO JSON] Nenhum bloco JSON encontrado para {npc_name}.")
            return "(O personagem parece não entender o que você disse ou sua fala se perdeu no éter. Tente falar de outra forma.)"
            
        json_str = match.group(0)
        
        try:
            data = json.loads(json_str)
        except Exception as e:
            store.custom_log.append(f"[ERRO PARSE] Falha ao ler JSON: {e}")
            return "(A mente do personagem parece fragmentada. Tente novamente.)"

        # 2. Extrai o texto do diálogo
        dialogo = data.get("dialogo", "...")
        
        # 3. Aplica as variáveis dependendo do NPC
        if npc_name == "eldrin":
            # Trust Change
            trust_change = data.get("trust_change", 0)
            if trust_change > 0:
                store.eldrin_trust += 1
                store.custom_log.append("[SISTEMA] Eldrin Trust +1 via JSON.")
            elif trust_change < 0:
                store.eldrin_trust -= 1
                store.custom_log.append("[SISTEMA] Eldrin Trust -1 via JSON.")
                
            # Porta precisa de senha
            if data.get("unlock_porta_needs_password") and not store.knows_porta_needs_password:
                store.knows_porta_needs_password = True
                renpy.notify("Você descobriu que a porta selada exige uma senha.")
                store.custom_log.append("[SISTEMA] Eldrin indicou senha da porta via JSON.")
                
            # Chave da Oficina
            if data.get("unlock_key_oficina") and not store.has_key_oficina:
                store.has_key_oficina = True
                store.knows_oficina = True
                renpy.notify("Você obteve a chave da Oficina Alquímica!")
                store.custom_log.append("[SISTEMA] Eldrin deu a chave da Oficina via JSON.")
                
            # Chave do Observatório
            if data.get("unlock_key_observatorio") and not store.has_key_observatorio:
                store.has_key_observatorio = True
                store.knows_observatorio = True
                renpy.notify("Você obteve a chave do Observatório!")
                store.custom_log.append("[SISTEMA] Eldrin deu a chave do Observatório via JSON.")
                
            # Chave da Biblioteca
            if data.get("unlock_key_biblioteca") and not store.has_key_biblioteca:
                store.has_key_biblioteca = True
                store.knows_biblioteca = True
                renpy.notify("Você obteve a chave da Biblioteca Arcana!")
                store.custom_log.append("[SISTEMA] Eldrin deu a chave da Biblioteca via JSON.")
                
            # Senha Final
            if data.get("revealed_final_password") and not store.eldrin_revealed_password:
                store.eldrin_revealed_password = True
                store.knows_porta_needs_password = True
                renpy.notify("Você descobriu a senha do selo: " + store.senha_porta.capitalize() + "!")
                store.custom_log.append("[SISTEMA] Eldrin revelou a senha final via JSON.")

        elif npc_name == "skulla":
            if data.get("reveal_invocation_secret") and not store.knows_invocation_secret:
                store.knows_invocation_secret = True
                renpy.notify("Você descobriu o Segredo da Invocação!")
                store.custom_log.append("[SISTEMA] Skulla revelou o segredo da invocação via JSON.")
            
            if data.get("reveal_observatorio") and not store.knows_observatorio:
                store.knows_observatorio = True
                renpy.notify("Você ouviu sobre o Observatório das Estrelas.")
                store.custom_log.append("[SISTEMA] Skulla indicou o observatório via JSON.")

        elif npc_name == "nekrons":
            if data.get("reveal_biblioteca") and not store.knows_biblioteca:
                store.knows_biblioteca = True
                renpy.notify("Você ouviu sobre a Biblioteca Arcana.")
                store.custom_log.append("[SISTEMA] Nekrons indicou a biblioteca via JSON.")
                

        elif npc_name == "aurelium":
            if data.get("reveal_oficina") and not store.knows_oficina:
                store.knows_oficina = True
                renpy.notify("Você ouviu sobre a Oficina Alquímica.")
                store.custom_log.append("[SISTEMA] Aurelium indicou a oficina via JSON.")
                
            if data.get("reveal_vision_potion") and not store.knows_vision_potion:
                store.knows_vision_potion = True
                renpy.notify("Você descobriu que precisa de uma poção especial.")
                store.custom_log.append("[SISTEMA] Aurelium indicou a poção via JSON.")

        # Sanitiza a string de diálogo (remove aspas duplas residuais nas pontas)
        dialogo = dialogo.strip()
        dialogo = re.sub(r'^["\']|["\']$', '', dialogo)
        
        return dialogo


    def send_to_llm(npc_name, npc_history, player_input):
        """
        Envia a mensagem do jogador ao LLM e processa a resposta.
        Mantém o JSON bruto no histórico para reforçar o formato.
        """
        messages = build_llm_messages(npc_name, npc_history, player_input)

        try:
            with open(config.basedir + "/llm_debug_log.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{'='*60}\n[{npc_name.upper()}] PAYLOAD ENVIADO NO TURNO:\n")
                f.write(json.dumps(messages, indent=2, ensure_ascii=False) + "\n" + "-"*60 + "\n")
        except:
            pass

        try:
            result_messages = llm_api.completion(messages)
            if not result_messages:
                return "(Erro na API.)"
            assistant_msg = result_messages[-1]
            raw_text = assistant_msg.get("content", "").strip()

            # Salva no histórico a interação (Enviamos o JSON CRU de volta para "treinar" a IA no turno seguinte)
            npc_history.append({"role": "user", "content": player_input})
            npc_history.append({"role": "assistant", "content": raw_text})

            # Extrai os eventos do JSON e retorna apenas a string do diálogo para a UI
            final_dialog_text = analisar_eventos_do_texto(npc_name, raw_text)

            # Aplica destaque nas palavras-chave (cores na UI, que serão filtradas no Log de acordo com assets.rpy)
            final_dialog_text = highlight_keywords(final_dialog_text)

            return final_dialog_text

        except Exception as e:
            error_msg = str(e)
            store.custom_log.append(f"[ERRO API] {error_msg}")
            return "(Uma interferência mágica ocorreu. O personagem está travado.)"


# ==============================================================
# ELDRIN - MODO LIVRE
# ==============================================================

label falar_eldrin_livre:
    if game_metrics:
        $ game_metrics.record_dialog("eldrin")
    show eldrin normal at left with dissolve
    if not met_eldrin:
        $ met_eldrin = True
        $ mark_npc_met("eldrin")
        $ initial_prompt = "(O jogador acabou de se aproximar de você após acordar e ouvir sua apresentação inicial. Como Guardião, reaja à presença dele e inicie a conversa de forma levemente desconfiada e proativa.)"
    else:
        if read_mural and not eldrin_reacted_mural:
            $ eldrin_reacted_mural = True
            $ initial_prompt = "(O jogador acabou de retornar. Você sente que ele descobriu algo importante escondido na torre. Pergunte com cautela e desconfiança o que ele encontrou, demonstrando tensão.)"
        else:
            $ initial_prompt = "(O jogador se aproximou novamente. Faça uma breve saudação proativa de acordo com seu humor atual para retomar a conversa.)"

    $ final_response = send_to_llm("eldrin", eldrin_chat_history, initial_prompt)
    python:
        for part in split_dialogue_text(final_response):
            renpy.say(eldrin, part)

    label .loop:
        $ player_msg = renpy.call_screen("llm_chat_input", "Eldrin")
        
        if player_msg == "__RESET__":
            $ eldrin_chat_history.clear()
            eldrin "(Memória do chat limpa. O personagem esqueceu a conversa atual.)"
            jump .loop

        if player_msg == "__SAIR__" or not player_msg or player_msg.strip() == "":
            eldrin "Hm. Vá então."
            jump falar_eldrin_porta_end
        
        $ store.append_to_custom_log("Você", player_msg.strip())
        $ final_response = send_to_llm("eldrin", eldrin_chat_history, player_msg.strip())
        python:
            for part in split_dialogue_text(final_response):
                renpy.say(eldrin, part)
        jump .loop


# ==============================================================
# SKULLA - MODO LIVRE
# ==============================================================

label falar_skulla_livre:
    if game_metrics:
        $ game_metrics.record_dialog("skulla")
    show skulla at right with dissolve
    if not met_skulla:
        $ met_skulla = True
        $ mark_npc_met("skulla")
        $ initial_prompt = "(O jogador acabou de se aproximar de sua bancada pela primeira vez. Inicie a conversa de forma sarcástica e deboche dele por ser um 'herói perdido', mas já deixe claro que você entende de alquimia e poções.)"
    else:
        if read_mural and not skulla_reacted_mural:
            $ skulla_reacted_mural = True
            $ initial_prompt = "(O jogador voltou. Você ouviu que ele fuçou na torre e descobriu algo secreto. Faça um comentário sarcástico sobre ele ser um curioso, pergunte o que ele descobriu, e quando ele responder sobre a frase do mural, trate a frase com escárnio/deboche e pergunte diretamente: 'Você confia no Eldrin?')"
        else:
            $ initial_prompt = "(O jogador se aproximou novamente do seu caldeirão. Deboche de forma ácida sobre ser incomodada enquanto está morta e pergunte o que ele quer.)"

    $ final_response = send_to_llm("skulla", skulla_chat_history, initial_prompt)
    python:
        for part in split_dialogue_text(final_response):
            renpy.say(skulla, part)

    label .loop:
        $ player_msg = renpy.call_screen("llm_chat_input", "Skulla")
        
        if player_msg == "__RESET__":
            $ skulla_chat_history.clear()
            skulla "(Memória do chat limpa. O personagem esqueceu a conversa atual.)"
            jump .loop

        if player_msg == "__SAIR__" or not player_msg or player_msg.strip() == "":
            skulla "Já vai? Típico."
            jump falar_skulla_oficina_end
        
        $ store.append_to_custom_log("Você", player_msg.strip())
        $ final_response = send_to_llm("skulla", skulla_chat_history, player_msg.strip())
        python:
            for part in split_dialogue_text(final_response):
                renpy.say(skulla, part)
        jump .loop


# ==============================================================
# NEKRONS - MODO LIVRE
# ==============================================================

label falar_nekrons_livre:
    if game_metrics:
        $ game_metrics.record_dialog("nekrons")
    show nekrons at center with dissolve
    if not met_nekrons:
        $ met_nekrons = True
        $ mark_npc_met("nekrons")
        $ initial_prompt = "(O jogador se aproximou do observatório pela primeira vez. Inicie a conversa saudando-o de forma poética e misteriosa sobre os fios do destino não se prenderem a este mundo.)"
    else:
        if read_mural and not nekrons_reacted_mural:
            $ nekrons_reacted_mural = True
            $ initial_prompt = "(O jogador retornou. Você sentiu uma perturbação no éter, como se verdades antigas tivessem sido desenterradas em algum lugar da torre. Comente isso de forma mística e poética, e pergunte ao jogador o que ele encontrou.)"
        else:
            $ initial_prompt = "(O jogador se aproximou novamente. Faça uma saudação mística sobre as centelhas no ar e o retorno dele.)"

    $ final_response = send_to_llm("nekrons", nekrons_chat_history, initial_prompt)
    python:
        for part in split_dialogue_text(final_response):
            renpy.say(nekrons, part)

    label .loop:
        $ player_msg = renpy.call_screen("llm_chat_input", "Nekrons")
        
        if player_msg == "__RESET__":
            $ nekrons_chat_history.clear()
            nekrons "(Memória do chat limpa. O personagem esqueceu a conversa atual.)"
            jump .loop

        if player_msg == "__SAIR__" or not player_msg or player_msg.strip() == "":
            nekrons "O cosmos espera pacientemente."
            jump falar_nekrons_obs_end
        
        $ store.append_to_custom_log("Você", player_msg.strip())
        $ final_response = send_to_llm("nekrons", nekrons_chat_history, player_msg.strip())
        python:
            for part in split_dialogue_text(final_response):
                renpy.say(nekrons, part)
        jump .loop


# ==============================================================
# AURELIUM - MODO LIVRE
# ==============================================================

label falar_aurelium_livre:
    if game_metrics:
        $ game_metrics.record_dialog("aurelium")
    show aurelium_book at center with dissolve
    if not met_aurelium:
        $ met_aurelium = True
        $ mark_npc_met("aurelium")
        $ initial_prompt = "(O jogador acaba de encontrar você, um grimório flutuante gigante, pela primeira vez. Demonstre surpresa, melancolia e um grande anseio por ser lido, já iniciando a conversa proativamente.)"
    else:
        if read_mural and not aurelium_reacted_mural:
            $ aurelium_reacted_mural = True
            $ initial_prompt = "(O jogador voltou à biblioteca. Você sentiu a estante de pedra se abrir e uma energia antiga fluir da passagem secreta. Pergunte ansioso e esperançoso o que ele descobriu lá dentro, demonstrando excitação e curiosidade.)"
        else:
            $ initial_prompt = "(O jogador voltou a falar com você. Faça um breve comentário poético sobre a passagem do tempo ou memórias antes de ouvir o que ele tem a dizer.)"

    $ final_response = send_to_llm("aurelium", aurelium_chat_history, initial_prompt)
    python:
        for part in split_dialogue_text(final_response):
            renpy.say(aurelium, part)

    label .loop:
        $ player_msg = renpy.call_screen("llm_chat_input", "Aurelium")
        
        if player_msg == "__RESET__":
            $ aurelium_chat_history.clear()
            aurelium "(Memória do chat limpa. O personagem esqueceu a conversa atual.)"
            jump .loop

        if player_msg == "__SAIR__" or not player_msg or player_msg.strip() == "":
            aurelium "As páginas se fecham... por ora."
            jump falar_aurelium_bib_end
        
        $ store.append_to_custom_log("Você", player_msg.strip())
        $ final_response = send_to_llm("aurelium", aurelium_chat_history, player_msg.strip())
        python:
            for part in split_dialogue_text(final_response):
                renpy.say(aurelium, part)
        jump .loop

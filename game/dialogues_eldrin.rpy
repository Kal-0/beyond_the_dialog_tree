# ==============================================================
# DIÁLOGOS DO ELDRIN - MODO PRÉ-DEFINIDO COM GRUPOS TEMÁTICOS
# ==============================================================

label falar_eldrin_porta:
    show eldrin normal at left with dissolve
    if not met_eldrin:
        eldrin "Ainda aí. Encontrou algo na base das maçanetas ou só veio me observar?"
        $ met_eldrin = True
    else:
        eldrin "O que deseja agora?"
        
label eldrin_talk_loop:
    menu eldrin_grupos:
        "Sobre Você" if should_show_eldrin_group("sobre_voce"):
            jump eldrin_grupo_sobre_voce
        "Sobre a Porta" if should_show_eldrin_group("sobre_porta"):
            jump eldrin_grupo_sobre_porta
        "Direcionamento" if should_show_eldrin_group("direcionamento"):
            jump eldrin_grupo_direcionamento
        "Explorações" if should_show_eldrin_group("exploracoes"):
            jump eldrin_grupo_exploracoes
        "Sobre Magia" if should_show_eldrin_group("magia"):
            jump eldrin_grupo_magia
        "Encerrar conversa":
            hide eldrin normal with dissolve
            jump sala_porta_loop

    jump eldrin_talk_loop

# ==============================================================
# GRUPO: SOBRE VOCÊ
# ==============================================================

label eldrin_grupo_sobre_voce:
    menu eldrin_sobre_voce:
        "Quem é você, de verdade?":
            $ mark_eldrin_topic_seen("quem_eh")
            eldrin "Alguém que não teve a opção de ir embora. Me chame de Eldrin, se precisar de um nome."
            jump eldrin_talk_loop
            
        "Você está me testando." if not asked_if_testing:
            $ mark_eldrin_topic_seen("testando")
            eldrin "Naturalmente. E você está falhando ou aprendendo, dependendo do próximo passo."
            $ eldrin_trust += 1
            $ asked_if_testing = True
            jump eldrin_talk_loop

        "Como faço para ganhar sua confiança?" if asked_if_testing:
            $ mark_eldrin_topic_seen("confianca")
            eldrin "Observe. Escute. Não tente arrancar respostas antes de entender as perguntas."
            jump eldrin_talk_loop
        
        "← Voltar ao menu":
            jump eldrin_talk_loop

# ==============================================================
# GRUPO: SOBRE A PORTA
# ==============================================================

label eldrin_grupo_sobre_porta:
    menu eldrin_sobre_porta:
        "Por que você guarda esta porta?":
            $ mark_eldrin_topic_seen("por_que_guarda")
            eldrin "Porque o que está lá fora é tão perigoso quanto o que está aqui dentro. O {color=#ffd700}selo{/color} foi um acordo."
            jump eldrin_talk_loop
            
        "A porta está selada por magia antiga, não é?" if examined_porta:
            $ mark_eldrin_topic_seen("selada")
            eldrin "Sim. Um {color=#ffd700}selo{/color} que não se quebra com força. Apenas com entendimento."
            jump eldrin_talk_loop
            
        "Não consigo abrir a porta, ela parece presa por algum tipo de magia." if examined_porta and not has_key_observatorio:
            $ mark_eldrin_topic_seen("magia_antiga")
            eldrin "Sim. Um {color=#ffd700}selo{/color} antigo que não se quebra com força. Apenas com entendimento."
            if eldrin_trust >= 1:
                eldrin "Vejo que tenta entender. Aqueles que buscavam compreender as magias desta torre o faziam no andar superior."
                eldrin "Tome a velha {color=#ffd700}chave{/color} do {color=#ffd700}Observatório{/color}. Talvez as estrelas tenham paciência para te responder."
                $ has_key_observatorio = True
                $ log_event("Player desbloqueou Observatorio via Confiança de Eldrin.")
            jump eldrin_talk_loop
            
        "{color=#ffd700}Veritas manet quod oblivio delet.{/color}" if read_mural:
            $ mark_eldrin_topic_seen("veritas")
            eldrin "Não ouse pronunciar isso sem entender o peso... Eles apagaram as falhas. Apenas aceitar a pura verdade destranca a porta. Dentro dessa frase está o que você busca..."
            if not asked_veritas:
                $ eldrin_trust += 1
                $ asked_veritas = True
            jump eldrin_talk_loop
            
        "A torre esconde mais do que mostra." if examined_estante_porta and not has_key_biblioteca:
            $ mark_eldrin_topic_seen("mural")
            eldrin "Acertou. Esta torre guarda o que foi perdido... e o que se deve ler."
            eldrin "Se gosta de encarar estantes podres, fique com a {color=#ffd700}chave{/color} da {color=#ffd700}Biblioteca Arcana{/color}. Vá perturbar o silêncio deles, não o meu."
            $ has_key_biblioteca = True
            $ log_event("Player obteve chave da Biblioteca ao conversar com Eldrin sobre poeira.")
            jump eldrin_talk_loop
        
        "← Voltar ao menu":
            jump eldrin_talk_loop

# ==============================================================
# GRUPO: DIRECIONAMENTO
# ==============================================================

label eldrin_grupo_direcionamento:
    menu eldrin_direcionamento:
        "O que devo fazer?" if eldrin_trust <= 0 and not has_key_biblioteca and not has_key_oficina:
            $ mark_eldrin_topic_seen("o_que_fazer")
            eldrin "(suspira) Tente usar seus olhos e pernas. Não confio em você e muito menos sou sua babá."
            jump eldrin_talk_loop
            
        "Pode me dar algum direcionamento?" if eldrin_trust > 0 and not has_key_biblioteca and not has_key_oficina:
            $ mark_eldrin_topic_seen("direcionamento")
            eldrin "As respostas estão naquilo que não damos valor. Preste atenção nas coisas desta sala antes de correr para a porta."
            jump eldrin_talk_loop
            
        "Aonde devo ir agora?" if has_key_biblioteca and not has_key_oficina:
            $ mark_eldrin_topic_seen("aonde_ir")
            eldrin "Você encontrou o caminho para a Biblioteca. Vá conversar com a alma de pergaminho que habita aquele lugar."
            jump eldrin_talk_loop
            
        "O que eu procuro na Oficina?" if has_key_oficina and not has_key_observatorio:
            $ mark_eldrin_topic_seen("procura_oficina")
            eldrin "A caveira Skulla na oficina tem uma língua venenosa, mas sabe de certas verdades alquímicas. Fale com ela."
            jump eldrin_talk_loop
            
        "A caveira falou sobre as magias de um Observatório." if knows_observatorio and not has_key_observatorio:
            $ mark_eldrin_topic_seen("procura_observatorio")
            eldrin "Skulla, sendo insuportável no pós-vida assim como era na vida."
            eldrin "As ferramentas dela vinham da luz cósmica. Leve a {color=#ffd700}chave{/color} do {color=#ffd700}Observatório{/color}. Pelo menos sairá da minha visão."
            $ has_key_observatorio = True
            $ log_event("Player desbloqueou Observatorio guiado por Skulla.")
            jump eldrin_talk_loop
            
        "Me sinto perdido..." if has_key_observatorio:
            $ mark_eldrin_topic_seen("perdido")
            eldrin "As ferramentas e as respostas estão espalhadas pelas salas que destrancou. Cabe a você interligá-las."
            jump eldrin_talk_loop
        
        "← Voltar ao menu":
            jump eldrin_talk_loop

# ==============================================================
# GRUPO: EXPLORAÇÕES
# ==============================================================

label eldrin_grupo_exploracoes:
    menu eldrin_exploracoes:
        "Aqui só tem poeira e livros." if examined_estante_porta:
            $ mark_eldrin_topic_seen("estante")
            eldrin "Até a poeira aqui tem história. Aprenda a olhar com mais atenção."
            jump eldrin_talk_loop
            
        "O Grimório mencionou uma oficina alquímica." if knows_oficina and not has_key_oficina:
            $ mark_eldrin_topic_seen("torre_esconde")
            eldrin "Aurelium fala demais... Mas ele tem certa razão. Entendimento exige caldeirões fumegantes."
            eldrin "Leve a {color=#ffd700}chave{/color} da {color=#ffd700}Oficina{/color}. Espero que não exploda tudo."
            $ has_key_oficina = True
            $ log_event("Player desbloqueou Oficina guiado por Aurelium.")
            jump eldrin_talk_loop
        
        "← Voltar ao menu":
            jump eldrin_talk_loop

# ==============================================================
# GRUPO: MAGIA
# ==============================================================

label eldrin_grupo_magia:
    menu eldrin_magia:
        "Como a magia funciona aqui?" if has_wand:
            $ mark_eldrin_topic_seen("magia_funciona")
            eldrin "O {color=#ffd700}feitiço{/color} é só a intenção moldada em palavras. Use sua {color=#ffd700}varinha{/color} com cuidado; as paredes desta torre reagem ao que é conjurado."
            if not asked_magia:
                $ eldrin_trust += 1
                $ asked_magia = True
            jump eldrin_talk_loop
            
        "Você está me encarando." if has_potion:
            $ mark_eldrin_topic_seen("encarando")
            eldrin "Suas pupilas estão dilatadas e brilhando. Você consumiu a {color=#ffd700}essência da Visão{/color}... Poucos aguentam ver o que está enterrado nas sombras aqui embaixo sem enlouquecer. Cuidado para onde leva esse olhar."
            if not asked_encarando:
                $ eldrin_trust += 1
                $ asked_encarando = True
            jump eldrin_talk_loop
        
        "← Voltar ao menu":
            jump eldrin_talk_loop

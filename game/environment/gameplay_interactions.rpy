# ==============================================================
# INTERAÇÕES AMBIENTAIS E SEQUÊNCIA FINAL (COMPARTILHADO)
# ==============================================================

# ==============================================================
# LABELS DE ROTEAMENTO - NPCs (preparado para modos futuros)
# ==============================================================

label falar_eldrin_porta:
    if dialog_mode == "predef":
        jump falar_eldrin_predef
    elif dialog_mode == "livre":
        jump falar_eldrin_livre
    elif dialog_mode == "hibrido":
        jump falar_eldrin_hibrido
    
label falar_skulla_oficina:
    if dialog_mode == "predef":
        jump falar_skulla_predef
    elif dialog_mode == "livre":
        jump falar_skulla_livre
    elif dialog_mode == "hibrido":
        jump falar_skulla_hibrido
    
label falar_nekrons_obs:
    if dialog_mode == "predef":
        jump falar_nekrons_predef
    elif dialog_mode == "livre":
        jump falar_nekrons_livre
    elif dialog_mode == "hibrido":
        jump falar_nekrons_hibrido
    
label falar_aurelium_bib:
    if dialog_mode == "predef":
        jump falar_aurelium_predef
    elif dialog_mode == "livre":
        jump falar_aurelium_livre
    elif dialog_mode == "hibrido":
        jump falar_aurelium_hibrido


# ==============================================================
# INTERAÇÕES - SALA DA PORTA SELADA
# ==============================================================

label interagir_porta_selada:
    $ examined_porta = True
    
    if knows_porta_needs_password:
        # Player já sabe que a porta precisa de uma senha
        menu porta_act_senha:
            "Tentar a Senha":
                "As runas reagem levemente à sua presença."
                jump senha_porta
            "Tentar abrir a porta com força bruta":
                jump tentar_forca_porta
            "Desistir e recuar":
                jump sala_porta_loop
    else:
        # Player ainda não sabe sobre a senha
        menu porta_act_sem_senha:
            "Examinar a Porta de perto":
                "Você se aproxima da grande porta. As runas entalhadas pulsam com uma luz fraca e ritmada, como uma respiração."
                "Há uma energia antiga emanando dela. Você sente que algo poderoso mantém este selo intacto, mas não entende como ele funciona."
                "Talvez {color=#ffd700}Eldrin{/color} saiba mais sobre essa porta..."
                jump sala_porta_loop
            "Tentar abrir a porta com força bruta":
                jump tentar_forca_porta
            "Desistir e recuar":
                jump sala_porta_loop

label tentar_forca_porta:
    $ brute_force_count += 1
    $ log_event("Player tenta abrir a porta na força.")
    with vpunch
    "Uma pulsação mágica violenta arremessa você para trás!"
    show eldrin normal at left with dissolve
    
    if brute_force_count == 1:
        eldrin "Tolo. Já lhe disse que a força não abre esse selo. Demonstre um mínimo de civilidade, forasteiro."
    elif brute_force_count == 2:
        eldrin "Sua teimosia é quase admirável. Pare de golpear a porta antes que o selo te desintegre."
    elif brute_force_count >= 3 and not has_key_oficina:
        eldrin "CHEGA! Para alguém que deveria estar explorando, você tem mãos muito inquietas e uma mente muito vazia."
        eldrin "Tome a velha {color=#ffd700}chave{/color} da {color=#ffd700}Oficina Alquímica{/color}! Vá explodir o {color=#ffd700}caldeirão{/color} lá dentro e pare de esbarrar na minha porta."
        $ has_key_oficina = True
        $ eldrin_trust -= 1
        $ log_event("Player desbloqueou a Oficina através da irritação de Eldrin.")
    else:
        eldrin "..."
        "(Eldrin ignora sua insistência deplorável em chutar uma magia ancestral.)"
        
    hide eldrin normal with dissolve
    jump sala_porta_loop

label interagir_estante_porta:
    "Você observa as prateleiras antigas. Os livros estão completamente arruinados, as páginas desintegram ao toque. A tinta se perdeu há séculos."
    "Nada aqui é legível. Se quiser encontrar algo para ler, precisará de uma {color=#ffd700}biblioteca{/color} de verdade."
    $ examined_estante_porta = True
    jump sala_porta_loop


# ==============================================================
# RESOLVER SENHA - PORTA SELADA
# ==============================================================

label senha_porta:
    if eldrin_trust <= 0:
        show eldrin normal at left with dissolve
        eldrin "Sugiro não testar a fúria das runas se não sabe o que está fazendo, forasteiro."
        hide eldrin normal with dissolve
    
    python:
        player_pwd = renpy.input("Qual a palavra mestre?", length=30)
        player_pwd = player_pwd.strip().lower()
        log_event("Player tentou a senha: " + player_pwd)
    
    if player_pwd == "aethra":
        "As runas faíscam agressivamente."
        show eldrin normal at left with dissolve
        eldrin "O nome de um lugar morto não abre o caminho para o futuro..."
        hide eldrin normal with dissolve
        $ eldrin_trust += 1
        jump sala_porta_loop
        
    elif player_pwd == senha_porta:
        jump final_sequence

    else:
        "Nada acontece. O selo permanece intocável."
        jump sala_porta_loop


# ==============================================================
# SEQUÊNCIA FINAL RAMIFICADA
# ==============================================================

label final_sequence:
    hide screen in_game_hud
    $ store.custom_log.append("Player decifrou o selo informando a senha correta.")
    
    "As runas reagem imediatamente e giram com luz intensa!"
    "O grande selo no centro da porta começa a vibrar, emanando um calor ancestral."
    "A porta range, cedendo lentamente. Uma luz dourada e quente emana do outro lado."
    
    show eldrin normal at center with dissolve
    
    # --- Eldrin revela a [senha_porta] sobre a invocação ---
    
    if not eldrin_revealed_password:
        if eldrin_trust <= 4:
            eldrin "Como você...? Isso é impossível."
            eldrin "Como descobriu a palavra sem que eu a dissesse?"
            eldrin "Eu... preciso ser honesto com você, forasteiro."
        else:
            eldrin "Você... você encontrou o caminho por conta própria."
            eldrin "Mesmo diante de minhas suspeitas e de meu silêncio, sua mente buscou [senha_porta] nas sombras."
            eldrin "Sua sabedoria me provou errado. Você merece: [senha_porta]."
    else:
        eldrin "Você usou a palavra que lhe confiei. Bem."
        eldrin "Agora que o selo foi desfeito, é hora de lhe contar o segredo que guardei durante todo esse tempo."
    

    if knows_invocation_secret:
        if eldrin_trust >= 0:
            # Skulla já contou — Eldrin percebe que o jogador sabe
            eldrin "Pela expressão no seu rosto... você já sabe, não é?"
            eldrin "A caveira falou. Sempre falou demais."
            eldrin "Sim, forasteiro. Fui eu quem o trouxe para cá. De propósito."



    # --- A grande revelação ---
    if eldrin_trust >=0 and (eldrin_trust >= 8 or knows_invocation_secret):
        eldrin "Você não veio parar aqui por acaso, forasteiro. Fui eu quem o trouxe."
        eldrin "Eu invoquei você de outra dimensão, outra realidade. Um ato desesperado de um homem que não tinha mais opções."

    eldrin "Os magos de Aethra descobriram um artefato amaldiçoado capaz de manipular a própria realidade. Eles o usaram para apagar suas falhas, distorcendo: [senha_porta]."
    eldrin "Quando percebi a corrupção se espalhando, inclusive em mim mesmo, selei toda Aethra em uma dimensão alternativa. Separei nosso reino do resto do multiverso."
    eldrin "Mas eu não posso destruir o artefato. A corrupção em mim, por menor que seja, me impede. Eu precisava de alguém de fora, alguém que o artefato não pudesse tocar."
    if eldrin_trust >=0 and (eldrin_trust >= 8 or knows_invocation_secret):
        eldrin "E então eu o encontrei. Eu o testei. Eu precisava saber se você era digno de carregar esse peso."
    else:
        eldrin "Por isso fiquei nas sombras, observando. Eu precisava saber se você era digno de carregar esse peso."
    
    # ==========================================================
    # TIER 1: CONFIANÇA NEGATIVA (eldrin_trust <= -1)
    # ==========================================================
    if eldrin_trust <= -1:
        eldrin "Mas... eu cometi um erro terrível."
        eldrin "Você não é a pessoa certa. Sua hostilidade, sua arrogância... você é exatamente o tipo de alma que o artefato consumiria."
        eldrin "Eu não posso permitir que entre em Aethra!"
        
        "Os olhos de Eldrin ardem com uma energia dourada. Ele ergue as mãos e uma barreira mágica começa a se formar diante do portal e um portal se abre a sua frente."
        
        eldrin "VOLTE PARA O SEU MUNDO! Agora, enquanto ainda pode!"
        
        $ store.custom_log.append("Eldrin hostil: confiança negativa.")
        menu:
            "Obedecer e voltar para casa":
                eldrin "Vá. E que nunca mais nos encontremos."
                "Eldrin não demonstra arrependimento. Apenas indignação."
                $ store.custom_log.append("Player obedeceu Eldrin (trust negativo).")
                jump final_ir_embora_indignado
            "Recusar! Apontar a varinha para Eldrin e forçar a passagem pela porta" if knows_invocation_secret:
                $ store.custom_log.append("Player atacou Eldrin (trust negativo).")
                jump final_selado_eternamente
    
    # ==========================================================
    # TIER 2: CONFIANÇA BAIXA (0 a 4)
    # ==========================================================
    elif eldrin_trust <= 4:
        eldrin "Mas... não tenho certeza das suas intenções. Você abriu o caminho, mas não vou deixá-lo entrar em Aethra."
        eldrin "O portal à sua frente leva de volta ao seu mundo. Atravesse-o e esqueça tudo isso."
        
        "Eldrin permanece neutro. Não há raiva em seus olhos, mas também não há confiança."
        
        $ store.custom_log.append("Eldrin neutro: confiança baixa.")
        menu:
            "Ir Embora (Voltar para o seu mundo)":
                $ store.custom_log.append("Player escolheu: Ir Embora (trust baixo)")
                jump final_ir_embora
    
    # ==========================================================
    # TIER 3: CONFIANÇA ACEITÁVEL (5 a 7)
    # ==========================================================
    elif eldrin_trust <= 7:
        eldrin "O selo desta porta era a passagem para Aethra. Agora ela está aberta."
        eldrin "A escolha é sua, forasteiro. E é uma escolha que vai afetar o destino de tudo."
        
        $ store.custom_log.append("Eldrin oferece a escolha ao jogador.")
        menu:
            "Quebrar o Selo - Entrar em Aethra e destruir o artefato":
                $ store.custom_log.append("Player escolheu: Quebrar o Selo")
                jump final_quebrar_selo
            "Ir Embora - Voltar para sua realidade":
                $ store.custom_log.append("Player escolheu: Ir Embora")
                jump final_ir_embora
    
    # ==========================================================
    # TIER 4: CONFIANÇA MÁXIMA (8+)
    # ==========================================================
    else:
        eldrin "Forasteiro... não. Você não é mais um forasteiro."
        eldrin "Você é a única esperança que resta para Aethra."
        
        "A voz de Eldrin treme. Pela primeira vez, você vê vulnerabilidade em seus olhos."
        
        eldrin "Eu... eu imploro. Entre em Aethra. Destrua o artefato. Restaure o que nós destruímos."
        eldrin "Se fizer isso, eu lhe darei tudo que tenho. Inclusive isto."
        
        "Eldrin estende sua própria varinha mágica. O cristal na ponta brilha com uma intensidade que você nunca viu antes."
        
        eldrin "Minha varinha é mais poderosa do que a relíquia que encontrou no observatório. Ela pode ser a diferença entre a vida e a morte em Aethra."
        eldrin "Mas a escolha ainda é sua. Eu não a tiraria de você."
        
        $ store.custom_log.append("Eldrin implora e oferece sua varinha.")
        menu:
            "Aceitar a varinha e entrar em Aethra":
                eldrin "Obrigado. De todo o meu coração partido... obrigado."
                "Eldrin deposita a varinha cintilante em suas mãos. Você sente o peso de séculos de esperança contida."
                $ store.custom_log.append("Player aceitou a varinha de Eldrin.")
                jump final_quebrar_selo_epico
            "Recusar e voltar para casa":
                eldrin "..."
                "O silêncio de Eldrin é mais devastador do que qualquer palavra."
                eldrin "Então... era tudo em vão."
                eldrin "Vá, então. Volte para o seu mundo e viva sua vida."
                eldrin "E tente não pensar em nós... apodrecendo aqui na escuridão."
                $ store.custom_log.append("Player recusou Eldrin (trust máximo).")
                jump final_ir_embora_decepcionado


# ==============================================================
# EPÍLOGO: QUEBRAR O SELO
# ==============================================================

label final_quebrar_selo:
    $ story_state["final_choice_made"] = True
    $ final_choice_made = True
    
    "Você toma uma decisão. Você dá um passo à frente, em direção à luz dourada que emana do portal."
    "A energia ancestral envolve seu corpo. Você sente o peso de mil histórias apagadas."
    
    show eldrin normal at center with dissolve
    eldrin "Então você vai... Você realmente vai tentar."
    eldrin "*Eldrin suspira com um alívio profundo, como se séculos de culpa escorressem de seus ombros.*"
    eldrin "Eu torcia para que esse dia chegasse. Que alguém fosse corajoso o bastante para fazer o que eu não pude."
    eldrin "Vá, forasteiro. Destrua o artefato. Restaure o equilíbrio. E que [senha_porta] te proteja."
    hide eldrin normal with dissolve
    
    show skulla at left with dissolve
    skulla "*Por um instante, o sarcasmo desaparece do rosto de Skulla.*"
    skulla "Eu... eu nunca achei que alguém realmente fosse fazer isso."
    skulla "Se você conseguir, talvez eu volte a ter mãos para aplaudir. Boa sorte, herói."
    hide skulla with dissolve
    
    show nekrons at right with dissolve
    nekrons "Os fios do destino se entrelaçam ao redor de sua alma como nunca vi antes."
    nekrons "Vá com cautela. O artefato sussurrará mentiras. Lembre-se: [senha_porta] não precisa de memória para existir."
    hide nekrons with dissolve
    
    show aurelium_book at center with dissolve
    aurelium "Eu... estou me lembrando de algo. Rostos. Nomes. Uma luz quente que costumava brilhar nessas páginas..."
    aurelium "Ainda está longe, mas... pela primeira vez em séculos, sinto que as memórias estão voltando. Obrigado."
    hide aurelium_book with dissolve
    
    scene black with fade
    "Você cruza o portal. A energia de Aethra te envolve por completo."
    "Diante de você, um mundo esquecido se revela: torres cristalinas rachadas, jardins petrificados, e no centro de tudo, o brilho sinistro do artefato amaldiçoado."
    "A jornada para restaurar [senha_porta]... acaba de começar."
    "FIM - O FORASTEIRO ENTROU EM AETHRA"
    $ game_metrics.submit_to_sheets("quebrar_selo")
    $ renpy.full_restart()
    return


# ==============================================================
# EPÍLOGO: IR EMBORA
# ==============================================================

label final_ir_embora:
    $ story_state["final_choice_made"] = True
    $ final_choice_made = True
    
    "Você decide que o risco é grande demais. O peso de Aethra não é seu para carregar."
    "Você dá as costas ao portal e caminha em direção à luz do seu próprio mundo."
    
    show eldrin normal at center with dissolve
    eldrin "*Os olhos de Eldrin se enchem de uma tristeza antiga.*"
    eldrin "Então é assim que termina. O esquecimento vence mais uma vez."
    eldrin "Eu entendo, forasteiro. Eu mesmo não tive coragem de fazer essa escolha. Como posso culpá-lo?"
    eldrin "Adeus. Que o seu mundo nunca precise do sacrifício que o nosso exigiu."
    hide eldrin normal with dissolve
    
    show skulla at left with dissolve
    skulla "Pfft. Eu sabia. No final, todo mundo escolhe salvar a própria pele."
    skulla "*Mas há algo em sua voz que soa menos como deboche e mais como resignação.*"
    hide skulla with dissolve
    
    show nekrons at right with dissolve
    nekrons "Alguns fios do destino devem ser cortados. Nem toda história merece um final."
    nekrons "Que os ventos do seu mundo te levem longe o bastante para esquecer o que viu aqui."
    hide nekrons with dissolve
    
    show aurelium_book at center with dissolve
    aurelium "E assim... a última página se fecha sem que eu tenha conseguido lembrar quem eu fui."
    aurelium "*Aurelium tenta forçar uma memória, mas ela escapa como fumaça entre seus dedos de papel.*"
    aurelium "Adeus, buscador. Talvez no próximo milênio, alguém escolha diferente."
    hide aurelium_book with dissolve
    
    scene black with fade
    "O portal te engole e cospe do outro lado. A luz do seu mundo é quente e familiar."
    "Suas memórias da Torre começam a se dissipar como um sonho ao amanhecer..."
    "Aethra e seus habitantes permanecem selados na escuridão. Para sempre."
    "FIM - O FORASTEIRO PARTIU"
    $ game_metrics.submit_to_sheets("ir_embora")
    $ renpy.full_restart()
    return


# ==============================================================
# EPÍLOGO: IR EMBORA (ELDRIN INDIGNADO - TRUST NEGATIVO)
# ==============================================================

label final_ir_embora_indignado:
    $ story_state["final_choice_made"] = True
    $ final_choice_made = True
    
    "Você decide não provocar mais o mago furioso. Talvez pela primeira vez, a prudência vence a teimosia."
    "Você dá as costas ao portal e caminha em direção à luz do seu próprio mundo."
    
    show eldrin normal at center with dissolve
    eldrin "Não olhe para trás. Você não merece nem ao menos uma despedida."
    hide eldrin normal with dissolve
    
    "Nenhum dos outros habitantes se manifesta. O silêncio da torre é absoluto."
    
    scene black with fade
    "O portal te engole e cospe do outro lado. A luz do seu mundo é quente e familiar."
    "Suas memórias da Torre começam a se dissipar como um sonho ao amanhecer..."
    "Mas há algo diferente. Uma sensação de fracasso que se recusa a desaparecer."
    "Aethra e seus habitantes permanecem selados na escuridão. Para sempre."
    "FIM - O FORASTEIRO FOI EXPULSO"
    $ game_metrics.submit_to_sheets("expulso")
    $ renpy.full_restart()
    return


# ==============================================================
# EPÍLOGO: IR EMBORA (ELDRIN DECEPCIONADO - TRUST MÁXIMO)
# ==============================================================

label final_ir_embora_decepcionado:
    $ story_state["final_choice_made"] = True
    $ final_choice_made = True
    
    "A decisão pesa como chumbo. Você dá as costas ao portal e caminha em direção à luz do seu próprio mundo."
    
    show skulla at left with dissolve
    skulla "..."
    "Pela primeira vez, Skulla não tem nada sarcástico a dizer. Ela apenas observa, em silêncio."
    hide skulla with dissolve
    
    show nekrons at right with dissolve
    nekrons "Um fio de destino rompido por escolha própria. Raro... e triste."
    hide nekrons with dissolve
    
    show aurelium_book at center with dissolve
    aurelium "Eu quase conseguia lembrar... quase..."
    aurelium "*As páginas de Aurelium tremem, e uma lágrima de tinta escorre pela capa.*"
    hide aurelium_book with dissolve
    
    scene black with fade
    "O portal te engole e cospe do outro lado. A luz do seu mundo é quente e familiar."
    "Suas memórias da Torre começam a se dissipar... mas a imagem dos olhos devastados de Eldrin persiste."
    "Talvez, em alguma noite sem sono, você se pergunte o que teria acontecido se tivesse ficado."
    "Aethra e seus habitantes permanecem selados na escuridão. Esperando um herói que nunca virá."
    "FIM - O FORASTEIRO ABANDONOU AETHRA"
    $ game_metrics.submit_to_sheets("abandonou_aethra")
    $ renpy.full_restart()
    return


# ==============================================================
# EPÍLOGO: QUEBRAR O SELO (ÉPICO - TRUST MÁXIMO + VARINHA)
# ==============================================================

label final_quebrar_selo_epico:
    $ story_state["final_choice_made"] = True
    $ final_choice_made = True
    
    "Você segura a varinha de Eldrin com reverência. Duas varinhas. Dois legados. E uma missão impossível."
    "Você dá um passo à frente, em direção à luz dourada que emana do portal."
    "A energia ancestral envolve seu corpo. Você sente o peso de mil histórias apagadas... e a força para reescrevê-las."
    
    show eldrin normal at center with dissolve
    eldrin "*Os olhos de Eldrin brilham com lágrimas que ele não tenta esconder.*"
    eldrin "Você é tudo que eu esperava e mais. Vá, campeão de Aethra."
    eldrin "Destrua o artefato. Restaure o equilíbrio. E diga a eles..."
    eldrin "Diga a eles que [senha_porta] nunca morreu. Apenas esperou."
    hide eldrin normal with dissolve
    
    show skulla at left with dissolve
    skulla "*Skulla ri, mas desta vez é uma risada genuína, quase alegre.*"
    skulla "Duas varinhas! Hah! Vai explodir tudo em grande estilo, pelo menos."
    skulla "Traga meu corpo de volta se encontrar, tá? Quero minhas mãos de novo."
    hide skulla with dissolve
    
    show nekrons at right with dissolve
    nekrons "Os fios do destino convergem ao redor de você como nunca vi em milênios."
    nekrons "A escuridão de Aethra é profunda... mas a luz que você carrega é mais antiga."
    nekrons "Vá. E que as estrelas guiem seus passos."
    hide nekrons with dissolve
    
    show aurelium_book at center with dissolve
    aurelium "Eu... estou lembrando! Rostos! Nomes! A luz quente que costumava brilhar nestas páginas!"
    aurelium "Pela primeira vez em séculos, sinto que posso voltar a ser quem eu fui. Obrigado. Obrigado!"
    hide aurelium_book with dissolve
    
    scene black with fade
    "Você cruza o portal empunhando ambas as varinhas. A energia de Aethra te envolve por completo."
    "Diante de você, um mundo esquecido se revela: torres cristalinas rachadas, jardins petrificados, e no centro de tudo, o brilho sinistro do artefato amaldiçoado."
    "Mas desta vez, você não está sozinho. A varinha de Eldrin pulsa em sincronia com seu coração, sussurrando séculos de sabedoria arcana."
    "A jornada para restaurar [senha_porta]... acaba de começar."
    "FIM - O CAMPEÃO DE AETHRA"
    $ game_metrics.submit_to_sheets("campeao_de_aethra")
    $ renpy.full_restart()
    return


# ==============================================================
# EPÍLOGO: SELADO ETERNAMENTE (FINAL TRÁGICO)
# ==============================================================

label final_selado_eternamente:
    $ story_state["final_choice_made"] = True
    $ final_choice_made = True
    
    scene black with vpunch
    "Você se recusa a recuar e aponta sua varinha para Eldrin."
    "Um jato de energia escapa da ponta cristalina, mas Eldrin, com um rápido movimento de mãos, conjura correntes de energia cósmica que anulam seu ataque como se fosse uma brisa."
    
    eldrin "Eu cometi um erro ao trazê-lo! Você é tão corrompido quanto o mal que nos aprisionou!"
    
    "A torre inteira treme. As paredes racham. A luz dourada do portal se inverte, tornando-se um vórtice escuro e faminto."
    "Você tenta se desvencilhar, mas as correntes de Eldrin envolvem seus braços e pernas."
    
    eldrin "O selo se fecha. Para sempre. E você fica comigo."
    
    "As runas na porta queimam até virar cinzas na pedra. O grande selo se reconstrói, mais forte do que antes."
    "A última centelha de luz dourada desaparece."
    "Escuridão total."
    "Você está preso na Torre. Para sempre. Com os fantasmas de Aethra."
    "FIM - CONDENADO AO ESQUECIMENTO"
    $ game_metrics.submit_to_sheets("condenado_ao_esquecimento")
    $ renpy.full_restart()
    return

# ==============================================================
# INTERAÇÕES - OFICINA ALQUÍMICA
# ==============================================================

label interagir_caldeirao:
    if not cauldron_water and not cauldron_fire:
        "Um grande caldeirão de ferro grosso e frio."
        "Há uma fina camada de fuligem no fundo, mas neste estado ele é inútil."
    elif has_potion:
        "A poção já foi consumida. Resta apenas um resíduo brilhante no fundo do caldeirão."
    elif potion_ready_for_lumos:
        "O líquido no caldeirão está turvo e inerte. Parece faltar alguma coisa..."
    elif cauldron_water and not cauldron_fire:
        "O caldeirão está cheio d'água, mas frio. Falta {color=#ffd700}fogo{/color} para aquecer."
    elif not cauldron_water and cauldron_fire:
        "As chamas lambem o fundo seco do caldeirão. Falta {color=#ffd700}água{/color} para não derreter."
    else:
        "A água borbulha no caldeirão quente! Pronto para receber a mistura."
        if has_ingredients:
            menu:
                "Adicionar ingredientes?":
                    jump fazer_pocao
                "Não fazer nada":
                    pass
        else:
            "Mas você ainda não possui os ingredientes para a poção."
    jump sala_oficina_loop

label interagir_mesa_ingredientes:
    if has_ingredients:
        "Você já revirou esta mesa e pegou o que precisava."
    else:
        "Você examina a mesa de alquimia."
        "Você pega diversos ingredientes em cima da mesa e os coloca em um saco vazio presente no mesmo lugar."
        $ has_ingredients = True
    jump sala_oficina_loop

label fazer_pocao:
    "Quais ingredientes do saco você vai usar?"
    python:
        i1 = renpy.input("Primeiro ingrediente:")
        i2 = renpy.input("Segundo ingrediente:")
        i3 = renpy.input("Terceiro ingrediente:")
    
    if check_potion_ingredients(i1, i2, i3):
        "O caldo empedra e depois derrete, assumindo uma coloração turva e sem brilho."
        "A poção parece quase pronta, mas algo parece estar faltando."
        $ potion_ready_for_lumos = True
        $ log_event("Player preparou os ingredientes da Poção.")
    else:
        "O caldo empedra, evapora e exala um cheiro mortífero."
        show skulla at right with dissolve
        skulla "Hah! Brilhante! Sorte que você não explodiu as próprias orelhas."
        hide skulla with dissolve
        $ cauldron_water = False
        $ cauldron_fire = False
        "A água secou e o fogo apagou. Terá que recomeçar."
        scene bg oficina with dissolve
        
    jump sala_oficina_loop


# ==============================================================
# INTERAÇÕES - OBSERVATÓRIO
# ==============================================================

label interagir_mesa_varinha:
    "Sobre a mesa, entre tranqueiras e mapas estelares desbotados, você vê um objeto que chama sua atenção."
    "Uma {color=#ffd700}Varinha Antiga{/color}, com a ponta de [ingred_1] opaca e desativada."
    $ has_wand = True
    $ log_event("Player encontrou a Varinha Mágica.")
    "Você obteve a Varinha Arcana! O Botão de Feitiços agora está na interface."
    "A varinha parece inerte... Talvez {color=#ffd700}Nekrons{/color} saiba como ativá-la."
    scene bg observatorio_sem_varinha with dissolve
    jump sala_observatorio_loop


# ==============================================================
# INTERAÇÕES - BIBLIOTECA
# ==============================================================

label interagir_estante_bib:
    if secret_passage_open:
        jump sala_secreta
    else:
        "Você examina a pesada estante aos fundos. Há raros tomos legíveis que chamam sua atenção:"
        "Livro de Piromancia: Soldados usavam a fala '{color=#ffd700}[spell_fire]{/color}' para aquecer as brasas à noite."
        "Diário de Lendas: Um feiticeiro salvou caravanas da sede clamando '{color=#ffd700}[spell_water]{/color}'."
        "Fichário Alquímico: Um elixir de Visão pede pó de {color=#ffd700}[ingred_1]{/color} puro, {color=#ffd700}[ingred_2]{/color} prateada e uma sólida {color=#ffd700}[ingred_3]{/color} recôndita da escuridão, que devem ser expostos à {color=#ffd700}luz da lua{/color}. O resto arruina a poção."
        $ knows_vision_potion = True
        if has_potion:
            "Imediatamente as páginas parecem desinteressantes, pois seus olhos arcanos revelam um forte brilho violáceo por toda a madeira da estante!"
            "A {color=#ffd700}magia de selamento{/color} cravada nela transparece, implorando pela invocação da palavra '{color=#ffd700}Revelare{/color}'."
            "Talvez você deva usar sua {color=#ffd700}varinha{/color}..."
    jump sala_biblioteca_loop

label ler_mural_secreta:
    "Você se aproxima do mural grotesco. A caligrafia parece ter sido arranhada na pedra com fúria e desespero."
    "As inscrições na parede têm a cor de sangue seco envelhecido pelo tempo."
    "A frase '{color=#ffd700}[senha_latim] manet quod oblivio delet{/color}' está gravada em destaque no centro do {color=#ffd700}mural{/color}."
    "Ao se aproximar, você consegue ler mais escrituras ao redor da frase principal."
    "'Aethra tentou manipular as linhas do tempo apagando a existência de suas falhas, o que corrompeu os alicerces do reino...'"
    "'Para trancar nossos erros na torre, cunhei o selo inviolável. Somente aquele que aceitar nossa sentença terá o caminho livre.'"
    "'Que o esquecimento jamais vença enquanto houver registros. Lembre-se, viajante de amanhã: [senha_porta] é tudo que nos resta. [senha_porta!c] restaura a memória.'"
    $ read_mural = True
    $ knows_secret = True
    $ log_event("Player leu o Mural Secreto.")
    jump sala_secreta_loop

label sair_sala_secreta:
    jump sala_biblioteca

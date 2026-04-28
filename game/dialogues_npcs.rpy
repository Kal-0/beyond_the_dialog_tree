# ==============================================================
# DIÁLOGOS - OUTROS NPCs (MODO PRÉ-DEFINIDO COM GRUPOS)
# ==============================================================

# ==============================================================
# SKULLA - OFICINA ALQUÍMICA
# ==============================================================

label falar_skulla_oficina:
    show skulla at right with dissolve
    if not met_skulla:
        skulla "Ah, ótimo. Mais um aventureiro. Me diga, costuma resolver enigmas com coragem ou só com perguntas óbvias?"
        $ met_skulla = True
    else:
        skulla "O que você precisa, humano frágil? Não vê que estou ocupada estando morta?"
        
label skulla_talk_loop:
    menu skulla_grupos:
        "Sobre Você" if should_show_skulla_group("sobre_voce"):
            jump skulla_grupo_sobre_voce
        "Conhecimento" if should_show_skulla_group("conhecimento"):
            jump skulla_grupo_conhecimento
        "Ingredientes" if should_show_skulla_group("ingredientes"):
            jump skulla_grupo_ingredientes
        "Encerrar conversa":
            hide skulla with dissolve
            jump sala_oficina_loop

    jump skulla_talk_loop

label skulla_grupo_sobre_voce:
    menu skulla_sobre_voce:
        "Quem é você?":
            $ mark_skulla_topic_seen("quem_eh")
            skulla "Eu era a Mestra Alquimista desta torre. Agora, sou a principal atração de decoração macabra. Skulla, ao seu indispor."
            jump skulla_talk_loop
            
        "Como você perdeu seu corpo?":
            $ mark_skulla_topic_seen("como_perdeu")
            skulla "Uma mistura infeliz de curiosidade e pó de estrelas instável. Meu corpo virou fumaça, mas minha mente brilhante continuou presa neste meu lindo crânio."
            jump skulla_talk_loop
            
        "Preciso de ajuda.":
            $ mark_skulla_topic_seen("precisava_ajuda")
            skulla "Eu também precisava, mas veja como a vida é cruel."
            jump skulla_talk_loop
        
        "← Voltar ao menu":
            jump skulla_talk_loop

label skulla_grupo_conhecimento:
    menu skulla_conhecimento:
        "Você sabe algo útil?":
            $ mark_skulla_topic_seen("sabe_util")
            skulla "Se eu soubesse a senha, já teria ido embora. Mas sei que Eldrin respeita coerência."
            jump skulla_talk_loop
            
        "Essa sala costumava produzir que tipos de maravilhas?":
            $ mark_skulla_topic_seen("producoes")
            skulla "Eu mesma faria uma {color=#ffd700}poção{/color} fantástica agora, se toda a luz astral não estivesse trancada naquele maldito {color=#ffd700}Observatório{/color} no andar de cima."
            if not has_key_observatorio:
                skulla "Ouvi dizer que Eldrin confiscou a chave do lugar, típico dele, não é?"
                $ knows_observatorio = True
                $ log_event("Player aprendeu a existência do Observatório.")
            jump skulla_talk_loop
            
        "Eu bebi a mistura e não explodi." if has_potion:
            $ mark_skulla_topic_seen("pocao")
            skulla "Decepcionante, de fato. Mas esses olhos aí estão brilhando. Faça um favor a si mesmo e vá piscar essa mágica em frente às prateleiras e grimórios mofados da biblioteca."
            jump skulla_talk_loop
        
        "← Voltar ao menu":
            jump skulla_talk_loop

label skulla_grupo_ingredientes:
    menu skulla_ingredientes:
        "A água está fria." if cauldron_water and not cauldron_fire:
            $ mark_skulla_topic_seen("agua_fria")
            skulla "Que tipo de sopa fria você esta tentando fazer? Sabe ao menos como um caldeirão funciona? Você precisa de FOGO imbecil!"
            jump skulla_talk_loop
        
        "← Voltar ao menu":
            jump skulla_talk_loop

# ==============================================================
# NEKRONS - OBSERVATÓRIO
# ==============================================================

label falar_nekrons_obs:
    show nekrons at center with dissolve
    if not met_nekrons:
        nekrons "Você acordou tarde demais ou cedo demais. Depende do que está procurando."
        $ met_nekrons = True
    else:
        nekrons "As sombras me contaram que você voltaria..."
        
label nekrons_talk_loop:
    menu nekrons_grupos:
        "Sobre Você" if should_show_nekrons_group("sobre_voce"):
            jump nekrons_grupo_sobre_voce
        "Conhecimento" if should_show_nekrons_group("conhecimento"):
            jump nekrons_grupo_conhecimento
        "Magia" if should_show_nekrons_group("magia"):
            jump nekrons_grupo_magia
        "Encerrar conversa":
            hide nekrons with dissolve
            jump sala_observatorio_loop

    jump nekrons_talk_loop

label nekrons_grupo_sobre_voce:
    menu nekrons_sobre_voce:
        "Quem é você?":
            $ mark_nekrons_topic_seen("quem_eh")
            nekrons "Eu sou Nekrons. Os magos me chamavam de familiar, mas eu os via como animais de estimação bem treinados."
            jump nekrons_talk_loop
            
        "Você não é apenas um gato, é?":
            $ mark_nekrons_topic_seen("nao_gato")
            nekrons "Tenho mais olhos neste mundo do que você tem em sua cabeça, viajante. O formato felino é apenas conveniente para caminhar entre as sombras."
            jump nekrons_talk_loop
            
        "Você sabe como sair?":
            $ mark_nekrons_topic_seen("como_sair")
            nekrons "Talvez. Mas portas raramente se abrem para quem apenas quer escapar."
            jump nekrons_talk_loop
        
        "← Voltar ao menu":
            jump nekrons_talk_loop

label nekrons_grupo_conhecimento:
    menu nekrons_conhecimento:
        "O que é este lugar?":
            $ mark_nekrons_topic_seen("o_que_lugar")
            nekrons "Um lugar onde o passado aprendeu a se esconder."
            jump nekrons_talk_loop
            
        "Você conhece Eldrin?":
            $ mark_nekrons_topic_seen("conhece_eldrin")
            nekrons "Conheço sua culpa. Conhecer alguém de verdade é diferente."
            jump nekrons_talk_loop
            
        "O que posso fazer aqui?" if not has_wand:
            $ mark_nekrons_topic_seen("o_que_fazer")
            nekrons "Você olha demais para as estrelas. O poder que sobrou sempre fica renegado às sombras e à poeira, como no alto daquela estante empoeirada."
            jump nekrons_talk_loop
        
        "← Voltar ao menu":
            jump nekrons_talk_loop

label nekrons_grupo_magia:
    menu nekrons_magia:
        "A varinha que encontrei parece morta." if has_wand and not wand_active:
            $ mark_nekrons_topic_seen("varinha")
            nekrons "Morta? Assim como as memórias desta torre. Mas as estrelas... elas ainda têm voz."
            "A gata preta salta graciosamente até o bocal do grande telescópio, direcionando-o para uma fresta no teto."
            "A luz mágica do céu estrelado converge pela lente e foca diretamente na ponta de cristal da sua varinha."
            nekrons "Lumos."
            with vpunch
            "A varinha treme e se acende com uma luz inebriante!"
            $ wand_active = True
            $ log_event("Nekrons despertou a Varinha canalizando a luz de constelações arcanas.")
            jump nekrons_talk_loop
            
        "Você sentiu esse tremor?" if secret_passage_open:
            $ mark_nekrons_topic_seen("tremor")
            nekrons "O cheiro de sangue ancestral subiu pelas escadas da biblioteca. Você abriu velhas feridas nas pedras acreditando que estava apenas cavando tesouros."
            jump nekrons_talk_loop
        
        "← Voltar ao menu":
            jump nekrons_talk_loop

# ==============================================================
# AURELIUM - BIBLIOTECA
# ==============================================================

label falar_aurelium_bib:
    show aurelium_book at center with dissolve
    if not met_aurelium:
        aurelium "Finalmente alguém que lê com os olhos e não apenas com a pressa."
        $ met_aurelium = True
    else:
        aurelium "Mais perguntas rudimentares? Folheie logo as páginas se procura conhecimento."
        
label aurelium_talk_loop:
    menu aurelium_grupos:
        "Sobre Você" if should_show_aurelium_group("sobre_voce"):
            jump aurelium_grupo_sobre_voce
        "Conhecimento" if should_show_aurelium_group("conhecimento"):
            jump aurelium_grupo_conhecimento
        "Encerrar conversa":
            hide aurelium_book with dissolve
            jump sala_biblioteca_loop

    jump aurelium_talk_loop

label aurelium_grupo_sobre_voce:
    menu aurelium_sobre_voce:
        "Quem é você?":
            $ mark_aurelium_topic_seen("quem_eh")
            aurelium "Eu sou Aurelium. Um oráculo de no passado, agora confinado a tinta em páginas pela eternidade."
            jump aurelium_talk_loop
            
        "É solitário ser um livro?":
            $ mark_aurelium_topic_seen("solitario")
            aurelium "As palavras nunca estão sozinhas. Mas sim, sinto falta de fazer outra coisa além de virar minhas próprias páginas."
            jump aurelium_talk_loop
        
        "← Voltar ao menu":
            jump aurelium_talk_loop

label aurelium_grupo_conhecimento:
    menu aurelium_conhecimento:
        "O que sabe sobre esta torre?":
            $ mark_aurelium_topic_seen("sobre_torre")
            aurelium "Aethra tentou controlar a verdade e falhou feio."
            jump aurelium_talk_loop
            
        "A senha da porta está nas suas páginas?":
            $ mark_aurelium_topic_seen("senha_porta")
            aurelium "Não de forma explícita. O selo responde a compreensão, não a memorização cega."
            jump aurelium_talk_loop
            
        "Onde ficavam os alquimistas?" if not knows_oficina and not has_key_oficina:
            $ mark_aurelium_topic_seen("sobre_alquimistas")
            aurelium "Ah, os barulhentos dos fundos. Eles trituravam essências puras na velha Oficina de baixo. Eldrin deve ter a chave."
            $ knows_oficina = True
            $ log_event("Player aprendeu a existência da Oficina.")
            jump aurelium_talk_loop
            
        "O que pode me dizer sobre essa sala?" if not has_potion:
            $ mark_aurelium_topic_seen("magia_selamento")
            aurelium "Há {color=#ffd700}magias de selamento{/color} nesta biblioteca. Você precisa de olhos novos. O alquimista escondia a essencia para enxergar o invisivel em algum lugar dessa biblioteca."
            jump aurelium_talk_loop
            
        "O que significa a frase do mural?" if read_mural:
            $ mark_aurelium_topic_seen("interpretacao")
            aurelium "Aparenta ser a verdade sobre o que aconteceu em Aethra. Pense no que o mural diz sobre apagar as falhas..."
            jump aurelium_talk_loop
        
        "← Voltar ao menu":
            jump aurelium_talk_loop

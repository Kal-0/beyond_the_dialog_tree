# ==============================================================
# DIÁLOGOS DE ELDRIN - MODO PRÉ-DEFINIDO COM GRUPOS TEMÁTICOS
# ==============================================================

label falar_eldrin_porta:
    show eldrin normal at left with dissolve
    if not met_eldrin:
        eldrin "Encontrou algo em meio aos restos deste lugar? Ou só veio me observar?"
        $ met_eldrin = True
        $ mark_npc_met("eldrin")
    else:
        eldrin "Ainda aqui... O que deseja agora?"
        
    call call_npc_dialog("eldrin", "falar_eldrin_porta_end")
    return

label falar_eldrin_porta_end:
    hide eldrin normal with dissolve
    jump sala_porta_loop

# ==============================================================
# TÓPICOS PAIS: ELDRIN
# ==============================================================

label dialog_eldrin_group_sobre_voce:
    eldrin "Sou apenas o zelador de um túmulo de memórias. O que mais quer arrancar de mim?"
    return

label dialog_eldrin_group_sobre_porta:
    eldrin "A porta selada, uma barreira que protege o mundo daquilo que jaz nas profundezas. É a sua saida daqui, mas para onde ela o levará é um mistério."
    return

label dialog_eldrin_group_direcionamento:
    eldrin "Uhhh... (suspira pesadamente) Vejamos se você é digno de caminhar além deste corredor."
    return

label dialog_eldrin_group_exploracoes:
    eldrin "Esta torre guarda segredos antigos. O que você acha que descobriu?"
    return

label dialog_eldrin_group_magia:
    eldrin "A magia aqui foi torcida e mutilada por ambição. Me diga o que quer saber."
    return

label dialog_eldrin_group_a_verdade:
    eldrin "Você caminhou nas sombras. Você viu as correntes que prendem este lugar. O que tem a me dizer?"
    return

# ==============================================================
# TÓPICOS ATÔMICOS FILHOS: ELDRIN
# ==============================================================

label dialog_eldrin_quem_eh:
    eldrin "Meu nome é Eldrin. Já fui um Mago de Aethra, mas agora sou apenas o guardião dos nossos erros."
    return

label dialog_eldrin_testando:
    eldrin "Naturalmente. Se não puder entender as menores engrenagens desta torre, você não seria de uso nenhum."
    $ eldrin_trust += 1
    $ asked_if_testing = True
    return

label dialog_eldrin_confianca:
    eldrin "Porque a curiosidade impensada é uma doença que destrói mundos. Mas você parece querer entender o peso das coisas, não apenas usá-las."
    $ eldrin_trust += 1
    return

label dialog_eldrin_por_que_guarda:
    eldrin "Porque fui eu que ajudei a forjar os cadeados. A corrupção ainda sussurra para mim. Eu a mantenho contida... ou tento."
    return

label dialog_eldrin_selada:
    eldrin "Sim. Um selo que não responde à força bruta, apenas ao entendimento de um propósito maior."
    return

label dialog_eldrin_magia_antiga:
    eldrin "Sim, você precisa provar que entende o porquê desta porta estar selada."
    if eldrin_trust >= 3:
        eldrin "Se insiste em entender de onde veio nosso orgulho e queda, vá ao {color=#ffd700}Observatório{/color}. Talvez a lua ainda brilhe para você."
        eldrin "Pegue esta {color=#ffd700}chave{/color}."
        $ has_key_observatorio = True
        $ log_event("Player desbloqueou Observatorio via Confiança de Eldrin.")
    return

label dialog_eldrin_o_que_fazer:
    eldrin "Não corra em direção ao abismo de olhos fechados. Explore cada sala de minuciosamente, talvez você encontre algo interessante."
    return

label dialog_eldrin_direcionamento:
    eldrin "Se você não prestar atenção ao passado, repetirá nossos fracassos. Vá à {color=#ffd700}Biblioteca Arcana{/color} e veja se os velhos livros dali ainda têm sabedoria."
    eldrin "Tome a {color=#ffd700}chave{/color}. E não me incomode com tolices."
    $ has_key_biblioteca = True
    $ log_event("Player obteve chave da Biblioteca.")
    return

label dialog_eldrin_aonde_ir:
    eldrin "Você tem acesso à Biblioteca. Procure respostas entre as prateleiras esquecidas e fale com Aurelium."
    return

label dialog_eldrin_procura_oficina:
    eldrin "A caveira de Skulla. Cuidado com ela, seu deboche esconde o remorso."
    return

label dialog_eldrin_perdido:
    eldrin "A torre é um labirinto, mas também um espelho. As respostas estão nas salas que você abriu."
    return

label dialog_eldrin_torre_esconde:
    eldrin "Alquimia. O começo da nossa ruína. Leve a {color=#ffd700}chave{/color} da {color=#ffd700}Oficina{/color}, e veja os restos de nossa arrogância por si mesmo."
    $ has_key_oficina = True
    $ log_event("Player desbloqueou Oficina guiado por Aurelium.")
    return

label dialog_eldrin_procura_observatorio:
    eldrin "As magias que selaram este lugar vieram do cosmos. Leve a {color=#ffd700}chave{/color} do {color=#ffd700}Observatório{/color}. Pode ser que uma centelha de esperança ainda esteja lá."
    $ has_key_observatorio = True
    $ log_event("Player desbloqueou Observatorio guiado por Skulla.")
    return

label dialog_eldrin_magia_funciona:
    eldrin "Neste lugar, a intenção se torna realidade. Cuidado com o que deseja empunhando essa varinha."
    if not asked_magia:
        $ eldrin_trust += 1
        $ asked_magia = True
    return

label dialog_eldrin_encarando:
    eldrin "Vejo que algo expandiu sua visão. Você agora vê as marcas ocultas. Não enlouqueça tentando ler o que não deve."
    if not asked_encarando:
        $ eldrin_trust += 1
        $ asked_encarando = True
    return

label dialog_eldrin_provando_verdade:
    eldrin "Você encontrou o coração do nosso pecado. Os magos tentaram alterar a verdade usando um artefato amaldiçoado."
    eldrin "O selo que eu criei cortou Aethra do resto do multiverso para que a corrupção não se espalhasse."
    eldrin "Eu trouxe você de outro mundo porque sua alma não está amarrada às nossas leis. O artefato não tem poder absoluto sobre você."
    eldrin "Agora me diga... o que aquela frase significa?"
    
    menu:
        "A verdade é imutável, mesmo quando esquecida.":
            eldrin "Exatamente. Eles tentaram apagar suas falhas mudando a realidade. Mas a verdade sempre permanece."
            $ eldrin_trust += 3
        "Significa que a memória é o mais importante.":
            eldrin "Não. É muito mais profundo. A verdade não precisa ser lembrada para existir."

    eldrin "A porta final pode ser aberta agora. Mas você deve fazer a escolha que não pude fazer para salvar o que restou, ou que fui covarde demais para tentar..."
    return

label dialog_eldrin_quebrar_selo:
    $ final_choice_made = True
    eldrin "*Os olhos de Eldrin se arregalam com um misto de alívio e pavor.* Você vai enfrentar o artefato..."
    eldrin "Que o multiverso tenha piedade de sua alma, forasteiro. O selo será quebrado."
    eldrin "Até mais, Viajante. Estarei esperando por você do outro lado, torcendo pelo seu sucesso!"
    
    $ final_choice = "break"
    return

label dialog_eldrin_ir_embora:
    $ final_choice_made = True
    eldrin "*Ele fecha os olhos e um longo suspiro escapa de seus lábios.* Então o sacrifício de Aethra será eterno. Nos deixará ao esquecimento."
    eldrin "É uma escolha sábia... Porém, eu torcia para que você não agisse da mesma forma que eu. O portal para seu mundo original se abrirá, e nunca mais poderá voltar."
    eldrin "Adeus, Forasteiro. Tudo isso não passará de um sonho bizarro para você."

    $ final_choice = "leave"
    return


# ==============================================================
# SKULLA - OFICINA ALQUÍMICA
# ==============================================================

label falar_skulla_oficina:
    show skulla at right with dissolve
    if not met_skulla:
        skulla "Ah, ótimo. Um herói perdido que vive em outro mundo. Bem-vindo à minha humilde bancada de decomposição."
        $ met_skulla = True
        $ mark_npc_met("skulla")
    else:
        skulla "Esse caldeirão não se ferve sozinho. O que você quer? Não vê que estou ocupada estando morta?"
        
    call call_npc_dialog("skulla", "falar_skulla_oficina_end")
    return

label falar_skulla_oficina_end:
    hide skulla with dissolve
    jump sala_oficina_loop

label dialog_skulla_group_sobre_voce:
    skulla "Óbvio que sim!! Sou Skulla, Mestra Alquimista. Eldrin gosta de dizer que fomos arrogantes. Eu digo que fomos grandiosos e só."
    return

label dialog_skulla_group_conhecimento:
    skulla "Alquimia. A arte de mudar o universo de dentro pra fora. Eu poderia te ensinar se você não fosse tão tapado."
    return

label dialog_skulla_group_a_verdade:
    skulla "A 'verdade'? haha...(Risada seca). Vamos ver o quanto você é inocente."
    return

label dialog_skulla_quem_eh:
    skulla "Eu já fui a mente mais brilhante deste buraco. Hoje sou um objeto de decoração rústica."
    return

label dialog_skulla_como_perdeu:
    skulla "Uma explosão astral na tentativa de sublimar essências da realidade pura. Foi lindo... por dois segundos."
    return

label dialog_skulla_sabe_util:
    skulla "Eldrin e o resto do conselho eram hipócritas. Se você quer sair daqui, pare de ouvi-lo e comece a ver por si mesmo."
    return

label dialog_skulla_producoes:
    skulla "A poção de Visão Arcana? Vá até a mesa, use o caldeirão. Se for incompetente demais para saber os ingredientes, estude os livros empoeirados da biblioteca."
    return

label dialog_skulla_pocao:
    skulla "Não explodiu? Surpreendente. Vá para a biblioteca e olhe com atenção. Os segredos foram gravdados onde há algo para se esconder."
    return

label dialog_skulla_sobre_verdade:
    skulla "A 'Veritas'?! Pfft... A frase secreta é patética. É só uma mentira que Eldrin conta para si mesmo no espelho para justificar nos ter enterrado vivos!"
    skulla "Se tem coragem, desfaça a magia dele. A torre é uma prisão, não um escudo."
    return


# ==============================================================
# NEKRONS - OBSERVATÓRIO
# ==============================================================

label falar_nekrons_obs:
    show nekrons at center with dissolve
    if not met_nekrons:
        nekrons "Bem-vindo ao topo do mundo esquecido. Vejo que os fios do seu destino não se prendem a Aethra."
        $ met_nekrons = True
        $ mark_npc_met("nekrons")
    else:
        nekrons "As centelhas no ar indicaram que você voltaria."
        
    call call_npc_dialog("nekrons", "falar_nekrons_obs_end")
    return

label falar_nekrons_obs_end:
    hide nekrons with dissolve
    jump sala_observatorio_loop

label dialog_nekrons_group_sobre_voce:
    nekrons "Um gato? Talvez. Um reflexo cósmico? Certamente."
    return

label dialog_nekrons_group_conhecimento:
    nekrons "O que deseja descobrir através da lente do cosmos?"
    return

label dialog_nekrons_group_magia:
    nekrons "A magia pura reage à vontade. Use-a apenas quando as palavras não bastarem."
    return

label dialog_nekrons_group_a_verdade:
    nekrons "A verdade ressoa nas paredes como um acorde dissonante."
    return

label dialog_nekrons_quem_eh:
    nekrons "Sou Nekrons. Os antigos magos achavam que me possuíam como familiar. Quanta ingenuidade..."
    return

label dialog_nekrons_nao_gato:
    nekrons "O formato felino é apenas uma vestimenta confortável para observar o fim de um mundo."
    return

label dialog_nekrons_o_que_lugar:
    nekrons "Este observatório não olhava apenas para as estrelas do nosso céu, mas para as frestas de outras realidades."
    nekrons "No entanto, no momento, o que você precisa está em um lugar muito mais mundano... no topo daquela mesa, pegue a varinha."
    return

label dialog_nekrons_conhece_eldrin:
    nekrons "Pobre Eldrin. Ele tenta segurar as comportas de um oceano com as próprias mãos. Uma culpa pesada demais para um homem só."
    return

label dialog_nekrons_varinha:
    nekrons "Ela não está quebrada, apenas sem ressonância."
    "*A gata preta salta até o telescópio, ajustando as lentes para alinhar com uma constelação oculta.*"
    nekrons "A magia é intenção, forasteiro. Acorde-a com a sua."
    with vpunch
    "*A varinha brilha com intensidade e parece pulsar com sua própria vontade.*"
    $ wand_active = True
    $ log_event("Nekrons reativou a varinha.")
    return

label dialog_nekrons_como_magia:
    nekrons "A magia não é um fogo que se domina, mas um rio que se navega."
    nekrons "Uma forte convicção é o que materializa a magia."
    return 

label dialog_nekrons_sobre_verdade:
    nekrons "Veritas manet quod oblivio delet... Essa frase vibra. É a âncora que Eldrin usou para selar a Torre."
    nekrons "Quando o conselho manipulou a realidade com o artefato, eles queriam esquecer os pecados, mas a frase os acorrentou."
    nekrons "Dentro dela reside a chave para quebrar o selo."
    return


# ==============================================================
# AURELIUM - BIBLIOTECA
# ==============================================================

label falar_aurelium_bib:
    show aurelium_book at center with dissolve
    if not met_aurelium:
        aurelium "vozes... tantas vozes... Ah, um leitor de carne e osso. Faz séculos que não sinto o calor de uma mão."
        $ met_aurelium = True
        $ mark_npc_met("aurelium")
    else:
        aurelium "Vire a página, buscador. As areias do tempo não param para ninguém."
        
    call call_npc_dialog("aurelium", "falar_aurelium_bib_end")
    return

label falar_aurelium_bib_end:
    hide aurelium_book with dissolve
    jump sala_biblioteca_loop

label dialog_aurelium_group_sobre_voce:
    aurelium "Sou apenas o que sobrou de mim mesmo... Ecos e pedaços de um homem sábio."
    return

label dialog_aurelium_group_conhecimento:
    aurelium "As prateleiras sabem de coisas... sussurram."
    return

label dialog_aurelium_group_a_verdade:
    aurelium "O segredo oculto... está ardendo na tinta."
    return

label dialog_aurelium_quem_eh:
    aurelium "Me chamo Aurelium. Fui um humano, um oráculo. Mas minhas profecias eram tão enigmáticas que me puniram aprisionando minha alma a estas páginas."
    return

label dialog_aurelium_solitario:
    aurelium "As prateleiras não são quietas. Há ecos aflitos de magos que foram selados aqui. Eles gritam por uma passagem nas paredes..."
    return

label dialog_aurelium_sobre_torre:
    aurelium "Um santuário do saber... que virou um matadouro de realidades. Mexeram com forças imensuráveis. O guardião trancou tudo para nos salvar... ou nos condenar."
    return

label dialog_aurelium_escrituras_estante:
    aurelium "As runas brilham intensamente acima daquela estante grande. O que dizem?"
    "*Você olha para a estante, mas não vê brilho algum.*"
    "Eu não vejo nada."
    aurelium "Sua visão material é inútil. Você não bebeu nenhuma poção de visão arcana? Estude os livros daquelas estantes, há de haver alguma receita alquímica perdida por ali."
    $ knows_vision_potion = True
    $ log_event("Player descobriu sobre a poção de visão através de Aurelium.")
    return

label dialog_aurelium_sobre_alquimistas:
    aurelium "Alquimia? Fumaça verde, explosões, frascos que mostram o invisível... Os idiotas brilhantes trabalhavam na Oficina."
    $ knows_oficina = True
    $ log_event("Player aprendeu sobre a oficina com Aurelium.")
    return

label dialog_aurelium_sobre_magia:
    aurelium "As estrelas... magias ancestrais guiadas por luz. O gato preto vigia o Observatório no andar de cima."
    $ knows_observatorio = True
    $ log_event("Player aprendeu sobre o observatorio com Aurelium.")
    return

label dialog_aurelium_interpretacao:
    aurelium "A língua antiga de Aethra... Significa algo como 'A verdade permanece onde o esquecimento apaga'. É uma resposta a quem tenta alterar a história com magia."
    return

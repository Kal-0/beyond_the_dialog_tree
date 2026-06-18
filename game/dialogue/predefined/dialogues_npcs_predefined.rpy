# ==============================================================
# DIÁLOGOS DOS NPCS - MODO PRÉ-DEFINIDO (CONCEITO ALINHADO)
# ==============================================================

# ==============================================================
# ELDRIN - SALA DA PORTA (GUARDIÃO DESCONFIADO)
# ==============================================================

label falar_eldrin_predef:
    if game_metrics:
        $ game_metrics.record_dialog("eldrin")
    show eldrin normal at left with dissolve
    if not met_eldrin:
        eldrin "Encontrou algo em meio aos restos deste lugar? Ou só veio me observar, forasteiro?"
        $ met_eldrin = True
        $ mark_npc_met("eldrin")
    else:
        eldrin "Ainda rondando a porta? A pressa não vai quebrar este selo. O que você quer?"
        
    call call_npc_dialog("eldrin", "falar_eldrin_porta_end") from _call_call_npc_dialog
    return

label falar_eldrin_porta_end:
    hide eldrin normal with dissolve
    jump sala_porta_loop

# --- TÓPICOS PAIS: ELDRIN ---

label dialog_eldrin_group_sobre_voce:
    eldrin "Não há muito o que saber sobre mim. Sou apenas o zelador deste túmulo de memórias. O que quer arrancar de mim?"
    return

label dialog_eldrin_group_sobre_porta:
    eldrin "A porta selada. Uma barreira que protege o que está além... e o que está além de nós. O que quer saber?"
    return

label dialog_eldrin_group_direcionamento:
    eldrin "O tempo não espera, mas a pressa só atrai o desastre. Vejamos se você tem juízo."
    return

label dialog_eldrin_group_descobertas:
    eldrin "Esta torre guarda segredos antigos. O que você acha que descobriu?"
    return

label dialog_eldrin_group_magia:
    eldrin "A magia aqui foi torcida e mutilada por ambição. Me diga o que quer saber."
    return

label dialog_eldrin_group_a_verdade:
    eldrin "Você desceu às profundezas e viu as marcas do passado. O que tem a me dizer?"
    return

# --- TÓPICOS FILHOS: ELDRIN ---

label dialog_eldrin_quem_eh:
    eldrin "Eldrin. Outrora conselheiro e mago de Aethra. Hoje, apenas uma sombra que vigia o que restou."
    eldrin "Não me pergunte sobre o passado. Há coisas que é melhor não remexer."
    
    menu:
        "Entendo. Todos carregam cicatrizes que preferem não mostrar.":
            eldrin "...Talvez haja esperança para você, afinal."
            $ eldrin_trust += 1
        "Se o passado te assombra tanto assim, talvez devesse enfrentá-lo em vez de fugir.":
            eldrin "Fugir? Você não sabe nada sobre o que enfrentei."
            eldrin "Mas... talvez suas palavras tenham um fundo de verdade que prefiro não admitir."
            
        "Segredos são ferramentas de controle. Quero saber o que você esconde.":
            eldrin "Controle? Eu estou tentando proteger o que resta deste mundo!"
            eldrin "Sua desconfiança é um veneno, forasteiro. Tome cuidado com ela."
            $ eldrin_trust -= 2
    return

label dialog_eldrin_testando:
    eldrin "Talvez. Esta torre não é lugar para tolos. Se não puder desvendar as menores runas daqui, não será de serventia nenhuma."
    $ eldrin_trust += 1
    $ asked_if_testing = True
    return

label dialog_eldrin_confianca:
    eldrin "Porque a curiosidade impensada é o que destrói mundos. Eu vi isso acontecer."
    eldrin "Mas... vejo em seus olhos um desejo sincero de compreensão, não apenas sede de poder. Isso é raro neste lugar."
    $ eldrin_trust += 1
    return

label dialog_eldrin_por_que_guarda:
    eldrin "Porque ajudei a forjar os cadeados. A corrupção de Aethra ainda sussurra atrás deste selo."
    eldrin "Alguém precisa segurá-la. Se não eu, quem?"
    
    menu:
        "Um fardo pesado. Admiro sua dedicação.":
            eldrin "Dedicação... ou penitência. Mas agradeço suas palavras."
            $ eldrin_trust += 1
        "Parece que você se trancou aqui junto com o problema. Isso foi sabedoria ou medo?":
            if eldrin_trust >= 3:
                eldrin "...medo."
                eldrin "Talvez eu tenha sido covarde. Mas a alternativa era deixar a corrupção se espalhar. Você teria feito diferente?"
            else:
                eldrin "Você não tem ideia do que está falando."
                eldrin "Sua insolencia mostra que você não entende a gravidade do que aconteceu aqui."
                "*Eldrin fica visivelmente incomodado com a insinuação, mais do que o normal.*"
                

        "Você criou essa prisão e agora quer que eu sinta pena? Assuma suas culpas sozinho.":
            eldrin "Pena? Eu não peço sua pena, forasteiro."
            eldrin "Peço apenas que não piore o que já está destruído. Mas talvez isso seja demais para alguém como você."
            $ eldrin_trust -= 2
    return

label dialog_eldrin_selada:
    eldrin "Sim. O selo é mantido por uma magia ancestral."
    eldrin "Ela não cede à força bruta, forasteiro. Ela pede por uma {color=#ffd700}palavra{/color}. Uma única palavra que prove que você compreendeu o propósito deste selo."
    eldrin "Não me pergunte qual é. Você terá que descobrir por conta própria."
    $ knows_porta_needs_password = True
    $ renpy.notify("Você descobriu que a porta selada exige uma senha.")
    
    menu:
        "Então precisarei estudar este lugar a fundo. Onde devo começar?":
            eldrin "Boa pergunta. Comece pelas salas que já tem acesso. As respostas estão espalhadas pela torre."
            $ eldrin_trust += 1
        "Uma palavra? Parece um ritual desnecessário. Deve haver outro caminho.":
            eldrin "Outro caminho? Não há atalhos quando se trata de magia ancestral."
            eldrin "Sua impaciência o leva a perdição."
            $ eldrin_trust -= 1
        "Se a palavra existe, alguém a conhece. E algo me diz que esse alguém é você.":
            eldrin "Mesmo que eu a soubesse, entregá-la a um desconhecido seria irresponsável."
            eldrin "Você não merece respostas que não conquistou. Prove seu valor primeiro."
            $ eldrin_trust -= 2
    return

label dialog_eldrin_magia_antiga:
    eldrin "Você quer abrir a porta, mas ainda não entendeu o porquê de ela estar selada."
    if eldrin_trust >= 2:
        eldrin "No entanto... você demonstrou cautela e respeito ao investigar os segredos deste lugar."
        eldrin "Se insiste em entender de onde veio nossa queda, vá ao {color=#ffd700}Observatório{/color}. A magia que selou este lugar veio do cosmos."
        eldrin "Tome a {color=#ffd700}chave{/color}."
        $ has_key_observatorio = True
        $ knows_observatorio = True
        $ renpy.notify("Você obteve a chave do Observatório!")
        $ log_event("Player desbloqueou Observatorio via Confiança de Eldrin.")
    else:
        eldrin "Busque respostas nas salas que já tem acesso. Você ainda não provou que merece minha confiança."
    return

label dialog_eldrin_o_que_fazer:
    eldrin "Explore cada canto com atenção. A resposta não está em um único lugar, mas na conexão entre eles."
    return

label dialog_eldrin_direcionamento:
    eldrin "Se quer livros legíveis, vá à {color=#ffd700}Biblioteca Arcana{/color} para saciar sua fome de conhecimento."
    eldrin "Tome a {color=#ffd700}chave{/color}. E não me interrompa mais com perguntas óbvias."
    $ has_key_biblioteca = True
    $ knows_biblioteca = True
    $ renpy.notify("Você obteve a chave da Biblioteca Arcana!")
    $ log_event("Player obteve chave da Biblioteca.")
    return

label dialog_eldrin_aonde_ir:
    eldrin "Você tem acesso à Biblioteca. Procure respostas entre as prateleiras e fale com quem encontrar lá."
    return

label dialog_eldrin_procura_oficina:
    eldrin "A Oficina Alquímica. Cuidado com a caveira que reside lá. Seu deboche esconde o peso do próprio remorso."
    return

label dialog_eldrin_perdido:
    eldrin "A torre é um labirinto, mas também um espelho. As respostas estão nas salas que você abriu."
    return

label dialog_eldrin_torre_esconde:
    eldrin "Alquimia. O começo da nossa ruína. Leve a {color=#ffd700}chave{/color} da {color=#ffd700}Oficina{/color}, e veja os restos de nossa arrogância por si mesmo."
    $ has_key_oficina = True
    $ knows_oficina = True
    $ renpy.notify("Você obteve a chave da Oficina Alquímica!")
    $ log_event("Player desbloqueou Oficina após saber da alquimia via Aurelium.")
    return

label dialog_eldrin_procura_observatorio:
    eldrin "Energia mágica no observatório? Faz sentido. As magias que selaram este lugar vieram do cosmos."
    eldrin "Leve a {color=#ffd700}chave{/color} do {color=#ffd700}Observatório{/color}. Pode ser que uma centelha de esperança esteja lá."
    $ has_key_observatorio = True
    $ knows_observatorio = True
    $ renpy.notify("Você obteve a chave do Observatório!")
    $ log_event("Player desbloqueou Observatorio após saber via Skulla.")
    return

label dialog_eldrin_procura_biblioteca:
    eldrin "Sim, os tomos antigos estão lá. Se você pretende brincar com as palavras de poder que selaram nosso destino, não serei eu a impedi-lo."
    eldrin "Tome a {color=#ffd700}chave{/color} da {color=#ffd700}Biblioteca Arcana{/color}."
    $ has_key_biblioteca = True
    $ knows_biblioteca = True
    $ renpy.notify("Você obteve a chave da Biblioteca Arcana!")
    $ log_event("Player desbloqueou Biblioteca após saber via Nekrons.")
    return

label dialog_eldrin_magia_funciona:
    eldrin "Neste lugar, a intenção molda o éter. Cuidado com o que deseja empunhando essa varinha."
    if not asked_magia:
        $ eldrin_trust += 1
        $ asked_magia = True
    return

label dialog_eldrin_encarando:
    eldrin "Vejo que algo expandiu sua visão. Você agora vê marcas que estavam ocultas."
    eldrin "Não enlouqueça tentando ler o que não deve."
    if not asked_encarando:
        $ eldrin_trust += 1
        $ asked_encarando = True
    return

label dialog_eldrin_provando_verdade:
    $ mark_topic_seen("eldrin", "provando_verdade")
    eldrin "Você desceu à catacumba secreta. Viu o mural onde a história de nossa queda está escrita em sangue."
    eldrin "Diga-me então. O que aquela frase significa?"
    
    menu:
        "A verdade permanece ativa, mesmo quando a memória a apaga.":
            eldrin "Sim! Você compreendeu!"
            eldrin "Nós tentamos apagar a dor das nossas falhas apagando as memórias da própria realidade. Mas a verdade é uma rocha que não pode ser desfeita."
            eldrin "Seu entendimento provou que eu estava certo em... em trazê-lo para cá."
            $ eldrin_trust += 2

            if eldrin_trust >= 7:
                eldrin "Você já deveria saber, ou ao menos suspeitar, mas a palavra que abre o selo é: '{color=#ffd700}[senha_porta!t]{/color}'. Use-a na porta principal."
    
                $ eldrin_revealed_password = True
                $ story_state["eldrin_revealed_password"] = True
                $ renpy.notify("Você descobriu a senha do selo: " + senha_porta.capitalize() + "!")
            else:
                eldrin "Mas percebo que ainda não confio plenamente em você. Eu lhe darei a chave, mas você terá que forjá-la em sua própria mente."
                eldrin "A palavra que abre o selo principal é o próprio conceito sobre o qual conversamos. Aquilo que permanece quando as mentiras caem."
                eldrin "Vá até a porta principal e proclame essa palavra. Em sua língua ou na língua antiga."
        "A memória das pessoas é mais importante do que fatos frios.":
            eldrin "Não. Isso é exatamente a mentira que nos destruiu."
            eldrin "Tentamos priorizar o sentimento em detrimento dos fatos, e por isso distorcemos o próprio tempo."
            eldrin "Vá refletir sobre o mural. Converse com os outros. Talvez eles consigam abrir seus olhos para o que eu não consigo."
            $ eldrin_trust -= 2

        "A Skulla já me contou a verdade. Significa que você me invocou para limpar sua própria bagunça!" if knows_invocation_secret:
            eldrin "A caveira sempre teve a língua solta... até quando não tem língua."
            eldrin "Mas não muda nada. Você está aqui, e o selo precisa ser quebrado."
            eldrin "Eu fiz o que precisava ser feito para salvar Aethra. Se você não entende isso, então não temos mais o que conversar."
            $ eldrin_trust -= 1
            jump falar_eldrin_porta_end
    return

# ==============================================================
# SKULLA - OFICINA ALQUÍMICA (SARCÁSTICA E CÉTICA)
# ==============================================================

label falar_skulla_predef:
    if game_metrics:
        $ game_metrics.record_dialog("skulla")
    show skulla at right with dissolve
    if not met_skulla:
        skulla "Ah, ótimo. Mais um herói perdido que vem de outro mundo. Bem-vindo à minha humilde bancada de decomposição."
        $ met_skulla = True
        $ mark_npc_met("skulla")
    else:
        skulla "Esse caldeirão não se ferve sozinho. O que você quer? Não vê que estou ocupada estando morta?"
        
    call call_npc_dialog("skulla", "falar_skulla_oficina_end") from _call_call_npc_dialog_1
    return

label falar_skulla_oficina_end:
    hide skulla with dissolve
    jump sala_oficina_loop

# --- TÓPICOS PAIS: SKULLA ---

label dialog_skulla_group_sobre_voce:
    skulla "Óbvio que sim!! Sou Skulla, Mestra Alquimista. Eldrin gosta de dizer que fomos arrogantes. Eu digo que fomos grandiosos e só."
    return

label dialog_skulla_group_conhecimento:
    skulla "Alquimia. A arte de mudar o universo de dentro pra fora. Eu poderia te ensinar se você não fosse tão tapado."
    return

label dialog_skulla_group_a_verdade:
    skulla "A 'verdade'? haha...(Risada seca). Vamos ver o quanto você é inocente."
    return

# --- TÓPICOS FILHOS: SKULLA ---

label dialog_skulla_quem_eh:
    skulla "Eu já fui a mente mais brilhante deste buraco. Hoje sou um objeto de decoração rústica."
    return

label dialog_skulla_como_perdeu:
    skulla "Uma explosão astral na tentativa de sublimar essências da realidade pura. Foi lindo... por dois segundos."
    return

label dialog_skulla_sabe_util:
    skulla "Eldrin e o resto do conselho eram hipócritas. Se você quer sair daqui, pare de ouvi-lo e comece a encontrar uma saída por si mesmo."
    return

label dialog_skulla_producoes:
    skulla "A poção de Visão Arcana? Use o {color=#ffd700}caldeirão{/color} ali. Acenda o fogo com um feitiço, encha de água e jogue os {color=#ffd700}ingredientes{/color} que encontrar na {color=#ffd700}mesa{/color}."
    skulla "Se for incompetente demais para saber quais ingredientes usar, estude os livros empoeirados da biblioteca."
    return

label dialog_skulla_pocao:
    skulla "Não explodiu? Surpreendente. Agora vá para a {color=#ffd700}biblioteca{/color} e olhe com atenção."
    skulla "Os segredos foram gravados onde há algo para se esconder. Use esses novos olhos para encontrar o que está oculto."
    return

label dialog_skulla_sobre_lumos:
    skulla "Se você lesse os livros direito, saberia que a poção da Visão Arcana precisa de uma luz especial para catalisar."
    skulla "Antigamente usavam a luz da lua... Mas um feitiço iluminador deve servir, já que estamos confinados aqui."
    return

label dialog_skulla_sobre_observatorio:
    skulla "Eu mesma poderia fazer essa poção, mas estou sem luz arcana."
    skulla "Você deveria ir para o andar de cima, no {color=#ffd700}Observatório{/color}. Aquele lugar emana energia mágica constantemente."
    skulla "Se houver algo que possa te ajudar com magia, vai estar lá."
    $ knows_observatorio = True
    $ renpy.notify("Você ouviu sobre o Observatório das Estrelas.")
    $ log_event("Player descobriu sobre o observatório com Skulla.")
    return

label dialog_skulla_sobre_verdade:
    skulla "Pfft... que bando de idiotices."
    skulla "Como se a verdade fosse algo que sobrevive numa torre de mentiras."
    skulla "É só mais uma frase bonita que Eldrin repetiria para si mesmo no espelho para justificar nos ter enterrado vivos!"
    skulla "Se tem coragem, desfaça o selo e vá embora. A torre é uma prisão, não um escudo."
    
    skulla "Aliás... me diga uma coisa, forasteiro."
    skulla "Você confia no Eldrin?"
    
    menu:
        "Sim. Ele parece genuíno, mesmo que desconfiado.":
            skulla "Heh. Ingênuo. Mas quem sou eu para julgar... já fui ingênua o bastante para brincar com forças que não compreendia."
            skulla "Só não diga que eu não avisei quando descobrir que nem tudo é o que parece."
        "Não. Tem algo que ele não está me contando.":
            skulla "Finalmente alguém com meio neurônio funcionando nessa torre."
            skulla "Olha... eu sei de uma coisa que o velho não quer que você saiba."
            skulla "Você não 'caiu' aqui por acidente, forasteiro. Eldrin te {color=#ffd700}invocou{/color}. De propósito."
            skulla "Ele puxou você de outra dimensão porque precisava de alguém de fora para fazer o trabalho sujo dele."
            skulla "Destruir o artefato que corrompeu Aethra. Algo que ele mesmo não consegue fazer."
            skulla "Então antes de confiar cegamente no 'guardião nobre', lembre-se: você é uma ferramenta pra ele. Nada mais."
            skulla "Não estou dizendo que ele é mau... mas ele não é honesto. E nesta torre, desonestidade tem um preço."
            $ knows_invocation_secret = True
            $ renpy.notify("Você descobriu o Segredo da Invocação!")
    return


# ==============================================================
# NEKRONS - OBSERVATÓRIO (MÍSTICA E OBSERVADORA DO TEMPO)
# ==============================================================

label falar_nekrons_predef:
    if game_metrics:
        $ game_metrics.record_dialog("nekrons")
    show nekrons at center with dissolve
    if not met_nekrons:
        nekrons "Bem-vindo ao topo do mundo esquecido. Vejo que os fios do seu destino não se prendem a Aethra."
        $ met_nekrons = True
        $ mark_npc_met("nekrons")
    else:
        nekrons "As centelhas no ar indicaram que você voltaria."
        
    call call_npc_dialog("nekrons", "falar_nekrons_obs_end") from _call_call_npc_dialog_2
    return

label falar_nekrons_obs_end:
    hide nekrons with dissolve
    jump sala_observatorio_loop

# --- TÓPICOS PAIS: NEKRONS ---

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

# --- TÓPICOS FILHOS: NEKRONS ---

label dialog_nekrons_quem_eh:
    nekrons "Sou Nekrons. Os antigos magos achavam que me possuíam como familiar. Quanta ingenuidade..."
    return

label dialog_nekrons_nao_gato:
    nekrons "O formato felino é apenas uma vestimenta confortável para observar o fim de um mundo."
    return

label dialog_nekrons_o_que_lugar:
    nekrons "Este observatório não olhava apenas para as estrelas do nosso céu, mas para as frestas de outras realidades."
    nekrons "No entanto, no momento, o que você precisa está em um lugar muito mais mundano..."
    nekrons "Na {color=#ffd700}mesa{/color} à sua frente. Pegue a {color=#ffd700}varinha antiga{/color}."
    return

label dialog_nekrons_conhece_eldrin:
    nekrons "Pobre Eldrin. Ele tenta segurar as comportas de um oceano com as próprias mãos."
    nekrons "Uma culpa pesada demais para um homem só. Eu não o temo... sinto piedade."
    return

label dialog_nekrons_sobre_biblioteca:
    nekrons "Feitiços são intenções cristalizadas em palavras. Cada palavra carrega um eco de poder."
    nekrons "Os antigos magos registraram suas palavras de poder em livros na {color=#ffd700}Biblioteca Arcana{/color}, nos andares inferiores."
    nekrons "Se quer dominar mais feitiços, é lá que deve ir."
    if not has_key_biblioteca:
        $ knows_biblioteca = True
        $ renpy.notify("Você ouviu sobre a Biblioteca Arcana.")
        $ log_event("Player descobriu sobre a biblioteca com Nekrons.")
    return

label dialog_nekrons_varinha:
    nekrons "Ela não está quebrada, apenas sem ressonância."
    "*A gata preta observa a varinha em suas mãos.*"
    nekrons "A magia é intenção, forasteiro. Para acordar um conduíte arcano, você precisa preenchê-lo com luz primordial."
    nekrons "Concentre-se e pronuncie a palavra '{color=#ffd700}Lumos{/color}' enquanto a empunha."
    nekrons "Isso será o suficiente para despertá-la."
    $ log_event("Nekrons ensinou lumos para reativar a varinha.")
    return

label dialog_nekrons_como_magia:
    nekrons "A magia não é um fogo que se domina, mas um rio que se navega."
    nekrons "Uma forte convicção é o que a materializa. Fale a palavra de poder com clareza e a realidade responderá."
    return 

label dialog_nekrons_sobre_verdade:
    nekrons "Veritas manet quod oblivio delet..."
    nekrons "Essa frase vibra nas profundezas da torre. Existe uma palavra nela que ressoa com o resto desse lugar."
    nekrons "Eu consigo sentir sua vibração... como um coração batendo dentro do selo."
    return


# ==============================================================
# AURELIUM - BIBLIOTECA (ORÁCULO AMNÉSICO APRISIONADO)
# ==============================================================

label falar_aurelium_predef:
    if game_metrics:
        $ game_metrics.record_dialog("aurelium")
    show aurelium_book at center with dissolve
    if not met_aurelium:
        aurelium "Vozes... tantas vozes... Ah, um leitor de carne e osso. Faz séculos que não sinto o calor de uma mão."
        $ met_aurelium = True
        $ mark_npc_met("aurelium")
    else:
        aurelium "Vire a página, buscador. As areias do tempo não param para ninguém."
        
    call call_npc_dialog("aurelium", "falar_aurelium_bib_end") from _call_call_npc_dialog_3
    return

label falar_aurelium_bib_end:
    hide aurelium_book with dissolve
    jump sala_biblioteca_loop

# --- TÓPICOS PAIS: AURELIUM ---

label dialog_aurelium_group_sobre_voce:
    aurelium "Sou apenas o que sobrou de mim mesmo... Ecos e pedaços de um homem sábio aprisionado nesta tinta."
    return

label dialog_aurelium_group_conhecimento:
    aurelium "As prateleiras sabem de coisas... sussurram em minha mente."
    return

label dialog_aurelium_group_a_verdade:
    aurelium "O segredo oculto... está ardendo na tinta sob o peso da culpa."
    return

# --- TÓPICOS FILHOS: AURELIUM ---

label dialog_aurelium_quem_eh:
    aurelium "Me chamo Aurelium. Fui um humano, um oráculo de Aethra. Minhas profecias eram enigmáticas demais para o conselho."
    aurelium "Me puniram aprisionando minha alma nestas páginas para sempre. Diziam que minhas previsões eram muito vagas e confusas."
    aurelium "Irônico... porque não estavam erradas."
    return

label dialog_aurelium_solitario:
    aurelium "As prateleiras não são quietas. Há ecos aflitos de magos que antes habitavam aqui."
    aurelium "Eles gritam por algo... uma passagem, talvez?"
    return

label dialog_aurelium_sobre_torre:
    aurelium "Um santuário do saber que virou um matadouro de realidades. O conselho mexeu com forças imensuráveis."
    aurelium "O guardião trancou tudo para nos salvar... ou nos condenar. Eu não me lembro dos detalhes."
    return

label dialog_aurelium_escrituras_estante:
    aurelium "Eu consigo ver {color=#ffd700}runas{/color} brilhando intensamente acima daquela grande {color=#ffd700}estante{/color} de pedra."
    aurelium "Elas pulsam com uma energia de selamento antiga. Há algo escondido atrás dela, tenho certeza."
    aurelium "Mas você não vai conseguir vê-las com seus olhos normais. Você precisa de uma poção de {color=#ffd700}visão arcana{/color}."
    aurelium "Estude os tomos de alquimia nas estantes, a receita deve estar por lá."
    $ knows_vision_potion = True
    $ renpy.notify("Você descobriu que precisa de uma poção especial.")
    $ log_event("Aurelium apontou as runas na estante e indicou a poção de visão.")
    return

label dialog_aurelium_sobre_alquimistas:
    aurelium "Alquimia? Eu me lembro vagamente... antigamente a alquimia era praticada em locais como essa torre."
    aurelium "Não me lembro quem exatamente a praticava ou como, mas havia uma {color=#ffd700}Oficina Alquímica{/color} nesta torre."
    aurelium "Fumaça verde, explosões, frascos que mostram o invisível... os alquimistas trabalhavam lá."
    $ knows_oficina = True
    $ renpy.notify("Você ouviu sobre a Oficina Alquímica.")
    $ log_event("Player aprendeu sobre a oficina com Aurelium.")
    return

label dialog_aurelium_interpretacao:
    aurelium "A língua antiga de Aethra... Deixe-me ver..."
    aurelium "Significa algo como: 'A verdade permanece onde o esquecimento apaga'."
    aurelium "É uma sentença. Um juízo. Quem escreveu isso acreditava que a verdade é indestrutível, mesmo quando tudo ao redor é apagado."
    aurelium "Há algo nessa frase que me faz sentir... que a resposta está mais perto do que parece. Mas não consigo precisar o quê."
    return

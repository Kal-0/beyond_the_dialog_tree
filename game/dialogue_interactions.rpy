# ==============================================================
# INTERAÇÕES AMBIENTAIS - SALA DA PORTA
# ==============================================================

label interagir_porta_selada:
    $ examined_porta = True
    menu porta_act:
        "Examinar a Porta e Tentar a Senha":
            "As runas reagem levemente à sua presença."
            jump senha_porta
        "Tentar abrir a porta com força bruta":
            $ brute_force_count += 1
            $ log_event("Player tenta abrir a porta na força.")
            with vpunch
            "Uma pulsação mágica violenta arremessa você para trás!"
            show eldrin normal at left with dissolve
            
            if brute_force_count == 1:
                eldrin "Tolo. Já lhe disse que a força não abre esse selo. Demonstre um mínimo de civilidade."
            elif brute_force_count == 2:
                eldrin "Sua imbecilidade é quase admirável. Pare de golpear a porta antes que o selo te desintegre."
            elif brute_force_count >= 3 and not has_key_oficina:
                eldrin "CHEGA! Para um suposto mago, você tem mãos muito inquietas e uma mente muito vazia."
                eldrin "Tome a velha {color=#ffd700}chave{/color} da {color=#ffd700}Oficina Alquímica{/color}! Vá explodir o {color=#ffd700}caldeirão{/color} lá dentro e pare de esbarrar na minha porta."
                $ has_key_oficina = True
                $ eldrin_trust -= 1
                $ log_event("Player desbloqueou a Oficina através da irritação de Eldrin.")
            else:
                eldrin "..."
                "(Eldrin ignora sua insistência deplorável em chutar uma magia ancestral.)"
                
            hide eldrin normal with dissolve
            jump sala_porta_loop
        "Desistir e recuar":
            jump sala_porta_loop

label interagir_estante_porta:
    "Você observa as prateleiras antigas da recepção. Não há de fato nada além de livros completamente arruinados e poeira secular."
    $ examined_estante_porta = True
    jump sala_porta_loop

# ==============================================================
# RESOLVER SENHA - PORTA SELADA
# ==============================================================

label senha_porta:
    if eldrin_trust <= 0:
        show eldrin normal at left with dissolve
        eldrin "Sugiro não testar a fúria das runas se não sabe o que está fazendo, intruso."
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
        
    elif player_pwd == "veritas":
        "As runas reagem imediatamente e giram com luz intensa!"
        "A energia se dissipa. A porta se abre pesadamente, emitindo uma luz radiante do mundo exterior."
        hide screen in_game_hud
        
        show aurelium_book at center with dissolve
        aurelium "Correto. A verdade foi reconhecida."
        hide aurelium_book with dissolve
        
        show nekrons at right with dissolve
        nekrons "Nem toda resposta é apenas palavra. Às vezes é compreensão."
        hide nekrons with dissolve
        
        show skulla at left with dissolve
        skulla "Uau. Você realmente não explodiu. Estou levemente impressionada."
        hide skulla with dissolve
        
        show eldrin normal at center with dissolve
        eldrin "Você entendeu."
        
        menu fechamento:
            "Você não vem?":
                eldrin "Meu lugar ainda é aqui. Alguém precisa guardar o que restou."
            "O que vai acontecer com esta torre?":
                eldrin "Talvez desmorone. Talvez continue existindo."
            "Obrigado.":
                eldrin "Não agradeça a mim. Agradeça ao que escolheu aprender."
                
        hide eldrin normal with dissolve
                
        "Você caminha em direção à luz. {color=#ffd700}Veritas{/color} não abriu apenas a sua saída..."
        "...Mas desatou um nó que sufocava a história esquecida de Aethra."
        "FIM DE JOGO."
        return

    else:
        "Nada acontece. O selo permanece intocável."
        jump sala_porta_loop

# ==============================================================
# INTERAÇÕES - OFICINA ALQUÍMICA
# ==============================================================

label interagir_caldeirao:
    if not cauldron_water and not cauldron_fire:
        "Um grande caldeirão vazio e gelado. Sem água e sem fogo, não serve para nada."
    elif cauldron_water and not cauldron_fire:
        "O caldeirão está cheio d'água, mas frio."
    elif not cauldron_water and cauldron_fire:
        "As chamas lambem o fundo seco do caldeirão. Vai eventualmente derreter se não por algum líquido."
    else:
        "A água borbulha no caldeirão quente! Pronto para receber a mistura."
        menu:
            "Adicionar ingredientes da mesa?":
                jump fazer_pocao
            "Não fazer nada":
                pass
    jump sala_oficina_loop

label fazer_pocao:
    "Você se aproxima da mesa ao canto da sala e vê que ela transbordando de frascos, insetos, venenos, raízes, folhas raras e outras coisas que você nunca viu antes..."
    "Quais ingredientes você vai usar?"
    python:
        i1 = renpy.input("Primeiro ingrediente:")
        i2 = renpy.input("Segundo ingrediente:")
        i3 = renpy.input("Terceiro ingrediente:")
    
    if check_potion_ingredients(i1, i2, i3):
        "A {color=#ffd700}poção{/color} muda de cor até assumir um brilho azulado, suave como o luar."
        "Você a engole em um gole só. Seus olhos ardem e se enchem de luz!"
        $ has_potion = True
        $ log_event("Player preparou a Poção de Visão Arcana com sucesso.")
        "Você agora tem a {color=#ffd700}Visão Arcana{/color}."
        scene bg oficina_caldeirao_pocao with dissolve
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

label interagir_entulho_obs:
    "Vasculhando sob pedaços de vidro escuro, você encontra um compartimento..."
    "Dentro dele, repousa uma {color=#ffd700}Varinha Antiga{/color}, com a ponta de cristal torta."
    $ has_wand = True
    $ log_event("Player encontrou a Varinha Mágica.")
    "Você obteve a Varinha Arcana! O Botão de Feitiços agora está na interface."
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
        "Livro de Piromancia: Soldados usavam a fala 'Ignis Menor' para aquecer as brasas à noite."
        "Diário de Lendas: Um feiticeiro salvou caravanas da sede clamando 'Aqua Fons'."
        "Fichário Alquímico: Um elixir de Visão pede pó de cristal puro, folha prateada e uma sólida raiz recôndita da escuridão. O resto arruina a poção."
        if has_potion:
            "Imediatamente as páginas parecem desinteressantes, pois seus olhos arcanos revelam um forte brilho violáceo por toda a madeira da estante!"
            "A {color=#ffd700}magia de selamento{/color} cravada nela transparece, implorando pela invocação da palavra '{color=#ffd700}Revelare{/color}'."
            "Talvez você deva usar sua varinha..."
    jump sala_biblioteca_loop

label ler_mural_secreta:
    "Você se aproxima do mural grotesco. A caligrafia daquelas atas finais parece ter sido arranhada na pedra com fúria e desespero."
    "As inscrições na parede têm a cor de sangue seco envelhecido pelo tempo apesar do lugar parecer muito bem conservado, como se você fosse a primeira pessoa a entrar ali em séculos."
    "A frase '{color=#ffd700}Veritas manet quod oblivio delet{/color}' está gravada em destaque no centro do {color=#ffd700}mural{/color}."
    "Ao se aproximar, você consegue ler mais escrituras ao redor da frase principal."
    "'Aethra tentou manipular as linhas do tempo apagando a existência de suas falhas, o que corrompeu os alicerces do reino...'"
    "'Para trancar nossos erros na torre, cunhei o selo inviolável. Somente aquele que aceitar nossa sentença terá o caminho livre.'"
    "'Que o esquecimento jamais vença enquanto houver registros. Lembre-se, viajante de amanhã: {color=#ffd700}Veritas{/color} é tudo que nos resta. A verdade restaura a memória.'"
    $ read_mural = True
    $ log_event("Player leu o Mural Secreto e descobriu que Veritas resolve o dilema.")
    jump sala_secreta_loop

label sair_sala_secreta:
    jump sala_biblioteca

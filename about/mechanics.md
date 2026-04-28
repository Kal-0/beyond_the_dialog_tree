# Mecânicas do Jogo

O jogo é uma visual novel exploratória com estrutura de "Hub" (Mapa Central de Navegação Livre). A progressão não depende de "flags" ocultas de sistema para aprendizado de magias, mas sim do **conhecimento do próprio jogador** (Player Knowledge).

## Sistema de Hub e Exploração
- Após o despertar, o jogador tem liberdade incontestável. Ele transita via menu entre 4 áreas: Porta Selada, Oficina Alquímica, Observatório e Biblioteca.
- Não existem bloqueios artificiais. O jogador pode interagir com o enigma final na Porta Selada a qualquer momento, assim que souber a resposta.

## O Guardião e a Confiança (Eldrin)
- A torre tem um sistema moral atrelado a Eldrin. Opções de diálogo reflexivas e polidas elevam a sua confiança (`eldrin_trust += 1`).
- **Penalidade de Força Bruta**: Tentar forçar fisicamente a Porta Selada é visto como uma ofensa bárbara. Ao fazer isso, a confiança de Eldrin despenca (`eldrin_trust -= 1`). Se for muito baixa, o comportamento dele muda para hostil.

## Feitiços e Interação Manual (Varinha)
- A **Varinha Arcana** é encontrada na sucata do Observatório. Obtê-la libera na Interface o **Botão de Magia**.
- **Mão na Massa**: O jogo NÃO registra os feitiços magicamente na interface do personagem. O jogador deve perambular pela biblioteca, ler pequenas histórias de viajantes passados, **memorizar** as palavras em latim (ex: "Ignis Menor", "Aqua Fons", "Revelare"), e **digitar manualmente** o feitiço num input de texto quando for focar a varinha em algum objeto.

## O Diário Arcano (Log de Conversas)
- Para contornar a volatilidade dos diálogos gerados e das pistas orais, o jogador tem acesso contínuo a um **Botão de Diário (Log)** na interface (HUD).
- **Transcrição**: Diferente do "Histórico" convencional, este Diário armazena o histórico do que o jogador digitou ("Player:") e as respostas exatas dos NPCs ("Eldrin: ..."). Isso é vital para analisar posteriormente em silêncio uma rima de Nekrons ou uma pista dada por Aurelium sem perder a imersão de investigação.

## Alquimia (Caldeirão)
- Como na magia, a poção requer memória. O jogador deve encontrar um livro velho detalhando um elixir de "Pó de Cristal, Folha Prateada e Raiz Escura". 
- Na Oficina Alquímica, a Mesa contém dezenas de falsos-positivos (Cogumelos venenosos, veneno de rato, etc). O jogador deverá escolher ativamente apenas aqueles três.
- A panela só funciona em cadeia: O caldeirão deve receber os feitiços de Água e Fogo do jogador antes de ter os itens jogados em si. 

## Visão Arcana
- Realizar a poção com sucesso e bebê-la altera o visual perceptivo do jogo.
- Elementos antes vazios ganham contexto, como o painel lateral da Biblioteca que revela a palavra "Revelare", sendo o convite para o jogador usar sua destreza e arrastar a prateleira escondida que leva ao clímax da trama.
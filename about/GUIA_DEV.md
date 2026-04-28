# Guia do Desenvolvedor: Dicas, Point & Click e Variáveis

Este documento ajuda a entender a arquitetura do projeto e os melhores atalhos para não perder a sanidade desenvolvendo no Ren'Py.

---

## 💡 Truques de Mestre para Testar o Jogo Rápido
Uma das maiores dores de cabeça é ter que ler a mesma introdução 50 vezes para testar uma porta no final do jogo. O Ren'Py tem ferramentas de desenvolvimento secretas para evitar isso:

### 1. O Milagroso `Shift + R` (Auto-Reload)
Você **NÃO** precisa fechar o jogo para testar uma mudança de código.
Se você estiver jogando e chegou na Biblioteca, e percebeu que um texto está com erro de português ou uma caixa de colisão está torta:
- Sem fechar o jogo, dê *Alt+Tab*, mude o código no VS Code / Bloco de Notas e salve.
- Volte no jogo e aperte **`Shift + R`**.
O Ren'Py recarrega todos os arquivos instantaneamente na exata tela em que você estava. Nada de fechar e dar Launch de novo!

### 2. O Atalho de Pulo Direto (Jump Hack)
Se você quer gastar o fim de semana testando só a Sala da Oficina, vá no arquivo `script.rpy`, logo debaixo da `label start:`, e digite um `jump`:
```renpy
label start:
    jump sala_oficina # <- O jogo ignora tudo e começa AQUI!
    # ... resto do codigo
```
Apenas se lembre de apagar esse "jump" pirata quando for publicar a versão oficial. E **SEMPRE** pule para o nome principal da sala (`sala_oficina`, `sala_porta`, `sala_biblioteca`), nunca pule para a versão `_loop`! O label principal é quem diz para o jogo em qual sala você está para as mágicas funcionarem!

### 3. O Console de Desenvolvedor (`Shift + O`)
Dê Play no jogo. Aperte `Shift + O`. 
Um console estilo "Matrix" desce na tela. Se você quiser ver o que acontece quando confiam no Eldrin, digite no console:
`eldrin_trust = 5`
E dê Enter. Pronto, a variável mudou ao vivo no código sem você ter que jogar e tomar as decisões corretas!

---

## Como Funciona o Clique na Tela (Point and Click)
No Ren'Py, para ter um cenário interativo usamos um conjunto de **Screens** e **Buttons** ao invés de textinhos.

### 1. Criando as Caixas Invisíveis (Screens)
Para a tela da Porta Selada, criamos uma screen que contém os polígonos que recebem cliques:
```renpy
screen click_sala_porta():
    # NPC
    button:
        xpos 80 ypos 300 xsize 300 ysize 600
        background Solid("#ff000055") 
        action Jump("falar_eldrin_porta")
```

### 2. A Matemática: X, Y, W, H
No bloco de código acima passamos as coordenadas reais:
- `xpos`: Quantos pixels a partir da esquerda a caixa inicia.
- `ypos`: Quantos pixels para baixo a caixa inicia.
- `xsize`: A largura total (Width) da área de clique.
- `ysize`: A altura total (Height).

**Dica de Colisão:** O código foi deixado inicialmente com cores como `"#ff000055"` (um vermelho translúcido). Rode o jogo desse jeito! Você vai ver as caixas na tela e pode ficar ajustando os números no código e apertando `Shift + R` para ver a caixa recuar e cobrir o seu personagem magicamente em 1 segundo.
Quando ela estiver posicionada, troque os dois últimos números da cor para 00 (ex: `"#ff000000"`). Isso significa Alfa Zero, ou seja: a caixa continua lá detectável para o rato (mouse), mas ficou invísivel aos olhos humanos!

### 3. Chamando a Animação e o Diálogo (Jumps)
Em vez do NPC ficar pregado como um poste, escondemos o sprite e esperamos o clique (`action Jump("falar_eldrin_porta")`).
Dentro dessa label que foi "saltada":
```renpy
label falar_eldrin_porta:
    show eldrin normal at left with dissolve
    eldrin "Encontrou algo?"
    ...
```
O NPC aparece subitamente por cima do cenário com um clarão suave (`dissolve`), diz sua frase textual, e quando o jogador encerra a conversa... o Ren'Py executa `hide eldrin` e volta a ouvir os cliques invisíveis no mapa!

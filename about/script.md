# Roteiro Completo do Modo Pré-definido (Adaptado com Desbloqueio Geográfico e Árvores Dinâmicas)

Este roteiro preserva os diálogos originais da história de Aethra, integrando um modelo de "Múltiplos Caminhos para Roma" (Gating System).
**A maior mudança mecânica:** As salas do jogo não estão abertas desde o início. O jogador deve investigar o ambiente e dialogar para receber as "Chaves" que destrancam áreas no Menu do Mapa. As falas também são progressivas e contam com uma memória de "Primeiro Encontro" (met_npc).

## Variáveis Iniciais de Controle (Ren'Py)
```renpy
default eldrin_trust = 0
default has_wand = False
default wand_active = False
default has_potion = False
default secret_passage_open = False
default cauldron_water = False
default cauldron_fire = False
default brute_force_count = 0

# (Mais as 8 Variáveis de Exploração e Chaves detalhadas em modo_predefined)
```

---

## 1. Despertar na Torre (Ato 1)
**Label:** `intro_predef`

*(O jogo começa com uma tela escura. Sons de vento, eco distante e um leve ruído mágico aparecem ao fundo. Letras surgem lentamente:)*
**"Há lugares que não foram abandonados. Foram esquecidos."**

A cena abre na **Câmara Principal**. O jogador desperta no chão de pedra fria. A cabeça dói. Há um zumbido arcano no ar. À frente, uma grande porta selada por runas pulsa com luz fraca. Estantes de livros ocupam as paredes laterais.

**Eldrin:** "Finalmente acordou. Você está na Torre de Aethra. E, antes que pergunte, sim… ainda há magia aqui."

**Menu:**
- **"Onde estou?"** -> "Uma torre esquecida. Um lugar onde o que foi apagado ainda insiste em permanecer."
- **"Quem é você?"** -> "Meu nome é Eldrin. Guardião desta torre. Ou o que restou dela."
- **"Quero sair daqui."** -> "Então terá de fazer mais do que desejar isso. A porta não responde à pressa."

**Eldrin:** "Se quer sair, primeiro vai precisar entender este lugar. E, se pretende tocar em qualquer coisa aqui, faça isso com cuidado."

---

### Interface de Navegação Visual (HUD)
- **Botão de MAPA**: Abre o `map_overlay`. O Mapa inicia Apenas com a "Porta Selada". Outras 3 salas exigirão o `has_key_...` fornecido por Eldrin.
- **Botão de DIÁRIO (Log)**: Abre o `chat_log_screen`, uma grande janela com a trilha de pistas.
- **Botão de VARINHA**: Só aparece quando encontrada no Observatório (`has_wand == True`).

---

## 3. Local: Porta Selada
Aqui fica **Eldrin**, as **Estantes de Recepção** e a grande **Porta Selada**.

### A. Interação Ambiental
- **Lendo a Estante Velha:** O jogador deve clicar nos livros podres. Isso gera o insight de que a sala guarda mais conhecimento e libera a opção de diálogo "Só poeira e livros" no Eldrin.
- **Batendo na Porta (Força Bruta):** Uma pulsação mágica arremessa o jogador. Fazer isso libera a opção "Não consigo abrir a porta".
- **A Rota da Fúria (3x Força Bruta):** Bater 3 vezes na porta faz Eldrin surtar. *"CHEGA! Para um suposto mago, você tem mãos muito inquietas. Tome a chave da Oficina! Vá explodir o caldeirão lá dentro e pare de esbarrar na minha porta."* -> **Destranca Oficina.**

### B. Conversar com Eldrin (O Caminho de Roma)
**Saudação Dinâmica:** Se você já o conheceu, ele diz *"O que deseja agora?"*.

**Diálogos e Recompensas:**
- **(DIRETO) "O que devo fazer?"**
  - Se estiver zerado, Eldrin é ríspido e sugere você usar seus olhos.
- **"Você está me testando."**
  - **Eldrin:** "Naturalmente. E você está falhando ou aprendendo, dependendo do próximo passo." `$ eldrin_trust += 1` `(Libera o diálogo abaixo)`
- **(SE PERGUNTOU SOBRE TESTE) "Como faço para ganhar sua confiança?"**
  - **Eldrin:** "Observe. Escute. Não tente arrancar respostas antes de entender as perguntas."
- **(DEST. PELA ESTANTE) "Dizem que esta torre esconde mais do que mostra."**
  - **Eldrin:** "Acertou... Se gosta de encarar estantes podres, fique com a chave da Biblioteca Arcana. Vá perturbar o silêncio deles, não o meu." -> **Destranca Biblioteca**.
- **(DEST. PELA PORTA E CONFIANÇA) "Não consigo abrir a porta."**
  - Se a Confiança for alta (`>= 1`), Eldrin vê seu esforço intelectual e lhe entrega a Chave do Observatório Celeste. -> **Destranca Observatório**.
- **(DEST. POR AURELIUM) "Aurelium mencionou uma oficina alquímica."**
  - **Eldrin:** "O livro velho fala demais... Mas ele tem certa razão. Entendimento exige caldeirões fumegantes." -> **Destranca Oficina**.
- **(DEST. POR SKULLA) "A caveira falou sobre as magias de um Observatório."**
  - **Eldrin:** "Skulla... As ferramentas dela vinham da luz cósmica. Leve a chave do Observatório." -> **Destranca Observatório**.

Outras interações passivas de Eldrin: *"Você está me encarando"* (Se poção visionária), *"Veritas manet..."* (Se descobriu o mural) que sobem a sua Confiança.

---

## 4. Local: Oficina Alquímica
Aqui fica **Skulla** (a caveira) e o **Caldeirão**.

### A. Conversa com Skulla (Dicas de Sobrevivência)
**Saudação:** Skulla te elogia como "Aventureiro de enigmas óbvios" somente de primeira. Depois ela quer saber o que seu corpo frágil deseja.

- **(A DICA DO OBSERVATÓRIO) "Essa sala costumava produzir maravilhas?"**
  - Skulla chora as pitangas do Laboratório Lunar abandonado no andar de cima e avisa que Eldrin tem a chave de acesso. (*Isso libera o Diálogo de obter a chave do Observatório!*).
- **As cobranças de Poção:** Skulla avisa agressivamente que Caldeirões precisam de Ignis (`FOGO`) e Aqua (`ÁGUA`) ou você vai evaporar seus pés.

### B. O Caldeirão (Puzzle)
Fabricar a poção com "cristal", "folha" e "raiz". Falhar apaga a água e o fogo (forçando a rejogar a magia de elementos).

---

## 5. Local: Observatório de Fragmentos
Aqui fica **Nekrons**, a gata, e o puzzle da Varinha.

### A. Conversa com Nekrons (A Luz Inebriante)
**Saudação:** "Acordou tarde demais ou cedo demais..." -> Vira "As sombras contaram que você voltaria..."

- Só Nekrons pode reanimar sua varinha encontrada no lixo do Observatório. Ela usa a fresta do teto (onde as estrelas espiam a torre) para bater a luz celestial no vidro fosco da varinha dizendo *Lumos*!

---

## 6. Local: Biblioteca
Aqui fica **Aurelium** (o grimório) e a **Estante Falsa**.

### A. Conversa com Aurelium (O Literato)
**Saudação:** Exalta aquele que lê com os olhos e não com a fome de saqueador da primeira vez. Depois pede pra você se apressar.

- **(A DICA DA OFICINA) "Onde ficavam os alquimistas?"**
  - Aurelium te alerta sobre a existência dos fundos químicos e pede pra você procurar a chave com o Eldrin chato (*Isso libera um gancho direto com Eldrin para dar a Oficina*).

### B. Revelare (Passagem Secreta)
É nesta sala que bater as magias "Aqua", "Ignis" irrita o livro. Só "Revelare" acionado enquanto as pupilas estiverem embriagadas de Magia (Poção Púrpura) rasga a sala ao meio.

Você adentra as catacumbas de confissões da torre para absorver os dizeres no Mural sobre "Veritas" e limpar seu nome com o selo final.

---

## 7. Clímax: A Solução
Ao chegar à porta de Eldrin e tentar abrir na senha:
- **Aethra** causa dor e rechaço.
- **Veritas** rasga o portão, enche as linhas de tela e evoca todas as assombrações da obra para atestarem o seu feito.
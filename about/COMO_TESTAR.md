# Como Testar - Sistema de Diálogos Agrupados

## 🚀 Executar o Jogo

### Pré-requisitos
- Ren'Py instalado
- Projeto em `c:\Users\caioc\Desktop\CESAR\TCC\beyond_the_dialog_tree`

### Passos para Rodar

**1. Abrir Ren'Py**
```
Executar: renpy-9.x.x (ou versão instalada)
```

**2. Adicionar Projeto**
```
Ren'Py Launcher
├─ Projects (no painel esquerdo)
├─ Add Project...
└─ Selecionar: c:\Users\caioc\Desktop\CESAR\TCC\beyond_the_dialog_tree
```

**3. Verificar Erros de Sintaxe**
```
Ren'Py Launcher
├─ Selecionar projeto
├─ Build
└─ Verify (checa erros Ren'Py)
```

**4. Executar Jogo**
```
Ren'Py Launcher
├─ Selecionar projeto
└─ Launch (ou apertar "Play")
```

---

## 🧪 Teste Unitário - Verificar Rastreamento

### Teste 1: Grupo desaparece após ver TODAS as opções

**Ação:**
1. Converse com **Eldrin**
2. Acesse grupo **"Sobre Você"** (3 opções)
3. Selecione:
   - "Quem é você, de verdade?"
   - "Você está me testando." (precisa de `not asked_if_testing`)
   - "Como faço para ganhar sua confiança?" (precisa de `asked_if_testing`)
4. Volte para menu principal

**Esperado:**
- Grupo "Sobre Você" fica cinza/exaurido OU desaparece
- Outros grupos continuam normais

**Se falhar:**
```
Possível causa: Uma das condições (if statements) não foi satisfeita
Solução: Verificar em dialogues_eldrin.rpy se todas as opções estão acessíveis
```

---

### Teste 2: Grupo reaparece quando nova opção surge

**Ação:**
1. Converse com **Eldrin** e marque todos os tópicos de um grupo como visto
2. Grupo fica exaurido
3. Vá para a **Biblioteca** e leia o **Mural**
4. Volte para **Eldrin**

**Esperado:**
- Grupo **"Sobre a Porta"** deveria ficar claro novamente
- Motivo: Nova opção `"{color=#ffd700}Veritas manet quod oblivio delet.{/color}"` agora é visível (porque `read_mural = True`)

**Se não funcionar:**
```
Verificar: read_mural foi definido como True em ler_mural_secreta?
```

---

### Teste 3: Verificar Contagem de Tópicos

**Ação:**
1. Abra `dialogue_system.rpy`
2. Conte manualmente os tópicos em `ELDRIN_TOPICS`
3. Compare com a tabela abaixo:

**Esperado:**
```
"sobre_voce": 3 tópicos ✓
"sobre_porta": 5 tópicos ✓
"direcionamento": 6 tópicos ✓
"exploracoes": 2 tópicos ✓
"magia": 2 tópicos ✓
TOTAL: 18 tópicos
```

---

## 🎮 Teste Funcional - Interação Completa

### Teste 4: Fluxo Completo do Eldrin

**Sequência:**

```
1. Iniciar jogo
2. Conversar com ELDRIN
   ├─ Selecionar "Sobre Você"
   │  ├─ "Quem é você?" → sai "Alguém que não teve..."
   │  └─ Voltar
   │
   ├─ Selecionar "Sobre a Porta"
   │  ├─ "Por que você guarda?" → sai "Porque o que está lá fora..."
   │  └─ Voltar
   │
   ├─ Selecionar "Direcionamento"
   │  ├─ (opções aparecem conforme progresso do jogo)
   │  └─ Voltar
   │
   ├─ (repetir para outros grupos)
   └─ Encerrar conversa

3. Explorar [SALA_PORTA]
   ├─ Examinar porta selada
   ├─ Examinar estante
   └─ Tentar força bruta (3x, vê Eldrin react)

4. Voltar para ELDRIN
   └─ Verificar se grupos mudaram de estado
```

**Esperado:**
- Cada opção funciona
- Respostas são apropriadas
- Menu retorna corretamente
- Variáveis são setadas (has_key_biblioteca, etc)

---

### Teste 5: Teste Todos os NPCs

**Eldrin:** ✓ Acima

**Skulla (Oficina):**
```
1. Ir para SALA_OFICINA
2. Conversar com SKULLA
   ├─ Grupo "Sobre Você" (3 opções)
   ├─ Grupo "Conhecimento" (3 opções)
   └─ Grupo "Ingredientes" (1 opção)
3. Interagir com caldeirão
```

**Nekrons (Observatório):**
```
1. Ir para SALA_OBSERVATORIO
2. Conversar com NEKRONS
   ├─ Grupo "Sobre Você" (3 opções)
   ├─ Grupo "Conhecimento" (3 opções)
   └─ Grupo "Magia" (2-3 opções)
3. Interagir com entulho
```

**Aurelium (Biblioteca):**
```
1. Ir para SALA_BIBLIOTECA
2. Conversar com AURELIUM
   ├─ Grupo "Sobre Você" (2 opções)
   └─ Grupo "Conhecimento" (5 opções)
3. Interagir com estante
```

---

## 🔍 Teste de Debug

### Ativar Debug no Ren'Py

**Em `script.rpy` (ou arquivo principal):**
```python
# No início do arquivo, adicione:
define config.console = True  # Ativa console de debug
define config.developer = True  # Modo developer
```

### Usar Console de Debug

**Durante jogo:**
```
Pressione: Shift + O (ou Ctrl + Shift + Y, dependendo da versão)

Comandos úteis:
$ eldrin_topics_seen
  → mostra quais tópicos foram vistos

$ mark_eldrin_topic_seen("quem_eh")
  → marca um tópico manualmente

$ is_eldrin_group_exhausted("sobre_voce")
  → verifica se grupo está exaurido

$ should_show_eldrin_group("sobre_voce")
  → verifica se grupo deve aparecer
```

---

## 📋 Checklist de Teste Completo

### Pré-Teste
- [ ] Nenhum erro de sintaxe Ren'Py
- [ ] Arquivos salvos: `.rpy` e `.rpyc` atualizados

### Teste de Grupos
- [ ] Eldrin: 5 grupos aparecem
- [ ] Skulla: 3 grupos aparecem
- [ ] Nekrons: 3 grupos aparecem
- [ ] Aurelium: 2 grupos aparecem

### Teste de Rastreamento
- [ ] Tópicos são marcados após seleção
- [ ] Grupos desaparecem quando exauridos
- [ ] Grupos reaparecem quando nova opção surge

### Teste de Interações
- [ ] Porta selada funciona
- [ ] Caldeirão funciona
- [ ] Estante funciona
- [ ] Mural funciona

### Teste de Fluxo
- [ ] Menu volta após submenu
- [ ] Variáveis globais são setadas corretamente
- [ ] NPC não desaparece quando deveria permanecer
- [ ] Encerrar conversa funciona

### Teste de Edge Cases
- [ ] Voltar para grupo vazio (não deveria acontecer)
- [ ] Tentar acessar tópico com condição não satisfeita (não deveria aparecer)
- [ ] Marca tópico 2x (não deveria quebrar)

---

## 🐛 Debug - Problemas Comuns

### Problema: "Label not found: eldrin_grupo_sobre_voce"

**Causa:** Label foi digitado errado em `dialogues_eldrin.rpy`

**Solução:**
```
1. Verificar em dialogue_eldrin.rpy se label existe exatamente como:
   label eldrin_grupo_sobre_voce:

2. No menu, a referência deve ser:
   jump eldrin_grupo_sobre_voce

3. Cuidado com espaços/tabs antes da label
```

### Problema: Grupo não desaparece mesmo vendo TODAS as opções

**Causa:** Uma das opções tem condição que nunca fica True

**Debug:**
```
1. Em dialogue_system.rpy, verificar todos os "topics" definidos
2. Em dialogues_eldrin.rpy, verificar se TODAS as opções marcam esse tópico
3. Usar console:
   $ eldrin_topics_seen
   → deveria ter TODOS os IDs do grupo
```

### Problema: Menu não volta após submenu

**Causa:** Jump para label errado

**Solução:**
```
No final de cada submenu, deve ter:
    "← Voltar ao menu":
        jump eldrin_talk_loop  ← volta para menu principal
```

### Problema: Opção aparece mesmo com condição False

**Causa:** Condição foi interpretada errado

**Debug:**
```
Adicione temporariamente antes da opção:
# DEBUG: variavel_importante = [valor_real]
"Opção" if variavel_importante:
    ...
```

---

## 📊 Métricas de Sucesso

Após testes, considere bem-sucedida a implementação se:

- ✅ 95%+ de opcionalidades funcionam
- ✅ Nenhum erro de compilação
- ✅ Menus retornam corretamente
- ✅ Rastreamento funciona (tópicos vistos)
- ✅ Grupos aparecem/desaparecem conforme esperado
- ✅ Interações ambientais funcionam

---

## 🎯 Próximas Fases (Após Testes Passarem)

1. **Integração com LLM**
   - [ ] Criar `dialogue_free_mode.rpy`
   - [ ] API de LLM configurada
   - [ ] Input livre do jogador funciona

2. **Modo Híbrido**
   - [ ] Menu de intenções criado
   - [ ] LLM usa contexto + intenção

3. **Dados para Dissertação**
   - [ ] Logging de interações
   - [ ] Métricas de cada modo
   - [ ] Análise comparativa

---

## 📞 Se Encontrar Erro

1. Verifique o arquivo **errors.txt** na raiz do projeto
2. Procure a linha do erro
3. Abra `dialogue_system.rpy`, `dialogues_eldrin.rpy`, etc
4. Compare com exemplo em `QUICK_REFERENCE.md`
5. Se ainda não resolver, me avise!

---

## ✅ Teste Final - Indicador de Sucesso

Quando você conseguir:
1. Conversar com os 4 NPCs
2. Ver todos os grupos aparecerem
3. Ver um grupo ficar exaurido
4. Ver um grupo voltar a aparecer (com nova opção)
5. Resolver a password da porta com "veritas"

**Significa que o sistema está funcionando 100%!** 🎉

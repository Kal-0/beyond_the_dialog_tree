# Sistema de Diálogos Agrupados - Resumo da Implementação

## O que foi feito

Você solicitou reorganizar os diálogos que estavam "poluídos" em um menu gigante. Implementei um **sistema de grupos temáticos** onde:

1. **Diálogos agrupados por contexto** (ex: "Sobre Você", "Sobre a Porta", etc)
2. **Menu principal limpo** - mostra apenas os grupos disponíveis
3. **Rastreamento de tópicos** - sistema sabe quais opções foram vistas
4. **Grupos "exauridos"** - quando TODAS as opções de um grupo são vistas, o grupo fica escuro/desabilitado
5. **Re-ativação dinâmica** - quando uma NOVA opção surge (via condições), o grupo volta a brilhar

## Arquivos Criados/Modificados

```
game/
├── dialogue_system.rpy          [NOVO] Sistema base de rastreamento
├── dialogues_eldrin.rpy         [NOVO] Eldrin com 5 grupos temáticos
├── dialogues_npcs.rpy           [NOVO] Skulla, Nekrons, Aurelium em grupos
├── dialogue_interactions.rpy    [NOVO] Interações ambientais (porta, caldeirão, etc)
├── screens_dialogue.rpy         [NOVO] Screens customizadas para menu agrupado
└── dialogues_predefined.rpy     [MODIFICADO] Removidos diálogos movidos
```

## Estrutura de Grupos

### Eldrin (Porta)
- **Sobre Você** (3 tópicos)
- **Sobre a Porta** (5 tópicos)  
- **Direcionamento** (6 tópicos)
- **Explorações** (2 tópicos)
- **Sobre Magia** (2 tópicos)

### Skulla (Oficina)
- **Sobre Você** (3 tópicos)
- **Conhecimento** (3 tópicos)
- **Ingredientes** (1 tópico)

### Nekrons (Observatório)
- **Sobre Você** (3 tópicos)
- **Conhecimento** (3 tópicos)
- **Magia** (3 tópicos)

### Aurelium (Biblioteca)
- **Sobre Você** (2 tópicos)
- **Conhecimento** (5 tópicos)

## Como Funciona - Exemplo Prático

**Fluxo de Interação:**

```
┌─────────────────────────────────────────┐
│  Menu Principal (eldrin_grupos)         │
├─────────────────────────────────────────┤
│ ✓ Sobre Você                            │
│ ✓ Sobre a Porta                         │
│ ✓ Direcionamento                        │
│ ✓ Explorações                           │
│ ✓ Sobre Magia                           │
└─────────────────────────────────────────┘
                  ↓ (jogador clica em "Sobre Você")
┌─────────────────────────────────────────┐
│ Submenu: Sobre Você                     │
├─────────────────────────────────────────┤
│ ○ Quem é você, de verdade?              │
│ ○ Você está me testando.                │
│ ○ Como faço para ganhar sua confiança?  │
│ ← Voltar ao menu                        │
└─────────────────────────────────────────┘
                  ↓ (seleciona "Quem é você")
        $ mark_eldrin_topic_seen("quem_eh")
                  ↓
  [próxima vez que volta ao menu, verifica:]
  
  is_eldrin_group_exhausted("sobre_voce")?
  - "quem_eh" está visto? SIM
  - "testando" está visto? NÃO → retorna False
  
  [Grupo continua visível e claro]
                  ↓
  [Quando TODAS as 3 opções forem vistas...]
  
  is_eldrin_group_exhausted("sobre_voce")?
  - "quem_eh" está visto? SIM
  - "testando" está visto? SIM
  - "confianca" está visto? SIM → retorna True
  
  [Grupo fica escuro/(exaurido) ou desaparece]
```

## Código Principal

### Rastreamento (dialogue_system.rpy)

```python
# Marking como visto
$ mark_eldrin_topic_seen("quem_eh")

# Verificando se grupo está exaurido (TODAS as opções vistas)
is_eldrin_group_exhausted("sobre_voce")  # True/False

# Verificando se deve mostrar grupo (tem algo novo?)
should_show_eldrin_group("sobre_voce")   # True/False
```

### Menu Principal (dialogues_eldrin.rpy)

```renpy
label eldrin_talk_loop:
    menu eldrin_grupos:
        "Sobre Você" if should_show_eldrin_group("sobre_voce"):
            jump eldrin_grupo_sobre_voce
        # ... outros grupos
```

### Submenu de Grupo (dialogues_eldrin.rpy)

```renpy
label eldrin_grupo_sobre_voce:
    menu eldrin_sobre_voce:
        "Quem é você, de verdade?":
            $ mark_eldrin_topic_seen("quem_eh")
            eldrin "Resposta..."
            jump eldrin_talk_loop
        # ... outras opções
```

## Próximos Passos Recomendados

### Fase 1: Testes
- [ ] Testar se grupos aparecem/desaparecem corretamente
- [ ] Verificar visual "exaurido" (se não gostar, customizar screens)
- [ ] Validar que nenhuma label foi quebrada

### Fase 2: Integração com LLM (Modo Livre)
- [ ] Criar `dialogue_free_mode.rpy` para input livre do jogador
- [ ] Integrar função `chamar_llm(contexto, input_player)` em `dialogue_system.rpy`
- [ ] Usar modelo de LLM configurado (GPT, Claude, etc)

### Fase 3: Modo Híbrido
- [ ] Criar `dialogue_hybrid_mode.rpy` com menu de intenções
- [ ] Estender `dialogue_system.rpy` com função `gerar_resposta_hibrida(npc, intencao, contexto)`
- [ ] Implementar seletor de intenção (agressivo, amigável, neutro, etc)

### Fase 4: Comparação de Modos
- [ ] Criar sistema de logging que rastreia qual modo foi usado
- [ ] Armazenar respostas para análise posterior
- [ ] Gerar métricas para sua dissertação

## Customizações Possíveis

### Visual de "Exaurido"
Em `screens_dialogue.rpy`, linha 30, você pode:

```renpy
# Opção 1: Deixar cinza/desabilitado
background Frame("gui/button/choice_disabled_background.png", 12, 12)

# Opção 2: Adicionar ícone
text "✓ Sobre Você (explorado)"

# Opção 3: Remover da lista
if not is_eldrin_group_exhausted(group_key):
    # Mostrar grupo
```

### Adicionar Novo Grupo
1. Em `dialogue_system.rpy`, adicionar ao dict `ELDRIN_TOPICS`
2. Em `dialogues_eldrin.rpy`, criar novo `label eldrin_grupo_novogrupo`
3. Pronto!

## Status da Implementação

✅ Sistema de rastreamento criado
✅ Eldrin reorganizado em 5 grupos
✅ Skulla reorganizada em 3 grupos
✅ Nekrons reorganizada em 3 grupos
✅ Aurelium reorganizada em 2 grupos
✅ Interações ambientais organizadas
⏳ Testes com o jogo
⏳ Customização visual conforme preferência
⏳ Integração com LLM (próxima fase)

## Dúvidas ou Ajustes?

A arquitetura está montada de forma **modular e extensível**, então é fácil:
- Adicionar novos NPCs
- Criar novos grupos
- Ajustar visual
- Integrar features novas

Teste o jogo agora! Se encontrar bugs ou quiser melhorias no visual, me avisa.

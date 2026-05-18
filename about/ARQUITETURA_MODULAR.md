# 🏗️ ARQUITETURA MODULAR - Sistema de Diálogos com Progressão Narrativa

## 📋 Visão Geral

A nova arquitetura organiza diálogos em **3 camadas reutilizáveis** entre os 3 modos:

```
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 1: CORE (dialogue_core.rpy)                         │
│  - Variáveis de progresso (ato, localidade, NPCs, ações)    │
│  - Definições de tópicos com requisitos de desbloqueio      │
│  - Sistema de Gates (verifica permissão de tópicos)         │
└─────────────────────────────────────────────────────────────┘
                            ▲
           ┌────────────────┼────────────────┐
           │                │                │
┌──────────▼─────────┐  ┌───▼──────────────┐  ┌──────────────▼─┐
│  CAMADA 2A:        │  │  CAMADA 2B:      │  │ CAMADA 2C:     │
│  SHARED            │  │  SHARED          │  │ SHARED         │
│  (dialogue_shared) │  │  (dialogue_menus)│  │ (dialogue_logs)│
│  - Processamento   │  │  - Menu          │  │ - Analytics    │
│    de tópicos      │  │    dinâmicos     │  │ - Estatísticas │
│  - Progressão      │  │  - Grupos        │  │   para tese    │
│  - Lógica comum    │  │  - Renderização  │  │                │
└────────────────────┘  └──────────────────┘  └────────────────┘
           ▲                    ▲                      ▲
           │        ┌───────────┼───────────┐         │
           └────────┤           │           ├─────────┘
                    │           │           │
    ┌───────────────▼─┐  ┌──────▼────────┐  ┌────────────────┐
    │ CAMADA 3A:      │  │ CAMADA 3B:    │  │ CAMADA 3C:     │
    │ PREDEFINED      │  │ FREE          │  │ HYBRID         │
    │ (modos predef)  │  │ (modos livre) │  │ (modos híbrido)│
    │ - Diálogos      │  │ - Input texto │  │ - Intenções    │
    │   (labels)      │  │ - Integração  │  │ - Contextual   │
    │ - Menus         │  │   LLM         │  │ - Inteligente  │
    │ - Progressão    │  │ - Validade    │  │ - LLM          │
    │   scripted      │  │   respostas   │  │                │
    └────────────────┘  └───────────────┘  └────────────────┘
```

---

## 🎯 Arquivo: dialogue_core.rpy

**Responsabilidade:** Dados compartilhados entre todos os modos

```python
# 1. PROGRESSO NARRATIVO
get_story_act()              # Qual ato: 1, 2, 3, 4
set_story_act(act_num)       # Avança ato
get_current_location()       # Sala atual
set_current_location(loc)    # Muda sala
has_visited_location(loc)    # Foi visitado?
mark_location_visited(loc)   # Marca como visitado

# 2. NPCs
is_first_meeting_with(npc)   # Primeiro encontro?
mark_npc_met(npc)            # Marca como conhecido

# 3. DEFINIÇÕES DE TÓPICOS (com requisitos)
ELDRIN_TOPICS = {
    "quem_eh_intro": {
        "label": "Quem é você?",
        "group": "about_you",
        "npc": "eldrin",
        "act": 1,
        "requires": {
            "min_act": 1,
            "first_meeting": True,
            "has_item": "wand",      # opcional
            "visited": ["bib"],      # opcional
            "action": "read_mural"   # opcional
        }
    }
}

# 4. SISTEMA DE GATES
check_topic_unlocked(topic_id, npc)  # Pode aparecer?
mark_action_done(action)             # Marca ação
```

---

## 🎮 Arquivo: dialogue_shared.rpy

**Responsabilidade:** Lógica reutilizável em qualquer modo

```python
# 1. LISTAR TÓPICOS DESBLOQUEADOS
get_available_topics_for_npc(npc)
# Retorna: [(id, label, group), ...]

get_topics_by_group(npc)
# Retorna: {"about_you": [(id, label), ...], ...}

# 2. PROCESSAR SELEÇÃO
process_topic_selection(npc, topic_id)
# - Marca visto
# - Marca NPC conhecido
# - Incrementa confiança
# - Retorna label do diálogo

# 3. RASTREAMENTO
is_topic_seen(npc, topic_id)
get_topics_seen_count(npc)
get_group_completion_percent(npc, group)

# 4. DISPLAY
should_show_group(npc, group)
get_npc_greeting(npc, first_time)
```

---

## 📋 Arquivo: dialogue_menus.rpy

**Responsabilidade:** Geração dinâmica de menus

```python
generate_npc_menu(npc)
# Retorna estrutura para renderizar menu

screen npc_dialog_menu(npc_name)
# Screen Ren'Py customizada para display
```

---

## 💬 Arquivo: dialogue_predefined_eldrin.rpy

**Responsabilidade:** Diálogos reais do Eldrin (MODO PREDE-DEFINIDO)

```renpy
label dialog_eldrin_quem_eh_intro:
    eldrin "Meu nome é Eldrin..."
    $ log_dialog_interaction("eldrin", "quem_eh_intro", dialog_mode)
    jump eldrin_talk_loop

label dialog_eldrin_onde_estou:
    eldrin "Uma torre esquecida..."
    $ log_dialog_interaction("eldrin", "onde_estou", dialog_mode)
    jump eldrin_talk_loop

# Cada tópico = 1 label
# Nomeação padrão: dialog_{npc}_{topic_id}
```

---

## 🔄 Como Funciona: Fluxo Completo

### ANTES (Sistema Antigo - PROBLEMA)
```
Menu Eldrin:
┌─────────────────────────────────┐
│ ✓ Sobre Você (3)                │ ← Tudo sempre visível
│ ✓ Sobre a Porta (5)             │   29 opções misturadas
│ ✓ Direcionamento (6)            │   Sem lógica narrativa
│ ✓ Explorações (2)               │
│ ✓ Sobre Magia (2)               │
│                                 │
│ [Mas você está no COMEÇO]        │ ← Problema!
│ [Algumas opções NÃO fazem       │   Você não deveria saber
│  sentido narrativo ainda]       │   sobre a cripta no ato 1!
└─────────────────────────────────┘
```

### DEPOIS (Sistema Novo - SOLUÇÃO)

**ATO 1:**
```
Menu Eldrin:
┌──────────────────────────┐
│ Sobre Você (3)           │ ← Apenas perguntas de
│   - Quem é você?         │   introdução aparecem
│   - Testando?            │
│   - Confiança?           │
│                          │
│ Sobre Este Local (2)     │ ← Perguntas sobre a sala
│   - Onde estou?          │
│   - Como sair?           │
└──────────────────────────┘

[Você não pode explorar] ← Não visitou outras salas
[Você não tem varinha]    ← Não encontrou varinha
[Não leu o mural ainda]   ← Não está no ato 3
```

**ATO 2 (Após visitar Biblioteca e Oficina):**
```
Menu Eldrin:
┌──────────────────────────────┐
│ Sobre Você (3)               │ ← Tudo anterior
│   ✓ Quem é você?             │   MAIS:
│   ✓ Testando?                │
│   ✓ Confiança?               │
│                              │
│ Sobre Este Local (5) [66%]   │ ← Novas opções
│   ✓ Onde estou?              │   desbloqueadas
│   ✓ Como sair?               │
│   - Por que a porta?         │   (visitou outras salas)
│   - Você mencionou...        │
│                              │
│ Outros Locais (3)            │ ← NOVO GRUPO
│   - Sobre a Oficina...       │   (pode falar sobre
│   - Sobre o Observatório...  │    lugares que viu)
│   - Sobre a Biblioteca...    │
│                              │
│ Sobre Magia (1)              │ ← Desbloqueado
│   - Encontrei uma varinha    │   (tem varinha)
└──────────────────────────────┘
```

**ATO 3 (Após ler Mural na Cripta):**
```
Menu Eldrin:
┌──────────────────────────────┐
│ Segredos (2) [50%]          │ ← NOVO GRUPO
│   - O que diz o mural?      │   (descobriu cripta)
│   - Veritas manet?          │
│                              │
│ [Todos os anteriores...]    │
└──────────────────────────────┘
```

---

## 📌 Variáveis de Progresso (em dialogue_core.rpy)

```python
story_state = {
    "act": 1,                           # Ato atual (1-4)
    "current_location": "none",         # Sala atual
    "visited_locations": set(),         # Salas visitadas
    "met_npcs": set(),                  # NPCs conhecidos
    "actions_done": set(),              # Ações completadas
    "seen": set(),                      # Tópicos vistos
    "first_dialogs": set(),             # Primeiros diálogos
    "logs": []                          # Para análise
}
```

### Que Afeta Desbloqueio:
```
get_story_act()              # min_act: 1, 2, 3
has_visited_location(loc)    # visited: ["bib", "oficina"]
is_first_meeting_with(npc)   # first_meeting: True
renpy.has_variable("has_wand")  # has_item: "wand"
renpy.has_variable("eldrin_trust") # eldrin_trust_min: 2
"read_mural" in story_state["actions_done"] # action: "read_mural"
```

---

## 🎮 Como Usar em MODO PRÉ-DEFINIDO

### 1. Iniciar Conversa
```renpy
label falar_eldrin_porta:
    if is_npc_first_dialog("eldrin"):
        eldrin "[get_npc_greeting('eldrin', True)]"
        $ mark_npc_first_dialog("eldrin")
    
    $ mark_location_visited("porta")
    jump eldrin_talk_loop
```

### 2. Menu Dinâmico
```renpy
label eldrin_talk_loop:
    $ available = get_available_topics_for_npc("eldrin")
    
    menu eldrin_menu:
        "Voltar":
            jump porta_main_loop
        
        "Sobre Você":
            jump eldrin_group_about_you
        
        "Sobre Este Local" if should_show_group("eldrin", "about_location"):
            jump eldrin_group_about_location
        
        # ... outros grupos
```

### 3. Submenu de Grupo
```renpy
label eldrin_group_about_you:
    $ topics = get_topics_by_group("eldrin")["about_you"]
    
    menu eldrin_about_you:
        "Voltar":
            jump eldrin_talk_loop
        
        "Quem é você?" if not is_topic_seen("eldrin", "quem_eh_intro"):
            $ label_to_jump = process_topic_selection("eldrin", "quem_eh_intro")
            jump expression label_to_jump
```

### 4. Diálogo Realizado
```renpy
label dialog_eldrin_quem_eh_intro:
    eldrin "Meu nome é Eldrin..."
    $ log_dialog_interaction("eldrin", "quem_eh_intro", dialog_mode)
    jump eldrin_talk_loop
```

---

## ♻️ Reutilização Entre Modos

### MODO LIVRE (próximo)
```
Reutiliza:
✓ dialogue_core.rpy      (progresso narrativo)
✓ dialogue_shared.rpy    (lógica de tópicos)
✓ dialogue_menus.rpy     (estrutura de menu)

Implementa novo:
✗ dialogue_free_*.rpy    (integração com LLM)
  - Aceita input texto
  - Faz prompt para LLM
  - Valida coerência
  - Marca tópicos explorados
```

### MODO HÍBRIDO (próximo)
```
Reutiliza:
✓ dialogue_core.rpy      (progresso narrativo)
✓ dialogue_shared.rpy    (lógica de tópicos)
✓ dialogue_menus.rpy     (estrutura de menu)

Implementa novo:
✗ dialogue_hybrid_*.rpy  (intenções + LLM)
  - Menu de intenções
  - Passa contexto para LLM
  - Resposta contextualizada
  - Marca tópicos explorados
```

---

## 🎯 Próximas Ações

### Fase 1: Completar Diálogos Pré-definidos ✓ (Em Progresso)
- [x] dialogue_core.rpy
- [x] dialogue_shared.rpy
- [x] dialogue_menus.rpy
- [x] dialogue_predefined_eldrin.rpy (BASE)
- [ ] dialogue_predefined_skulla.rpy
- [ ] dialogue_predefined_nekrons.rpy
- [ ] dialogue_predefined_aurelium.rpy
- [ ] Menus dinâmicos funcionais

### Fase 2: Testar no Ren'Py
- [ ] Compilar sem erros
- [ ] Verificar desbloqueio de tópicos
- [ ] Testar progresso de atos
- [ ] Validar rastreamento

### Fase 3: Implementar Modo Livre
- [ ] dialogue_free_core.rpy
- [ ] Integração LLM
- [ ] Validação de respostas

### Fase 4: Implementar Modo Híbrido
- [ ] dialogue_hybrid_core.rpy
- [ ] Menu de intenções
- [ ] LLM contextualizado

### Fase 5: Análise & Tese
- [ ] Logging de dados
- [ ] Comparação de modos
- [ ] Relatório de estatísticas

---

## 💡 Benefícios da Nova Arquitetura

✅ **Modular:** Cada camada tem uma responsabilidade clara
✅ **Reutilizável:** Os 3 modos compartilham 80% do código
✅ **Narrativo:** Diálogos progridem com a história
✅ **Extensível:** Fácil adicionar novos tópicos
✅ **Testável:** Funções isoladas são fáceis de testar
✅ **Analisável:** Logging integrado desde o início
✅ **Manutenível:** Código organizado e documentado

---

**Status:** Arquitetura completa, aguardando implementação dos diálogos restantes e testes.

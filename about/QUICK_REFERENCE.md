# Quick Reference - Sistema de Diálogos Agrupados

## TL;DR - Rápido

### Ver grupos de um NPC
Abra `dialogue_system.rpy` e procure:
```python
define ELDRIN_TOPICS = { ... }
define SKULLA_TOPICS = { ... }
# etc
```

### Adicionar novo TÓPICO a um grupo existente

**1. Em `dialogue_system.rpy`**
```python
define ELDRIN_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "testando", "confianca", "NOVO_TOPICO"]  # ← AQUI
    },
}
```

**2. Em `dialogues_eldrin.rpy`**
```renpy
label eldrin_grupo_sobre_voce:
    menu eldrin_sobre_voce:
        # ... opções existentes ...
        
        "Sua nova pergunta aqui?" if condicao_especial:  # ← NOVO
            $ mark_eldrin_topic_seen("NOVO_TOPICO")
            eldrin "Resposta para a pergunta..."
            jump eldrin_talk_loop
```

### Adicionar novo GRUPO a um NPC

**1. Em `dialogue_system.rpy`**
```python
define ELDRIN_TOPICS = {
    # ... grupos existentes ...
    "novo_grupo": {                           # ← NOVO
        "label": "Rótulo do Grupo",
        "topics": ["topico1", "topico2"]
    }
}
```

**2. Em `dialogues_eldrin.rpy`**

Menu principal:
```renpy
label eldrin_talk_loop:
    menu eldrin_grupos:
        # ... grupos existentes ...
        "Rótulo do Grupo" if should_show_eldrin_group("novo_grupo"):  # ← NOVO
            jump eldrin_grupo_novo_grupo
```

Submenu:
```renpy
label eldrin_grupo_novo_grupo:              # ← NOVO
    menu eldrin_novo_grupo:
        "Primeira pergunta":
            $ mark_eldrin_topic_seen("topico1")
            eldrin "Resposta 1..."
            jump eldrin_talk_loop
            
        "Segunda pergunta":
            $ mark_eldrin_topic_seen("topico2")
            eldrin "Resposta 2..."
            jump eldrin_talk_loop
        
        "← Voltar ao menu":
            jump eldrin_talk_loop
```

### Functions Úteis

```python
# Marca tópico como visto
$ mark_eldrin_topic_seen("topico_id")

# Verifica se TODOS os tópicos de um grupo foram vistos
is_eldrin_group_exhausted("grupo_key")  # → True/False

# Verifica se grupo deve ser mostrado (tem algo novo?)
should_show_eldrin_group("grupo_key")   # → True/False

# Retorna label com "(exaurido)" se aplicável
get_eldrin_group_label("grupo_key")     # → "Sobre Você" ou "Sobre Você (exaurido)"
```

### Aplicar para outro NPC

Trocar `eldrin` por: `skulla`, `nekrons`, `aurelium`

Exemplo para Skulla:
```python
$ mark_skulla_topic_seen("topico_id")
is_skulla_group_exhausted("grupo_key")
should_show_skulla_group("grupo_key")
```

## Estrutura de Arquivos

```
game/
│
├── dialogue_system.rpy
│   └─ Defines de TÓPICOS por NPC
│   └─ Functions de rastreamento
│
├── dialogues_eldrin.rpy
│   └─ Label: falar_eldrin_porta (inicio)
│   └─ Label: eldrin_talk_loop (menu principal)
│   └─ Labels: eldrin_grupo_* (submenus)
│
├── dialogues_npcs.rpy
│   └─ Skulla, Nekrons, Aurelium (estrutura similar)
│
├── dialogue_interactions.rpy
│   └─ Interações: porta, caldeirão, estante, mural
│
├── screens_dialogue.rpy
│   └─ Screens customizadas para visual
│
└── dialogues_predefined.rpy
    └─ VAZIO (diálogos foram movidos)
```

## Fluxo de Execução

```
jogo.rpy (ou script.rpy)
    ↓
    chama: label falar_eldrin_porta
    ↓
    show Eldrin
    ↓
    jump eldrin_talk_loop
    ↓
    menu eldrin_grupos (mostra grupos disponíveis)
    ├─ Sobre Você (if should_show_eldrin_group("sobre_voce"))
    ├─ Sobre a Porta (if should_show_eldrin_group("sobre_porta"))
    └─ ... etc
    ↓
    jogador seleciona um grupo
    ↓
    jump eldrin_grupo_*
    ↓
    menu submenu (mostra tópicos do grupo)
    ├─ "Pergunta 1"
    ├─ "Pergunta 2"
    └─ "← Voltar ao menu"
    ↓
    jogador seleciona uma pergunta
    ↓
    $ mark_eldrin_topic_seen("topico_id")  ← Rastreia!
    eldrin "Resposta..."
    ↓
    jump eldrin_talk_loop ← Volta ao menu principal
    ↓
    sistema verifica: should_show_eldrin_group("sobre_voce")?
    └─ Se TRUE → grupo continua visível
    └─ Se FALSE → grupo não aparece (exaurido)
```

## Sintaxe Ren'Py - Dicas

### Condicional no menu
```renpy
menu:
    "Opção 1" if variavel == True:
        # executar
    "Opção 2" if not variavel_booleana:
        # executar
    "Opção 3":  # sem condição, sempre aparece
        # executar
```

### Variáveis customizadas
```python
$ minha_variavel = True
$ meu_dict = {"chave": "valor"}
$ minha_lista = [1, 2, 3]
```

### Return vs Jump
```renpy
jump label_name          # Vai para label, não volta
return                   # Volta para onde chamou (se foi via call)
```

## Checklist - Antes de Publicar

- [ ] Todos os tópicos têm um ID único em `dialogue_system.rpy`
- [ ] Todos os IDs aparecem em um `mark_*_topic_seen()` em `dialogues_*.rpy`
- [ ] Nenhum grupo vazio (tem pelo menos 1 tópico?)
- [ ] Labels nos nomes de grupos (ex: `"Sobre Você"` no label, `sobre_voce` na key)
- [ ] Todos os submenus têm "← Voltar ao menu" como opção final
- [ ] Jump correto após cada diálogo (volta para `*_talk_loop`)

## Debug - Problema Comum

**Problema: Grupo não desaparece mesmo depois de ver TODAS as opções**

Solução:
```python
# Verificar em dialogue_system.rpy se TODOS os tópicos estão definidos
define ELDRIN_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "testando", "confianca"]  # ← tem 3
    }
}

# Verificar se TODOS os 3 são marcados em dialogues_eldrin.rpy
$ mark_eldrin_topic_seen("quem_eh")       # ✓
$ mark_eldrin_topic_seen("testando")      # ✓
$ mark_eldrin_topic_seen("confianca")     # ✓
```

**Problema: Opção não aparece no submenu**

Solução:
```python
# Verificar se a CONDICÃO é True
"Opção aqui?" if variavel_importante:     # ← variavel_importante é True?
    
# Ou:
"Opção aqui?":                             # Sem condição, sempre aparece
```

## Próximas Features

- [ ] Integrar com LLM para Modo Livre
- [ ] Sistema de intenções para Modo Híbrido
- [ ] Logging de respostas para análise
- [ ] Metricas de comparação de modos

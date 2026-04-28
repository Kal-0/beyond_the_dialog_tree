# Sistema de Diálogos Agrupados - Documentação

## Visão Geral

O novo sistema de diálogos reorganiza as conversas por **grupos temáticos**, tornando o menu principal menos poluído e mais intuitivo.

## Arquitetura

### Arquivos Criados/Modificados:

1. **`dialogue_system.rpy`** - Sistema base
   - Define grupos temáticos (dicts)
   - Funções de rastreamento de tópicos vistos
   - Lógica para determinar se grupo está "exaurido"

2. **`dialogues_eldrin.rpy`** - Diálogos do Eldrin
   - Menu principal com 5 grupos temáticos
   - Labels separados para cada grupo
   - Cada tópico marca seu ID como "visto"

3. **`screens_dialogue.rpy`** - Screens customizadas
   - `grouped_dialogue_menu` - Menu com states de grupos
   - `dialogue_choice_group` - Submenu para dentro de grupos

4. **`dialogue_interactions.rpy`** - Interações ambientais
   - Lógica da porta selada e password
   - Interações com estante

5. **`dialogues_predefined.rpy`** - Mantém outros NPCs (Skulla, Nekrons, Aurelium)

## Estrutura de Grupos (Eldrin)

```
├── Sobre Você (quem_eh, testando, confianca)
├── Sobre a Porta (por_que_guarda, selada, magia_antiga, veritas, mural)
├── Direcionamento (o_que_fazer, direcionamento, aonde_ir, procura_oficina, procura_observatorio, perdido)
├── Explorações (estante, torre_esconde)
└── Sobre Magia (magia_funciona, encarando)
```

## Como Funciona

### Rastreamento de Tópicos

```python
# Ao selecionar uma opção, marca como visto:
$ mark_eldrin_topic_seen("quem_eh")
```

### Verificar se Grupo Está Exaurido

```python
# Retorna True se TODOS os tópicos do grupo foram vistos:
is_eldrin_group_exhausted("sobre_voce")
```

### Mostrar/Ocultar Grupos

```python
# No menu, grupos só aparecem se tiverem pelo menos UM tópico não visto:
"Sobre Você" if should_show_eldrin_group("sobre_voce"):
```

## Fluxo de Interação

```
Menu Principal (eldrin_grupos)
    ↓
Jogador seleciona "Sobre Você"
    ↓
Submenu (eldrin_grupo_sobre_voce)
    ├─ "Quem é você, de verdade?" → marca "quem_eh" como visto
    ├─ "Você está me testando?" → marca "testando" como visto
    └─ "Como faço para ganhar sua confiança?" → marca "confianca" como visto
    ↓
Jogador seleciona "← Voltar ao menu"
    ↓
Volta para Menu Principal
    ↓
Sistema verifica: is_eldrin_group_exhausted("sobre_voce")
    ↓
Se True → grupo não aparece mais (ou aparece com "(exaurido)")
```

## Próximos Passos

### 1. Aplicar Sistema para Outros NPCs
Modificar `dialogues_predefined.rpy` para adicionar estruturas similares:
- Skulla (Oficina Alquímica)
- Nekrons (Observatório)
- Aurelium (Biblioteca)

### 2. Customizar Visual de "Exaurido"
No Ren'Py, opções desabilitadas podem mostrar:
- Texto em cinza
- Ícone de "✓" ou "(exaurido)"
- Remover da lista completamente

### 3. Integração com LLM (Modo Livre/Híbrido)
Expandir `dialogue_system.rpy` com:
```python
def gerar_resposta_llm(npc_nome, input_player, contexto):
    # Chamar API da LLM
    # Retornar resposta
    pass
```

## Modificações Necessárias no `script.rpy`

Se houver um `script.rpy` principal que carrega os outros arquivos, adicionar:

```renpy
# No início do script.rpy, adicionar:
init python:
    # Import dos arquivos de diálogo (se necessário)
    pass

# Ou simplesmente deixar Ren'Py carregá-los automaticamente
# (ele processa todos os .rpy na pasta /game)
```

## Exemplo: Adicionar Novo Tópico

Se quisermos adicionar um novo tópico ao grupo "Sobre Você":

1. **Em `dialogue_system.rpy`**, modificar dict:
```python
define ELDRIN_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "testando", "confianca", "NOVO_TOPICO"]  # ← Adicionar aqui
    },
    # ... resto
}
```

2. **Em `dialogues_eldrin.rpy`**, adicionar no submenu:
```renpy
label eldrin_grupo_sobre_voce:
    menu eldrin_sobre_voce:
        # ... opções existentes ...
        
        "Novo Tópico de Conversa" if condicao_especial:
            $ mark_eldrin_topic_seen("NOVO_TOPICO")
            eldrin "Resposta para novo tópico..."
            jump eldrin_talk_loop
```

## Status Atual

✅ Sistema base criado
✅ Diálogos de Eldrin reorganizados em grupos
✅ Rastreamento de tópicos implementado
⏳ Testar compilação Ren'Py
⏳ Customizar visual de "exaurido"
⏳ Aplicar para outros NPCs
⏳ Integração com LLM

## Testes Recomendados

1. Conversar com Eldrin e selecionar todas as opções de um grupo
2. Verificar se grupo desaparece do menu principal
3. Explorar a sala para desbloquear novas opções (ex: "A torre esconde mais do que mostra")
4. Verificar se grupo "reaparece" quando nova opção surge

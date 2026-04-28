# 🎮 CHEAT SHEET - Sistema de Diálogos Agrupados

## ⚡ TL;DR - Muito Resumido

```
PROBLEMA: Menu gigante com 29 opções misturadas
          ❌ Desorganizado, confuso, sem rastreamento

SOLUÇÃO:  5 grupos temáticos com rastreamento automático
          ✅ Organizado, limpo, dinamicamente atualizado

COMO?:    Arquivos novos que organizam tópicos por tema
          e rastreiam quais foram vistos
```

---

## 🗂️ Arquivos Criados

```
dialogue_system.rpy
  └─ Defines de tópicos por NPC
  └─ Functions de rastreamento

dialogues_eldrin.rpy
  └─ Eldrin: 5 grupos, 18 tópicos

dialogues_npcs.rpy  
  └─ Skulla, Nekrons, Aurelium

dialogue_interactions.rpy
  └─ Porta, caldeirão, estante, mural

screens_dialogue.rpy
  └─ Visual customizado
```

---

## 🔄 Como Funciona em 3 Passos

### PASSO 1: Selecionar Grupo
```
Menu Eldrin:
✓ Sobre Você
✓ Sobre a Porta
✓ Direcionamento
✓ Explorações
✓ Sobre Magia
```

### PASSO 2: Ver Opções do Grupo
```
Menu Sobre Você:
- "Quem é você?"
- "Você está me testando?"
- "Como ganho sua confiança?"
← Voltar
```

### PASSO 3: Grupo Desaparece (Exaurido)
```
Após ver TODAS as 3 opções:
(i) Sobre Você        ← CINZA/EXAURIDO
✓ Sobre a Porta
✓ Direcionamento
...
```

---

## 💻 Código Principal (3 Functions)

```python
# Marca como visto
$ mark_eldrin_topic_seen("quem_eh")

# Verifica se TODAS vistas (exaurido)
is_eldrin_group_exhausted("sobre_voce")  # True/False

# Verifica se deve mostrar (tem algo novo?)
should_show_eldrin_group("sobre_voce")   # True/False
```

---

## ➕ Adicionar Nova Opção (2 Minutos)

### Passo 1: Em `dialogue_system.rpy`
```python
define ELDRIN_TOPICS = {
    "sobre_voce": {
        "topics": ["quem_eh", "testando", "confianca", "NOVO"]  # ← AQUI
    }
}
```

### Passo 2: Em `dialogues_eldrin.rpy`
```renpy
label eldrin_grupo_sobre_voce:
    menu eldrin_sobre_voce:
        "Sua pergunta aqui?" if condicao:
            $ mark_eldrin_topic_seen("NOVO")
            eldrin "Resposta..."
            jump eldrin_talk_loop
```

**Pronto!** ✅

---

## 🧪 Testes Rápidos

### Teste 1: Grupo fica cinza?
```
1. Fale com Eldrin
2. Veja "Sobre Você" (3 opções)
3. Selecione todas as 3
4. Volte: deveria estar CINZA
```

### Teste 2: Grupo volta a brilhar?
```
1. Leia mural na biblioteca
2. Volte para Eldrin
3. "Sobre Porta" deveria estar CLARO (nova opção!)
```

---

## 🐛 Troubleshooting (3 Problemas Comuns)

| Problema | Causa | Solução |
|----------|-------|---------|
| Grupo não desaparece | Condição não satisfeita | Verificar `if` statements |
| Opção não aparece | Label com erro | Procure em dialogue_system.rpy |
| Menu não volta | Jump errado | Deve ser `jump eldrin_talk_loop` |

---

## 📊 Números

| Métrica | Valor |
|---------|-------|
| NPCs organizados | 4 (Eldrin, Skulla, Nekrons, Aurelium) |
| Grupos totais | 13 |
| Tópicos totais | 40 |
| Linhas de documentação | 1500+ |
| Arquivos criados | 6 |
| Documentos criados | 7 |

---

## 🎯 Próximos Passos

1. **Agora:** Teste o jogo (COMO_TESTAR.md)
2. **Depois:** Integre com LLM
3. **Depois:** Compare modo pré-definido vs livre vs híbrido
4. **Depois:** Use dados para sua dissertação

---

## 📚 Documentação Rápida

| Preciso de... | Arquivo |
|---|---|
| Overview visual | ANTES_DEPOIS.md |
| Ver todos os tópicos | MAPA_VISUAL_TOPICOS.md |
| Entender técnica | SISTEMA_DIALOGOS.md |
| Copiar/colar código | QUICK_REFERENCE.md |
| Testar | COMO_TESTAR.md |
| Índice completo | INDICE_DOCUMENTACAO.md |

---

## ✨ Vantagens

| Aspecto | Benefício |
|--------|----------|
| **Organização** | Grupos temáticos, sem poluição |
| **Rastreamento** | Sabe automaticamente o progresso |
| **Dinâmico** | Grupos aparecem/desaparecem sozinhos |
| **Extensível** | Fácil adicionar novos conteúdos |
| **Modular** | Pronto para integração com LLM |
| **Documentado** | 1500+ linhas de documentação |

---

## 🚀 Status

```
✅ Sistema implementado
✅ Documentação completa
⏳ Teste no Ren'Py (próximo)
⏳ Integração com LLM
⏳ Análise para dissertação
```

---

## 🎓 Conclusão

```
Antes:  Menu gigante, sem organização, sem rastreamento
Depois: 5 grupos organizados, rastreamento automático, pronto para LLM

Tempo de implementação: ~2 horas
Tempo de documentação: ~1 hora
Sua próxima ação: Testar no Ren'Py!
```

---

## 💡 One-Liner

```
Sistema de diálogos modular com rastreamento automático 
de progresso e grupos dinâmicos - pronto para LLM.
```

---

## 🔗 Links Rápidos

- **Comece aqui:** [ANTES_DEPOIS.md](ANTES_DEPOIS.md)
- **Teste aqui:** [COMO_TESTAR.md](COMO_TESTAR.md)
- **Modifique assim:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Aprenda aqui:** [SISTEMA_DIALOGOS.md](SISTEMA_DIALOGOS.md)

---

**Tempo até o jogo estar testado: ~15-20 minutos ⏱️**

**Tempo até LLM estar integrada: ~1-2 horas 🚀**

Vamos lá! 🎉

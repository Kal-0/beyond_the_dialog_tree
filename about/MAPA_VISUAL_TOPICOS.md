# Mapa Visual - Grupos e Tópicos por NPC

## 📊 ELDRIN (Sala da Porta)

```
ELDRIN_TALK_LOOP (Menu Principal)
│
├─ Sobre Você
│  ├─ [quem_eh] "Quem é você, de verdade?"
│  ├─ [testando] "Você está me testando." (if not asked_if_testing)
│  └─ [confianca] "Como faço para ganhar sua confiança?" (if asked_if_testing)
│
├─ Sobre a Porta
│  ├─ [por_que_guarda] "Por que você guarda esta porta?"
│  ├─ [selada] "A porta está selada por magia antiga, não é?" (if examined_porta)
│  ├─ [magia_antiga] "Não consigo abrir a porta..." (if examined_porta and not has_key_observatorio)
│  ├─ [veritas] "{color=#ffd700}Veritas manet quod oblivio delet.{/color}" (if read_mural)
│  └─ [mural] "A torre esconde mais do que mostra." (if examined_estante_porta and not has_key_biblioteca)
│
├─ Direcionamento
│  ├─ [o_que_fazer] "O que devo fazer?" (if eldrin_trust <= 0 and ...)
│  ├─ [direcionamento] "Pode me dar algum direcionamento?" (if eldrin_trust > 0 and ...)
│  ├─ [aonde_ir] "Aonde devo ir agora?" (if has_key_biblioteca and not has_key_oficina)
│  ├─ [procura_oficina] "O que eu procuro na Oficina?" (if has_key_oficina and not has_key_observatorio)
│  ├─ [procura_observatorio] "A caveira falou sobre as magias..." (if knows_observatorio and ...)
│  └─ [perdido] "Me sinto perdido..." (if has_key_observatorio)
│
├─ Explorações
│  ├─ [estante] "Aqui só tem poeira e livros." (if examined_estante_porta)
│  └─ [torre_esconde] "O Grimório mencionou uma oficina..." (if knows_oficina and ...)
│
├─ Sobre Magia
│  ├─ [magia_funciona] "Como a magia funciona aqui?" (if has_wand)
│  └─ [encarando] "Você está me encarando." (if has_potion)
│
└─ Encerrar conversa
```

**Total: 5 grupos, 18 tópicos**

---

## 💀 SKULLA (Oficina Alquímica)

```
SKULLA_TALK_LOOP (Menu Principal)
│
├─ Sobre Você
│  ├─ [quem_eh] "Quem é você?"
│  ├─ [como_perdeu] "Como você perdeu seu corpo?"
│  └─ [precisava_ajuda] "Preciso de ajuda."
│
├─ Conhecimento
│  ├─ [sabe_util] "Você sabe algo útil?"
│  ├─ [producoes] "Essa sala costumava produzir que tipos de maravilhas?"
│  └─ [pocao] "Eu bebi a mistura e não explodi." (if has_potion)
│
├─ Ingredientes
│  └─ [agua_fria] "A água está fria." (if cauldron_water and not cauldron_fire)
│
└─ Encerrar conversa
```

**Total: 3 grupos, 7 tópicos**

---

## 🐱 NEKRONS (Observatório)

```
NEKRONS_TALK_LOOP (Menu Principal)
│
├─ Sobre Você
│  ├─ [quem_eh] "Quem é você?"
│  ├─ [nao_gato] "Você não é apenas um gato, é?"
│  └─ [como_sair] "Você sabe como sair?"
│
├─ Conhecimento
│  ├─ [o_que_lugar] "O que é este lugar?"
│  ├─ [conhece_eldrin] "Você conhece Eldrin?"
│  └─ [o_que_fazer] "O que posso fazer aqui?" (if not has_wand)
│
├─ Magia
│  ├─ [varinha] "A varinha que encontrei parece morta." (if has_wand and not wand_active)
│  └─ [tremor] "Você sentiu esse tremor?" (if secret_passage_open)
│
└─ Encerrar conversa
```

**Total: 3 grupos, 8 tópicos**

---

## 📖 AURELIUM (Biblioteca)

```
AURELIUM_TALK_LOOP (Menu Principal)
│
├─ Sobre Você
│  ├─ [quem_eh] "Quem é você?"
│  └─ [solitario] "É solitário ser um livro?"
│
├─ Conhecimento
│  ├─ [sobre_torre] "O que sabe sobre esta torre?"
│  ├─ [senha_porta] "A senha da porta está nas suas páginas?"
│  ├─ [sobre_alquimistas] "Onde ficavam os alquimistas?" (if not knows_oficina and ...)
│  ├─ [magia_selamento] "O que pode me dizer sobre essa sala?" (if not has_potion)
│  └─ [interpretacao] "O que significa a frase do mural?" (if read_mural)
│
└─ Encerrar conversa
```

**Total: 2 grupos, 7 tópicos**

---

## 📊 Estatísticas Gerais

| NPC | Grupos | Tópicos | Opções/Grupo | Condicionals |
|-----|--------|---------|--------------|--------------|
| **Eldrin** | 5 | 18 | 3-6 | 10 |
| **Skulla** | 3 | 7 | 2-3 | 3 |
| **Nekrons** | 3 | 8 | 2-3 | 3 |
| **Aurelium** | 2 | 7 | 2-5 | 3 |
| **TOTAL** | **13** | **40** | - | **19** |

---

## 🔄 Interações Ambientais

```
INTERAÇÕES (Não-NPC)
│
├─ Porta Selada
│  ├─ interagir_porta_selada
│  └─ senha_porta
│
├─ Estante (Porta)
│  └─ interagir_estante_porta
│
├─ Caldeirão (Oficina)
│  ├─ interagir_caldeirao
│  └─ fazer_pocao
│
├─ Entulho (Observatório)
│  └─ interagir_entulho_obs
│
├─ Estante (Biblioteca)
│  └─ interagir_estante_bib
│
└─ Mural (Sala Secreta)
   └─ ler_mural_secreta
```

---

## 🎯 Mapa Mental - Fluxo Completo

```
JOGO INICIA
    ↓
    Jogador vai para [SALA_PORTA]
    ↓
    Interage com [ELDRIN]
        ↓
        label falar_eldrin_porta
            ↓
            label eldrin_talk_loop (MENU PRINCIPAL)
                ├─ Sobre Você ─→ label eldrin_grupo_sobre_voce
                ├─ Sobre a Porta ─→ label eldrin_grupo_sobre_porta
                ├─ Direcionamento ─→ label eldrin_grupo_direcionamento
                ├─ Explorações ─→ label eldrin_grupo_exploracoes
                └─ Sobre Magia ─→ label eldrin_grupo_magia
                    ↓ (após submenu)
                    volta para eldrin_talk_loop
    
    Jogador vai para [SALA_OFICINA]
    ↓
    Interage com [SKULLA]
        ↓ (estrutura similar ao Eldrin)
    
    Jogador vai para [SALA_OBSERVATORIO]
    ↓
    Interage com [NEKRONS]
        ↓ (estrutura similar)
    
    Jogador vai para [SALA_BIBLIOTECA]
    ↓
    Interage com [AURELIUM]
        ↓ (estrutura similar)
    
    Jogador tenta abrir [PORTA_SELADA]
    ↓
    Digita senha
        ├─ "aethra" → Eldrin reage
        ├─ "veritas" → FIM DO JOGO
        └─ outra coisa → Nada acontece
```

---

## 📋 Exemplo: Adicionar Novo Tópico

### Cenário: Adicionar "O que você vai fazer após a porta abrir?" a Eldrin

**Passo 1:** Em `dialogue_system.rpy`
```python
define ELDRIN_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "testando", "confianca", "futuro"]  # ← NOVO
    },
    # ...
}
```

**Passo 2:** Em `dialogues_eldrin.rpy`
```renpy
label eldrin_grupo_sobre_voce:
    menu eldrin_sobre_voce:
        # ... opções existentes ...
        
        "O que você vai fazer após a porta abrir?" if has_potion:
            $ mark_eldrin_topic_seen("futuro")
            eldrin "Talvez finalmente eu também possa sair daqui..."
            jump eldrin_talk_loop
```

**Resultado:**
- Novo tópico aparece no submenu "Sobre Você"
- Rastreado automaticamente
- Grupo "Sobre Você" continua visível até que TODAS as 4 opções sejam vistas

---

## ✅ Validação - Checklist de Completude

- [x] Todos os tópicos têm IDs únicos por NPC
- [x] Cada tópico é marcado como visto em exatamente 1 lugar
- [x] Nenhum grupo vazio
- [x] Labels de grupos correspondem aos defines
- [x] Todos os submenus têm "← Voltar ao menu"
- [x] Condicionais são válidas (variáveis existem)
- [x] Documentação visual completa

---

## 🔗 Arquivos Relacionados

- `dialogue_system.rpy` - Defines e functions
- `dialogues_eldrin.rpy` - Eldrin + labels
- `dialogues_npcs.rpy` - Skulla, Nekrons, Aurelium
- `dialogue_interactions.rpy` - Interações ambientais
- `screens_dialogue.rpy` - Screens customizadas
- `SISTEMA_DIALOGOS.md` - Documentação técnica
- `QUICK_REFERENCE.md` - Referência rápida

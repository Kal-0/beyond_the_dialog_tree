# ==============================================================
# CAMADA 1: CORE DE DIÁLOGOS E ESTADO DE PROGRESSÃO
# ==============================================================

init python:
    # ----------------------------------------------------------
    # ESTADO GLOBAL DO JOGO E PROGRESSÃO NARRATIVA
    # ----------------------------------------------------------
    
    if not hasattr(store, 'seen_choices_set'):
        store.seen_choices_set = set() # Backward compatibility

    SECRET_PHRASE = "Veritas manet quod oblivio delet"

    # Dicionário de estado narrativo global
    story_state = {
        "act": 1,                           # Ato atual (1 a 4)
        "current_location": "none",         # Sala atual
        "visited_locations": set(),         # Salas visitadas
        "met_npcs": set(),                  # NPCs conhecidos
        "actions_done": set(),              # Ações concluídas (ex: "read_mural")
        "seen_topics": set(),               # Tópicos de diálogo já visualizados
        "dialog_logs": [],                  # Registro de analytics/histórico
        "knows_vision_potion": False,       # O player aprendeu sobre a poção
        "knows_secret": False,              # O player encontrou a sala secreta
        "final_choice_made": False,         # O player tomou a decisão final
        "eldrin_revealed_password": False   # Eldrin revelou a senha veritas ao player
    }

    def get_story_act():
        return story_state["act"]

    def mark_location_visited(loc):
        story_state["visited_locations"].add(loc)

    def has_visited_location(loc):
        return loc in story_state["visited_locations"]

    def mark_action_done(action):
        story_state["actions_done"].add(action)

    def is_action_done(action):
        return action in story_state["actions_done"]

    def is_first_meeting_with(npc):
        return npc not in story_state["met_npcs"]

    def mark_npc_met(npc):
        story_state["met_npcs"].add(npc)

    def mark_topic_seen(npc, topic_id):
        story_state["seen_topics"].add(f"{npc}_{topic_id}")
        store.seen_choices_set.add(f"{npc}_{topic_id}")

    def is_topic_seen(npc, topic_id):
        return f"{npc}_{topic_id}" in story_state["seen_topics"] or f"{npc}_{topic_id}" in store.seen_choices_set

    # ----------------------------------------------------------
    # DICIONÁRIOS DE TÓPICOS (COM REQUISITOS DE DESBLOQUEIO)
    # ----------------------------------------------------------
    # Fluxo de desbloqueio circular:
    #   Aurelium menciona alquimia → Oficina (Skulla)
    #   Skulla menciona observatório → Observatório (Nekrons)
    #   Nekrons menciona livros/feitiços → Biblioteca (Aurelium)
    #
    # Atalhos pela sala do selo:
    #   Estante livros ilegíveis → Biblioteca (Aurelium)
    #   Forçar porta 3x → Oficina (Skulla)
    #   Porta + trust >= 3 → Observatório (Nekrons)

    NPC_TOPICS = {
        "eldrin": {
            "groups": {
                "sobre_voce": {"label": "Me conte sobre Você", "requires": {}},
                "sobre_porta": {"label": "O que tem atrás dessa Porta?", "requires": {}},
                "direcionamento": {"label": "Preciso de direcionamento", "requires": {}},
                "descobertas": {"label": "Quero conversar sobre algo que descobri", "requires": {}},
                "magia": {"label": "Sobre a magia desse lugar...", "requires": {"var": "has_wand"}},
                "a_verdade": {"label": "Descobri o segredo da Torre...", "requires": {"var": "knows_secret", "not_var": "final_choice_made"}}
            },
            "topics": {
                "quem_eh": {
                    "label": "Quem é você, de verdade?", "group": "sobre_voce", 
                    "requires": {}
                },
                "testando": {
                    "label": "Você está me testando.", "group": "sobre_voce", 
                    "requires": {"not_var": "asked_if_testing"}
                },
                "confianca": {
                    "label": "Por que desconfia tanto de mim?", "group": "sobre_voce", 
                    "requires": {"var": "asked_if_testing", "min_trust": 1}
                },
                "por_que_guarda": {
                    "label": "Por que você guarda esta porta?", "group": "sobre_porta", 
                    "requires": {"min_trust": 3}
                },
                "selada": {
                    "label": "A porta está selada com magia, não é?", "group": "sobre_porta", 
                    "requires": {"var": "examined_porta"}
                },
                "magia_antiga": {
                    "label": "Não consigo abrir a porta, não faço ideia de qual é senha.", "group": "sobre_porta", 
                    "requires": {"var": "knows_porta_needs_password", "not_var": "has_key_observatorio"}
                },
                "o_que_fazer": {
                    "label": "O que devo fazer?", "group": "direcionamento", 
                    "requires": {"min_trust": 1, "not_var": "has_key_biblioteca"}
                },
                "direcionamento": {
                    "label": "Os livros aqui estão todos destruídos, ilegíveis...", "group": "direcionamento", 
                    "requires": {"var": "examined_estante_porta", "not_var": "has_key_biblioteca"}
                },
                "aonde_ir": {
                    "label": "Aonde devo ir agora?", "group": "direcionamento", 
                    "requires": {"var": "has_key_biblioteca", "not_var": "has_key_oficina"}
                },
                "procura_oficina": {
                    "label": "O que eu procuro na Oficina?", "group": "direcionamento", 
                    "requires": {"var": "has_key_oficina"}
                },
                "perdido": {
                    "label": "Me sinto perdido...", "group": "direcionamento", 
                    "requires": {"var": "has_key_observatorio"}
                },
                "torre_esconde": {
                    "label": "Aurelium falou sobre alquimia praticada nesta torre.", "group": "descobertas", 
                    "requires": {"var": "knows_oficina", "not_var": "has_key_oficina"}
                },
                "procura_observatorio": {
                    "label": "Skulla falou sobre energia mágica no observatório.", "group": "descobertas", 
                    "requires": {"var": "knows_observatorio", "not_var": "has_key_observatorio"}
                },
                "procura_biblioteca": {
                    "label": "Nekrons mencionou que há livros de feitiços em uma Biblioteca Arcana.", "group": "descobertas", 
                    "requires": {"var": "knows_biblioteca", "not_var": "has_key_biblioteca"}
                },
                "magia_funciona": {
                    "label": "Como a magia funciona aqui?", "group": "magia", 
                    "requires": {"var": "has_wand"}
                },
                "encarando": {
                    "label": "Por que está me olhando assim?", "group": "magia", 
                    "requires": {"var": "has_potion"}
                },
                "provando_verdade": {
                    "label": "Eu descobri o que foi selado. Eu sei o que a frase significa.", "group": "a_verdade",
                    "requires": {"not_seen": ["eldrin_provando_verdade"]}
                }
            }
        },

        "skulla": {
            "groups": {
                "sobre_voce": {"label": "Uh... você está viva?", "requires": {}},
                "conhecimento": {"label": "Que tipo de conhecimento você pode me oferecer?", "requires": {}},
                "a_verdade": {"label": "Descobri o que Eldrin escondia de verdade", "requires": {"var": "knows_secret"}}
            },
            "topics": {
                "quem_eh": {"label": "O que você é?", "group": "sobre_voce", "requires": {}},
                "como_perdeu": {"label": "Como você perdeu seu corpo?", "group": "sobre_voce", "requires": {}},
                "sabe_util": {"label": "Você sabe algo útil?", "group": "conhecimento", "requires": {}},
                "producoes": {"label": "Como faço uma poção que me faça ver o que está oculto?", "group": "conhecimento", "requires": {"var": "knows_vision_potion", "not_var": "has_potion"}},
                "pocao": {"label": "Eu bebi a poção, não estou vendo nada diferente...", "group": "conhecimento", "requires": {"var": "has_potion"}},
                "sobre_lumos": {"label": "A poção está turva, o que falta?", "group": "conhecimento", "requires": {"var": "potion_ready_for_lumos", "not_var": "has_potion"}},
                "sobre_observatorio": {"label": "Feitiços? Como faço isso?", "group": "conhecimento", "requires": {"seen": ["producoes"], "not_var": "has_key_observatorio"}},
                "sobre_verdade": {"label": f"'{SECRET_PHRASE}'. Essa é a verdade que Eldrin esconde.", "group": "a_verdade", "requires": {}}
            }
        },

        "nekrons": {
            "groups": {
                "sobre_voce": {"label": "Você não é apenas um gato, é?", "requires": {}},
                "conhecimento": {"label": "Que tipo de conhecimento você pode me oferecer?", "requires": {}},
                "magia": {"label": "Me fale sobre a magia", "requires": {}},
                "a_verdade": {"label": "Descobri o que afligia Eldrin...", "requires": {"var": "knows_secret"}}
            },
            "topics": {
                "quem_eh": {"label": "Quem é você?", "group": "sobre_voce", "requires": {}},
                "nao_gato": {"label": "Mas você é uma gata mesmo? Por que tem essa forma?", "group": "sobre_voce", "requires": {}},
                "o_que_lugar": {"label": "O que é este lugar?", "group": "conhecimento", "requires": {}},
                "conhece_eldrin": {"label": "O que você pode me dizer sobre o Eldrin?", "group": "conhecimento", "requires": {}},
                "sobre_biblioteca": {"label": "Onde posso aprender mais feitiços?", "group": "magia", "requires": {"var": "wand_active"}},
                "varinha": {"label": "Encontrei a varinha, mas ela parece desativada...", "group": "magia", "requires": {"var": "has_wand", "not_var": "wand_active"}},
                "como_magia": {"label": "Como a magia funciona?", "group": "magia", "requires": {"var": "wand_active"}},
                "sobre_verdade": {"label": "Encontrei essa escritura nas profundezas da torre", "group": "a_verdade", "requires": {}}
            }
        },

        "aurelium": {
            "groups": {
                "sobre_voce": {"label": "Um livro falante?", "requires": {}},
                "conhecimento": {"label": "Que tipo de conhecimento você pode me oferecer?", "requires": {}},
                "a_verdade": {"label": "Descobri algo terrível...", "requires": {"var": "knows_secret"}}
            },
            "topics": {
                "quem_eh": {"label": "Quem foi você?", "group": "sobre_voce", "requires": {}},
                "solitario": {"label": "Você ouve vozes?", "group": "sobre_voce", "requires": {}},
                "sobre_torre": {"label": "O que sabe sobre o passado de Aethra?", "group": "conhecimento", "requires": {}},
                "escrituras_estante": {"label": "O que você pode me dizer sobre essa sala?", "group": "conhecimento", "requires": {"not_var": "has_potion"}},
                "sobre_alquimistas": {"label": "Como eu posso praticar alquimia?", "group": "conhecimento", "requires": {"var":"knows_vision_potion", "not_var": "knows_oficina"}},
                "interpretacao": {"label": f"Sabe o que isso significa?: '{SECRET_PHRASE}'", "group": "a_verdade", "requires": {}}
            }
        }
    }

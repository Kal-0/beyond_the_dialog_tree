# ==============================================================
# SISTEMA DE DIÁLOGOS - RASTREAMENTO E GERENCIAMENTO
# ==============================================================

# Rastreamento de tópicos vistos por NPC
default eldrin_topics_seen = set()
default skulla_topics_seen = set()
default nekrons_topics_seen = set()
default aurelium_topics_seen = set()

# Definição de grupos de tópicos e suas opções
define ELDRIN_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "testando", "confianca"]
    },
    "sobre_porta": {
        "label": "Sobre a Porta",
        "topics": ["por_que_guarda", "selada", "magia_antiga", "veritas", "mural"]
    },
    "direcionamento": {
        "label": "Direcionamento",
        "topics": ["o_que_fazer", "direcionamento", "aonde_ir", "procura_oficina", "procura_observatorio", "perdido"]
    },
    "exploracoes": {
        "label": "Explorações",
        "topics": ["estante", "poeira", "torre_esconde"]
    },
    "magia": {
        "label": "Sobre Magia",
        "topics": ["magia_funciona", "varinha", "encarando"]
    }
}

# Funções de rastreamento
def mark_eldrin_topic_seen(topic_id):
    """Marca um tópico como visto para Eldrin"""
    eldrin_topics_seen.add(topic_id)

def is_eldrin_group_exhausted(group_key):
    """Verifica se TODOS os tópicos de um grupo foram vistos"""
    if group_key not in ELDRIN_TOPICS:
        return False
    
    topics_in_group = ELDRIN_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in eldrin_topics_seen:
            return False
    return True

def get_eldrin_group_label(group_key):
    """Retorna o label de um grupo"""
    if group_key in ELDRIN_TOPICS:
        label = ELDRIN_TOPICS[group_key]["label"]
        if is_eldrin_group_exhausted(group_key):
            return f"{label} {'{i}(exaurido){/i}'}"
        return label
    return ""

def should_show_eldrin_group(group_key):
    """Verifica se o grupo deve ser mostrado (tem pelo menos um tópico disponível)"""
    if group_key not in ELDRIN_TOPICS:
        return False
    
    topics_in_group = ELDRIN_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in eldrin_topics_seen:
            return True
    return True

# Definição de grupos para Skulla (Oficina)
define SKULLA_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "como_perdeu", "precisava_ajuda"]
    },
    "conhecimento": {
        "label": "Conhecimento",
        "topics": ["sabe_util", "producoes", "pocao"]
    },
    "ingredientes": {
        "label": "Ingredientes",
        "topics": ["agua_fria", "agua_quente", "bebeu_pocao"]
    }
}

# Definição de grupos para Nekrons (Observatório)
define NEKRONS_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "nao_gato", "como_sair"]
    },
    "conhecimento": {
        "label": "Conhecimento",
        "topics": ["o_que_lugar", "conhece_eldrin", "o_que_fazer"]
    },
    "magia": {
        "label": "Magia",
        "topics": ["varinha", "tremor", "telescopio"]
    }
}

# Definição de grupos para Aurelium (Biblioteca)
define AURELIUM_TOPICS = {
    "sobre_voce": {
        "label": "Sobre Você",
        "topics": ["quem_eh", "solitario"]
    },
    "conhecimento": {
        "label": "Conhecimento",
        "topics": ["sobre_torre", "senha_porta", "sobre_alquimistas", "interpretacao", "magia_selamento"]
    }
}

# Funções para Skulla

def mark_skulla_topic_seen(topic_id):
    """Marca um tópico como visto para Skulla"""
    skulla_topics_seen.add(topic_id)

def is_skulla_group_exhausted(group_key):
    """Verifica se TODOS os tópicos de um grupo foram vistos para Skulla"""
    if group_key not in SKULLA_TOPICS:
        return False
    
    topics_in_group = SKULLA_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in skulla_topics_seen:
            return False
    return True

def get_skulla_group_label(group_key):
    """Retorna o label de um grupo para Skulla"""
    if group_key in SKULLA_TOPICS:
        label = SKULLA_TOPICS[group_key]["label"]
        if is_skulla_group_exhausted(group_key):
            return f"{label} {'{i}(exaurido){/i}'}"
        return label
    return ""

def should_show_skulla_group(group_key):
    """Verifica se o grupo deve ser mostrado para Skulla"""
    if group_key not in SKULLA_TOPICS:
        return False
    
    topics_in_group = SKULLA_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in skulla_topics_seen:
            return True
    return True

# Funções para Nekrons

def mark_nekrons_topic_seen(topic_id):
    """Marca um tópico como visto para Nekrons"""
    nekrons_topics_seen.add(topic_id)

def is_nekrons_group_exhausted(group_key):
    """Verifica se TODOS os tópicos de um grupo foram vistos para Nekrons"""
    if group_key not in NEKRONS_TOPICS:
        return False
    
    topics_in_group = NEKRONS_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in nekrons_topics_seen:
            return False
    return True

def get_nekrons_group_label(group_key):
    """Retorna o label de um grupo para Nekrons"""
    if group_key in NEKRONS_TOPICS:
        label = NEKRONS_TOPICS[group_key]["label"]
        if is_nekrons_group_exhausted(group_key):
            return f"{label} {'{i}(exaurido){/i}'}"
        return label
    return ""

def should_show_nekrons_group(group_key):
    """Verifica se o grupo deve ser mostrado para Nekrons"""
    if group_key not in NEKRONS_TOPICS:
        return False
    
    topics_in_group = NEKRONS_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in nekrons_topics_seen:
            return True
    return True

# Funções para Aurelium

def mark_aurelium_topic_seen(topic_id):
    """Marca um tópico como visto para Aurelium"""
    aurelium_topics_seen.add(topic_id)

def is_aurelium_group_exhausted(group_key):
    """Verifica se TODOS os tópicos de um grupo foram vistos para Aurelium"""
    if group_key not in AURELIUM_TOPICS:
        return False
    
    topics_in_group = AURELIUM_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in aurelium_topics_seen:
            return False
    return True

def get_aurelium_group_label(group_key):
    """Retorna o label de um grupo para Aurelium"""
    if group_key in AURELIUM_TOPICS:
        label = AURELIUM_TOPICS[group_key]["label"]
        if is_aurelium_group_exhausted(group_key):
            return f"{label} {'{i}(exaurido){/i}'}"
        return label
    return ""

def should_show_aurelium_group(group_key):
    """Verifica se o grupo deve ser mostrado para Aurelium"""
    if group_key not in AURELIUM_TOPICS:
        return False
    
    topics_in_group = AURELIUM_TOPICS[group_key]["topics"]
    for topic_id in topics_in_group:
        if topic_id not in aurelium_topics_seen:
            return True
    return True

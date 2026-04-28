# ==============================================================
# ÁREA FACILITADA DE ASSETS (IMAGENS E PERSONAGENS)
# ==============================================================

# --- PERSONAGENS (DEFINIÇÃO C/ NOME E COR) ---
define p = Character("Você", color="#c8ffc8")
define eldrin = Character("Eldrin", color="#a3a3a3")
define skulla = Character("Skulla", color="#e0e0e0")
define nekrons = Character("Nekrons", color="#6a4c93")
define aurelium = Character("Aurelium", color="#ffd700")

# --- PERSONAGENS (SPRITES) ---
image eldrin normal = "images/new/eldrin.png"
image skulla = "images/new/skulla.png"
image nekrons = "images/new/nekrons.png"
image aurelium_book = "images/new/aurelium.png"

# --- FUNDOS DE TELA (PORTA SELADA) ---
image bg porta_selada = "images/new/selo.png"
# O roteiro usa bg porta_selada como identificador geral do hub da porta

# --- FUNDOS DE TELA (OBSERVATÓRIO) ---
image bg observatorio = "images/new/observatorio.png"
image bg observatorio_sem_varinha = "images/new/observatorio_sem_varinha.png"

# --- FUNDOS DE TELA (BIBLIOTECA) ---
image bg biblioteca = "images/new/biblioteca.png"
image bg biblioteca_revelare = "images/new/biblioteca_revelare.png"
image bg biblioteca_passagem = "images/new/biblioteca_passagem.png"

# --- FUNDOS DE TELA (OFICINA ALQUÍMICA) ---
image bg oficina = "images/new/oficina.png"
image bg oficina_caldeirao_agua = "images/new/oficina_caldeirao_agua.png"
image bg oficina_caldeirao_aceso = "images/new/oficina_caldeirao_aceso.png"
image bg oficina_caldeirao_agua_aceso = "images/new/oficina_caldeirao_agua_aceso.png"
image bg oficina_caldeirao_pocao = "images/new/oficina_caldeirao_pocao.png"

# --- SALA SECRETA ---
# No repositório de novas texturas a imagem sala_secreta.png não estava listada nativamente
# mas caso o usuário vá usar a passagem como entrada:
image bg sala_secreta = "images/new/sala_secreta.png"

# --- ÍCONES DA HUD ---
# Redimensionando para 80x80 como os antigos blocos de cor
image icon_map = im.Scale("images/new/icon map.png", 100, 100)
image icon_wand = im.Scale("images/new/icon wand.png", 100, 100)
image icon_journal = im.Scale("images/new/icon journal.png", 100, 100)

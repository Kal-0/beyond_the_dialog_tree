# ==============================================================
# SISTEMA DE MÉTRICAS DE INTERAÇÃO — ANALYTICS DO TCC
# ==============================================================

init -2 python:
    import time
    import threading

    class GameMetrics(object):
        """Rastreia métricas de interação e tempo por ato/NPC."""

        def __init__(self):
            # Contadores de diálogo (falas individuais) por ato
            self.dialog_per_act = {1: 0, 2: 0, 3: 0, 4: 0}
            # Contadores de gameplay por ato
            self.gameplay_per_act = {1: 0, 2: 0, 3: 0, 4: 0}
            # Contadores de diálogo por NPC (falas individuais)
            self.dialog_per_npc = {
                "eldrin": 0,
                "skulla": 0,
                "nekrons": 0,
                "aurelium": 0
            }

            # Timer por ato (tempo acumulado em segundos)
            self.time_per_act = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
            self._act_start_time = None  # timestamp de quando o ato atual começou a contar
            self._timer_running = False

        # ----------------------------------------------------------
        # CONTADORES
        # ----------------------------------------------------------

        def record_dialog(self, npc_name):
            """Registra uma fala individual de um NPC."""
            act = get_story_act() if 'get_story_act' in dir() else store.story_state.get("act", 1)
            npc_key = npc_name.lower()

            if act in self.dialog_per_act:
                self.dialog_per_act[act] += 1
            if npc_key in self.dialog_per_npc:
                self.dialog_per_npc[npc_key] += 1

        def record_gameplay(self):
            """Registra uma ação de gameplay."""
            act = get_story_act() if 'get_story_act' in dir() else store.story_state.get("act", 1)
            if act in self.gameplay_per_act:
                self.gameplay_per_act[act] += 1

        # ----------------------------------------------------------
        # TIMER
        # ----------------------------------------------------------

        def start_timer(self):
            """Inicia o timer (chamado no início do jogo)."""
            self._act_start_time = time.time()
            self._timer_running = True

        def pause_timer(self):
            """Pausa o timer (chamado ao salvar/sair)."""
            if self._timer_running and self._act_start_time is not None:
                act = get_story_act() if 'get_story_act' in dir() else store.story_state.get("act", 1)
                elapsed = time.time() - self._act_start_time
                if act in self.time_per_act:
                    self.time_per_act[act] += elapsed
                self._act_start_time = None
                self._timer_running = False

        def resume_timer(self):
            """Resume o timer (chamado ao carregar save)."""
            if not self._timer_running:
                self._act_start_time = time.time()
                self._timer_running = True

        def on_act_change(self, new_act):
            """Chamado quando o ato muda. Finaliza timer do ato anterior."""
            self.pause_timer()
            self._act_start_time = time.time()
            self._timer_running = True

        def _finalize_timer(self):
            """Finaliza o timer atual antes de enviar dados."""
            if self._timer_running and self._act_start_time is not None:
                act = get_story_act() if 'get_story_act' in dir() else store.story_state.get("act", 1)
                elapsed = time.time() - self._act_start_time
                if act in self.time_per_act:
                    self.time_per_act[act] += elapsed
                self._act_start_time = None
                self._timer_running = False

        # ----------------------------------------------------------
        # ENVIO AO GOOGLE SHEETS
        # ----------------------------------------------------------

        def get_payload(self, final_escolhido):
            """Monta o dicionário de dados para envio."""
            self._finalize_timer()

            dialog_total = sum(self.dialog_per_act.values())
            gameplay_total = sum(self.gameplay_per_act.values())
            tempo_total = sum(self.time_per_act.values())

            return {
                "email": getattr(store, 'player_email', ''),
                "modo_jogo": getattr(store, 'dialog_mode', ''),
                "final_escolhido": final_escolhido,
                "eldrin_trust_final": getattr(store, 'eldrin_trust', 0),
                "interacoes_dialogo_total": dialog_total,
                "interacoes_gameplay_total": gameplay_total,
                "interacoes_dialogo_ato1": self.dialog_per_act.get(1, 0),
                "interacoes_dialogo_ato2": self.dialog_per_act.get(2, 0),
                "interacoes_dialogo_ato3": self.dialog_per_act.get(3, 0),
                "interacoes_dialogo_ato4": self.dialog_per_act.get(4, 0),
                "interacoes_gameplay_ato1": self.gameplay_per_act.get(1, 0),
                "interacoes_gameplay_ato2": self.gameplay_per_act.get(2, 0),
                "interacoes_gameplay_ato3": self.gameplay_per_act.get(3, 0),
                "interacoes_gameplay_ato4": self.gameplay_per_act.get(4, 0),
                "interacoes_eldrin": self.dialog_per_npc.get("eldrin", 0),
                "interacoes_skulla": self.dialog_per_npc.get("skulla", 0),
                "interacoes_nekrons": self.dialog_per_npc.get("nekrons", 0),
                "interacoes_aurelium": self.dialog_per_npc.get("aurelium", 0),
                "tempo_ato1": round(self.time_per_act.get(1, 0.0)),
                "tempo_ato2": round(self.time_per_act.get(2, 0.0)),
                "tempo_ato3": round(self.time_per_act.get(3, 0.0)),
                "tempo_ato4": round(self.time_per_act.get(4, 0.0)),
                "tempo_total": round(tempo_total)
            }

        def submit_to_sheets(self, final_escolhido):
            """Envia métricas ao Google Sheets via Apps Script."""
            payload = self.get_payload(final_escolhido)

            # URL do Google Apps Script Web App (configurar após deploy)
            APPS_SCRIPT_URL = getattr(store, 'METRICS_SUBMIT_URL', '')

            if not APPS_SCRIPT_URL:
                renpy.notify("Métricas: URL de envio não configurada.")
                return False

            try:
                import json
                try:
                    from urllib.request import Request, urlopen
                    from urllib.error import URLError
                except ImportError:
                    from urllib2 import Request, urlopen, URLError

                data = json.dumps(payload).encode('utf-8')
                req = Request(APPS_SCRIPT_URL, data=data, headers={'Content-Type': 'application/json'})

                def _send():
                    try:
                        import ssl
                        ctx = ssl.create_default_context()
                        ctx.check_hostname = False
                        ctx.verify_mode = ssl.CERT_NONE
                        response = urlopen(req, timeout=15, context=ctx)
                        response.read()
                    except Exception as e:
                        import traceback
                        with open(config.basedir + "/metrics_error.txt", "w", encoding="utf-8") as f:
                            f.write(traceback.format_exc())

                # Envia em thread separada para não travar a UI
                t = threading.Thread(target=_send)
                t.daemon = True
                t.start()
                t.join(timeout=10)  # Espera até 10 segundos
                
                # Se houver erro, notificar
                import os
                if os.path.exists(config.basedir + "/metrics_error.txt"):
                    renpy.notify("Erro ao enviar métricas (veja metrics_error.txt)")
                else:
                    renpy.notify("Métricas enviadas com sucesso!")
                return True

            except Exception as e:
                renpy.notify("Falha ao enviar métricas.")
                return False

# ----------------------------------------------------------
# VARIÁVEIS DEFAULT
# ----------------------------------------------------------

default game_metrics = GameMetrics()

# URL do Google Apps Script (será configurada pelo desenvolvedor)
# Para configurar: crie um Apps Script vinculado à planilha, 
# faça deploy como Web App e cole a URL aqui.
define METRICS_SUBMIT_URL = "https://script.google.com/macros/s/AKfycbxD5HmKOsrb9-B4Q51t4c90avUXuEoe6P7LUdO73YItdQsaCcHTUsjCGPAPeol-SibqLQ/exec"

# ----------------------------------------------------------
# CALLBACKS DE CICLO DE VIDA DO REN'PY
# ----------------------------------------------------------

init python:
    import time as _time

    # Pausar timer ao sair/salvar
    def _metrics_quit_callback():
        if hasattr(store, 'game_metrics') and store.game_metrics:
            store.game_metrics.pause_timer()

    # Resumir timer ao carregar save
    def _metrics_after_load_callback():
        if hasattr(store, 'game_metrics') and store.game_metrics:
            store.game_metrics.resume_timer()

    config.quit_callbacks.append(_metrics_quit_callback)
    config.after_load_callbacks.append(_metrics_after_load_callback)

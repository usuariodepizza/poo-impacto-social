"""Plataforma (controlador central) e RelatorioImpacto do App Rota Acessível."""
from collections import Counter

from .modelos import (BarreiraArquitetonica, CidadaoColaborador, GestorPublico,
                      LocalPublico, OcorrenciaBarreira, StatusOcorrencia,
                      Usuario)


class RelatorioImpacto:
    """Consolida os indicadores de inclusão e acessibilidade urbana."""

    def __init__(self, locais, ocorrencias, usuarios):
        self._locais = locais
        self._ocorrencias = ocorrencias
        self._usuarios = usuarios

    def gerar_texto(self):
        total_locais = len(self._locais)
        acessiveis = sum(1 for loc in self._locais
                         if loc.media_acessibilidade() >= 4.0 and loc.barreiras_ativas() == 0)
        total_av = sum(len(loc.avaliacoes) for loc in self._locais)
        total_oc = len(self._ocorrencias)
        resolvidas = sum(1 for o in self._ocorrencias if o.status == StatusOcorrencia.RESOLVIDA)
        taxa = (resolvidas / total_oc * 100) if total_oc else 0
        por_categoria = Counter(o.barreira.categoria() for o in self._ocorrencias)
        cidadaos = sorted(
            [u for u in self._usuarios if isinstance(u, CidadaoColaborador)],
            key=lambda c: c.pontos, reverse=True)

        linhas = [
            "=" * 58,
            "   RELATÓRIO DE IMPACTO - APP ROTA ACESSÍVEL (ODS 10)",
            "=" * 58,
            f"Locais públicos mapeados ....... {total_locais}",
            f"Rotas/locais 100% acessíveis ... {acessiveis}",
            f"Avaliações colaborativas ....... {total_av}",
            f"Barreiras denunciadas .......... {total_oc}",
            f"Barreiras resolvidas ........... {resolvidas} ({taxa:.0f}%)",
            "Por tipo de barreira: " + (
                ", ".join(f"{cat} ({qtd})" for cat, qtd in por_categoria.most_common()) or "-"),
            "-" * 58,
            "Ranking de cidadãos colaboradores:",
        ]
        for i, c in enumerate(cidadaos[:5], 1):
            linhas.append(f"   {i}. {c.nome} ({c.perfil_mobilidade}) - {c.pontos} pts - nível {c.nivel()}")
        linhas.append("=" * 58)
        return "\n".join(linhas)


class Plataforma:
    """Controlador central do App Rota Acessível."""

    def __init__(self, nome="Rota Acessível"):
        self._nome = nome
        self._usuarios = {}     # agregação
        self._locais = {}       # agregação
        self._ocorrencias = {}  # agregação

    @property
    def nome(self):
        return self._nome

    def registrar_usuario(self, usuario: Usuario):
        self._usuarios[usuario.id] = usuario
        return usuario

    def registrar_local(self, local: LocalPublico):
        self._locais[local.id] = local
        return local

    def buscar_usuario(self, usuario_id, tipo=Usuario):
        u = self._usuarios.get(usuario_id)
        if not isinstance(u, tipo):
            raise ValueError(f"{tipo.__name__} #{usuario_id} não encontrado.")
        return u

    def buscar_local(self, local_id):
        if local_id not in self._locais:
            raise ValueError(f"Local #{local_id} não encontrado.")
        return self._locais[local_id]

    def buscar_ocorrencia(self, ocorrencia_id):
        if ocorrencia_id not in self._ocorrencias:
            raise ValueError(f"Ocorrência #{ocorrencia_id} não encontrada.")
        return self._ocorrencias[ocorrencia_id]

    def listar_usuarios(self, tipo=Usuario):
        return [u for u in self._usuarios.values() if isinstance(u, tipo)]

    def listar_locais(self, cidade=None, apenas_acessiveis=False):
        locais = [loc for loc in self._locais.values()
                  if cidade is None or loc.cidade.lower() == cidade.lower()]
        if apenas_acessiveis:
            locais = [loc for loc in locais
                      if loc.media_acessibilidade() >= 4.0 and loc.barreiras_ativas() == 0]
        return sorted(locais, key=lambda loc: loc.media_acessibilidade(), reverse=True)

    def avaliar_local(self, local_id, usuario_id, nota, comentario, possui_rampa=True, possui_piso_tatil=False):
        local = self.buscar_local(local_id)
        usuario = self.buscar_usuario(usuario_id)
        return local.avaliar(usuario, nota, comentario, possui_rampa, possui_piso_tatil)

    def denunciar_barreira(self, local_id, usuario_id, barreira: BarreiraArquitetonica):
        local = self.buscar_local(local_id)
        usuario = self.buscar_usuario(usuario_id)
        ocorrencia = OcorrenciaBarreira(local, usuario, barreira)
        self._ocorrencias[ocorrencia.id] = ocorrencia
        return ocorrencia

    def listar_ocorrencias_prioritarias(self, cidade=None):
        ativas = [o for o in self._ocorrencias.values()
                  if o.status != StatusOcorrencia.RESOLVIDA
                  and (cidade is None or o.local.cidade.lower() == cidade.lower())]
        return sorted(ativas, key=lambda o: (o.barreira.gravidade_base(), o.confirmacoes), reverse=True)

    def resolver_ocorrencia(self, ocorrencia_id, gestor_id):
        ocorrencia = self.buscar_ocorrencia(ocorrencia_id)
        gestor = self.buscar_usuario(gestor_id, GestorPublico)
        ocorrencia.marcar_resolvida(gestor)
        return ocorrencia

    def gerar_relatorio(self):
        return RelatorioImpacto(
            list(self._locais.values()),
            list(self._ocorrencias.values()),
            list(self._usuarios.values()),
        )
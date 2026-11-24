"""Plataforma (controlador central) e RelatorioImpacto da Rede Mulher Segura."""
from .modelos import (AdvogadaVoluntaria, Denuncia, NivelUrgencia, PontoApoio,
                      ProfissionalVoluntaria, PsicologaVoluntaria,
                      RelatoOcorrencia, StatusDenuncia, Usuaria)


class RelatorioImpacto:
    """Consolida os indicadores de proteção e acolhimento da plataforma."""

    def __init__(self, denuncias, profissionais, pontos_apoio):
        self._total_denuncias = len(denuncias)
        self._anonimas = sum(1 for d in denuncias if d.anonima)
        self._emergencias = sum(1 for d in denuncias if d.urgencia == NivelUrgencia.EMERGENCIA)
        self._em_acolhimento = sum(1 for d in denuncias
                                   if d.status in (StatusDenuncia.EM_ACOLHIMENTO, StatusDenuncia.ENCAMINHADA))
        self._encerradas = sum(1 for d in denuncias if d.status == StatusDenuncia.ENCERRADA)
        self._total_atendimentos = sum(len(d.atendimentos) for d in denuncias)
        self._psicologas = sum(1 for p in profissionais if isinstance(p, PsicologaVoluntaria))
        self._advogadas = sum(1 for p in profissionais if isinstance(p, AdvogadaVoluntaria))
        self._pontos_ativos = len(pontos_apoio)

    def gerar_texto(self):
        taxa_acolhimento = ((self._em_acolhimento + self._encerradas) / self._total_denuncias * 100
                            if self._total_denuncias else 0)
        return "\n".join([
            "=" * 56,
            "   RELATÓRIO DE IMPACTO - REDE MULHER SEGURA (ODS 5)",
            "=" * 56,
            f"Denúncias registradas .......... {self._total_denuncias}",
            f"Denúncias anônimas ............. {self._anonimas}",
            f"Casos de emergência ............ {self._emergencias}",
            f"Casos em acolhimento/rede ...... {self._em_acolhimento}",
            f"Casos concluídos/encerrados .... {self._encerradas}",
            f"Taxa de cobertura da rede ...... {taxa_acolhimento:.0f}%",
            f"Atendimentos voluntários ....... {self._total_atendimentos} "
            f"({self._psicologas} psicólogas / {self._advogadas} advogadas)",
            f"Pontos de apoio mapeados ....... {self._pontos_ativos}",
            "=" * 56,
        ])


class Plataforma:
    """Controlador central da Rede Mulher Segura."""

    def __init__(self, nome="Rede Mulher Segura"):
        self._nome = nome
        self._usuarias = {}        # agregação: entidades existem fora da plataforma
        self._profissionais = {}
        self._pontos_apoio = {}
        self._denuncias = {}

    @property
    def nome(self):
        return self._nome

    def registrar_usuaria(self, usuaria: Usuaria):
        self._usuarias[usuaria.id] = usuaria
        return usuaria

    def registrar_profissional(self, profissional: ProfissionalVoluntaria):
        self._profissionais[profissional.id] = profissional
        return profissional

    def registrar_ponto_apoio(self, ponto: PontoApoio):
        self._pontos_apoio[ponto.id] = ponto
        return ponto

    def buscar_usuaria(self, usuaria_id):
        if usuaria_id not in self._usuarias:
            raise ValueError(f"Usuária #{usuaria_id} não encontrada.")
        return self._usuarias[usuaria_id]

    def buscar_profissional(self, prof_id):
        if prof_id not in self._profissionais:
            raise ValueError(f"Profissional #{prof_id} não encontrada.")
        return self._profissionais[prof_id]

    def buscar_ponto_apoio(self, ponto_id):
        if ponto_id not in self._pontos_apoio:
            raise ValueError(f"Ponto de apoio #{ponto_id} não encontrado.")
        return self._pontos_apoio[ponto_id]

    def buscar_denuncia(self, denuncia_id):
        if denuncia_id not in self._denuncias:
            raise ValueError(f"Denúncia #{denuncia_id} não encontrada.")
        return self._denuncias[denuncia_id]

    def listar_profissionais(self, tipo=ProfissionalVoluntaria, apenas_disponiveis=False):
        return [p for p in self._profissionais.values()
                if isinstance(p, tipo) and (not apenas_disponiveis or p.disponivel)]

    def listar_pontos_apoio(self, cidade=None):
        return [pt for pt in self._pontos_apoio.values()
                if cidade is None or pt.cidade.lower() == cidade.lower()]

    def registrar_denuncia(self, usuaria_id, cidade, urgencia, tipo_violencia, descricao, anonima=True):
        usuaria = self.buscar_usuaria(usuaria_id)
        relato = RelatoOcorrencia(tipo_violencia, descricao)
        denuncia = Denuncia(usuaria, cidade, urgencia, [relato], anonima=anonima)
        usuaria.vincular_denuncia(denuncia)
        self._denuncias[denuncia.id] = denuncia
        return denuncia

    def listar_denuncias_prioritarias(self, cidade=None):
        """Ordena denúncias ativas da maior urgência para a menor."""
        ativas = [d for d in self._denuncias.values()
                  if d.status != StatusDenuncia.ENCERRADA
                  and (cidade is None or d.cidade.lower() == cidade.lower())]
        return sorted(ativas, key=lambda d: d.urgencia.value, reverse=True)

    def conectar_voluntaria(self, denuncia_id, prof_id):
        denuncia = self.buscar_denuncia(denuncia_id)
        prof = self.buscar_profissional(prof_id)
        return denuncia.iniciar_atendimento(prof)

    def encaminhar_para_ponto(self, denuncia_id, ponto_id):
        denuncia = self.buscar_denuncia(denuncia_id)
        ponto = self.buscar_ponto_apoio(ponto_id)
        denuncia.encaminhar_ponto_apoio(ponto)
        return ponto

    def gerar_relatorio(self):
        return RelatorioImpacto(
            list(self._denuncias.values()),
            list(self._profissionais.values()),
            list(self._pontos_apoio.values()),
        )
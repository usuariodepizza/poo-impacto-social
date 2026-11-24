"""Plataforma (controlador central) e RelatorioImpacto do App Saúde em Dia."""
from datetime import datetime

from .modelos import (CompromissoSaude, Cuidador, FamiliarResponsavel, Idoso,
                      LembreteMedicacao, StatusCompromisso)


class RelatorioImpacto:
    """Consolida indicadores de adesão terapêutica, prevenção e alertas familiares."""

    def __init__(self, idosos, compromissos):
        self._total_idosos = len(idosos)
        validos = [c for c in compromissos if c.status != StatusCompromisso.CANCELADO]
        self._total_compromissos = len(validos)
        self._confirmados = sum(1 for c in validos if c.status == StatusCompromisso.CONFIRMADO)
        self._alertas_enviados = sum(1 for c in validos if c.status == StatusCompromisso.ATRASADO_ALERTADO)
        self._medicacoes = sum(1 for c in validos if isinstance(c, LembreteMedicacao))
        self._medicacoes_confirmadas = sum(
            1 for c in validos if isinstance(c, LembreteMedicacao) and c.status == StatusCompromisso.CONFIRMADO
        )

    def gerar_texto(self):
        adesao_geral = (self._confirmados / self._total_compromissos * 100
                        if self._total_compromissos else 0)
        adesao_med = (self._medicacoes_confirmadas / self._medicacoes * 100
                      if self._medicacoes else 0)
        return "\n".join([
            "=" * 56,
            "   RELATÓRIO DE IMPACTO - APP SAÚDE EM DIA (ODS 3)",
            "=" * 56,
            f"Idosos acompanhados ............ {self._total_idosos}",
            f"Lembretes ativos ............... {self._total_compromissos}",
            f"Lembretes confirmados .......... {self._confirmados}",
            f"Taxa geral de adesão ........... {adesao_geral:.0f}%",
            f"Adesão medicamentosa ........... {adesao_med:.0f}% ({self._medicacoes_confirmadas}/{self._medicacoes})",
            f"Alertas preventivos a familiares {self._alertas_enviados}",
            "=" * 56,
        ])


class Plataforma:
    """Controlador central do App Saúde em Dia."""

    def __init__(self, nome="Saúde em Dia"):
        self._nome = nome
        self._pessoas = {}       # agregação
        self._compromissos = {}  # agregação

    @property
    def nome(self):
        return self._nome

    def registrar_pessoa(self, pessoa):
        self._pessoas[pessoa.id] = pessoa
        return pessoa

    def buscar_pessoa(self, pessoa_id, tipo=None):
        p = self._pessoas.get(pessoa_id)
        if p is None or (tipo is not None and not isinstance(p, tipo)):
            nome_tipo = tipo.__name__ if tipo else "Pessoa"
            raise ValueError(f"{nome_tipo} #{pessoa_id} não encontrado(a).")
        return p

    def buscar_compromisso(self, comp_id):
        if comp_id not in self._compromissos:
            raise ValueError(f"Lembrete #{comp_id} não encontrado.")
        return self._compromissos[comp_id]

    def listar_pessoas(self, tipo=None):
        if tipo is None:
            return list(self._pessoas.values())
        return [p for p in self._pessoas.values() if isinstance(p, tipo)]

    def vincular_rede_apoio(self, idoso_id, familiar_id=None, cuidador_id=None):
        idoso = self.buscar_pessoa(idoso_id, Idoso)
        if familiar_id is not None:
            idoso.vincular_familiar(self.buscar_pessoa(familiar_id, FamiliarResponsavel))
        if cuidador_id is not None:
            idoso.vincular_cuidador(self.buscar_pessoa(cuidador_id, Cuidador))

    def agendar_compromisso(self, compromisso: CompromissoSaude):
        compromisso.idoso.adicionar_compromisso(compromisso)
        self._compromissos[compromisso.id] = compromisso
        return compromisso

    def confirmar_compromisso(self, comp_id, responsavel_id, agora=None):
        comp = self.buscar_compromisso(comp_id)
        resp = self.buscar_pessoa(responsavel_id)
        comp.confirmar(resp, agora)
        return comp

    def verificar_alertas_atraso(self, agora=None):
        """Varre lembretes pendentes e dispara alertas aos familiares quando atrasados."""
        agora = agora or datetime.now()
        disparados = []
        for comp in self._compromissos.values():
            alerta = comp.verificar_atraso(agora)
            if alerta is not None:
                disparados.append(alerta)
        return disparados

    def listar_compromissos(self, idoso_id=None):
        lista = list(self._compromissos.values())
        if idoso_id is not None:
            lista = [c for c in lista if c.idoso.id == idoso_id]
        return sorted(lista, key=lambda c: c.horario_previsto)

    def gerar_relatorio(self):
        return RelatorioImpacto(
            self.listar_pessoas(Idoso),
            list(self._compromissos.values()),
        )
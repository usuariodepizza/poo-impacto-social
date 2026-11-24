"""Modelos (classes de domínio) do App Saúde em Dia - ODS 3 (Saúde e Bem-Estar).

Pilares de POO usados neste módulo:
  * Encapsulamento: atributos privados (_x) expostos por @property; AlertaFamiliar
    é um objeto de valor imutável (@dataclass(frozen=True)); coleções retornadas
    como tuplas imutáveis.
  * Herança: Idoso, Cuidador e FamiliarResponsavel herdam de Pessoa;
    LembreteMedicacao, LembreteVacina e LembreteConsulta herdam de CompromissoSaude.
  * Polimorfismo: resumo() (Pessoa) e instrucoes_cuidado() / tolerancia_minutos()
    (CompromissoSaude) comportam-se de forma específica em cada subclasse.
  * Composição: um Idoso compõe seus CompromissoSaude e os AlertaFamiliar gerados.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class StatusCompromisso(Enum):
    PENDENTE = "Pendente"
    CONFIRMADO = "Confirmado"
    ATRASADO_ALERTADO = "Atrasado (Alerta Enviado)"
    CANCELADO = "Cancelado"


@dataclass(frozen=True)
class AlertaFamiliar:
    """Objeto de valor imutável que registra um disparo de alerta ao familiar."""
    destinatario_nome: str
    destinatario_telefone: str
    mensagem: str
    enviado_em: datetime

    def __str__(self):
        hora = self.enviado_em.strftime("%d/%m/%Y %H:%M")
        return f"[ALERTA {hora}] Para {self.destinatario_nome} ({self.destinatario_telefone}): {self.mensagem}"


# --------------------------------------------------------------------------
# Pessoas (herança + polimorfismo)
# --------------------------------------------------------------------------
class Pessoa(ABC):
    """Classe base abstrata dos atores do ecossistema de cuidado ao idoso."""

    _proximo_id = 1

    def __init__(self, nome, telefone, cidade):
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")
        if not telefone or not telefone.strip():
            raise ValueError("O telefone é obrigatório.")
        self._id = Pessoa._proximo_id
        Pessoa._proximo_id += 1
        self._nome = nome.strip()
        self._telefone = telefone.strip()
        self._cidade = cidade.strip()

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def telefone(self):
        return self._telefone

    @property
    def cidade(self):
        return self._cidade

    @abstractmethod
    def resumo(self):
        """Cada ator se apresenta conforme seu papel no acompanhamento."""

    def __str__(self):
        return self.resumo()


class FamiliarResponsavel(Pessoa):
    """Familiar que recebe notificações automáticas em caso de não confirmação."""

    def __init__(self, nome, telefone, cidade, parentesco):
        super().__init__(nome, telefone, cidade)
        self._parentesco = parentesco.strip()
        self._alertas_recebidos = []

    @property
    def parentesco(self):
        return self._parentesco

    @property
    def alertas_recebidos(self):
        return tuple(self._alertas_recebidos)

    def receber_alerta(self, alerta: AlertaFamiliar):
        self._alertas_recebidos.append(alerta)

    def resumo(self):
        return (f"[Familiar #{self._id}] {self._nome} ({self._parentesco}) - "
                f"Tel: {self._telefone} | {len(self._alertas_recebidos)} alerta(s) recebido(s)")


class Cuidador(Pessoa):
    """Profissional ou acompanhante que auxilia o idoso na rotina diária."""

    def __init__(self, nome, telefone, cidade, turno="Integral", registro_profissional=None):
        super().__init__(nome, telefone, cidade)
        self._turno = turno.strip()
        self._registro_profissional = registro_profissional.strip() if registro_profissional else "Cuidador Familiar"
        self._confirmacoes_realizadas = 0

    @property
    def turno(self):
        return self._turno

    @property
    def registro_profissional(self):
        return self._registro_profissional

    @property
    def confirmacoes_realizadas(self):
        return self._confirmacoes_realizadas

    def registrar_confirmacao(self):
        self._confirmacoes_realizadas += 1

    def resumo(self):
        return (f"[Cuidador #{self._id}] {self._nome} ({self._registro_profissional} - Turno: {self._turno}) | "
                f"{self._confirmacoes_realizadas} cuidado(s) confirmado(s)")


class Idoso(Pessoa):
    """Paciente acompanhado na plataforma. Compõe sua agenda de compromissos de saúde."""

    def __init__(self, nome, telefone, cidade, idade, condicoes_saude=None):
        super().__init__(nome, telefone, cidade)
        if idade < 60:
            raise ValueError("O cadastro de paciente principal é destinado a pessoas com 60 anos ou mais.")
        self._idade = int(idade)
        self._condicoes_saude = condicoes_saude.strip() if condicoes_saude else "Acompanhamento preventivo"
        self._familiar_responsavel = None
        self._cuidador = None
        self._compromissos = []  # composição: agenda pertence ao idoso

    @property
    def idade(self):
        return self._idade

    @property
    def condicoes_saude(self):
        return self._condicoes_saude

    @property
    def familiar_responsavel(self):
        return self._familiar_responsavel

    @property
    def cuidador(self):
        return self._cuidador

    @property
    def compromissos(self):
        return tuple(self._compromissos)

    def vincular_familiar(self, familiar: FamiliarResponsavel):
        self._familiar_responsavel = familiar

    def vincular_cuidador(self, cuidador: Cuidador):
        self._cuidador = cuidador

    def adicionar_compromisso(self, compromisso):
        self._compromissos.append(compromisso)
        return compromisso

    def taxa_adesao(self):
        validos = [c for c in self._compromissos if c.status != StatusCompromisso.CANCELADO]
        if not validos:
            return 100.0
        confirmados = sum(1 for c in validos if c.status == StatusCompromisso.CONFIRMADO)
        return (confirmados / len(validos)) * 100

    def resumo(self):
        fam = self._familiar_responsavel.nome if self._familiar_responsavel else "Não vinculado"
        cuid = self._cuidador.nome if self._cuidador else "Sem cuidador"
        return (f"[Idoso #{self._id}] {self._nome}, {self._idade} anos ({self._condicoes_saude}) | "
                f"Familiar: {fam} | Cuidador: {cuid} | Adesão: {self.taxa_adesao():.0f}%")


# --------------------------------------------------------------------------
# Compromissos de Saúde (herança + polimorfismo)
# --------------------------------------------------------------------------
class CompromissoSaude(ABC):
    """Classe base abstrata para lembretes de medicação, vacinas e consultas."""

    _proximo_id = 1

    def __init__(self, idoso: Idoso, titulo, horario_previsto: datetime):
        if not titulo or not titulo.strip():
            raise ValueError("O título do compromisso é obrigatório.")
        self._id = CompromissoSaude._proximo_id
        CompromissoSaude._proximo_id += 1
        self._idoso = idoso
        self._titulo = titulo.strip()
        self._horario_previsto = horario_previsto
        self._status = StatusCompromisso.PENDENTE
        self._confirmado_por = None
        self._confirmado_em = None
        self._alerta_gerado = None

    @property
    def id(self):
        return self._id

    @property
    def idoso(self):
        return self._idoso

    @property
    def titulo(self):
        return self._titulo

    @property
    def horario_previsto(self):
        return self._horario_previsto

    @property
    def status(self):
        return self._status

    @property
    def alerta_gerado(self):
        return self._alerta_gerado

    @abstractmethod
    def tolerancia_minutos(self):
        """Tempo máximo de atraso antes de disparar alerta ao familiar (polimorfismo)."""

    @abstractmethod
    def instrucoes_cuidado(self):
        """Detalhes específicos de cada tipo de lembrete (polimorfismo)."""

    def confirmar(self, responsavel: Pessoa, agora=None):
        if self._status == StatusCompromisso.CANCELADO:
            raise ValueError(f"Compromisso #{self._id} está cancelado.")
        if self._status == StatusCompromisso.CONFIRMADO:
            raise ValueError(f"Compromisso #{self._id} já foi confirmado anteriormente.")
        self._status = StatusCompromisso.CONFIRMADO
        self._confirmado_por = responsavel
        self._confirmado_em = agora or datetime.now()
        if isinstance(responsavel, Cuidador):
            responsavel.registrar_confirmacao()

    def verificar_atraso(self, agora=None):
        """Dispara alerta automático ao familiar se ultrapassou a tolerância sem confirmação."""
        agora = agora or datetime.now()
        if self._status != StatusCompromisso.PENDENTE:
            return None
        limite = self._horario_previsto + timedelta(minutes=self.tolerancia_minutos())
        if agora > limite:
            self._status = StatusCompromisso.ATRASADO_ALERTADO
            familiar = self._idoso.familiar_responsavel
            if familiar:
                msg = (f"Não houve confirmação de '{self._titulo}' para {self._idoso.nome} "
                       f"(previsto para {self._horario_previsto.strftime('%H:%M')}).")
                alerta = AlertaFamiliar(familiar.nome, familiar.telefone, msg, agora)
                self._alerta_gerado = alerta
                familiar.receber_alerta(alerta)
                return alerta
        return None

    def cancelar(self):
        if self._status == StatusCompromisso.CONFIRMADO:
            raise ValueError("Não é possível cancelar um compromisso já confirmado.")
        self._status = StatusCompromisso.CANCELADO

    def __str__(self):
        hora = self._horario_previsto.strftime("%d/%m %H:%M")
        conf = f" por {self._confirmado_por.nome}" if self._confirmado_por else ""
        return (f"Lembrete #{self._id} | {self._idoso.nome} | {self._titulo} ({hora}) | "
                f"Status: {self._status.value}{conf}\n      {self.instrucoes_cuidado()}")


class LembreteMedicacao(CompromissoSaude):
    """Lembrete de remédio contínuo ou pontual (tolerância rígida: 30 min)."""

    def __init__(self, idoso, nome_medicamento, horario_previsto, dosagem, via_administracao="Oral"):
        super().__init__(idoso, nome_medicamento, horario_previsto)
        self._dosagem = dosagem.strip()
        self._via_administracao = via_administracao.strip()

    @property
    def dosagem(self):
        return self._dosagem

    def tolerancia_minutos(self):
        return 30

    def instrucoes_cuidado(self):
        return f"Medicação: {self._dosagem} ({self._via_administracao}) | Tolerância de atraso: {self.tolerancia_minutos()} min"


class LembreteVacina(CompromissoSaude):
    """Lembrete de imunização (gripe, COVID-19, pneumocócica, herpes-zóster)."""

    def __init__(self, idoso, nome_vacina, horario_previsto, dose, posto_saude):
        super().__init__(idoso, nome_vacina, horario_previsto)
        self._dose = dose.strip()
        self._posto_saude = posto_saude.strip()

    def tolerancia_minutos(self):
        return 120

    def instrucoes_cuidado(self):
        return f"Vacina ({self._dose}) em {self._posto_saude} | Levar documento e cartão SUS"


class LembreteConsulta(CompromissoSaude):
    """Lembrete de consulta médica ou exame de acompanhamento."""

    def __init__(self, idoso, especialidade, horario_previsto, medico, local_atendimento):
        super().__init__(idoso, f"Consulta - {especialidade}", horario_previsto)
        self._medico = medico.strip()
        self._local_atendimento = local_atendimento.strip()

    def tolerancia_minutos(self):
        return 60

    def instrucoes_cuidado(self):
        return f"Atendimento com {self._medico} em {self._local_atendimento}"
"""Modelos (classes de domínio) da Rede Mulher Segura - ODS 5 (Igualdade de Gênero).

Pilares de POO usados neste módulo:
  * Encapsulamento: atributos privados (_x) expostos por @property; proteção de
    identidade em denúncias anônimas; listas retornadas como tuplas imutáveis.
  * Herança: PsicologaVoluntaria e AdvogadaVoluntaria herdam de ProfissionalVoluntaria.
  * Polimorfismo: resumo() e protocolo_acolhimento() possuem implementações
    específicas em cada especialidade de voluntária.
  * Composição: uma Denuncia é composta por seus RelatoOcorrencia (histórico de
    fatos/evidências que nascem e pertencem à denúncia).
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class StatusDenuncia(Enum):
    ABERTA = "Aberta"
    EM_ACOLHIMENTO = "Em Acolhimento"
    ENCAMINHADA = "Encaminhada para Rede"
    ENCERRADA = "Encerrada"


class NivelUrgencia(Enum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    EMERGENCIA = 4


# --------------------------------------------------------------------------
# Profissionais Voluntárias (herança + polimorfismo)
# --------------------------------------------------------------------------
class ProfissionalVoluntaria(ABC):
    """Classe base abstrata para profissionais voluntárias da rede."""

    _proximo_id = 1

    def __init__(self, nome, email, cidade, registro_profissional, disponivel=True):
        if not nome or not nome.strip():
            raise ValueError("O nome da profissional é obrigatório.")
        if "@" not in email:
            raise ValueError("E-mail inválido.")
        if not registro_profissional or not registro_profissional.strip():
            raise ValueError("O registro profissional (CRP/OAB) é obrigatório.")
        self._id = ProfissionalVoluntaria._proximo_id
        ProfissionalVoluntaria._proximo_id += 1
        self._nome = nome.strip()
        self._email = email.strip()
        self._cidade = cidade.strip()
        self._registro_profissional = registro_profissional.strip()
        self._disponivel = bool(disponivel)
        self._atendimentos = []

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def cidade(self):
        return self._cidade

    @property
    def registro_profissional(self):
        return self._registro_profissional

    @property
    def disponivel(self):
        return self._disponivel

    @disponivel.setter
    def disponivel(self, valor):
        self._disponivel = bool(valor)

    @property
    def atendimentos(self):
        return tuple(self._atendimentos)

    def registrar_atendimento(self, atendimento):
        self._atendimentos.append(atendimento)

    @abstractmethod
    def especialidade(self):
        """Retorna a área de atuação da voluntária."""

    @abstractmethod
    def protocolo_acolhimento(self, denuncia):
        """Define o protocolo inicial conforme a especialidade (polimorfismo)."""

    def resumo(self):
        status = "Disponível" if self._disponivel else "Ocupada"
        return (f"[{self.especialidade()} #{self._id}] {self._nome} ({self._registro_profissional}) "
                f"- {self._cidade} | {status} | {len(self._atendimentos)} atendimento(s)")

    def __str__(self):
        return self.resumo()


class PsicologaVoluntaria(ProfissionalVoluntaria):
    """Voluntária que oferece escuta qualificada e suporte emocional."""

    def __init__(self, nome, email, cidade, crp, abordagem="Acolhimento Humanizado", disponivel=True):
        super().__init__(nome, email, cidade, crp, disponivel)
        self._abordagem = abordagem.strip()

    @property
    def abordagem(self):
        return self._abordagem

    def especialidade(self):
        return "Psicóloga"

    def protocolo_acolhimento(self, denuncia):
        prioridade = "imediata" if denuncia.urgencia.value >= 3 else "agendada"
        return (f"Escuta psicológica {prioridade} ({self._abordagem}) para estabilização "
                f"emocional e avaliação de risco da denúncia #{denuncia.id}.")


class AdvogadaVoluntaria(ProfissionalVoluntaria):
    """Voluntária que presta orientação jurídica e apoio para medidas protetivas."""

    def __init__(self, nome, email, cidade, oab, area_atuacao="Direito da Mulher / Lei Maria da Penha", disponivel=True):
        super().__init__(nome, email, cidade, oab, disponivel)
        self._area_atuacao = area_atuacao.strip()

    @property
    def area_atuacao(self):
        return self._area_atuacao

    def especialidade(self):
        return "Advogada"

    def protocolo_acolhimento(self, denuncia):
        acao = "pedido urgente de Medida Protetiva" if denuncia.urgencia.value >= 3 else "orientação jurídica preventiva"
        return (f"Orientação jurídica ({self._area_atuacao}) com foco em {acao} "
                f"para a denúncia #{denuncia.id}.")


# --------------------------------------------------------------------------
# Usuária e Ponto de Apoio
# --------------------------------------------------------------------------
class Usuaria:
    """Mulher cadastrada na plataforma (pode optar por anonimato nas denúncias)."""

    _proximo_id = 1

    def __init__(self, nome, cidade, telefone_emergencia, codinome=None):
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")
        self._id = Usuaria._proximo_id
        Usuaria._proximo_id += 1
        self._nome = nome.strip()
        self._cidade = cidade.strip()
        self._telefone_emergencia = telefone_emergencia.strip()
        self._codinome = (codinome or f"Protegida_{self._id:03d}").strip()
        self._denuncias = []

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def cidade(self):
        return self._cidade

    @property
    def codinome(self):
        return self._codinome

    @property
    def denuncias(self):
        return tuple(self._denuncias)

    def identidade_publica(self, anonima=True):
        """Encapsulamento da identidade: oculta nome real se a denúncia for anônima."""
        return f"{self._codinome} (Anônima)" if anonima else self._nome

    def vincular_denuncia(self, denuncia):
        self._denuncias.append(denuncia)

    def __str__(self):
        return f"[Usuária #{self._id}] Codinome: {self._codinome} - {self._cidade}"


class PontoApoio:
    """Local físico seguro (DEAM, Casa da Mulher, CRAS, abrigo parceiro)."""

    _proximo_id = 1

    def __init__(self, nome, tipo, cidade, endereco, telefone, plantao_24h=False):
        if not nome or not nome.strip():
            raise ValueError("O nome do ponto de apoio é obrigatório.")
        self._id = PontoApoio._proximo_id
        PontoApoio._proximo_id += 1
        self._nome = nome.strip()
        self._tipo = tipo.strip()
        self._cidade = cidade.strip()
        self._endereco = endereco.strip()
        self._telefone = telefone.strip()
        self._plantao_24h = bool(plantao_24h)

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def tipo(self):
        return self._tipo

    @property
    def cidade(self):
        return self._cidade

    @property
    def endereco(self):
        return self._endereco

    @property
    def telefone(self):
        return self._telefone

    @property
    def plantao_24h(self):
        return self._plantao_24h

    def __str__(self):
        turno = "24h" if self._plantao_24h else "Horário Comercial"
        return (f"[Ponto de Apoio #{self._id}] {self._nome} ({self._tipo}) - {self._cidade} | "
                f"{self._endereco} | Tel: {self._telefone} [{turno}]")


# --------------------------------------------------------------------------
# RelatoOcorrencia (Composição), Denuncia e Atendimento
# --------------------------------------------------------------------------
class RelatoOcorrencia:
    """Registro de fato/evidência que compõe uma Denúncia."""

    def __init__(self, tipo_violencia, descricao, registrado_em=None):
        if not descricao or not descricao.strip():
            raise ValueError("A descrição do relato não pode ser vazia.")
        self._tipo_violencia = tipo_violencia.strip()
        self._descricao = descricao.strip()
        self._registrado_em = registrado_em or datetime.now()

    @property
    def tipo_violencia(self):
        return self._tipo_violencia

    @property
    def descricao(self):
        return self._descricao

    @property
    def registrado_em(self):
        return self._registrado_em

    def __str__(self):
        data = self._registrado_em.strftime("%d/%m/%Y %H:%M")
        return f"[{self._tipo_violencia} em {data}] {self._descricao}"


class Denuncia:
    """Denúncia registrada por uma usuária. Compõe uma lista de RelatoOcorrencia."""

    _proximo_id = 1

    def __init__(self, usuaria, cidade, urgencia, relatos, anonima=True, criada_em=None):
        if not relatos:
            raise ValueError("A denúncia precisa conter pelo menos um relato de ocorrência.")
        self._id = Denuncia._proximo_id
        Denuncia._proximo_id += 1
        self._usuaria = usuaria
        self._cidade = cidade.strip()
        self._urgencia = urgencia
        self._anonima = bool(anonima)
        self._relatos = list(relatos)  # composição: relatos pertencem à denúncia
        self._criada_em = criada_em or datetime.now()
        self._status = StatusDenuncia.ABERTA
        self._atendimentos = []
        self._ponto_encaminhado = None

    @property
    def id(self):
        return self._id

    @property
    def usuaria(self):
        return self._usuaria

    @property
    def cidade(self):
        return self._cidade

    @property
    def urgencia(self):
        return self._urgencia

    @property
    def anonima(self):
        return self._anonima

    @property
    def relatos(self):
        return tuple(self._relatos)  # cópia imutável protege encapsulamento

    @property
    def status(self):
        return self._status

    @property
    def atendimentos(self):
        return tuple(self._atendimentos)

    @property
    def ponto_encaminhado(self):
        return self._ponto_encaminhado

    def adicionar_relato(self, tipo_violencia, descricao):
        if self._status == StatusDenuncia.ENCERRADA:
            raise ValueError("Não é possível adicionar relatos a uma denúncia encerrada.")
        relato = RelatoOcorrencia(tipo_violencia, descricao)
        self._relatos.append(relato)
        return relato

    def iniciar_atendimento(self, profissional):
        if self._status == StatusDenuncia.ENCERRADA:
            raise ValueError(f"Denúncia #{self._id} já está encerrada.")
        if not profissional.disponivel:
            raise ValueError(f"Profissional {profissional.nome} não está disponível no momento.")
        atendimento = Atendimento(self, profissional)
        self._atendimentos.append(atendimento)
        profissional.registrar_atendimento(atendimento)
        self._status = StatusDenuncia.EM_ACOLHIMENTO
        return atendimento

    def encaminhar_ponto_apoio(self, ponto_apoio):
        if self._status == StatusDenuncia.ENCERRADA:
            raise ValueError(f"Denúncia #{self._id} já está encerrada.")
        self._ponto_encaminhado = ponto_apoio
        self._status = StatusDenuncia.ENCAMINHADA

    def encerrar(self):
        self._status = StatusDenuncia.ENCERRADA

    def __str__(self):
        identidade = self._usuaria.identidade_publica(self._anonima)
        resumo_relatos = "; ".join(str(r) for r in self._relatos)
        ponto = f" | Ponto: {self._ponto_encaminhado.nome}" if self._ponto_encaminhado else ""
        return (f"Denúncia #{self._id} | Solicitante: {identidade} | {self._cidade} | "
                f"Urgência: {self._urgencia.name} | Status: {self._status.value}{ponto}\n"
                f"      Relatos: {resumo_relatos}")


class Atendimento:
    """Vínculo de acolhimento entre uma Denúncia e uma ProfissionalVoluntaria."""

    _proximo_id = 1

    def __init__(self, denuncia, profissional, iniciado_em=None):
        self._id = Atendimento._proximo_id
        Atendimento._proximo_id += 1
        self._denuncia = denuncia
        self._profissional = profissional
        self._iniciado_em = iniciado_em or datetime.now()
        # Polimorfismo em ação: protocolo muda se for Psicóloga ou Advogada
        self._protocolo_aplicado = profissional.protocolo_acolhimento(denuncia)
        self._concluido = False

    @property
    def id(self):
        return self._id

    @property
    def denuncia(self):
        return self._denuncia

    @property
    def profissional(self):
        return self._profissional

    @property
    def protocolo_aplicado(self):
        return self._protocolo_aplicado

    @property
    def concluido(self):
        return self._concluido

    def concluir(self):
        self._concluido = True

    def __str__(self):
        estado = "Concluído" if self._concluido else "Em andamento"
        return (f"Atendimento #{self._id} ({self._profissional.especialidade()}: "
                f"{self._profissional.nome}) [{estado}]\n      Protocolo: {self._protocolo_aplicado}")
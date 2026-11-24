"""Modelos (classes de domínio) do App Rota Acessível - ODS 10 (Redução das Desigualdades).

Pilares de POO usados neste módulo:
  * Encapsulamento: atributos privados (_x) expostos por @property; AvaliacaoAcessibilidade
    é um objeto de valor imutável (@dataclass(frozen=True)); coleções protegidas.
  * Herança: CidadaoColaborador e GestorPublico herdam de Usuario; BarreiraRampa,
    BarreiraCalcada, BarreiraPisoTatil e BarreiraElevador herdam de BarreiraArquitetonica.
  * Polimorfismo: gravidade_base(), pontos_recompensa() e recomendacao_tecnica()
    mudam em cada tipo de barreira; pode_resolver_ocorrencia() e resumo() mudam por usuário.
  * Composição: LocalPublico compõe suas AvaliacaoAcessibilidade; OcorrenciaBarreira
    compõe sua BarreiraArquitetonica.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StatusOcorrencia(Enum):
    ABERTA = "Aberta"
    EM_ANALISE = "Em Análise Técnica"
    RESOLVIDA = "Resolvida"


@dataclass(frozen=True)
class AvaliacaoAcessibilidade:
    """Objeto de valor imutável com a nota e diagnóstico de um espaço público."""
    autor_nome: str
    nota: int
    comentario: str
    possui_rampa: bool = True
    possui_piso_tatil: bool = False

    def __post_init__(self):
        if not 1 <= self.nota <= 5:
            raise ValueError("A nota de acessibilidade deve ser de 1 a 5.")

    def __str__(self):
        rampa = "com rampa" if self.possui_rampa else "sem rampa"
        tatil = "com piso tátil" if self.possui_piso_tatil else "sem piso tátil"
        return f"Nota {self.nota}/5 ({rampa}, {tatil}) por {self.autor_nome}: {self.comentario}"


# --------------------------------------------------------------------------
# Barreiras Arquitetônicas (herança + polimorfismo)
# --------------------------------------------------------------------------
class BarreiraArquitetonica(ABC):
    """Classe base abstrata para obstáculos urbanos denunciados no mapa."""

    def __init__(self, descricao):
        if not descricao or not descricao.strip():
            raise ValueError("A barreira precisa de uma descrição.")
        self._descricao = descricao.strip()

    @property
    def descricao(self):
        return self._descricao

    @abstractmethod
    def categoria(self):
        """Nome da categoria da barreira."""

    @abstractmethod
    def gravidade_base(self):
        """Nível de impacto na locomoção: 1 (Baixa), 2 (Média), 3 (Alta), 4 (Bloqueio Total)."""

    @abstractmethod
    def pontos_recompensa(self):
        """Pontos de engajamento cívico concedidos pela denúncia (polimorfismo)."""

    @abstractmethod
    def recomendacao_tecnica(self):
        """Diretriz normativa (ABNT NBR 9050) para correção pela prefeitura."""

    def __str__(self):
        return (f"{self.categoria()}: {self._descricao} "
                f"(Gravidade {self.gravidade_base()}/4 | +{self.pontos_recompensa()} pts)")


class BarreiraRampa(BarreiraArquitetonica):
    """Rampa inexistente, quebrada ou com inclinação fora da norma."""

    def __init__(self, descricao, inexistente=False):
        super().__init__(descricao)
        self._inexistente = bool(inexistente)

    @property
    def inexistente(self):
        return self._inexistente

    def categoria(self):
        return "Rampa de Acesso"

    def gravidade_base(self):
        return 4 if self._inexistente else 3

    def pontos_recompensa(self):
        return 40 if self._inexistente else 30

    def recomendacao_tecnica(self):
        return "Reconstruir rampa com inclinação máxima de 8,33% conforme NBR 9050."


class BarreiraCalcada(BarreiraArquitetonica):
    """Calçada irregular, buracos, degraus ou obstrução por entulho/postes."""

    def __init__(self, descricao, bloqueia_passagem=False):
        super().__init__(descricao)
        self._bloqueia_passagem = bool(bloqueia_passagem)

    def categoria(self):
        return "Calçada Irregular"

    def gravidade_base(self):
        return 3 if self._bloqueia_passagem else 2

    def pontos_recompensa(self):
        return 25 if self._bloqueia_passagem else 15

    def recomendacao_tecnica(self):
        return "Nivelar pavimento e garantir faixa livre mínima de 1,20m sem degraus."


class BarreiraPisoTatil(BarreiraArquitetonica):
    """Ausência ou desgaste de piso tátil direcional e de alerta."""

    def categoria(self):
        return "Piso Tátil"

    def gravidade_base(self):
        return 2

    def pontos_recompensa(self):
        return 20

    def recomendacao_tecnica(self):
        return "Instalar sinalização tátil direcional e de alerta em travessias e acessos."


class BarreiraElevador(BarreiraArquitetonica):
    """Elevador ou plataforma elevatória pública fora de operação."""

    def categoria(self):
        return "Elevador / Plataforma"

    def gravidade_base(self):
        return 4

    def pontos_recompensa(self):
        return 50

    def recomendacao_tecnica(self):
        return "Manutenção corretiva emergencial e liberação de rota alternativa assistida."


# --------------------------------------------------------------------------
# Usuários (herança + polimorfismo)
# --------------------------------------------------------------------------
class Usuario(ABC):
    """Classe base abstrata dos usuários do App Rota Acessível."""

    _proximo_id = 1

    def __init__(self, nome, email, cidade):
        if not nome or not nome.strip():
            raise ValueError("O nome é obrigatório.")
        if "@" not in email:
            raise ValueError("E-mail inválido.")
        self._id = Usuario._proximo_id
        Usuario._proximo_id += 1
        self._nome = nome.strip()
        self._email = email.strip()
        self._cidade = cidade.strip()

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

    @abstractmethod
    def pode_resolver_ocorrencia(self):
        """Indica polimorficamente se o usuário tem perfil técnico para encerrar barreiras."""

    @abstractmethod
    def resumo(self):
        """Apresentação específica de cada perfil."""

    def __str__(self):
        return self.resumo()


class CidadaoColaborador(Usuario):
    """Cadeirante, pessoa com mobilidade reduzida ou apoiador que mapeia a cidade."""

    NIVEIS = [(120, "Ouro"), (50, "Prata"), (0, "Bronze")]

    def __init__(self, nome, email, cidade, perfil_mobilidade="Cadeirante"):
        super().__init__(nome, email, cidade)
        self._perfil_mobilidade = perfil_mobilidade.strip()
        self._pontos = 0
        self._ocorrencias = []

    @property
    def perfil_mobilidade(self):
        return self._perfil_mobilidade

    @property
    def pontos(self):
        return self._pontos

    @property
    def ocorrencias(self):
        return tuple(self._ocorrencias)

    def creditar_pontos(self, valor):
        if valor > 0:
            self._pontos += valor

    def nivel(self):
        return next(nome for minimo, nome in self.NIVEIS if self._pontos >= minimo)

    def registrar_ocorrencia(self, ocorrencia):
        self._ocorrencias.append(ocorrencia)

    def pode_resolver_ocorrencia(self):
        return False

    def resumo(self):
        return (f"[Cidadão #{self._id}] {self._nome} ({self._perfil_mobilidade}) - {self._cidade} | "
                f"nível {self.nivel()} | {self._pontos} pts")


class GestorPublico(Usuario):
    """Agente público responsável por vistoriar e resolver barreiras urbanas."""

    def __init__(self, nome, email, cidade, orgao, matricula):
        super().__init__(nome, email, cidade)
        if not orgao or not orgao.strip():
            raise ValueError("O órgão público é obrigatório.")
        self._orgao = orgao.strip()
        self._matricula = matricula.strip()
        self._resolvidas = 0

    @property
    def orgao(self):
        return self._orgao

    @property
    def matricula(self):
        return self._matricula

    @property
    def resolvidas(self):
        return self._resolvidas

    def registrar_resolucao(self):
        self._resolvidas += 1

    def pode_resolver_ocorrencia(self):
        return True

    def resumo(self):
        return (f"[Gestor #{self._id}] {self._nome} ({self._orgao} - Mat. {self._matricula}) - "
                f"{self._cidade} | {self._resolvidas} barreira(s) resolvida(s)")


# --------------------------------------------------------------------------
# LocalPublico e OcorrenciaBarreira
# --------------------------------------------------------------------------
class LocalPublico:
    """Espaço público avaliado no mapa colaborativo. Compõe suas avaliações."""

    _proximo_id = 1

    def __init__(self, nome, categoria, cidade, endereco):
        if not nome or not nome.strip():
            raise ValueError("O nome do local é obrigatório.")
        self._id = LocalPublico._proximo_id
        LocalPublico._proximo_id += 1
        self._nome = nome.strip()
        self._categoria = categoria.strip()
        self._cidade = cidade.strip()
        self._endereco = endereco.strip()
        self._avaliacoes = []  # composição: avaliações pertencem ao local
        self._ocorrencias = []

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def categoria(self):
        return self._categoria

    @property
    def cidade(self):
        return self._cidade

    @property
    def endereco(self):
        return self._endereco

    @property
    def avaliacoes(self):
        return tuple(self._avaliacoes)

    @property
    def ocorrencias(self):
        return tuple(self._ocorrencias)

    def avaliar(self, usuario, nota, comentario, possui_rampa=True, possui_piso_tatil=False):
        av = AvaliacaoAcessibilidade(usuario.nome, nota, comentario, possui_rampa, possui_piso_tatil)
        self._avaliacoes.append(av)
        if isinstance(usuario, CidadaoColaborador):
            usuario.creditar_pontos(10)
        return av

    def vincular_ocorrencia(self, ocorrencia):
        self._ocorrencias.append(ocorrencia)

    def media_acessibilidade(self):
        if not self._avaliacoes:
            return 0.0
        return sum(a.nota for a in self._avaliacoes) / len(self._avaliacoes)

    def barreiras_ativas(self):
        return sum(1 for o in self._ocorrencias if o.status != StatusOcorrencia.RESOLVIDA)

    def __str__(self):
        media = f"{self.media_acessibilidade():.1f}/5" if self._avaliacoes else "Sem avaliações"
        return (f"[Local #{self._id}] {self._nome} ({self._categoria}) - {self._cidade} | "
                f"Acessibilidade: {media} | Barreiras ativas: {self.barreiras_ativas()}")


class OcorrenciaBarreira:
    """Denúncia de barreira arquitetônica em um LocalPublico. Compõe a barreira."""

    _proximo_id = 1

    def __init__(self, local: LocalPublico, autor: Usuario, barreira: BarreiraArquitetonica, data=None):
        self._id = OcorrenciaBarreira._proximo_id
        OcorrenciaBarreira._proximo_id += 1
        self._local = local
        self._autor = autor
        self._barreira = barreira  # composição
        self._data = data or datetime.now()
        self._status = StatusOcorrencia.ABERTA
        self._confirmacoes = 1
        self._resolvida_por = None
        local.vincular_ocorrencia(self)
        if isinstance(autor, CidadaoColaborador):
            autor.creditar_pontos(barreira.pontos_recompensa())  # polimorfismo
            autor.registrar_ocorrencia(self)

    @property
    def id(self):
        return self._id

    @property
    def local(self):
        return self._local

    @property
    def autor(self):
        return self._autor

    @property
    def barreira(self):
        return self._barreira

    @property
    def status(self):
        return self._status

    @property
    def confirmacoes(self):
        return self._confirmacoes

    def confirmar_existencia(self, cidadao):
        if self._status == StatusOcorrencia.RESOLVIDA:
            raise ValueError(f"Ocorrência #{self._id} já foi resolvida.")
        self._confirmacoes += 1
        if isinstance(cidadao, CidadaoColaborador):
            cidadao.creditar_pontos(5)

    def iniciar_analise(self, gestor):
        if not gestor.pode_resolver_ocorrencia():
            raise PermissionError("Apenas gestores públicos podem colocar ocorrências em análise.")
        self._status = StatusOcorrencia.EM_ANALISE

    def marcar_resolvida(self, gestor):
        if not gestor.pode_resolver_ocorrencia():
            raise PermissionError("Apenas gestores públicos podem resolver ocorrências.")
        if self._status == StatusOcorrencia.RESOLVIDA:
            raise ValueError(f"Ocorrência #{self._id} já está resolvida.")
        self._status = StatusOcorrencia.RESOLVIDA
        self._resolvida_por = gestor
        gestor.registrar_resolucao()

    def __str__(self):
        resp = f" | Resolvida por: {self._resolvida_por.nome}" if self._resolvida_por else ""
        return (f"Ocorrência #{self._id} | {self._local.nome} ({self._local.cidade}) | "
                f"Confirmações: {self._confirmacoes} | Status: {self._status.value}{resp}\n"
                f"      {self._barreira}\n"
                f"      Ação recomendada: {self._barreira.recomendacao_tecnica()}")
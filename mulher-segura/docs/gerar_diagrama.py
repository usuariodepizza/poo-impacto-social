"""Gera o diagrama de classes UML da Rede Mulher Segura (requer Graphviz: `dot`)."""
import subprocess


def classe(nome, attrs, metodos, abstrata=False, estereotipo=None, cor="#FFFFFF"):
    def linhas(itens):
        return "".join(f'<TR><TD ALIGN="LEFT" BALIGN="LEFT">{i}</TD></TR>' for i in itens) or '<TR><TD> </TD></TR>'
    titulo = f"<I>{nome}</I>" if abstrata else nome
    est = ""
    if abstrata:
        est = '<TR><TD><FONT POINT-SIZE="9">«abstract»</FONT></TD></TR>'
    if estereotipo:
        est = f'<TR><TD><FONT POINT-SIZE="9">«{estereotipo}»</FONT></TD></TR>'
    return (f'{nome} [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="3" BGCOLOR="{cor}">'
            f'{est}<TR><TD><B>{titulo}</B></TD></TR>'
            f'<TR><TD><TABLE BORDER="0" CELLSPACING="0" CELLPADDING="1">{linhas(attrs)}</TABLE></TD></TR>'
            f'<TR><TD><TABLE BORDER="0" CELLSPACING="0" CELLPADDING="1">{linhas(metodos)}</TABLE></TD></TR>'
            f'</TABLE>>];')


c = []
c.append(classe("ProfissionalVoluntaria",
    ["-id: int", "-nome: str", "-email: str", "-cidade: str", "-registro_profissional: str", "-disponivel: bool"],
    ["+especialidade(): str  {abstract}", "+protocolo_acolhimento(d): str  {abstract}", "+resumo(): str"],
    abstrata=True, cor="#EAF2FB"))
c.append(classe("PsicologaVoluntaria",
    ["-abordagem: str"],
    ["+especialidade(): str", "+protocolo_acolhimento(d): str"], cor="#EAF2FB"))
c.append(classe("AdvogadaVoluntaria",
    ["-area_atuacao: str"],
    ["+especialidade(): str", "+protocolo_acolhimento(d): str"], cor="#EAF2FB"))
c.append(classe("Usuaria",
    ["-id: int", "-nome: str", "-cidade: str", "-telefone_emergencia: str", "-codinome: str"],
    ["+identidade_publica(anonima): str", "+vincular_denuncia(d): void"], cor="#FEF5E7"))
c.append(classe("PontoApoio",
    ["-id: int", "-nome: str", "-tipo: str", "-cidade: str", "-endereco: str", "-telefone: str", "-plantao_24h: bool"],
    ["+__str__(): str"], cor="#FEF5E7"))
c.append(classe("Denuncia",
    ["-id: int", "-cidade: str", "-urgencia: NivelUrgencia", "-anonima: bool", "-relatos: list[RelatoOcorrencia]", "-status: StatusDenuncia"],
    ["+adicionar_relato(tipo, desc): RelatoOcorrencia", "+iniciar_atendimento(prof): Atendimento", "+encaminhar_ponto_apoio(pt): void", "+encerrar(): void"],
    cor="#EAF7EA"))
c.append(classe("RelatoOcorrencia",
    ["-tipo_violencia: str", "-descricao: str", "-registrado_em: datetime"],
    ["+__str__(): str"], cor="#EAF7EA"))
c.append(classe("Atendimento",
    ["-id: int", "-iniciado_em: datetime", "-protocolo_aplicado: str", "-concluido: bool"],
    ["+concluir(): void"], cor="#EAF7EA"))
c.append(classe("StatusDenuncia",
    ["ABERTA", "EM_ACOLHIMENTO", "ENCAMINHADA", "ENCERRADA"], [], estereotipo="enumeration", cor="#F4F4F4"))
c.append(classe("NivelUrgencia",
    ["BAIXA = 1", "MEDIA = 2", "ALTA = 3", "EMERGENCIA = 4"], [], estereotipo="enumeration", cor="#F4F4F4"))
c.append(classe("Plataforma",
    ["-nome: str", "-usuarias: dict", "-profissionais: dict", "-pontos_apoio: dict", "-denuncias: dict"],
    ["+registrar_denuncia(...): Denuncia", "+listar_denuncias_prioritarias(): list[Denuncia]",
     "+conectar_voluntaria(d_id, p_id): Atendimento", "+encaminhar_para_ponto(d_id, pt_id): PontoApoio",
     "+gerar_relatorio(): RelatorioImpacto"], cor="#F3EAF9"))
c.append(classe("RelatorioImpacto",
    ["-total_denuncias: int", "-anonimas: int", "-emergencias: int", "-total_atendimentos: int"],
    ["+gerar_texto(): str"], cor="#F3EAF9"))

dot = """digraph G {
  graph [rankdir=BT, splines=ortho, nodesep=0.3, ranksep=0.45, dpi=170, bgcolor=white, pad=0.3,
         label=<<B>Diagrama de Classes UML - Solução 1: Rede Mulher Segura (ODS 5)</B>>, labelloc=t, fontsize=20, fontname="Helvetica"];
  node [shape=plain, fontname="Helvetica", fontsize=11];
  edge [fontname="Helvetica", fontsize=10];
""" + "\n".join(c) + """
  // Herança
  PsicologaVoluntaria -> ProfissionalVoluntaria [arrowhead=empty];
  AdvogadaVoluntaria -> ProfissionalVoluntaria [arrowhead=empty];

  // Composição
  RelatoOcorrencia -> Denuncia [arrowhead=diamond, headlabel="1", taillabel="1..*", labeldistance=2.2, label=" composta de "];

  // Associações
  Denuncia -> Usuaria [arrowhead=none, headlabel="1", taillabel="0..*", labeldistance=2.2, label=" registrada por "];
  Denuncia -> PontoApoio [arrowhead=none, headlabel="0..1", taillabel="0..*", labeldistance=2.2, label=" encaminhada para "];
  Atendimento -> Denuncia [arrowhead=none, headlabel="1", taillabel="0..*", labeldistance=2.2, label=" referente a "];
  Atendimento -> ProfissionalVoluntaria [arrowhead=none, headlabel="1", taillabel="0..*", labeldistance=2.2, label=" realizado por "];
  Denuncia -> StatusDenuncia [arrowhead=vee, style=dashed, label=" status "];
  Denuncia -> NivelUrgencia [arrowhead=vee, style=dashed, label=" urgencia "];

  // Agregação
  Usuaria -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.2];
  ProfissionalVoluntaria -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.2];
  PontoApoio -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.2];
  Denuncia -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.2];

  // Dependência
  Plataforma -> RelatorioImpacto [arrowhead=vee, style=dashed, label=" «cria» "];
}"""
open("diagrama_classes.dot", "w", encoding="utf-8").write(dot)
subprocess.run(["dot", "-Tpng", "diagrama_classes.dot", "-o", "diagrama_classes.png"], check=True)
subprocess.run(["dot", "-Tpdf", "diagrama_classes.dot", "-o", "diagrama_classes.pdf"], check=True)
print("ok")
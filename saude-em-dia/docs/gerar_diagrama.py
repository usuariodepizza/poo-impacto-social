"""Gera o diagrama de classes UML do App Saúde em Dia (requer Graphviz: `dot`)."""
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
c.append(classe("Pessoa",
    ["-id: int", "-nome: str", "-telefone: str", "-cidade: str"],
    ["+resumo(): str  {abstract}", "+__str__(): str"], abstrata=True, cor="#EAF2FB"))
c.append(classe("Idoso",
    ["-idade: int", "-condicoes_saude: str", "-compromissos: list[CompromissoSaude]"],
    ["+vincular_familiar(f): void", "+vincular_cuidador(c): void", "+taxa_adesao(): float", "+resumo(): str"], cor="#EAF2FB"))
c.append(classe("Cuidador",
    ["-turno: str", "-registro_profissional: str", "-confirmacoes_realizadas: int"],
    ["+registrar_confirmacao(): void", "+resumo(): str"], cor="#EAF2FB"))
c.append(classe("FamiliarResponsavel",
    ["-parentesco: str", "-alertas_recebidos: list[AlertaFamiliar]"],
    ["+receber_alerta(alerta): void", "+resumo(): str"], cor="#EAF2FB"))
c.append(classe("CompromissoSaude",
    ["-id: int", "-titulo: str", "-horario_previsto: datetime", "-status: StatusCompromisso", "-alerta_gerado: AlertaFamiliar"],
    ["+tolerancia_minutos(): int  {abstract}", "+instrucoes_cuidado(): str  {abstract}",
     "+confirmar(resp): void", "+verificar_atraso(agora): AlertaFamiliar"], abstrata=True, cor="#FEF5E7"))
c.append(classe("LembreteMedicacao",
    ["-dosagem: str", "-via_administracao: str"],
    ["+tolerancia_minutos(): int", "+instrucoes_cuidado(): str"], cor="#FEF5E7"))
c.append(classe("LembreteVacina",
    ["-dose: str", "-posto_saude: str"],
    ["+tolerancia_minutos(): int", "+instrucoes_cuidado(): str"], cor="#FEF5E7"))
c.append(classe("LembreteConsulta",
    ["-medico: str", "-local_atendimento: str"],
    ["+tolerancia_minutos(): int", "+instrucoes_cuidado(): str"], cor="#FEF5E7"))
c.append(classe("AlertaFamiliar",
    ["-destinatario_nome: str", "-destinatario_telefone: str", "-mensagem: str", "-enviado_em: datetime"],
    [], estereotipo="value object", cor="#EAF7EA"))
c.append(classe("StatusCompromisso",
    ["PENDENTE", "CONFIRMADO", "ATRASADO_ALERTADO", "CANCELADO"], [], estereotipo="enumeration", cor="#F4F4F4"))
c.append(classe("Plataforma",
    ["-nome: str", "-pessoas: dict", "-compromissos: dict"],
    ["+vincular_rede_apoio(i, f, c): void", "+agendar_compromisso(c): CompromissoSaude",
     "+confirmar_compromisso(c_id, r_id): CompromissoSaude", "+verificar_alertas_atraso(): list[AlertaFamiliar]",
     "+gerar_relatorio(): RelatorioImpacto"], cor="#F3EAF9"))
c.append(classe("RelatorioImpacto",
    ["-total_idosos: int", "-total_compromissos: int", "-confirmados: int", "-alertas_enviados: int"],
    ["+gerar_texto(): str"], cor="#F3EAF9"))

dot = """digraph G {
  graph [rankdir=BT, splines=ortho, nodesep=0.3, ranksep=0.45, dpi=170, bgcolor=white, pad=0.3,
         label=<<B>Diagrama de Classes UML - Solução 3: App Saúde em Dia (ODS 3)</B>>, labelloc=t, fontsize=20, fontname="Helvetica"];
  node [shape=plain, fontname="Helvetica", fontsize=11];
  edge [fontname="Helvetica", fontsize=10];
""" + "\n".join(c) + """
  // Herança
  Idoso -> Pessoa [arrowhead=empty];
  Cuidador -> Pessoa [arrowhead=empty];
  FamiliarResponsavel -> Pessoa [arrowhead=empty];
  LembreteMedicacao -> CompromissoSaude [arrowhead=empty];
  LembreteVacina -> CompromissoSaude [arrowhead=empty];
  LembreteConsulta -> CompromissoSaude [arrowhead=empty];

  // Composição
  CompromissoSaude -> Idoso [arrowhead=diamond, headlabel="1", taillabel="0..*", labeldistance=2.2, label=" agenda de "];
  AlertaFamiliar -> CompromissoSaude [arrowhead=diamond, headlabel="1", taillabel="0..1", labeldistance=2.2, label=" gera "];

  // Associações
  Idoso -> FamiliarResponsavel [arrowhead=none, headlabel="0..1", taillabel="0..*", labeldistance=2.2, label=" acompanhado por "];
  Idoso -> Cuidador [arrowhead=none, headlabel="0..1", taillabel="0..*", labeldistance=2.2, label=" assistido por "];
  CompromissoSaude -> StatusCompromisso [arrowhead=vee, style=dashed, label=" status "];

  // Agregação
  Pessoa -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.2];
  CompromissoSaude -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.2];

  // Dependência
  Plataforma -> RelatorioImpacto [arrowhead=vee, style=dashed, label=" «cria» "];
}"""
open("diagrama_classes.dot", "w", encoding="utf-8").write(dot)
subprocess.run(["dot", "-Tpng", "diagrama_classes.dot", "-o", "diagrama_classes.png"], check=True)
subprocess.run(["dot", "-Tpdf", "diagrama_classes.dot", "-o", "diagrama_classes.pdf"], check=True)
print("ok")
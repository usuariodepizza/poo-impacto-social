"""Gera o diagrama de classes UML do App Rota Acessível (requer Graphviz: `dot`)."""
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


AZ, LA, VE, RO, CI = "#EAF2FB", "#FEF5E7", "#EAF7EA", "#F3EAF9", "#F4F4F4"
c = [
    classe("Usuario", ["-id: int", "-nome: str", "-email: str", "-cidade: str"],
           ["+pode_resolver_ocorrencia(): bool  {abstract}", "+resumo(): str  {abstract}"], abstrata=True, cor=AZ),
    classe("CidadaoColaborador", ["-perfil_mobilidade: str", "-pontos: int", "-ocorrencias: list[OcorrenciaBarreira]"],
           ["+creditar_pontos(v): void", "+nivel(): str", "+pode_resolver_ocorrencia(): bool", "+resumo(): str"], cor=AZ),
    classe("GestorPublico", ["-orgao: str", "-matricula: str", "-resolvidas: int"],
           ["+registrar_resolucao(): void", "+pode_resolver_ocorrencia(): bool", "+resumo(): str"], cor=AZ),
    classe("BarreiraArquitetonica", ["-descricao: str"],
           ["+categoria(): str  {abstract}", "+gravidade_base(): int  {abstract}",
            "+pontos_recompensa(): int  {abstract}", "+recomendacao_tecnica(): str  {abstract}"], abstrata=True, cor=LA),
    classe("BarreiraRampa", ["-inexistente: bool"],
           ["+categoria(): str", "+gravidade_base(): int", "+pontos_recompensa(): int", "+recomendacao_tecnica(): str"], cor=LA),
    classe("BarreiraCalcada", ["-bloqueia_passagem: bool"],
           ["+categoria(): str", "+gravidade_base(): int", "+pontos_recompensa(): int", "+recomendacao_tecnica(): str"], cor=LA),
    classe("BarreiraPisoTatil", [],
           ["+categoria(): str", "+gravidade_base(): int", "+pontos_recompensa(): int", "+recomendacao_tecnica(): str"], cor=LA),
    classe("BarreiraElevador", [],
           ["+categoria(): str", "+gravidade_base(): int", "+pontos_recompensa(): int", "+recomendacao_tecnica(): str"], cor=LA),
    classe("LocalPublico", ["-id: int", "-nome: str", "-categoria: str", "-cidade: str", "-endereco: str", "-avaliacoes: list[AvaliacaoAcessibilidade]"],
           ["+avaliar(...): AvaliacaoAcessibilidade", "+media_acessibilidade(): float", "+barreiras_ativas(): int"], cor=VE),
    classe("AvaliacaoAcessibilidade", ["-autor_nome: str", "-nota: int", "-comentario: str", "-possui_rampa: bool", "-possui_piso_tatil: bool"],
           [], estereotipo="value object", cor=CI),
    classe("OcorrenciaBarreira", ["-id: int", "-status: StatusOcorrencia", "-confirmacoes: int"],
           ["+confirmar_existencia(c): void", "+iniciar_analise(g): void", "+marcar_resolvida(g): void"], cor=VE),
    classe("StatusOcorrencia", ["ABERTA", "EM_ANALISE", "RESOLVIDA"], [], estereotipo="enumeration", cor=CI),
    classe("Plataforma", ["-nome: str", "-usuarios: dict", "-locais: dict", "-ocorrencias: dict"],
           ["+avaliar_local(...): AvaliacaoAcessibilidade", "+denunciar_barreira(l_id, u_id, b): OcorrenciaBarreira",
            "+listar_ocorrencias_prioritarias(): list[OcorrenciaBarreira]", "+resolver_ocorrencia(o_id, g_id): OcorrenciaBarreira",
            "+gerar_relatorio(): RelatorioImpacto"], cor=RO),
    classe("RelatorioImpacto", ["-locais: list", "-ocorrencias: list", "-usuarios: list"],
           ["+gerar_texto(): str"], cor=RO),
]

dot = """digraph G {
  graph [rankdir=BT, splines=polyline, nodesep=0.3, ranksep=0.45, dpi=150, bgcolor=white, pad=0.3,
         label=<<B>Diagrama de Classes UML - Solução 2: App Rota Acessível (ODS 10)</B>>, labelloc=t, fontsize=20, fontname="Helvetica"];
  node [shape=plain, fontname="Helvetica", fontsize=11];
  edge [fontname="Helvetica", fontsize=10];
""" + "\n".join(c) + """
  // Herança
  CidadaoColaborador -> Usuario [arrowhead=empty];
  GestorPublico -> Usuario [arrowhead=empty];
  BarreiraRampa -> BarreiraArquitetonica [arrowhead=empty];
  BarreiraCalcada -> BarreiraArquitetonica [arrowhead=empty];
  BarreiraPisoTatil -> BarreiraArquitetonica [arrowhead=empty];
  BarreiraElevador -> BarreiraArquitetonica [arrowhead=empty];

  // Composição
  AvaliacaoAcessibilidade -> LocalPublico [arrowhead=diamond, headlabel="1", taillabel="0..*", labeldistance=2.4, label=" composta de "];
  BarreiraArquitetonica -> OcorrenciaBarreira [arrowhead=diamond, headlabel="1", taillabel="1", labeldistance=2.4, label=" descreve "];

  // Associações
  OcorrenciaBarreira -> LocalPublico [arrowhead=none, headlabel="1", taillabel="0..*", labeldistance=2.4, label=" registrada em "];
  OcorrenciaBarreira -> Usuario [arrowhead=none, headlabel="1", taillabel="0..*", labeldistance=2.4, label=" reportada por "];
  OcorrenciaBarreira -> StatusOcorrencia [arrowhead=vee, style=dashed, label=" status "];

  // Agregação
  Usuario -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.4];
  LocalPublico -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.4];
  OcorrenciaBarreira -> Plataforma [arrowhead=odiamond, headlabel="1", taillabel="0..*", labeldistance=2.4];

  // Dependência
  Plataforma -> RelatorioImpacto [arrowhead=vee, style=dashed, label=" «cria» "];
}"""
open("diagrama_classes.dot", "w", encoding="utf-8").write(dot)
subprocess.run(["dot", "-Tpng", "diagrama_classes.dot", "-o", "diagrama_classes.png"], check=True)
subprocess.run(["dot", "-Tpdf", "diagrama_classes.dot", "-o", "diagrama_classes.pdf"], check=True)
print("ok")
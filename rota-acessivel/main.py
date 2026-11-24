"""App Rota Acessível - protótipo de console (ODS 10: Redução das Desigualdades).

Uso:
    python main.py          -> menu interativo
    python main.py --demo   -> demonstração automática de todo o fluxo
"""
import sys

from rota_acessivel import (BarreiraCalcada, BarreiraElevador, BarreiraPisoTatil,
                            BarreiraRampa, CidadaoColaborador, GestorPublico,
                            LocalPublico, Plataforma)


def carregar_exemplo(p):
    c1 = p.registrar_usuario(CidadaoColaborador("Lucas Martins", "lucas@email.com", "Vitória", "Cadeirante"))
    c2 = p.registrar_usuario(CidadaoColaborador("Fernanda Souza", "fernanda@email.com", "Serra", "Mobilidade Reduzida"))
    g1 = p.registrar_usuario(GestorPublico("Eng. Carlos Mendes", "carlos.obras@vitoria.es.gov.br",
                                           "Vitória", "Secretaria de Obras", "PMV-9042"))

    l1 = p.registrar_local(LocalPublico("Parque Moscoso", "Parque Urbano", "Vitória", "Av. Cleto Nunes, Centro"))
    l2 = p.registrar_local(LocalPublico("Terminal de Laranjeiras", "Transporte Público", "Serra", "Av. Civit, Laranjeiras"))
    l3 = p.registrar_local(LocalPublico("UBS Praia do Suá", "Unidade de Saúde", "Vitória", "Rua Almirante Tamandaré, 80"))

    p.avaliar_local(l1.id, c1.id, 5, "Rampas novas em todas as entradas e banheiros adaptados.", True, True)
    p.avaliar_local(l2.id, c2.id, 2, "Elevador parado e piso tátil interrompido na plataforma B.", True, False)
    p.avaliar_local(l3.id, c1.id, 4, "Bom acesso interno, mas calçada externa precisa de nivelamento.", True, True)

    o1 = p.denunciar_barreira(l2.id, c1.id, BarreiraElevador("Elevador da plataforma B interditado há 5 dias"))
    o2 = p.denunciar_barreira(l3.id, c2.id, BarreiraCalcada("Buracos na faixa de travessia em frente à entrada", bloqueia_passagem=True))
    o3 = p.denunciar_barreira(l2.id, c1.id, BarreiraPisoTatil("Piso tátil arrancado no acesso à bilheteria"))
    return c1, c2, g1, l1, l2, l3, o1, o2, o3


def demo():
    p = Plataforma()
    print("\n>>> 1) Cadastro de cidadãos, gestores e locais públicos")
    c1, c2, g1, _, _, _, o1, o2, _ = carregar_exemplo(p)
    for u in p.listar_usuarios():
        print("  ", u)
    for loc in p.listar_locais():
        print("  ", loc)

    print("\n>>> 2) Ocorrências ordenadas por gravidade (Polimorfismo nas barreiras)")
    for oc in p.listar_ocorrencias_prioritarias():
        print("  ", oc)

    print("\n>>> 3) Regras de negócio protegendo o sistema")
    try:
        o1.marcar_resolvida(c1)  # cidadão não pode resolver ocorrência oficial
    except PermissionError as e:
        print("   Permissão negada (esperado):", e)

    print("\n>>> 4) Confirmação comunitária e resolução pelo Gestor Público")
    o1.confirmar_existencia(c2)
    print(f"   {c2.nome} confirmou a ocorrência #{o1.id} ({o1.confirmacoes} confirmações)")
    p.resolver_ocorrencia(o2.id, g1.id)
    print("  ", p.buscar_ocorrencia(o2.id))

    print("\n>>> 5) Rotas/locais recomendados (nota >= 4.0 e sem barreiras ativas)")
    for loc in p.listar_locais(apenas_acessiveis=True):
        print("  ", loc)

    print()
    print(p.gerar_relatorio().gerar_texto())


# ---------------------------- menu interativo ----------------------------
def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  Digite um número inteiro.")


def criar_barreira():
    print("  Tipo de barreira: 1-Rampa  2-Calçada  3-Piso Tátil  4-Elevador/Plataforma")
    op = input("  Escolha: ").strip()
    desc = input("  Descrição do problema: ")
    if op == "1":
        return BarreiraRampa(desc, input("  Rampa totalmente inexistente? (s/n): ").strip().lower() == "s")
    if op == "2":
        return BarreiraCalcada(desc, input("  Bloqueia totalmente a passagem? (s/n): ").strip().lower() == "s")
    if op == "3":
        return BarreiraPisoTatil(desc)
    return BarreiraElevador(desc)


def menu():
    p = Plataforma()
    opcoes = """
===== APP ROTA ACESSÍVEL (ODS 10) =====
1 - Carregar dados de exemplo
2 - Cadastrar cidadão colaborador
3 - Cadastrar gestor público
4 - Cadastrar local público
5 - Avaliar acessibilidade de um local
6 - Denunciar barreira arquitetônica
7 - Listar barreiras ativas por prioridade
8 - Confirmar existência de barreira (Cidadão)
9 - Marcar barreira como resolvida (Gestor)
10 - Buscar locais acessíveis (rota segura)
11 - Relatório de impacto social
0 - Sair"""
    while True:
        print(opcoes)
        op = input("Escolha: ").strip()
        try:
            if op == "1":
                carregar_exemplo(p)
                print("  Dados de exemplo carregados.")
            elif op == "2":
                c = p.registrar_usuario(CidadaoColaborador(
                    input("  Nome: "), input("  E-mail: "), input("  Cidade: "),
                    input("  Perfil (Cadeirante/Mobilidade Reduzida/Apoiador): ")))
                print("  Cadastrado:", c)
            elif op == "3":
                g = p.registrar_usuario(GestorPublico(
                    input("  Nome: "), input("  E-mail: "), input("  Cidade: "),
                    input("  Órgão público: "), input("  Matrícula: ")))
                print("  Cadastrado:", g)
            elif op == "4":
                loc = p.registrar_local(LocalPublico(
                    input("  Nome do local: "), input("  Categoria (Praça/Terminal/UBS...): "),
                    input("  Cidade: "), input("  Endereço: ")))
                print("  Cadastrado:", loc)
            elif op == "5":
                av = p.avaliar_local(
                    ler_int("  ID do local: "),
                    ler_int("  ID do usuário: "),
                    ler_int("  Nota (1 a 5): "),
                    input("  Comentário: "),
                    input("  Possui rampa? (s/n): ").strip().lower() == "s",
                    input("  Possui piso tátil? (s/n): ").strip().lower() == "s")
                print("  Avaliação registrada:", av)
            elif op == "6":
                lid = ler_int("  ID do local: ")
                uid = ler_int("  ID do usuário: ")
                oc = p.denunciar_barreira(lid, uid, criar_barreira())
                print("  Ocorrência registrada:\n  ", oc)
            elif op == "7":
                lista = p.listar_ocorrencias_prioritarias()
                print("\n".join(f"  {o}" for o in lista) if lista else "  Nenhuma barreira ativa.")
            elif op == "8":
                oc = p.buscar_ocorrencia(ler_int("  ID da ocorrência: "))
                oc.confirmar_existencia(p.buscar_usuario(ler_int("  ID do cidadão: ")))
                print(f"  Confirmada! Total de confirmações: {oc.confirmacoes}")
            elif op == "9":
                oc = p.resolver_ocorrencia(
                    ler_int("  ID da ocorrência: "),
                    ler_int("  ID do gestor público: "))
                print("  Resolvida:\n  ", oc)
            elif op == "10":
                cid = input("  Cidade (vazio para todas): ").strip() or None
                locais = p.listar_locais(cid, apenas_acessiveis=True)
                print("\n".join(f"  {loc}" for loc in locais) if locais else "  Nenhum local acessível encontrado.")
            elif op == "11":
                print(p.gerar_relatorio().gerar_texto())
            elif op == "0":
                print("Encerrando App Rota Acessível.")
                break
            else:
                print("  Opção inválida.")
        except (ValueError, PermissionError, KeyError) as e:
            print("  Erro:", e)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
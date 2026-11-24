"""Rede Mulher Segura - protótipo de console (ODS 5: Igualdade de Gênero).

Uso:
    python main.py          -> menu interativo
    python main.py --demo   -> demonstração automática de todo o fluxo
"""
import sys

from mulher_segura import (AdvogadaVoluntaria, NivelUrgencia, Plataforma,
                           PontoApoio, PsicologaVoluntaria, Usuaria)


def carregar_exemplo(p):
    u1 = p.registrar_usuaria(Usuaria("Mariana Silva", "Vitória", "(27) 99911-2233", codinome="Estrela_ES"))
    u2 = p.registrar_usuaria(Usuaria("Camila Rocha", "Serra", "(27) 98844-5566", codinome="Flor_Serra"))

    psi = p.registrar_profissional(
        PsicologaVoluntaria("Dra. Helena Costa", "helena.psi@rede.org", "Vitória", "CRP 16/4321",
                            abordagem="Terapia de Trauma e Acolhimento"))
    adv = p.registrar_profissional(
        AdvogadaVoluntaria("Dra.Beatriz Almeida", "beatriz.oab@rede.org", "Vitória", "OAB/ES 28.910",
                           area_atuacao="Medidas Protetivas e Direito de Família"))

    pt1 = p.registrar_ponto_apoio(
        PontoApoio("Casa da Mulher Brasileira - Vitória", "Centro de Referência", "Vitória",
                   "Av. Maruípe, 1500", "(27) 3333-1800", plantao_24h=True))
    pt2 = p.registrar_ponto_apoio(
        PontoApoio("DEAM Serra - Delegacia Especializada", "Delegacia", "Serra",
                   "Rua Maestro Antônio Cícero, 210", "(27) 3328-7210", plantao_24h=True))

    d1 = p.registrar_denuncia(
        u1.id, "Vitória", NivelUrgencia.EMERGENCIA, "Violência Física e Ameaça",
        "Agressor tentando invadir residência; solicitação urgente de abrigo e medida protetiva.",
        anonima=True)
    d2 = p.registrar_denuncia(
        u2.id, "Serra", NivelUrgencia.MEDIA, "Violência Psicológica e Patrimonial",
        "Retenção de documentos pessoais e ameaças constantes.",
        anonima=False)
    return u1, u2, psi, adv, pt1, pt2, d1, d2


def demo():
    p = Plataforma()
    print("\n>>> 1) Cadastro da rede (usuárias, voluntárias e pontos de apoio)")
    _, _, psi, adv, pt1, _, d1, d2 = carregar_exemplo(p)
    for prof in p.listar_profissionais():
        print("  ", prof)
    for pt in p.listar_pontos_apoio():
        print("  ", pt)

    print("\n>>> 2) Denúncias registradas (ordenadas por urgência - identidade anônima protegida)")
    for d in p.listar_denuncias_prioritarias():
        print("  ", d)

    print("\n>>> 3) Conexão com voluntárias (Polimorfismo no protocolo de acolhimento)")
    at1 = p.conectar_voluntaria(d1.id, psi.id)
    print("  ", at1)
    at2 = p.conectar_voluntaria(d1.id, adv.id)
    print("  ", at2)

    print("\n>>> 4) Encaminhamento para ponto de apoio seguro")
    p.encaminhar_para_ponto(d1.id, pt1.id)
    print("  ", p.buscar_denuncia(d1.id))

    print("\n>>> 5) Atualização de relato e encerramento de caso atendido")
    d2.adicionar_relato("Acompanhamento", "Usuária recebeu orientação jurídica inicial.")
    d2.encerrar()

    print()
    print(p.gerar_relatorio().gerar_texto())


# ---------------------------- menu interativo ----------------------------
def ler_inteiro(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  Valor inválido, digite um número inteiro.")


def menu():
    p = Plataforma()
    opcoes = """
===== REDE MULHER SEGURA (ODS 5) =====
1 - Carregar dados de exemplo
2 - Cadastrar usuária
3 - Cadastrar profissional voluntária (Psicóloga/Advogada)
4 - Cadastrar ponto de apoio
5 - Registrar denúncia (anônima ou identificada)
6 - Listar denúncias prioritárias
7 - Conectar denúncia a profissional voluntária
8 - Encaminhar denúncia para ponto de apoio
9 - Ver pontos de apoio por cidade
10 - Relatório de impacto social
0 - Sair"""
    while True:
        print(opcoes)
        op = input("Escolha: ").strip()
        try:
            if op == "1":
                carregar_exemplo(p)
                print("  Dados de exemplo carregados.")
            elif op == "2":
                u = p.registrar_usuaria(Usuaria(
                    input("  Nome real (protegido): "),
                    input("  Cidade: "),
                    input("  Telefone de emergência: "),
                    input("  Codinome (opcional): ").strip() or None))
                print("  Cadastrada:", u)
            elif op == "3":
                tipo = input("  Especialidade (1-Psicóloga / 2-Advogada): ").strip()
                nome = input("  Nome: ")
                email = input("  E-mail: ")
                cidade = input("  Cidade: ")
                reg = input("  Registro (CRP ou OAB): ")
                if tipo == "1":
                    ab = input("  Abordagem: ")
                    prof = PsicologaVoluntaria(nome, email, cidade, reg, ab)
                else:
                    area = input("  Área de atuação: ")
                    prof = AdvogadaVoluntaria(nome, email, cidade, reg, area)
                p.registrar_profissional(prof)
                print("  Cadastrada:", prof)
            elif op == "4":
                pt = p.registrar_ponto_apoio(PontoApoio(
                    input("  Nome do local: "),
                    input("  Tipo (DEAM/Abrigo/CRAS): "),
                    input("  Cidade: "),
                    input("  Endereço: "),
                    input("  Telefone: "),
                    input("  Plantão 24h? (s/n): ").strip().lower() == "s"))
                print("  Cadastrado:", pt)
            elif op == "5":
                uid = ler_inteiro("  ID da usuária: ")
                cidade = input("  Cidade da ocorrência: ")
                urg_num = ler_inteiro("  Urgência (1-Baixa, 2-Média, 3-Alta, 4-Emergência): ")
                urg = NivelUrgencia(max(1, min(4, urg_num)))
                tipo_v = input("  Tipo de violência: ")
                desc = input("  Relato detalhado: ")
                anon = input("  Manter anonimato? (s/n): ").strip().lower() != "n"
                d = p.registrar_denuncia(uid, cidade, urg, tipo_v, desc, anonima=anon)
                print("  Denúncia registrada:", d)
            elif op == "6":
                lista = p.listar_denuncias_prioritarias()
                print("\n".join(f"  {d}" for d in lista) if lista else "  Nenhuma denúncia ativa.")
            elif op == "7":
                for prof in p.listar_profissionais(apenas_disponiveis=True):
                    print("  ", prof)
                at = p.conectar_voluntaria(
                    ler_inteiro("  ID da denúncia: "),
                    ler_inteiro("  ID da profissional: "))
                print("  Atendimento iniciado:\n  ", at)
            elif op == "8":
                for pt in p.listar_pontos_apoio():
                    print("  ", pt)
                pt = p.encaminhar_para_ponto(
                    ler_inteiro("  ID da denúncia: "),
                    ler_inteiro("  ID do ponto de apoio: "))
                print(f"  Encaminhada para {pt.nome}!")
            elif op == "9":
                cid = input("  Cidade (vazio para todas): ").strip() or None
                pts = p.listar_pontos_apoio(cid)
                print("\n".join(f"  {pt}" for pt in pts) if pts else "  Nenhum ponto encontrado.")
            elif op == "10":
                print(p.gerar_relatorio().gerar_texto())
            elif op == "0":
                print("Encerrando Rede Mulher Segura.")
                break
            else:
                print("  Opção inválida.")
        except (ValueError, KeyError) as e:
            print("  Erro:", e)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
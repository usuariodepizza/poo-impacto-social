"""App Saúde em Dia - protótipo de console (ODS 3: Saúde e Bem-Estar).

Uso:
    python main.py          -> menu interativo
    python main.py --demo   -> demonstração automática de todo o fluxo
"""
import sys
from datetime import datetime, timedelta

from saude_em_dia import (Cuidador, FamiliarResponsavel, Idoso,
                          LembreteConsulta, LembreteMedicacao, LembreteVacina,
                          Plataforma)


def carregar_exemplo(p):
    idoso1 = p.registrar_pessoa(Idoso("Dona Maria Helena", "(27) 99900-1122", "Vitória", 78, "Hipertensão e Diabetes"))
    idoso2 = p.registrar_pessoa(Idoso("Seu Antônio Carlos", "(27) 99811-3344", "Serra", 82, "Cardiopatia"))

    fam1 = p.registrar_pessoa(FamiliarResponsavel("Juliana Helena", "(27) 99777-8899", "Vitória", "Filha"))
    fam2 = p.registrar_pessoa(FamiliarResponsavel("Ricardo Carlos", "(27) 99666-5544", "Serra", "Filho"))
    cuid1 = p.registrar_pessoa(Cuidador("Marta Oliveira", "(27) 99555-4433", "Vitória", "Diurno", "COREN-ES 112233"))

    p.vincular_rede_apoio(idoso1.id, familiar_id=fam1.id, cuidador_id=cuid1.id)
    p.vincular_rede_apoio(idoso2.id, familiar_id=fam2.id)

    agora = datetime.now()
    c1 = p.agendar_compromisso(LembreteMedicacao(
        idoso1, "Losartana 50mg", agora + timedelta(minutes=10), "1 comprimido", "Oral"))
    c2 = p.agendar_compromisso(LembreteVacina(
        idoso1, "Vacina Influenza (Gripe)", agora + timedelta(hours=3), "Dose Anual", "UBS Jardim da Penha"))
    c3 = p.agendar_compromisso(LembreteMedicacao(
        idoso2, "AAS Infantil 100mg", agora + timedelta(minutes=15), "1 comprimido após almoço", "Oral"))
    c4 = p.agendar_compromisso(LembreteConsulta(
        idoso2, "Cardiologia", agora + timedelta(hours=5), "Dr. Roberto Neves", "Hospital Meridional Serra"))
    return idoso1, idoso2, fam1, fam2, cuid1, c1, c2, c3, c4


def demo():
    p = Plataforma()
    print("\n>>> 1) Cadastro de idosos, familiares e cuidadores (polimorfismo de perfis)")
    idoso1, idoso2, fam1, fam2, cuid1, c1, _, c3, _ = carregar_exemplo(p)
    for pessoa in p.listar_pessoas():
        print("  ", pessoa)

    print("\n>>> 2) Agenda de lembretes (medicação, vacina e consulta)")
    for comp in p.listar_compromissos():
        print("  ", comp)

    print("\n>>> 3) Cuidadora confirma a medicação da Dona Maria Helena")
    p.confirmar_compromisso(c1.id, cuid1.id)
    print("  ", p.buscar_compromisso(c1.id))

    print("\n>>> 4) Simulando 1 hora depois: Seu Antônio não confirmou o remédio -> Alerta automático!")
    alertas = p.verificar_alertas_atraso(datetime.now() + timedelta(hours=1))
    for alerta in alertas:
        print("  ", alerta)
    print("   Status atualizado do familiar:", fam2)

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
===== APP SAÚDE EM DIA (ODS 3) =====
1 - Carregar dados de exemplo
2 - Cadastrar idoso
3 - Cadastrar familiar responsável
4 - Cadastrar cuidador
5 - Vincular familiar/cuidador a um idoso
6 - Agendar lembrete (Medicação / Vacina / Consulta)
7 - Listar lembretes agendados
8 - Confirmar realização de lembrete
9 - Verificar atrasos e disparar alertas aos familiares
10 - Relatório de impacto em saúde
0 - Sair"""
    while True:
        print(opcoes)
        op = input("Escolha: ").strip()
        try:
            if op == "1":
                carregar_exemplo(p)
                print("  Dados de exemplo carregados.")
            elif op == "2":
                i = p.registrar_pessoa(Idoso(
                    input("  Nome: "), input("  Telefone: "), input("  Cidade: "),
                    ler_inteiro("  Idade (60+): "), input("  Condições de saúde: ")))
                print("  Cadastrado:", i)
            elif op == "3":
                f = p.registrar_pessoa(FamiliarResponsavel(
                    input("  Nome: "), input("  Telefone: "), input("  Cidade: "),
                    input("  Parentesco (Filho/Filha/Neto...): ")))
                print("  Cadastrado:", f)
            elif op == "4":
                c = p.registrar_pessoa(Cuidador(
                    input("  Nome: "), input("  Telefone: "), input("  Cidade: "),
                    input("  Turno (Diurno/Noturno/Integral): "),
                    input("  Registro profissional (opcional): ").strip() or None))
                print("  Cadastrado:", c)
            elif op == "5":
                iid = ler_inteiro("  ID do idoso: ")
                fid = input("  ID do familiar (vazio para pular): ").strip()
                cid = input("  ID do cuidador (vazio para pular): ").strip()
                p.vincular_rede_apoio(iid, int(fid) if fid else None, int(cid) if cid else None)
                print("  Vínculo atualizado:", p.buscar_pessoa(iid))
            elif op == "6":
                idoso = p.buscar_pessoa(ler_inteiro("  ID do idoso: "), Idoso)
                tipo = input("  Tipo (1-Medicação / 2-Vacina / 3-Consulta): ").strip()
                minutos = ler_inteiro("  Daqui a quantos minutos será o horário previsto? ")
                horario = datetime.now() + timedelta(minutes=minutos)
                if tipo == "1":
                    comp = LembreteMedicacao(
                        idoso, input("  Nome do medicamento: "), horario,
                        input("  Dosagem (ex.: 1 comprimido): "), input("  Via (Oral/Injetável): "))
                elif tipo == "2":
                    comp = LembreteVacina(
                        idoso, input("  Nome da vacina: "), horario,
                        input("  Dose (1ª/2ª/Reforço): "), input("  Posto de saúde: "))
                else:
                    comp = LembreteConsulta(
                        idoso, input("  Especialidade: "), horario,
                        input("  Nome do médico: "), input("  Clínica/Hospital: "))
                p.agendar_compromisso(comp)
                print("  Agendado:", comp)
            elif op == "7":
                lista = p.listar_compromissos()
                print("\n".join(f"  {c}" for c in lista) if lista else "  Nenhum lembrete agendado.")
            elif op == "8":
                comp = p.confirmar_compromisso(
                    ler_inteiro("  ID do lembrete: "),
                    ler_inteiro("  ID de quem está confirmando (Idoso/Cuidador): "))
                print("  Confirmado:", comp)
            elif op == "9":
                atraso_min = ler_inteiro("  Simular avanço de quantos minutos no relógio? (0 = agora): ")
                alertas = p.verificar_alertas_atraso(datetime.now() + timedelta(minutes=atraso_min))
                if alertas:
                    print("\n".join(f"  {a}" for a in alertas))
                else:
                    print("  Nenhum lembrete ultrapassou o limite de tolerância.")
            elif op == "10":
                print(p.gerar_relatorio().gerar_texto())
            elif op == "0":
                print("Encerrando App Saúde em Dia.")
                break
            else:
                print("  Opção inválida.")
        except ValueError as e:
            print("  Erro:", e)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else menu()
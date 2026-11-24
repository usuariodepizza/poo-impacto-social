# Solução 3 — App "Saúde em Dia" (ODS 3)

## 1. Definição do problema e ODS

Com o envelhecimento populacional, cresce o número de pessoas idosas que convivem com doenças crônicas (como hipertensão, diabetes e cardiopatias) e dependem de múltiplas medicações diárias, campanhas de vacinação e consultas periódicas. O esquecimento de doses, a perda de prazos vacinais ou a falta de comunicação entre cuidadores e familiares levam a descompensações evitáveis, internações de urgência e sobrecarga do sistema de saúde.

**ODS relacionado:**
- **ODS 3 – Saúde e Bem-Estar:** contribui diretamente para as metas 3.4 (reduzir a mortalidade prematura por doenças não transmissíveis por meio de prevenção e tratamento) e 3.8 (assegurar o acesso a serviços de saúde essenciais e medicamentos seguros e eficazes), promovendo prevenção e continuidade do cuidado à pessoa idosa.

## 2. Descrição do sistema (empreendedorismo social)

**Usuários:**
- **Idosos (pacientes principais):** têm sua rotina de medicações, vacinas e consultas organizada em lembretes claros e confirmam a realização de cada cuidado.
- **Cuidadores (familiares ou profissionais de enfermagem):** auxiliam no acompanhamento presencial e registram a confirmação das doses e procedimentos realizados.
- **Familiares Responsáveis:** ficam vinculados ao idoso e recebem alertas automáticos caso um compromisso ultrapasse o tempo limite de tolerância sem confirmação.

**Como funciona na prática:** o sistema agenda lembretes de medicação, vacina ou consulta para o idoso. Cada categoria possui uma janela de tolerância específica (por exemplo, 30 minutos para medicação contínua e 60 minutos para consultas). Se o horário passar sem confirmação, a plataforma muda o status para atrasado e dispara um alerta automático para o familiar responsável agir preventivamente.

**Sustentabilidade:**
- **Social:** aumenta a segurança, a autonomia e a qualidade de vida da pessoa idosa, fortalecendo a rede de apoio familiar e comunitária.
- **Econômica:** previne internações hospitalares e atendimentos de emergência decorrentes da má adesão medicamentosa, reduzindo gastos tanto para as famílias quanto para o SUS e planos de saúde.
- **Ambiental:** reduz o desperdício de medicamentos vencidos ou inutilizados e substitui controles manuais em papel por registros digitais integrados.

## 3. Modelagem orientada a objetos

O diagrama de classes (`diagrama_classes.png`) possui **12 classes/tipos**: `Pessoa`, `Idoso`, `Cuidador`, `FamiliarResponsavel`, `CompromissoSaude`, `LembreteMedicacao`, `LembreteVacina`, `LembreteConsulta`, `AlertaFamiliar`, `StatusCompromisso`, `Plataforma` e `RelatorioImpacto`.

- **Herança:** `Idoso`, `Cuidador` e `FamiliarResponsavel` herdam de `Pessoa`; `LembreteMedicacao`, `LembreteVacina` e `LembreteConsulta` herdam de `CompromissoSaude`.
- **Polimorfismo:** os métodos abstratos `tolerancia_minutos()` e `instrucoes_cuidado()` de `CompromissoSaude` são implementados de forma distinta em cada subclasse (`30 min` para medicação, `60 min` para consulta e `120 min` para vacina), permitindo que `verificar_atraso()` calcule o disparo de alerta polimorficamente. O mesmo ocorre com `Pessoa.resumo()`.
- **Encapsulamento:** atributos privados (`_status`, `_compromissos`, `_alertas_recebidos`) expostos via `@property` e tuplas imutáveis; `AlertaFamiliar` é um *value object* imutável (`@dataclass(frozen=True)`).
- **Composição:** `Idoso` compõe sua agenda de `CompromissoSaude`; `CompromissoSaude` compõe o `AlertaFamiliar` gerado em caso de atraso.
- **Agregação:** `Plataforma` agrega `Pessoa` e `CompromissoSaude`.
- **Associação:** `Idoso` associa-se a `FamiliarResponsavel` e `Cuidador`.

## 4. Protótipo

Código em Python com menu interativo de console e demonstração automática (`python main.py --demo`).
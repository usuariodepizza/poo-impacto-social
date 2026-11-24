# Solução 1 — Rede "Mulher Segura" (ODS 5)

## 1. Definição do problema e ODS

A violência doméstica e de gênero continua sendo uma grave violação de direitos humanos. Muitas mulheres em situação de vulnerabilidade deixam de buscar ajuda por medo de exposição, dependência financeira, desconhecimento sobre seus direitos legais ou dificuldade em localizar serviços especializados próximos. A ausência de um canal integrado entre denúncia protegida, acolhimento psicológico, orientação jurídica e pontos físicos de apoio retarda o socorro em momentos críticos.

**ODS relacionado:**
- **ODS 5 – Igualdade de Gênero:** contribui diretamente para as metas 5.1 e 5.2 (eliminar todas as formas de discriminação e violência contra todas as mulheres e meninas nas esferas pública e privada), oferecendo mecanismos seguros de proteção e acesso à justiça.

## 2. Descrição do sistema (empreendedorismo social)

**Usuários:**
- **Usuárias (mulheres em situação de risco ou testemunhas):** registram denúncias escolhendo entre identificação ou anonimato (via codinome), descrevem os relatos de ocorrência e consultam pontos de apoio próximos.
- **Psicólogas e Advogadas Voluntárias:** profissionais habilitadas (com CRP ou OAB) que prestam acolhimento emocional e orientação jurídica gratuita por meio da plataforma.
- **Pontos de Apoio (DEAMs, Casas da Mulher, CRAS, abrigos):** instituições físicas mapeadas no sistema para encaminhamento presencial e proteção emergencial.

**Como funciona na prática:** a usuária registra uma denúncia classificando o nível de urgência e adicionando um ou mais relatos. O sistema protege sua identidade caso opte pelo anonimato, ordena os casos por gravidade e conecta a denúncia a psicólogas e advogadas voluntárias disponíveis, além de indicar pontos de apoio na cidade com plantão 24h. Ao final, um relatório consolida os indicadores de acolhimento.

**Sustentabilidade:**
- **Social:** promove segurança, acolhimento humanizado, sigilo e acesso gratuito à justiça e saúde mental para mulheres vulneráveis.
- **Econômica:** opera com rede de voluntariado qualificado e integração com equipamentos públicos já existentes (DEAMs/CRAS), reduzindo custos operacionais e gerando autonomia financeira futura às vítimas orientadas.
- **Ambiental:** substitui registros físicos fragmentados por triagem digital centralizada, reduzindo deslocamentos desnecessários e o consumo de papel em atendimentos iniciais.

## 3. Modelagem orientada a objetos

O diagrama de classes (`diagrama_classes.png`) conta com **12 classes/tipos**: `ProfissionalVoluntaria`, `PsicologaVoluntaria`, `AdvogadaVoluntaria`, `Usuaria`, `PontoApoio`, `Denuncia`, `RelatoOcorrencia`, `Atendimento`, `StatusDenuncia`, `NivelUrgencia`, `Plataforma` e `RelatorioImpacto`.

- **Herança:** `PsicologaVoluntaria` e `AdvogadaVoluntaria` herdam de `ProfissionalVoluntaria`, compartilhando identificação, cidade, registro profissional e controle de disponibilidade.
- **Polimorfismo:** os métodos abstratos `especialidade()` e `protocolo_acolhimento(denuncia)` são implementados de modo distinto em `PsicologaVoluntaria` (escuta psicológica e estabilização emocional) e `AdvogadaVoluntaria` (orientação jurídica e pedido de medida protetiva). Quando `Atendimento` é criado, invoca `profissional.protocolo_acolhimento(denuncia)` polimorficamente.
- **Encapsulamento:** todos os atributos usam prefixo privado `_` com acesso controlado via `@property`. O método `Usuaria.identidade_publica(anonima)` oculta o nome real da vítima quando a denúncia é anônima, e `Denuncia.relatos` retorna uma tupla imutável.
- **Composição:** `Denuncia` é composta por `RelatoOcorrencia` (os relatos pertencem exclusivamente ao ciclo de vida da denúncia).
- **Agregação:** `Plataforma` agrega `Usuaria`, `ProfissionalVoluntaria`, `PontoApoio` e `Denuncia`.
- **Associação:** `Denuncia` associa-se a `Usuaria` e `PontoApoio`; `Atendimento` associa `Denuncia` a `ProfissionalVoluntaria`.

## 4. Protótipo

Código em Python com menu interativo de console e demonstração automática (`python main.py --demo`).
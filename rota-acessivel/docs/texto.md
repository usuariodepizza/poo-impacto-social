# Solução 2 — App "Rota Acessível" (ODS 10)

## 1. Definição do problema e ODS

Milhões de pessoas cadeirantes, com mobilidade reduzida ou deficiência visual enfrentam diariamente barreiras urbanas invisíveis aos mapas tradicionais: rampas de acesso quebradas ou inexistentes, calçadas esburacadas, ausência de piso tátil e elevadores públicos fora de operação. Essa falta de informação confiável em tempo real restringe o direito de ir e vir, dificulta o acesso à saúde, educação e trabalho e aprofunda a exclusão social.

**ODS relacionado:**
- **ODS 10 – Redução das Desigualdades:** alinha-se diretamente à meta 10.2 (empoderar e promover a inclusão social, econômica e política de todos, independentemente de idade, gênero, deficiência, raça ou condição), garantindo autonomia e acessibilidade no espaço urbano.

## 2. Descrição do sistema (empreendedorismo social)

**Usuários:**
- **Cidadãos Colaboradores (cadeirantes, pessoas com mobilidade reduzida e apoiadores):** avaliam as condições de acessibilidade de locais públicos (notas de 1 a 5, presença de rampa e piso tátil) e denunciam barreiras arquitetônicas, acumulando pontos e subindo de nível (Bronze, Prata e Ouro).
- **Gestores Públicos (agentes de secretarias de obras e mobilidade):** acompanham as ocorrências priorizadas por gravidade e número de confirmações comunitárias, aplicando as diretrizes técnicas (NBR 9050) e atualizando o status até a resolução física do problema.

**Como funciona na prática:** ao visitar uma praça, terminal ou unidade de saúde, o cidadão consulta no mapa colaborativo a nota média de acessibilidade e verifica se há bloqueios ativos. Caso encontre uma barreira, registra uma ocorrência escolhendo a categoria (`BarreiraRampa`, `BarreiraCalcada`, `BarreiraPisoTatil` ou `BarreiraElevador`). O sistema calcula automaticamente a gravidade, os pontos de recompensa e a recomendação técnica, priorizando os bloqueios mais críticos.

**Sustentabilidade:**
- **Social:** devolve autonomia e segurança no deslocamento de pessoas com deficiência e mobilidade reduzida, dando voz ativa aos cidadãos na fiscalização urbana.
- **Econômica:** otimiza o orçamento de manutenção das prefeituras ao direcionar equipes técnicas exatamente para os pontos críticos validados pela população, reduzindo retrabalho e custos de vistoria.
- **Ambiental:** incentiva a mobilidade urbana ativa e o uso do transporte público acessível, diminuindo a dependência de transporte individual motorizado e melhorando a qualidade do espaço urbano.

## 3. Modelagem orientada a objetos

O diagrama de classes (`diagrama_classes.png`) apresenta **14 classes/tipos**: `Usuario`, `CidadaoColaborador`, `GestorPublico`, `BarreiraArquitetonica`, `BarreiraRampa`, `BarreiraCalcada`, `BarreiraPisoTatil`, `BarreiraElevador`, `LocalPublico`, `AvaliacaoAcessibilidade`, `OcorrenciaBarreira`, `StatusOcorrencia`, `Plataforma` e `RelatorioImpacto`.

- **Herança:** `CidadaoColaborador` e `GestorPublico` herdam de `Usuario`; `BarreiraRampa`, `BarreiraCalcada`, `BarreiraPisoTatil` e `BarreiraElevador` herdam de `BarreiraArquitetonica`.
- **Polimorfismo:** os métodos abstratos `gravidade_base()`, `pontos_recompensa()` e `recomendacao_tecnica()` são implementados de forma distinta em cada subclasse de barreira; da mesma forma, `pode_resolver_ocorrencia()` e `resumo()` diferenciam cidadãos colaboradores de gestores públicos.
- **Encapsulamento:** atributos privados (`_pontos`, `_status`, `_avaliacoes`, `_ocorrencias`) protegidos via `@property` e tuplas imutáveis; `AvaliacaoAcessibilidade` é um *value object* imutável (`@dataclass(frozen=True)`) com validação de nota (1 a 5).
- **Composição:** `LocalPublico` é composto por `AvaliacaoAcessibilidade`; `OcorrenciaBarreira` é composta por `BarreiraArquitetonica`.
- **Agregação:** `Plataforma` agrega `Usuario`, `LocalPublico` e `OcorrenciaBarreira`.
- **Associação:** `OcorrenciaBarreira` associa-se ao `Usuario` autor e ao `LocalPublico` correspondente.

## 4. Protótipo

Código em Python com menu interativo de console e demonstração automática (`python main.py --demo`). Repositório: https://github.com/usuariodepizza/poo-impacto-social
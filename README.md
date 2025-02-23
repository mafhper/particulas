SIMULAÇÃO DE PARTÍCULAS COM PYGAME
===================================

Uma simulação interativa de partículas com física realista, fusão de partículas e efeitos visuais em tempo real, desenvolvida em Python com Pygame.

FUNCIONALIDADES PRINCIPAIS
--------------------------
- Partículas dinâmicas com massa, velocidade e cor aleatórias
- Interação gravitacional entre partículas
- Fusão de partículas com conservação de momento e massa
- Limites físicos realistas (colisões com as bordas da tela)
- Rastros persistentes com efeito de desvanecimento
- Controles interativos via teclado
- Exibição da hora atual com atualização dinâmica
- Modo tela cheia automático

PRÉ-REQUISITOS
---------------
- Python 3.x
- Pygame 2.x

INSTALAÇÃO
----------
1. Clone o repositório:
   git clone https://github.com/seu-usuario/simulacao-particulas.git

2. Instale as dependências:
   pip install pygame

USO
---
Execute o script:
   python3 simulacao_particulas.py

CONTROLES DO TECLADO
--------------------
- R: Reiniciar simulação
- P: Pausar/Retomar simulação
- A: Redistribuir partículas
- H: Alternar exibição da hora
- ESC: Sair do programa

PERSONALIZAÇÃO
--------------
Modifique os parâmetros no código para ajustar a simulação:

1. Número inicial de partículas:
   particles = create_particles(300)

2. Propriedades físicas (classe Particle):
   self.mass = random.uniform(0.5, 5.0)
   self.radius = int((self.mass ** (1/3)) * 2)

3. Cores e efeitos visuais:
   trail_surface.fill((0, 0, 0, 20))  # Transparência dos rastros

ESTRUTURA DO CÓDIGO
-------------------
- Classe Particle: Gerencia propriedades físicas e visuais das partículas
- Funções principais:
  * gravitational_force(): Calcula forças gravitacionais
  * merge_particles(): Combina partículas em colisão
  * create_particles(): Gera partículas com propriedades aleatórias
- Loop principal: Gerencia atualizações físicas, renderização e controles

LICENÇA
-------
Distribuído sob licença MIT. Veja LICENSE para mais informações.

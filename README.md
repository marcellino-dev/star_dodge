# Star Dodge

#### Video Demo: https://youtu.be/AjvNu9KOhXw

#### Description:

Star Dodge é um jogo de sobrevivência em duas dimensões desenvolvido em Python com a biblioteca Pygame, criado como projeto final do curso CS50x (Introdução à Ciência da Computação) da HarvardX.

O jogador controla uma nave que precisa desviar de meteoros que caem do topo da tela. Conforme o tempo passa, a quantidade e a velocidade dos meteoros aumentam, tornando o jogo progressivamente mais difícil. Ao longo da partida, itens especiais (power-ups) caem aleatoriamente pela tela e concedem vantagens temporárias ao jogador.

## Como jogar

- Setas do teclado ou WASD movem a nave nas quatro direções.
- O jogador começa com 3 vidas. Cada colisão com um meteoro remove uma vida.
- O jogo termina quando as vidas chegam a zero.
- ESPAÇO inicia a partida a partir do menu.
- R reinicia a partida após o game over.
- ESC fecha o jogo a qualquer momento.

## Power-ups

| Cor | Efeito |
|---|---|
| Azul claro | Escudo temporário — o jogador fica imune a colisões por alguns segundos |
| Verde | Vida extra |
| Amarelo | Multiplicador de pontos temporário |

## Estrutura do projeto

- `project.py` — contém a função `main` e todas as demais funções do jogo (movimentação, geração de obstáculos e power-ups, detecção de colisão, desenho na tela, persistência do recorde).
- `test_project.py` — testes automatizados (`pytest`) para as funções que não dependem de renderização gráfica: `clamp`, `spawn_obstacle`, `update_obstacles`, `check_collision` e a leitura/escrita do recorde.
- `requirements.txt` — dependências do projeto (`pygame`, `pytest`).
- `highscore.txt` — arquivo gerado automaticamente na primeira execução para armazenar o recorde.

## Decisões de design

O recorde é salvo em um arquivo de texto simples (`highscore.txt`) em vez de um banco de dados, já que o jogo armazena apenas um único valor numérico e local — usar SQL aqui adicionaria complexidade sem benefício real.

A dificuldade aumenta de forma contínua com base no tempo de jogo (calculada a partir dos ticks do Pygame), em vez de níveis fixos, para que a curva de dificuldade seja suave.

Os power-ups foram implementados com durações temporárias controladas por comparação de timestamps (`pygame.time.get_ticks()`), evitando a necessidade de múltiplas threads ou temporizadores externos.

## Uso de ferramentas de IA

Este projeto foi desenvolvido com apoio de IA (Claude, da Anthropic) para estruturação do código, revisão de lógica e escrita dos testes automatizados, conforme permitido pela política do CS50 para o projeto final. O conceito do jogo, as decisões de design e a revisão final do trabalho são de autoria própria. Essa citação também está presente nos comentários do arquivo `project.py`.

## Como executar

```bash
pip install -r requirements.txt
python3 project.py
```

## Como rodar os testes

```bash
pytest test_project.py -v
```
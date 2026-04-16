# -- coding: latin-1 --
import networkx as nx  # Importa a biblioteca networkx para manipulação de grafos.
import matplotlib.pyplot as plt  # Importa o matplotlib para visualização de grafos.
import matplotlib
matplotlib.use('qtagg')

class Dijkstra:
   """
   Implementa o algoritmo de Dijkstra para um grafo ponderado
   representado por lista de adjacências.

   Convenções:
   - cada posição da lista principal corresponde a um vértice;
   - cada item da sublista é uma tupla (vizinho, peso);
   - pesos devem ser positivos.

   Restrições desta implementação:
   - não suporta pesos negativos, pois o algoritmo de Dijkstra exige
     pesos positivos;
   - melhor para grafo esparso (uso de lista): para grafos muito densos,
     a matriz pode ser uma representação mais direta;
   - funciona corretamente para grafos não direcionados e também para
     direcionados, desde que a lista represente corretamente as
     direções das arestas.
   """

   def __init__(self, grafo, origem):
      # Armazena a lista de adjacências do grafo.
      self.__grafo = grafo
      # Armazena o vértice inicial.
      self.__origem = origem
      # Determina a quantidade de vértices do grafo.
      self.__n = len(grafo)
      # Define um valor grande para representar infinito.
      self.__inf = 10 ** 9
      # Inicializa o vetor de distâncias com infinito.
      self.__dist = self.__n * [self.__inf]
      # Inicializa o vetor de predecessores com -1.
      self.__prev = self.__n * [-1]
      # Inicializa o vetor de vértices resolvidos como falso.
      self.__solv = self.__n * [False]
      # Define distância zero para o vértice inicial.
      self.__dist[self.__origem] = 0
      # Marca o vértice inicial como resolvido.
      self.__solv[self.__origem] = True
      # Executa o algoritmo de Dijkstra para todos os vértices.
      self.__calcular_caminhos()
    
   def __calcular_caminhos(self):
        while True:
            menor_dist = self.__inf
            prox = - 1
            for i in range(self.__n):
                if self.__solv[i] == True:
                    for j in range(self.__n):
                        if not self.__solv[j]:
                            nova_dist = self.__dist[i] + peso(i, j)
                            if nova_dist < self.__dist[j]:
                                self.__dist[j] = nova_dist
                                self.__prev[j] = i
                            if self.__dist[j] < menor_dist:
                                menor_dist = self.__dist[j]
                                prox = j
            if prox == -1:
                return
            self.__solv[prox] = True

   def menor_caminho(self, destino):
      # Caso em que origem e destino são iguais.
      if destino == self.__origem:
         # Retorna apenas o vértice inicial e distância zero.
         return [self.__origem], 0
      # Caso em que não existe caminho até o destino.
      if self.__dist[destino] == self.__inf:
         # Retorna mensagem e distância infinita.
         return "Caminho inexistente", self.__inf
      # Inicia a reconstrução do caminho a partir do destino.
      atual = destino
      # Cria lista contendo inicialmente o vértice final.
      caminho = [atual]
      # Reconstrução do caminho voltando pelos predecessores.
      while atual != self.__origem:
         # Atualiza para o predecessor do vértice atual.
         atual = self.__prev[atual]
         # Se não houver predecessor válido, não existe caminho.
         if atual == -1:
            return "Caminho inexistente", self.__inf
         # Insere o vértice no início da lista.
         caminho.insert(0, atual)
      # Retorna a lista com o caminho e o custo total.
      return caminho, self.__dist[destino]

def montar_rota(caminho, letra):
   """
   Monta uma string com a sequência de vértices do caminho mínimo,
   convertendo cada índice para sua letra correspondente e inserindo
   " > " entre eles para representar a rota.
   Exemplo: caminho = [0, 2, 3, 4, 6] -> rota = "A > C > D > E > G".
   """
   # Inicializa string vazia para montar a rota.
   rota = ""
   # Percorre todos os vértices do caminho.
   for i in range(len(caminho)):
      # Acrescenta a letra correspondente ao vértice.
      rota = rota + letra[caminho[i]]
      # Se não for o último elemento, adiciona separador.
      if i < len(caminho) - 1:
         rota = rota + " > "
   # Retorna a rota formatada.
   return rota

# Função para plotar os grafos original e resultante de Dijkstra.
# Apenas para grafos não direcionados.
# 'grafo' contém o grafo de adjacências e 'caminho' contém o menor caminho.
# 'ini' e 'fin' são os vértices inicial e final respectivamente.
# 'desig' são as designações dos vértices (nomes).
def plot_grafos(grafo, caminho, ini, fin, desig, Comp):
   G = nx.Graph()  # Grafo original.
   G_result = nx.Graph()  # Grafo resultante.
   # Adiciona as arestas do grafo original.
   for i in range(len(grafo)):  # Percorre os vértices.
      for vizinho, peso in grafo[i]:  # Arestas e pesos.
         G.add_edge(i, vizinho, weight=peso)  # Aresta no grafo original.
         G_result.add_edge(i, vizinho, weight=peso)  # Aresta no grafo resultante.
   pos = nx.spring_layout(G, seed=24)  # Define a disposição dos nós no gráfico.
   # Plotando o grafo original.
   plt.figure(figsize=(10, 5))
   plt.subplot(1, 2, 1)  # Primeiro gráfico.
   nx.draw(G, pos, with_labels=True, labels={i: desig[i] for i in range(len(desig))},
          node_color='lightgray', node_size=500, font_size=10, font_color='black',
          edge_color='black', linewidths=1, edgecolors='black') # Arestas/pesos em preto.
   nx.draw_networkx_nodes(G, pos, nodelist=[ini], node_color='lightgreen',
                         edgecolors='black', linewidths=0)  # Inicial em verde claro.
   nx.draw_networkx_nodes(G, pos, nodelist=[fin], node_color='lightsalmon',
                         edgecolors='black', linewidths=0)  # Final em laranja claro.
   nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d
                                                    in G.edges(data=True)}, 
                                                    font_color='black', rotate=False)
   plt.title("Grafo Original")  # Título.
   # Plota o grafo resultante.
   plt.subplot(1, 2, 2)  # Segundo gráfico.
   edge_colors = ['lightgray' if not (u in caminho and v in caminho and abs(
      caminho.index(u) - caminho.index(v)) == 1) else 'black' for u, v in
                 G_result.edges()]  # Arestas não pertencentes ao caminho em cinza claro.
   nx.draw(G_result, pos, with_labels=True, labels={i: desig[i] for i in range(
      len(desig))}, node_color='lightgray', node_size=500, font_size=10,
          font_color='black', edge_color=edge_colors, linewidths=1,
          edgecolors='black')  # Arestas configuradas.
   nx.draw_networkx_nodes(G_result, pos, nodelist=[ini], node_color='lightgreen',
                         edgecolors='black', linewidths=0)  # Inicial em verde claro.
   nx.draw_networkx_nodes(G_result, pos, nodelist=[fin], node_color='lightsalmon',
                         edgecolors='black', linewidths=0)  # Final em laranja claro.
   edge_labels_result = {(u, v): d['weight'] for u, v, d in G_result.edges(data=True)}
   # Exibe os rótulos das arestas do grafo resultante com cor apropriada
   for (u, v) in edge_labels_result:
      color = 'black' if (u in caminho and v in caminho and abs(
         caminho.index(u) - caminho.index(v)) == 1) else 'lightgray'
      nx.draw_networkx_edge_labels(G_result, pos, 
                                   edge_labels={(u, v): edge_labels_result[(u, v)]},
                                   font_color=color, rotate=False)
   plt.title("Grafo com Caminho Mínimo")  # Título.
   plt.text(0.5, -0.1, f"Comprimento caminho: {Comp}", fontsize=10, ha='center',
           transform=plt.gca().transAxes)  # Exibe o comprimento total correto.
   plt.show()  # Exibe os dois gráficos.

##### PROGRAMA PRINCIPAL ###############################################################

# Lista com as letras dos vértices.
letra = ['Aurora', 'Bonito', 'Carmo', 'Douras', 'Estrela', 'Felice', 'Gema', 'Herval', 'Ipiaú', 'Jaburu', 'Lindoa', 'Mundaú']
# Lista de adjacências do grafo.
LA = [
   [(1, 28), (2, 42), (4, 31)],                   # 0Aurora
   [(0, 28), (3, 33), (4, 27)],                   # 1Bonito
   [(0, 42), (4, 27), (5, 35)],                   # 2Carmo
   [(1, 32), (6, 40), (7, 34)],                   # 3Douras
   [(0, 31), (1, 27), (2, 27), (7, 38), (8, 32)], # 4Estrela
   [(2, 35), (9, 37)],                            # 5Felice
   [(3, 40), (9, 45)],                            # 6Gema
   [(3, 34), (4, 38), (9, 40), (10, 50)],         # 7Herval
   [(4, 32), (5, 44), (10, 45), (11, 52)],        # 8Ipiaú
   [(5, 37), (6, 45), (7, 40), (11, 53)],         # 9Jaburu
   [(7, 50), (8, 45)],                            # 10Lindoa
   [(8, 52), (9, 53)]                             # 11Mundaú
]
print(""" Cidades disponíveis:
        0 - Aurora
        1 - Bonito
        2 - Carmo
        3 - Douras
        4 - Estrela
        5 - Felice
        6 - Gema
        7 - Herval
        8 - Ipiaú
        9 - Jaburu
        10 - Lindoa
        11 Mundaú
    """)
# Define o vértice inicial.
orig = print(int(input("Escolha a cidade de origem (0 - 11): ")))
# Define o vértice final.
destf = print(int(input("Escolha a cidade de destino (0 - 11): ")))
# Cria objeto da classe Dijkstra.
dj = Dijkstra(LA, orig)
# Exibe vértice inicial.
print("\nVertice inicial.: " + letra[orig])
# Exibe vértice final.
print("Vertice final...: " + letra[destf])
# Calcula menor caminho.
caminho, comp = dj.menor_caminho(destf)
# O uso de type() abaixo ocorre porque a função menor_caminho pode retornar
# dois tipos diferentes: uma lista (quando há caminho) ou uma string
# ("Caminho inexistente"). Assim, o teste permite identificar quando não
# existe caminho e evitar operações inválidas sobre o resultado.
# Verifica se existe caminho.
if type(caminho) == str:
   # Exibe mensagem de erro.
   print(caminho)
   comp_tot = comp
else:
   # Monta a rota.
   rota = montar_rota(caminho, letra)
   # Exibe resultado.
   print("Menor caminho de %s ateh %s: %-13s\nValor: %3d" %
        (letra[orig], letra[destf], rota, comp))
   comp_tot = comp
# Cabeçalho da tabela de outros caminhos.
print("\n--------------------------")
print("     Outros destinos")
print("--------------------------")
print("Dest.  Caminho       Dist.")
print("--------------------------")
# Percorre todos os vértices como destino.
for dest in range(len(LA)):
   # Ignora origem e destino principal.
   if orig != dest and dest != destf:
      # Calcula caminho.
      path, comp = dj.menor_caminho(dest)
      # Exibe destino.
      print(" " + letra[dest], end="     ")
      # O uso de type() abaixo segue a mesma ideia: distinguir entre
      # caminho válido (lista) e caminho inexistente (string).
      # Se não houver caminho.
      if type(path) == str:
         print("%-13s %3s" % ("inexistente", "-"))
      else:
         # Monta rota.
         rota = montar_rota(path, letra)
         # Exibe resultado.
         print("%-13s %3d" % (rota, comp))
# Se houver caminho principal, desenha o grafo.
if type(caminho) != str:
   plot_grafos(LA, caminho, orig, destf, letra, comp_tot)

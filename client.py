#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from API_TCP_UDP import *

object_client = API_TCP_UDP()

#server_IP = raw_input("Insert the server IP: ")

'''while True:
    try:
        server_port = input("Insert the server port: ")
        break
    except:
        print ("You must to inform a integer number!\n")'''

connection = object_client.connection('localhost', 12000)

object_client.send_data(['Gremio Foot-Ball Porto Alegrense (conhecido apenas por Gremio e cujo acronimo e FBPA) e um clube de futebol brasileiro da cidade de Porto Alegre,'
                            +'no Rio Grande do Sul, fundado em 15 de setembro de 1903. Suas cores sao azul, preto e branco. O clube tem como alcunhas Imortal Tricolor, Tricolor'
                            +'dos Pampas, Tricolor Gaucho e Rei de Copas, devido ao seu historico especialmente vitorioso em competicoes de mata-mata.'
                            +'Ja foi campeao da Copa Libertadores da America em tres ocasioes (o que o torna o clube brasileiro com mais conquistas nesta competicao, ao lado de'
                            +'Sao Paulo e Santos) e vice em duas outras oportunidades, sendo o unico clube brasileiro a ter decidido a competicao em quatro decadas diferentes.[11]'
                            +'e o primeiro clube fora do Sudeste a conquistar titulos de dimensao continental e mundial, sendo campeao da America e do Mundo em 1983[12]. Tambem e'
                            +'bi-campeao da Recopa Sul-Americana, tendo conquistado este torneio em todas as vezes em que o disputou. Conquistou ainda dois Campeonatos Brasileiros da '
                            +'Serie A, um Campeonato Brasileiro da Serie B, cinco Copas do Brasil (recordista ao lado do Cruzeiro),[13] e uma Supercopa do Brasil (recordista ao lado do '
                            +'Corinthians), alem de uma Copa Sul (unico vencedor desta competicao) e um Campeonato Sul-Brasileiro (tambem sendo o unico vencedor desta competicao). Ja foi '
                            +'campeao trinta e sete vezes no Campeonato Gaucho e uma vez na Copa FGF.[14][15] O clube ja revelou varios futebolistas de renome internacional ao longo de sua '
                            +'historia, como Lucas Leiva, Emerson, Douglas Costa, Renato Portaluppi, anderson Polga e Ronaldinho Gaucho.[16][17] O Gremio e o clube de futebol com o maior numero '
                            +'de associados no Brasil. O Tricolor gaucho possui 136.062 associados em dia, conforme dados de dezembro de 2017.[18] Em pesquisa publicada em dezembro de 2016, do '
                            +'Instituto Parana Pesquisas, com a participacao de 10.500 brasileiros de 22 estados, alem do Distrito Federal, apontou-se que o valor percentual de torcedores gremistas '
                            +'e de 3,5%% dos brasileiros. O time aparece como a setima maior torcida do Pais. O estudo tambem demonstrou que na regiao Sul, os gremistas estao em maior numero de '
                            +'torcedores, correspondendo a 20,5%% dos entrevistados.[19][20] A torcida do Gremio, bastante identificada com a cultura incondicional das hinchas platinas, e considerada '
                            +'por estudos a torcida mais fanatica do Brasil, por seu engajamento, seu conhecimento sobre a historia do clube e sua disposicao em prover recursos ao Gremio atraves da compra '
                            +'de produtos e da presenca no estadio[21].',
                            'Apos o esvaziamento da bola da partida, o paulista Candido Dias da Silva, um comerciante sorocabano, emprestou a pelota que trazia. Em troca do favor, ele recebeu licoes de como '
                            +'se fundar um clube de futebol;[22] oito dias depois, trinta e dois homens se reuniram no Salao Grau, restaurante de um hotel da rua 15 de Novembro (atual Rua Jose Montauri), no '
                            +'Centro de Porto Alegre e fundaram o Gremio Foot-Ball Porto Alegrense.[23] O primeiro jogo do recem fundado clube ocorreu em 6 de marco de 1904, contra o FussBall Club Porto Alegre, '
                            +'fundado no mesmo dia que o Gremio. Em uma jornada dupla (dois jogos na mesma tarde), o Gremio garantiu as suas duas primeiras vitorias, vencendo ambas por 1 a 0.[22] Em 20 de julho '
                            +'de 1904, o uniforme foi mudado para um modelo metade azul metade preto.[22] A primeira competicao disputada foi a Taca Wanderpreiss, com a primeira edicao em 6 de marco de 1904, vencido '
                            +'pelo Gremio contra o Fussball Club Porto Alegre.[23] Alguns anos depois, em 18 de julho de 1909, o primeiro jogo contra o Sport Club Internacional, que mais tarde se tornaria o seu '
                            +'arquirrival, foi disputado, com vitoria de 10 a 0 para os tricolores. No ano seguinte, foi criada a 1ª Liga de Clubes de Porto Alegre, por ideia vinda do Gremio. Posteriormente, foi '
                            +'realizado o Campeonato Citadino de Porto Alegre, o qual o Tricolor venceu ininterruptamente de 1911 a 1915. Mesmo amador, o clube ja jogava contra equipes de outros estados, ou ate mesmo '
                            +'paises.[23] Na decada seguinte, a hegemonia do clube continuou. O pentacampeonato metropolitano (1919-1923) e o titulo de tres Campeonatos Gauchos de 1921, 1922 e 1926, Os anos 1930 continuaram '
                            +'dando animo ao desenvolvimento do Gremio. Conquistas como o tetracampeonato de Porto Alegre 1930 a 1933 e o bicampeonato gaucho 1931 e 1932.',
                            'O projeto realizado visa implementar funcionalidades do TCP. Dupla do projeto: Juliani Schlickmann Damasceno e Mateus Seenem Tavares.'], connection)



#object_client.close_connection(connection)

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

object_client.send_data(['Grêmio Foot-Ball Porto Alegrense (conhecido apenas por Grêmio e cujo acrônimo é FBPA) é um clube de futebol brasileiro da cidade de Porto Alegre,' 
                            +'no Rio Grande do Sul, fundado em 15 de setembro de 1903. Suas cores são azul, preto e branco. O clube tem como alcunhas Imortal Tricolor, Tricolor' 
                            +'dos Pampas, Tricolor Gaúcho e Rei de Copas, devido ao seu histórico especialmente vitorioso em competições de mata-mata.'
                            +'Já foi campeão da Copa Libertadores da América em três ocasiões (o que o torna o clube brasileiro com mais conquistas nesta competição, ao lado de' 
                            +'São Paulo e Santos) e vice em duas outras oportunidades, sendo o único clube brasileiro a ter decidido a competição em quatro décadas diferentes.[11]' 
                            +'É o primeiro clube fora do Sudeste a conquistar títulos de dimensão continental e mundial, sendo campeão da América e do Mundo em 1983[12]. Também é' 
                            +'bi-campeão da Recopa Sul-Americana, tendo conquistado este torneio em todas as vezes em que o disputou. Conquistou ainda dois Campeonatos Brasileiros da '
                            +'Série A, um Campeonato Brasileiro da Série B, cinco Copas do Brasil (recordista ao lado do Cruzeiro),[13] e uma Supercopa do Brasil (recordista ao lado do '
                            +'Corinthians), além de uma Copa Sul (único vencedor desta competição) e um Campeonato Sul-Brasileiro (também sendo o único vencedor desta competição). Já foi '
                            +'campeão trinta e sete vezes no Campeonato Gaúcho e uma vez na Copa FGF.[14][15] O clube já revelou vários futebolistas de renome internacional ao longo de sua '
                            +'história, como Lucas Leiva, Emerson, Douglas Costa, Renato Portaluppi, Ânderson Polga e Ronaldinho Gaúcho.[16][17] O Grêmio é o clube de futebol com o maior número '
                            +'de associados no Brasil. O Tricolor gaúcho possui 136.062 associados em dia, conforme dados de dezembro de 2017.[18] Em pesquisa publicada em dezembro de 2016, do '
                            +'Instituto Paraná Pesquisas, com a participação de 10.500 brasileiros de 22 estados, além do Distrito Federal, apontou-se que o valor percentual de torcedores gremistas '
                            +'é de 3,5% dos brasileiros. O time aparece como a sétima maior torcida do País. O estudo também demonstrou que na região Sul, os gremistas estão em maior número de '
                            +'torcedores, correspondendo à 20,5% dos entrevistados.[19][20] A torcida do Grêmio, bastante identificada com a cultura incondicional das hinchas platinas, é considerada '
                            +'por estudos a torcida mais fanática do Brasil, por seu engajamento, seu conhecimento sobre a história do clube e sua disposição em prover recursos ao Grêmio através da compra '
                            +'de produtos e da presença no estádio[21].', 
                            'Após o esvaziamento da bola da partida, o paulista Candido Dias da Silva, um comerciante sorocabano, emprestou a pelota que trazia. Em troca do favor, ele recebeu lições de como '
                            +'se fundar um clube de futebol;[22] oito dias depois, trinta e dois homens se reuniram no Salão Grau, restaurante de um hotel da rua 15 de Novembro (atual Rua José Montauri), no '
                            +'Centro de Porto Alegre e fundaram o Grêmio Foot-Ball Porto Alegrense.[23] O primeiro jogo do recém fundado clube ocorreu em 6 de março de 1904, contra o FussBall Club Porto Alegre, '
                            +'fundado no mesmo dia que o Grêmio. Em uma jornada dupla (dois jogos na mesma tarde), o Grêmio garantiu as suas duas primeiras vitórias, vencendo ambas por 1 a 0.[22] Em 20 de julho '
                            +'de 1904, o uniforme foi mudado para um modelo metade azul metade preto.[22] A primeira competição disputada foi a Taça Wanderpreiss, com a primeira edição em 6 de março de 1904, vencido '
                            +'pelo Grêmio contra o Fussball Club Porto Alegre.[23] Alguns anos depois, em 18 de julho de 1909, o primeiro jogo contra o Sport Club Internacional, que mais tarde se tornaria o seu '
                            +'arquirrival, foi disputado, com vitória de 10 a 0 para os tricolores. No ano seguinte, foi criada a 1ª Liga de Clubes de Porto Alegre, por ideia vinda do Grêmio. Posteriormente, foi '
                            +'realizado o Campeonato Citadino de Porto Alegre, o qual o Tricolor venceu ininterruptamente de 1911 a 1915. Mesmo amador, o clube já jogava contra equipes de outros estados, ou até mesmo '
                            +'países.[23] Na década seguinte, a hegemonia do clube continuou. O pentacampeonato metropolitano (1919-1923) e o título de três Campeonatos Gaúchos de 1921, 1922 e 1926, Os anos 1930 continuaram '
                            +'dando ânimo ao desenvolvimento do Grêmio. Conquistas como o tetracampeonato de Porto Alegre 1930 a 1933 e o bicampeonato gaúcho 1931 e 1932.',
                            'O projeto realizado visa implementar funcionalidades do TCP. Dupla do projeto: Juliani Schlickmann Damasceno e Mateus Seenem Tavares.'], connection)



#object_client.close_connection(connection)

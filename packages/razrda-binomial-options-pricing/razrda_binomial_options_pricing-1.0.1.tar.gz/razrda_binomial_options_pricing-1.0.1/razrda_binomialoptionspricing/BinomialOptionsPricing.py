import math
import networkx
import matplotlib.pyplot as plt


#BINOMIAL OPTIONS PRICING MUHAMMAD RAZA



class vanilla_binomial:
    #Muhammad Raza
    def __init__(self, s, K, T, R,div,n,h, draw_graph, vol=None, u=None, d=None, call=True, american=False, discrete_div=False):
        self.h = h
        self.s = s
        self.american=american
        self.div = div
        self.discrete_div=False
        self.vol=vol
        self.K= K
        self.T =T
        self.n= n
        if vol!=None:
            if discrete_div ==True:
                u = math.exp(vol*math.sqrt(self.h))
                d = 1/u
            else:
                u = math.exp((R - div) * self.h + (vol * math.sqrt(self.h)))
                d = math.exp((R - div) * self.h - (vol * math.sqrt(self.h)))

        self.call = call
        self.u = u
        self.d = d
        self.R = R

        if self._check_arbritrage() == True:
            print("incomplete market")
        self.draw_graph =draw_graph
        self.qu, self.qd = self.martingale_probability_measures()
        self.graph = networkx.Graph()

    def martingale_probability_measures(self):
        if self.discrete_div==False:
            return (math.exp((self.R - self.div)*self.h) -self.d )/ (self.u - self.d), (self.u - math.exp((self.R- self.div)*self.h)) / (self.u - self.d)
        else:
            return (math.exp((self.R)*self.h) -self.d )/ (self.u - self.d), (self.u - math.exp((self.R)*self.h)) / (self.u - self.d)
    def replicated_portfolio_weights(self,phi_d, phi_u, u, d, currnet_n, s):
        print(currnet_n)
        if currnet_n != 0:
            return float(math.exp(-self.R*currnet_n) * (((u * phi_d) - (d * phi_u)) / (u - d))), math.exp(-self.div*currnet_n)*( ((phi_u - phi_d) / (s*(u - d))))
        else:
            return float(math.exp(-self.R * (currnet_n+1)) * (((u * phi_d) - (d * phi_u)) / (u - d))), math.exp(
                -self.div * (currnet_n+1)) * (((phi_u - phi_d) / (s * (u - d))))

    def expected_value_martingale_measure(self,qu, qd, phiu, phid, R):
        return ((qu * phiu) + (qd * phid)) / (1 + R)
    def _check_arbritrage(self):
        return True if 1+self.R > self.u or 1+self.R < self.d else False

    def _create_inital_graph(self):

        n_nodes = sum([n for n in range(1, self.n + 2)])

        an = [l for l in range(n_nodes)]
        self.graph.add_nodes_from(an)

        degree_index = 0
        degree_n_nodes = []

        for s_i in range(n_nodes):
            if s_i < max(an[:-self.n]):
                if len(degree_n_nodes) + 1 > (degree_index + 1):
                    degree_index += 1
                    del degree_n_nodes[:]
                degree_n_nodes.append(0)
                if s_i == 0:
                    self.graph.nodes[s_i].update({"price": self.s})
                    self.graph.nodes[s_i + 1].update({"price": self.s * self.u})
                    self.graph.nodes[s_i + 2].update({"price": self.s * self.d})
                    self.graph.add_edge(s_i, s_i + 1)
                    self.graph.add_edge(s_i, s_i + 2)

                else:

                    self.graph.nodes[s_i + degree_index + 1].update({"price": self.graph.nodes[s_i]['price'] * self.u})
                    self.graph.nodes[s_i + degree_index + 2].update({"price": self.graph.nodes[s_i]['price'] * self.d})
                    self.graph.add_edge(s_i, s_i + degree_index + 1)
                    self.graph.add_edge(s_i, s_i + degree_index + 2)
            else:
                if self.K == 0:
                    p = self.s
                else:
                    p = self.K
                value = self.graph.nodes[s_i]['price'] - p if self.call==True else  p -self.graph.nodes[s_i]['price']
                self.graph.nodes[s_i].update({"value": max(value, 0)})
    def compute_values(self):
        self._create_inital_graph()
        
        n_nodes = sum([n for n in range(1, self.n + 2)])
        nds = [l for l in range(n_nodes - (self.n + 1))]

        for degree, f in zip(reversed(range(self.n)), range(self.n)):

            n_node = nds[-(degree + 1):]

            for s_i in n_node:
                phiu = self.graph.nodes[s_i + degree + 1]['value']

                phid = self.graph.nodes[s_i + degree + 2]['value']



                x, y = self.replicated_portfolio_weights(phid, phiu, self.u, self.d,self.h, self.graph.nodes[s_i]['price'])

                portfolio_value =  x + (y * self.graph.nodes[s_i]['price'])

                if self.american == True:
                    american_value = max(self.graph.nodes[s_i]['price'] - self.K if self.call==True else  self.K -self.graph.nodes[s_i]['price'],portfolio_value)
                    if american_value > portfolio_value:
                        self.graph.nodes[s_i]['early_ex']= 'TRUE'
                    else:
                        self.graph.nodes[s_i]['early_ex']= 'FALSE'
                    portfolio_value = american_value

                self.graph.nodes[s_i].update({"value": portfolio_value, "x": x, "y": y})

            del nds[-(degree + 1):]

    def show_graph(self):


        for n in range(sum([n for n in range(1, self.n + 2)])):
            print(self.graph.nodes[n])
        networkx.draw(self.graph, with_labels=True)
        plt.show()






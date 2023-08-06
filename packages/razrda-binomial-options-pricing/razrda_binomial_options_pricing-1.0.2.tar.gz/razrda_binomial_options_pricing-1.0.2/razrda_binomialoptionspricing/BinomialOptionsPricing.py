import networkx
import math
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')




'''Visualize Binomial Options Pricing (not meant for large scale n)

Currently supports American and European options pricing, replicating portfolio positions and probabilities 

'''






class vanilla_binomial:
    '''
    Parameters:
        s= price: float
        K = strike price of the claim: float, int
        n = periods: int
        T = expiration, terminal period: int
        h = delta, typically n/T : float
        R = intererst rate: float
        u = up multiplier: float
        d = down multiplier: float
        ##CAN USE VOL INSTEAD OF U and d
        vol = volatility : float
        call = True if claim is a call else False: Boolean
        american = True if claim is american esle False: Boolean


    EXAMPLE:
        #Price a European claim with current price 41, strike 40, periods 3, time to experiation 1, and given up and down multiplier
        pricing = vanilla_binomial(K=40, n=3, h=1/3,T=1, R=.08,u=1.4623, d=.8025, div=0, s=41, call=True, american=False)
        #compute the graph and values
        pricing.compute_values()
        #show the graph
        pricing.show_graph()
        #show the details of each node
        pricing.show_all_nodes()
    '''
    def __init__(self, s, K, T, R, h,div, n,  vol=None, u=None, d=None, call=True, american=False ):
        self.h = h
        self.s = s
        self.american = american
        self.div = div
        self.discrete_div = False
        self.vol = vol
        self.K = K
        self.T = T
        self.n = n
        if vol != None:
            u = math.exp((R - div) * self.h + (vol * math.sqrt(self.h)))
            d = math.exp((R - div) * self.h - (vol * math.sqrt(self.h)))
        self.call = call
        self.u = u
        self.d = d
        self.R = R

        if self._check_arbritrage() == True:
            print("incomplete market")

        self.qu, self.qd = self._martingale_probability_measures()
        self.graph =networkx.Graph()
        self.price = 0

    def _martingale_probability_measures(self):

        return (math.exp((self.R ) * self.h) - self.d) / (self.u - self.d), (
                        self.u - math.exp((self.R) * self.h)) / (self.u - self.d)


    def _replicated_portfolio_weights(self, phi_d, phi_u, u, d, currnet_n, s):
        if currnet_n != 0:
            return float(math.exp(-self.R * currnet_n) * (((u * phi_d) - (d * phi_u)) / (u - d))), math.exp(
                -self.div * currnet_n) * (((phi_u - phi_d) / (s * (u - d))))
        else:
            return float(math.exp(-self.R * (currnet_n + 1)) * (((u * phi_d) - (d * phi_u)) / (u - d))), math.exp(
                -self.div * (currnet_n + 1)) * (((phi_u - phi_d) / (s * (u - d))))

    def _expected_value_martingale_measure(self, qu, qd, phiu, phid, R):
        return ((qu * phiu) + (qd * phid)) / (1 + R)

    def _check_arbritrage(self):
        return True if 1 + self.R > self.u or 1 + self.R < self.d else False

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
                value = self.graph.nodes[s_i]['price'] - p if self.call == True else p - self.graph.nodes[s_i]['price']
                self.graph.nodes[s_i].update({'options value': max(value, 0)})


    def compute_values(self):
        self._create_inital_graph()
        n_nodes = sum([n for n in range(1, self.n + 2)])
        nds = [l for l in range(n_nodes - (self.n + 1))]
        for degree in  reversed(range(self.n)):
            n_node = nds[-(degree + 1):]
            for s_i in n_node:
                phiu = self.graph.nodes[s_i + degree + 1]['options value']

                phid = self.graph.nodes[s_i + degree + 2]['options value']

                x, y = self._replicated_portfolio_weights(phid, phiu, self.u, self.d, self.h,
                                                         self.graph.nodes[s_i]['price'])


                portfolio_value = x + (y * self.graph.nodes[s_i]['price'])

                if self.american == True:
                    american_value = max(self.graph.nodes[s_i]['price'] - self.K if self.call == True else self.K -
                                                                                                           self.graph.nodes[
                                                                                                               s_i][
                                                                                                               'price'],
                                         portfolio_value)
                    if american_value > portfolio_value:
                        self.graph.nodes[s_i]['early_ex'] = 'TRUE'
                    else:
                        self.graph.nodes[s_i]['early_ex'] = 'FALSE'
                    portfolio_value = american_value

                self.graph.nodes[s_i].update({'options value': portfolio_value, "bond": x, "stock": y})



            del nds[-(degree + 1):]
        
        print("Option Value: ",self.graph.nodes[0]['options value'])


    def show_all_nodes(self):
        current_level = 1
        n_iteration = current_level + 1
        print("Period", 0)
        print(self.graph.nodes[list(self.graph.nodes.keys())[0]])
        for n in self.graph.nodes:
            if n !=list(self.graph.nodes.keys())[0]:
                if n_iteration==current_level+1:
                    print("Period", str(current_level * self.T) + "/" + str(self.n))

                    print(self.graph.nodes[n])
                else:
                    print(self.graph.nodes[n])
                n_iteration -= 1
                if n_iteration == 0:
                    current_level += 1
                    n_iteration = current_level + 1
    def show_graph(self):
        new_labels= {}
        current_level= 1
        sign= current_level
        n_iteration=current_level+1
        pos= {}
        if self.call==True:
            t= 'Call'
        else:
            t= 'Put'
        for n in range(sum([n for n in range(1, self.n + 2)])):
            if 'bond' not in self.graph[n].keys():

                self.graph.nodes[n].setdefault('bond',0)
                self.graph.nodes[n].setdefault('stock', 0)
            new_labels.setdefault(n, "Level:"+str(round(self.graph.nodes[n]['price'], 3))+"\n"+"Price: "+str(round(self.graph.nodes[n]['options value'], 3))+"\n"+"Bond: "+str(round(self.graph.nodes[n]['bond'], 3))+" Stock: "+str(round(self.graph.nodes[n]['stock'], 3)))
            if n==0:
                pos.setdefault("Level:"+str(round(self.graph.nodes[n]['price'], 3))+"\n"+"Price: "+str(round(self.graph.nodes[n]['options value'], 3))+"\n"+"Bond: "+str(round(self.graph.nodes[n]['bond'], 3))+" Stock: "+str(round(self.graph.nodes[n]['stock'], 3)),(n,n))
                self.price= str(round(self.graph.nodes[n]['options value'], 3))
            else:
                pos.setdefault("Level:"+str(round(self.graph.nodes[n]['price'], 3))+"\n"+"Price: "+str(round(self.graph.nodes[n]['options value'], 3))+"\n"+"Bond: "+str(round(self.graph.nodes[n]['bond'], 3))+" Stock: "+str(round(self.graph.nodes[n]['stock'], 3)), (current_level, sign))

                n_iteration-=1
                sign-=2

                if n_iteration == 0:
                    current_level+=1
                    sign=current_level
                    n_iteration =current_level+1
        networkx.relabel_nodes(self.graph,new_labels, copy=False)


        networkx.draw_networkx(self.graph, with_labels=True, pos=pos, node_size=50, node_color='yellow', node_shape='.', font_size=9, edge_color='black')
        ax = plt.axes()
        plt.xlim(-1,current_level)

        plt.ylim(current_level,-current_level)
        ax.set_facecolor('silver')

        ax.legend([t+' Price: '+str(self.price)], loc='upper left')
        plt.show()










from razrda_binomialoptionspricing import BinomialOptionsPricing



pricing = vanilla_binomial(K=40, n=3, h=1,T=1, R=.08,u=1.4623, d=.8025, div=0, s=41, call=True, american=False)
pricing.compute_values()
pricing.show_graph()
pricing.show_all_nodes()

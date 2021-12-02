from starcli.draw_graph import draw_graph,draw_top_rep_graphs

def test_draw_graph():
    reponame = 'hedyhli/starcli'
    auth = 'tongjin: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'
    draw_graph(reponame,auth,path=None,graph_time_unit='monthly',category='star')
    draw_graph(reponame,auth,path=None,graph_time_unit='yearly',category='star')
    draw_graph(reponame,auth,path=None,graph_time_unit='monthly',category='fork')
    draw_graph(reponame,auth,path=None,graph_time_unit='yearly',category='fork')

def test_draw_graph():
    reponame = ['hedyhli/starcli', 'hedyhli/gtrending','hedyhli/passibility'] 
    auth = 'tongjin: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'
    draw_top_rep_graphs(reponame,auth,path=None,graph_time_unit='monthly',category='star')
    draw_top_rep_graphs(reponame,auth,path=None,graph_time_unit='yearly',category='star')
    draw_top_rep_graphs(reponame,auth,path=None,graph_time_unit='monthly',category='fork')
    draw_top_rep_graphs(reponame,auth,path=None,graph_time_unit='yearly',category='fork')
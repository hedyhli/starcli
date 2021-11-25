""" starcli.search """
import re
from typing import Dict
import github
from github import Github
import math
import requests
from requests import auth
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_dict_add(plot_dict,datetime_i,graph_time_unit,repo_index=-1,num_repos = -1):
    assert(graph_time_unit == 'monthly' or graph_time_unit == 'yearly')
    if repo_index ==-1:
        if graph_time_unit == 'monthly':
            key_i = str(datetime_i.year)+"-" + str(datetime_i.month)
            if key_i in plot_dict.keys():
                plot_dict[key_i] +=1
            else:
                plot_dict[key_i] = 1
        elif graph_time_unit == 'yearly':
            key_i = str(datetime_i.year)
            if key_i in plot_dict.keys():
                plot_dict[key_i] +=1
            else:
                plot_dict[key_i] = 1
        else:
            pass    
        return plot_dict
    else:
        if graph_time_unit == 'monthly':
            key_i = str(datetime_i.year)+"-" + str(datetime_i.month)
            if key_i not in plot_dict.keys():
                plot_dict[key_i] = np.zeros((num_repos))
            plot_dict[key_i][repo_index] +=1    
        elif graph_time_unit == 'yearly':
            key_i = str(datetime_i.year)
            if key_i not in plot_dict.keys():
                plot_dict[key_i] = np.zeros((num_repos))
            plot_dict[key_i][repo_index] +=1    
        else:
            pass    
        return plot_dict

def draw_graph(reponame,auth,path=None,graph_time_unit='monthly',category='star'):
    assert(reponame != '')
    assert(graph_time_unit == 'monthly' or graph_time_unit == 'yearly')
    assert(category == 'star' or category == 'fork')
    # todo: check how to save in the same folder
    # assert(os.path.exists(path))
    auth_key = auth.split(":")[1]
    g = Github(auth_key)
    repo = g.get_repo(reponame)
    plot_dict = dict()
    if category == 'star':
        for item in repo.get_stargazers_with_dates():
            datetime_i = item.starred_at
            plot_dict = plot_dict_add(plot_dict,datetime_i,graph_time_unit)
    elif category == 'fork':
        for item in repo.get_forks():
            datetime_i = item.created_at
            plot_dict = plot_dict_add(plot_dict,datetime_i,graph_time_unit)
    else:
        pass
    plt_x = list(plot_dict.keys())
    plt_y = list(plot_dict.values())
    if category == 'fork':
        plt_x.reverse()
        plt_y.reverse()
    for ind in range(len(plt_y)):
        if ind>0:
            plt_y [ind] += plt_y [ind-1]
    
    plt.xlabel("Time")
    if category == 'star':
        plt.plot(plt_x, plt_y, marker='*', ms=10)
        plt.ylabel("Stargazers") 
        plt.title(reponame + "'s stargazers over time")
    elif category == 'fork':
        plt.plot(plt_x, plt_y, marker='.', ms=10)
        plt.ylabel("Forks") 
        plt.title(reponame + "'s forks over time")
    else:
        pass
    plt.xticks(plt_x,plt_x,rotation=60)
    
    plt.text(plt_x[-1], plt_y[-1], plt_y[-1], ha='center', va='bottom')
    if path is None:
        plt.show()
    else:
        reponame = reponame.replace("/","-")
        plt.savefig(os.path.join(path, reponame + "_stargazers_over_time"))

def sort_date(date_time):
    if "-" in date_time:
        yaer_month = date_time.split("-")
        return int(yaer_month[0])*12 + int(yaer_month[1])
    else:
        return int(date_time)

def draw_top_rep_graphs(repos_name,auth,path=None,graph_time_unit='monthly',category='star'):
    assert(len(repos_name) > 0 and len(repos_name) < 20)
    assert(graph_time_unit == 'monthly' or graph_time_unit == 'yearly')
    assert(category == 'star' or category == 'fork')
    # todo: check how to save in the same folder
    # assert(os.path.exists(path))
    auth_key = auth.split(":")[1]
    g = Github(auth_key)
    plot_dict = dict()
    for ind,repo_i_name in enumerate(repos_name):
        print("Fetching data from " + repo_i_name)
        repo = g.get_repo(repo_i_name)
        if category == 'star':
            for item in repo.get_stargazers_with_dates():
                datetime_i = item.starred_at
                plot_dict = plot_dict_add(plot_dict,datetime_i,graph_time_unit,repo_index=ind,num_repos=len(repos_name))
        elif category == 'fork':
            for item in repo.get_forks():
                datetime_i = item.created_at
                plot_dict = plot_dict_add(plot_dict,datetime_i,graph_time_unit,repo_index=ind,num_repos=len(repos_name))
        else:
            pass
    # print("All data feteched and start to process data")
    plt_x_raw = list(plot_dict.keys())
    plt_x = plt_x_raw.copy()
    plt_x.sort(key=sort_date)
    plt_y_raw = list(plot_dict.values())
    plt_y = []
    for datetime_i in plt_x:
        corresponding_index = plt_x.index(datetime_i)
        # print(plt_y)
        # print(plt_y_raw[corresponding_index])
        if len(plt_y) !=0:
            plt_y.append(plt_y_raw[corresponding_index] + plt_y[-1])
        else:
            plt_y.append(plt_y_raw[corresponding_index])
    plt_y = np.array(plt_y)
    # print("Data processed and start to plot")
    for ind in range(plt_y.shape[1]):
        if category == 'star':
            plt.plot(plt_x, plt_y[:,ind], marker='*', ms=10)
        elif category == 'fork':
            plt.plot(plt_x, plt_y[:,ind], marker='.', ms=10)
        else:
            pass
        plt.text(plt_x[-1], plt_y[-1,ind],plt_y[-1,ind], ha='center', va='bottom')
    plt.xticks(plt_x,plt_x,rotation=60)
    plt.xlabel("Time")
    if category == 'star':
        plt.ylabel("Stargazers") 
        plt.title("Top repos' stargazers over time")
    elif category == 'fork':
        plt.ylabel("Forks") 
        plt.title("Top repos' forks over time")
    else:
        pass
    
    if path is None:
        plt.show()
    else:
        reponame = repos_name.replace("/","-")
        plt.savefig(os.path.join(path, reponame + "_stargazers_over_time"))

# reponame = ['hedyhli/starcli', 'hedyhli/gtrending'] 
# auth = 'tongjin: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'
# draw_top_rep_graphs(reponame,auth,graph_time_unit='monthly',category='fork')

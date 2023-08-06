# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np
import pandas as pd
import math
from graphviz import *
from subprocess import check_call
from decimal import Decimal

'''Global variables specified here that are used for storing data'''
pathways_filename = ''
output_directory_name = ''
image_directory_name = ''
# User-options!
arrow_type = 'double' # Options allowed should be single or double
label_type = 'net' # Options net, both, all labels on the edges
Rank_Sep = 0.75
Node_Sep = 0.75

#inputs = pd.read_csv(pathways_filename, header = 0, delimiter = '\t')

def print_header_species(fname, Rank_Sep, Node_Sep):
    '''
    This function generates the code for the header of the species visualization file
    
        fname : Visualization filename
        Rank_Sep : Vertical distance between nodes (if rankdir = TB)
                    Horizontal distance between nodes (if rankdir = LR)
        Node_Sep : Horizontal distance between nodes (if rankdir = TB)
                    Vertical distance between nodes (if rankdir = LR)          
    '''
    f = open(fname, "w+")
    f.write('digraph G {\n')
    f.write('splines = true;\n')
    f.write('graph [bgcolor=lightgray, resolution=64, fontname=Arial, fontcolor=blue, fontsize=36];\n')
    f.write('node [fontsize=12];\n')
    f.write('edge [fontsize=45];\n') #set312,, colorscheme=paired12
    f.write('label = "Reaction Path Analysis";\n')
    f.write('labelloc = "t";\n')
    f.write('center=1;\n')
    f.write('size="10,10";\n')
    f.write('ranksep="' + str(Rank_Sep) + ' equally";\n')
    f.write('nodesep="' + str(Node_Sep) + ' equally";\n')
    f.write('rankdir=LR;\n')
    f.write('bgcolor=white;\n')
    f.close()

def input_pathways_file(fname):
    global pathways_filename
    pathways_filename = fname
    
def input_output_directory(fname):
    '''
    This specifies the output directory desired where all the visualizations generated are stored.
    '''
    global output_directory_name
    output_directory_name = fname
    
def input_images_directory(fname):
    '''
    This specifies the output directory desired where all the visualizations generated are stored.
    '''
    global image_directory_name
    image_directory_name = fname
    
def input_species_population(spec_pop):
    global species_populations
    for i in range(len(spec_pop)):
        spec_pop[i] = float(spec_pop[i])
    species_populations = spec_pop


def generate_pathway_visualizations():
    #pathways_filename = ''
    #pathways_filename = 'paths_opposite_orientation.txt'
    pathway_graphviz = 'pathway_visualization.txt'
    identified_pathways = []
    pathway_types = []
    New_pathway_found = False
    All_pathways = []
    All_pathways_types = []
    All_pathways_num_type = []
    All_pathways_rates = []
    All_pathways_fwd_rates = []
    All_pathways_rev_rates = []
    All_pathways_RLS = []
    All_pathways_RLS_reactant = []
    All_pathways_RLS_product = []
    pathway_cycle = []
    pathway_cycle_rates = []
    pathway_cycle_fwd_rates = []
    pathway_cycle_rev_rates = []
    Maximum_rate = -1E30
    Minimum_rate = 1E30
    species_directory = { 0:'000000', 1:'000001', 2:'000010', 3:'000011', 4:'000100', 5:'000101',
                         6:'000110', 7:'000111', 8:'001000', 9:'001001', 10:'001010', 11:'001011',
                         12:'001100',13:'001101',14:'001110',
                         15:'001111',16:'010000', 17:'010001',18:'010010',
                         19:'010011',20:'010100',21:'010101',22:'010110',23:'010111',24:'011000',25:'011001',
                         26:'011010',27:'011011',28:'011100',29:'011101',30:'011110',31:'011111',32:'100000',
                         33:'100001',34:'100010',35:'100011',36:'100100',37:'100101',38:'100110',
                         39:'100111',40:'101000',41:'101001',42:'101010',43:'101011',44:'101100',
                         45:'101101',46:'101110',47:'101111',48:'110000',49:'110001',50:'110010',
                         51:'110011',52:'110100',53:'110101',54:'110110',55:'110111',56:'111000',
                         57:'111001',58:'111010',59:'111011',60:'111100',61:'111101',62:'111110',
                         63:'111111' }
    
    color_scheme = {1:'black',2:'blue',3:'blueviolet',4:'brown',5:'cadetblue',
                    6:'chocolate',7:'crimson',8:'darkblue',9:'darkgoldenrod',10:'darkgreen',
                    11:'darkmagenta',12:'darkred',13:'deeppink',14:'indigo',15:'red',
                    16:'darkslateblue'}
    
    #Creating a new folder for species
    species_output_dir = ''
    species_output_dir = os.path.join(str(species_output_dir), str(output_directory_name))
    species_output_dir = os.path.join(str(species_output_dir), 'Species_pathways/')
#    print(species_output_dir)
    check_species = os.path.exists(species_output_dir)
    if check_species == False:
        os.mkdir(species_output_dir)
    
    output_directory_name_spec = str(output_directory_name) + str('Species_pathways/')
    src_files = os.listdir(image_directory_name)
    for file_name in src_files:
        full_file_name = os.path.join(image_directory_name, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, output_directory_name)
            shutil.copy(full_file_name, output_directory_name_spec)
            shutil.copy(full_file_name, './')
    print('Files copied successfully!')
    
    
    with open(pathways_filename, 'r') as inputs:
        for line in inputs:
            line = line.replace('\n', '')
            line = line.replace(':', '')
            line = line.replace('(', '')
            line = line.replace(')', '')
            line = line.replace('*', '')
            line = line.replace(',', '')
            words = line.split()
            #print(words)
            if len(words) > 0:
                if words[0] == 'Paths':
                    #print(words[4],words[5],words[6],words[7])
                    pathway_type = {'Cl':words[5], 'H':words[7]}
                    pathway_types.append(pathway_type)
                
                if words[0] == 'Path':
                    New_pathway_found = True
                    #print(words[1],words[4],words[7],words[8])
                    All_pathways_RLS.append(words[4])
                    All_pathways_RLS_reactant.append(words[7])
                    All_pathways_RLS_product.append(words[8])
                    if len(pathway_cycle) > 0:
                        All_pathways.append(pathway_cycle)
                        All_pathways_rates.append(pathway_cycle_rates)
                        All_pathways_fwd_rates.append(pathway_cycle_fwd_rates)
                        All_pathways_rev_rates.append(pathway_cycle_rev_rates)
                        pathway_temp = {len(pathway_types):pathway_cycle}
                        All_pathways_types.append(pathway_temp)
                        pathway_num_type = {len(All_pathways):len(pathway_types)}
                        All_pathways_num_type.append(pathway_num_type)
                        pathway_cycle = []
                        pathway_cycle_rates = []
                        pathway_cycle_fwd_rates = []
                        pathway_cycle_rev_rates = []
                    
                if words[0] != 'Paths' and words[0] != 'Path':
                    pathway_cycle.append(words[0])
                    if len(words) > 7:
                        #print(words[7])
                        if float(words[7]) >= float(Maximum_rate):
                            Maximum_rate = words[7]
                        if float(words[7]) <= float(Minimum_rate):
                            Minimum_rate = words[7]
                        pathway_cycle_rates.append(words[7])
                        pathway_cycle_fwd_rates.append(words[7])
                        pathway_cycle_rev_rates.append(words[8])
                    
            if len(words) == 0:
                if len(pathway_cycle) > 0:
                    All_pathways.append(pathway_cycle)
                    All_pathways_rates.append(pathway_cycle_rates)
                    All_pathways_fwd_rates.append(pathway_cycle_fwd_rates)
                    All_pathways_rev_rates.append(pathway_cycle_rev_rates)
                    pathway_temp = {len(pathway_types):pathway_cycle}
                    All_pathways_types.append(pathway_temp)
                    pathway_num_type = {len(All_pathways):len(pathway_types)}
                    All_pathways_num_type.append(pathway_num_type)
                    pathway_cycle = []
                    pathway_cycle_rates = []
                    pathway_cycle_fwd_rates = []
                    pathway_cycle_rev_rates = []
                    
             
        #print(len(pathway_types))
        #print(All_pathways)
        #print(len(All_pathways))
        #print(pathway_types)
        #print(All_pathways_types)
        #print(All_pathways_num_type)
        #print(All_pathways_RLS)
        #print(All_pathways_RLS_reactant)
        #print(All_pathways_RLS_product)
        #print(All_pathways_rates)
        #print(Maximum_rate)
        #print(Minimum_rate)
        
        #Creating single visualization with all pathways
        
        filename = pathway_graphviz
        pre, ext = os.path.splitext(filename)
        filename = os.path.join(str(output_directory_name), str(filename))
        filename_svg = os.path.join(str(output_directory_name),
                                str(pre) + '.svg')
        #print(filename, filename_svg)
        f = open(filename, "w+")
        f.write('digraph G {\n')
        f.write('splines = true;\n')
        f.write('overlap = false;\n')
        f.write('esep=3;\n')
        f.write('linesep=2.0;\n')
        f.write('graph [bgcolor=lightgray, resolution=64, fontname=Arial, fontcolor=blue, fontsize=36];\n')
        f.write('node [fontsize=12];\n')
        f.write('edge [fontsize=45];\n') #set312,, colorscheme=paired12
        f.write('label = "Reaction Path Analysis";\n')
        f.write('labelloc = "t";\n')
        f.write('center=1;\n')
        f.write('size="10,10";\n')
        f.write('ranksep="' + str(2*Rank_Sep) + ' equally";\n')
        f.write('nodesep="' + str(Node_Sep) + ' equally";\n')
        f.write('rankdir=LR;\n')
        f.write('bgcolor=white;\n')
        
        Species_Processed = []
        
        for i in range(len(All_pathways)):
            pathway_t = All_pathways[i]
            pathway_r = All_pathways_rates[i]
            pathway_fwd_r = All_pathways_fwd_rates[i]
            pathway_rev_r = All_pathways_rev_rates[i]
            
            #print(pathway_t)
            for j in range(len(pathway_t)):
                if (Species_Processed.count(pathway_t[j]) == 0):
                    Species_Processed.append(pathway_t[j])
                if j < len(pathway_t) - 1:
                    #linewidth = abs(int((float(pathway_r[j])*10)/float(Maximum_rate))) + 5
                    linewidth = min(max(int((math.log10(float(pathway_r[j]))*5) + 12),1),14)
                    netrate = abs(float(pathway_fwd_r[j]) - float(pathway_rev_r[j]))
                    linewidth_d = min(max(int((math.log10(float(netrate))*5) + 12),1),14)
                    linewidth1 = 12
                    #arrowsize = abs(int((float(pathway_r[j])*10)/(float(Maximum_rate)*12))) + 1
                    #arrowsize = int((math.log10(float(pathway_r[j]))/10) + 2)
                    #arrowsize = linewidth/10
                    if str(All_pathways_RLS_reactant[i]) == str(pathway_t[j]) and str(All_pathways_RLS_product[i]) == str(pathway_t[j+1]):
                        if (arrow_type == 'single'):
                            f.write('edge[dir="forward",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=60,label="   ' + str(pathway_r[j]) + str('*') + '"];\n')
                        elif (arrow_type == 'double'):
                            #f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-20, arrowhead = lnormal, arrowtail = lnormal,color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=60,headlabel="  ' + str(pathway_fwd_r[j]) + str('*') + '",label = " ", taillabel="     ' + str(pathway_rev_r[j]) + str('*') +'"];\n')
                            f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=60,label="   ' + str('%.1E' % Decimal(netrate)) + str('*') + '"];\n')
                            #f.write('edge[dir="forward",style="setlinewidth(' + str(linewidth) + ')",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=60,label="   ' + str(pathway_r[j]) + str('*') + '"];\n')
                        f.write('"' + str(pathway_t[j]) + '" -> "' + str(pathway_t[j+1]) + '"\n')
                    else:
                        if (arrow_type == 'single'):
                            f.write('edge[dir="forward",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=45,label="   ' + str(pathway_r[j]) + '"];\n')
                        elif (arrow_type == 'double'):
                            #f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-20, arrowhead = lnormal, arrowtail = lnormal, color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=45,headlabel="    ' + str(pathway_fwd_r[j]) + '",label = " ", taillabel="    ' + str(pathway_rev_r[j]) +'"];\n')
                            f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=45,label="    ' + str('%.1E' % Decimal(netrate)) + '"];\n')
                            #f.write('edge[dir="forward",style="setlinewidth(' + str(linewidth) + ')",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,fontsize=45,label="   ' + str(pathway_r[j]) + '"];\n')
                        f.write('"' + str(pathway_t[j]) + '" -> "' + str(pathway_t[j+1]) + '"\n')
                    
    #    print(Species_Processed)
        #print(species_populations)
        #print(str("{:.3f}".format(species_populations[24])))
        #print(str("{:.3f}".format(species_populations[0])))
        #Generate nodes for each of these species in output file
        for i in range(len(Species_Processed)):
            #Species_Processed[i] = Species_Processed[i].strip('\'')
            #path_temp = os.path.join(str(output_directory_name),str(species_directory[int(Species_Processed[i])]))
            #path_temp = str('../.') + str(path_temp)
            #f.write('"' + str(Species_Processed[i]) + '"[width=5, height=5, fixedsize=true, imagescale = true, shape=box,image="' + str(path_temp) + '.png", label = "",URL="' + str("Species\\") + str(int(Species_Processed[i])) + '.svg"];\n')
            if (arrow_type == 'single'):
                f.write('"' + str(Species_Processed[i]) + '"[width=5, height=8, imagepos="tc", labelloc="bc", color="white", fontsize=60, fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(Species_Processed[i])]) + '.png", label = <<b>' + str("{:.3f}".format(species_populations[int(Species_Processed[i])])) +'</b>>,URL="' + str("Species_pathways\\") + str(int(Species_Processed[i])) + '.svg"];\n')
            elif (arrow_type == 'double'):
                #f.write('"' + str(Species_Processed[i]) + '"[width=5, height=5, margin=1,fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(Species_Processed[i])]) + '.png", label = "",URL="' + str("Species_pathways\\") + str(int(Species_Processed[i])) + '.svg"];\n')
                f.write('"' + str(Species_Processed[i]) + '"[width=5, height=8, imagepos="tc", labelloc="bc", color="white", fontsize=60, fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(Species_Processed[i])]) + '.png", label = <<b>' + str("{:.3f}".format(species_populations[int(Species_Processed[i])])) +'</b>>,URL="' + str("Species_pathways\\") + str(int(Species_Processed[i])) + '.svg"];\n')
        
        #print(os.path.dirname(os.path.abspath(__file__)))
        
        
        
        #Adding buttons 
        f.write('\n')
        first_nodes = []
        f.write('subgraph cluster0{\n')
        f.write('style = "invisible";\n')
        f.write('label = "Pathway types";\n')
        for i in range(len(pathway_types)):
            firstnode = True
            clustername = str('cluster') + str(i+1)
            path_name = str(pathway_types[i])
            path_name = path_name.replace('{', '')
            path_name = path_name.replace('}', '')
            path_name = path_name.replace('\'','')
            path_name = path_name.replace(',','')
            #f.write('{\n')
            #f.write('rank="sink";\n')
            f.write('subgraph ' + str(clustername) + '{\n')
            f.write('style = "solid";\n')
            f.write('color=white;\n')
            f.write('shape=box;\n')
            f.write('rank=same;\n')
            f.write('label = "' + str(path_name) + '";\n')
            f.write('labelloc = "t";\n')
            f.write('fontsize = 50;\n')
            for j in range(len(All_pathways)):
                test_dict = All_pathways_num_type[j]
                for k in test_dict:
                    if str(test_dict[k]) == str(i+1):
                        #print(k,firstnode)
                        if firstnode:
                            firstnode = False
                            first_nodes.append(k)
                        f.write('"' + str('P_') + str(k) + '"[shape=rectangle,width=10,height=2,style="filled",fillcolor=' + str(color_scheme[k]) + ',fontsize=45,fontcolor=white,label = "' + str('Pathway ') + str(k) + ' : Flow = ' + str(All_pathways_RLS[j]) + ' cycles/ms",URL="' + str('pathway_visualization') + str(k) + '.svg"];\n')
            f.write('}\n')
            f.write('\n')
        
        f.write('}\n')
        #print(first_nodes)
        f.write('edge[arrowhead=none,arrowtail=none,style="invisible",label="",taillabel="",headlabel=""];\n')
        f.write('"' + str(All_pathways[0][0]) + '" -> "P_1"[constraint=false];\n')
        for i in range(len(first_nodes)):
            if i < len(first_nodes) - 1:
                f.write('"P_' + str(first_nodes[i]) + '" -> "P_' + str(first_nodes[i+1]) + '"\n')
        #f.write('"P_1" -> "P_6"\n')
        #f.write('"P_6" -> "P_9"\n')
        #f.write('"P_9" -> "P_12"\n')
        f.write('}\n')
        f.close()
        
        #check_call(['dot', '-Tsvg', filename, '-o', filename_svg], shell=True)#
        check_call(['dot', '-Tsvg', filename, '-o', filename_svg])#
        
        ##################################################################################
        
        #Creating visualizations for each pathway
        pre, ext = os.path.splitext(pathway_graphviz)
        multiple_visualizations = str(pre)
        for i in range(len(All_pathways)):
            fname = str(output_directory_name) + str(multiple_visualizations) + str(i+1) + str('.txt')
            fname_svg = str(output_directory_name) + str(multiple_visualizations) + str(i+1) + str('.svg')
            spec_proc_temp = []
            f = open(fname, "w+")
            f.write('digraph G {\n')
            f.write('splines = true;\n')
            f.write('graph [bgcolor=lightgray, resolution=64, fontname=Arial, fontcolor=blue, fontsize=36];\n')
            f.write('node [fontsize=12];\n')
            f.write('edge [fontsize=45];\n') #set312, colorscheme=paired12
            f.write('label = "' + str('Pathway ') + str(i+1) + ' : Flow = ' + str(All_pathways_RLS[i]) + ' cycles/ms";\n')
            f.write('labelloc = "t";\n')
            f.write('fontsize = 100;\n')
            f.write('center=1;\n')
            f.write('size="10,10";\n')
            if (arrow_type == 'single'):
                f.write('ranksep="' + str(Rank_Sep) + ' equally";\n')
                f.write('nodesep="' + str(Node_Sep) + ' equally";\n')
            elif (arrow_type == 'double'):
                f.write('ranksep="' + str(6*Rank_Sep) + ' equally";\n')
                f.write('nodesep="' + str(Node_Sep) + ' equally";\n')
            f.write('rankdir=LR;\n')
            f.write('bgcolor=white;\n')
            pathway_t = All_pathways[i]
            pathway_r = All_pathways_rates[i]
            pathway_fwd_r = All_pathways_fwd_rates[i]
            pathway_rev_r = All_pathways_rev_rates[i]
            pathway_len = len(pathway_t)
            #print(pathway_len)
            for j in range(len(pathway_t)):
                if (spec_proc_temp.count(pathway_t[j]) == 0):
                    spec_proc_temp.append(pathway_t[j])
                if j < (len(pathway_t) - 1)/2 :
                    linewidth = min(max(int((math.log10(float(pathway_r[j]))*5) + 12),1),14)
                    netrate = abs(float(pathway_fwd_r[j]) - float(pathway_rev_r[j]))
                    linewidth_d = min(max(int((math.log10(float(netrate))*5) + 12),1),14)
                    if str(All_pathways_RLS_reactant[i]) == str(pathway_t[j]) and str(All_pathways_RLS_product[i]) == str(pathway_t[j+1]):
                        if (pathway_len % 2 == 0) and j == (pathway_len/2 - 1):
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,label="                    ' + str(pathway_r[j]) + str('*') + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",labeldistance=5, labelangle=-40, arrowhead = lnormal, arrowtail = lnormal,color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,headlabel=<<font color="blue">               ' + str('%.1E' % Decimal(pathway_fwd_r[j])) + str('*') + '</font>>,label=<<br/><font color="black">   ' + str('%.1E' % Decimal(netrate)) + str('*') + '         </font>>, taillabel=<<font color="red">' + str('%.1E' % Decimal(pathway_rev_r[j])) + str('*') +'             </font>>];\n')
                            f.write('"' + str(pathway_t[j]) + '" -> "' + str(pathway_t[j+1]) + '"[constraint=false];\n')
                        else:
                            if (arrow_type == 'single'):    
                                f.write('edge[dir="forward",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,label="   ' + str(pathway_r[j]) + str('*') + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal,color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,headlabel=<<font color="blue">  ' + str('%.1E' % Decimal(pathway_fwd_r[j])) + str('*') + '   </font>>,label=<<font color="black">   ' + str('%.1E' % Decimal(netrate)) + str('*') + '      </font><br/><br/>>, taillabel=<<font color="red">     ' + str('%.1E' % Decimal(pathway_rev_r[j])) + str('*') +'</font>>];\n')
                            f.write('"' + str(pathway_t[j]) + '" -> "' + str(pathway_t[j+1]) + '"\n')
                    else:
                        if (pathway_len % 2 == 0) and j == (pathway_len/2 - 1):
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,label="                     ' + str(pathway_r[j]) + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",labeldistance=5, labelangle=-40, arrowhead = lnormal, arrowtail = lnormal, color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,headlabel=<<font color="blue">            ' + str('%.1E' % Decimal(pathway_fwd_r[j])) + '</font>>,label=<<br/><font color="black">   ' + str('%.1E' % Decimal(netrate)) + '         </font>>, taillabel=<<font color="red">' + str('%.1E' % Decimal(pathway_rev_r[j])) +'          </font>>];\n')
                            f.write('"' + str(pathway_t[j]) + '" -> "' + str(pathway_t[j+1]) + '"[constraint=false];\n')
                        else:
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,label="   ' + str(pathway_r[j]) + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal, color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,headlabel=<<font color="blue">    ' + str('%.1E' % Decimal(pathway_fwd_r[j])) + '   </font>>,label=<<font color="black">   ' + str('%.1E' % Decimal(netrate)) + '      </font><br/><br/>>, taillabel=<<font color="red">    ' + str('%.1E' % Decimal(pathway_rev_r[j])) +'</font>>];\n')
                            f.write('"' + str(pathway_t[j]) + '" -> "' + str(pathway_t[j+1]) + '"\n')
                elif j < len(pathway_t) - 1:
                    linewidth = min(max(int((math.log10(float(pathway_r[j]))*5) + 12),1),14)
                    netrate = abs(float(pathway_fwd_r[j]) - float(pathway_rev_r[j]))
                    linewidth_d = min(max(int((math.log10(float(netrate))*5) + 12),1),14)
                    if str(All_pathways_RLS_reactant[i]) == str(pathway_t[j]) and str(All_pathways_RLS_product[i]) == str(pathway_t[j+1]):
                        if (arrow_type == 'single'):
                            f.write('edge[dir="back",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,label="   ' + str(pathway_r[j]) + str('*') + '"];\n')
                        elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal,color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,headlabel=<<font color="red">  ' + str('%.1E' % Decimal(pathway_rev_r[j])) + str('*') + '    </font>>,label=<<font color="black">   ' + str('%.1E' % Decimal(netrate)) + str('*') + '      </font><br/><br/>>, taillabel=<<font color="blue">     ' + str('%.1E' % Decimal(pathway_fwd_r[j])) + str('*') +'</font>>];\n')
                        f.write('"' + str(pathway_t[j+1]) + '" -> "' + str(pathway_t[j]) + '"\n')
                    else:
                        if (arrow_type == 'single'):
                            f.write('edge[dir="back",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,label="   ' + str(pathway_r[j]) + '"];\n')
                        elif (arrow_type == 'double'):
                            f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal, color=' + str(color_scheme[i+1]) + ',fontcolor=' + str(color_scheme[i+1]) + ',weight=2,headlabel=<<font color="red">    ' + str('%.1E' % Decimal(pathway_rev_r[j])) + '    </font>>,label=<<font color="black">   ' + str('%.1E' % Decimal(netrate)) + '      </font><br/><br/>>, taillabel=<<font color="blue">    ' + str('%.1E' % Decimal(pathway_fwd_r[j])) +'</font>>];\n')
                        f.write('"' + str(pathway_t[j+1]) + '" -> "' + str(pathway_t[j]) + '"\n')
            
            for n in range(len(spec_proc_temp)):
            #Species_Processed[i] = Species_Processed[i].strip('\'')
                if (arrow_type == 'single'):    
                    f.write('"' + str(spec_proc_temp[n]) + '"[width=5, height=8, imagepos="tc", labelloc="bc", color="white", fontsize=60, fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(spec_proc_temp[n])]) + '.png", label = <<b>' + str("{:.3f}".format(species_populations[int(spec_proc_temp[n])])) + '</b>>, URL="' + str("Species_pathways\\") + str(int(spec_proc_temp[n])) + '.svg"];\n')
                elif (arrow_type == 'double'):
                    f.write('"' + str(spec_proc_temp[n]) + '"[width=5, height=8, imagepos="tc", labelloc="bc", color="white", fontsize=60, margin=1,fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(spec_proc_temp[n])]) + '.png", label = <<b>' + str("{:.3f}".format(species_populations[int(spec_proc_temp[n])])) + '</b>>,URL="' + str("Species_pathways\\") + str(int(spec_proc_temp[n])) + '.svg"];\n')
        
    
            f.write('"Original"[shape=rectangle,width=4,height=1,style="filled",fillcolor=grey,fontsize=45,fontcolor=white,label = "All Pathways",URL="pathway_visualization.svg"];\n')
            f.write('edge[dir="forward",arrowhead=none,style="invisible",label=""];\n')
            f.write('"Original" -> "' + str(pathway_t[0]) + '";\n') 
            f.write('}\n')
            f.close()
            
            check_call(['dot', '-Tsvg', fname, '-o', fname_svg], shell=True)
        
        #Creating multiple files with specific pathways
        pre, ext = os.path.splitext(pathway_graphviz)
        multiple_visualizations = str(pre)
        
        for i in range(len(pathway_types)):
            fname = str(output_directory_name) + str(multiple_visualizations) + str('_pathtypes_') + str(i+1) + str('.txt')
            fname_svg = str(output_directory_name) + str(multiple_visualizations) + str('_pathtypes_') + str(i+1) + str('.svg')
            path_name = str(pathway_types[i])
            path_name = path_name.replace('{', '')
            path_name = path_name.replace('}', '')
            path_name = path_name.replace('\'','')
            path_name = path_name.replace(',','')
            spec_proc_temp = []
            f = open(fname, "w+")
            f.write('digraph G {\n')
            f.write('splines = true;\n')
            f.write('graph [bgcolor=lightgray, resolution=64, fontname=Arial, fontcolor=blue, fontsize=36];\n')
            f.write('node [fontsize=12];\n')
            f.write('edge [fontsize=45];\n') #set312, colorscheme=paired12
            f.write('label = "' + str(path_name) + '";\n')
            f.write('labelloc = "t";\n')
            f.write('fontsize = 100;\n')
            f.write('center=1;\n')
            f.write('size="10,10";\n')
            f.write('ranksep="' + str(Rank_Sep) + ' equally";\n')
            f.write('nodesep="' + str(Node_Sep) + ' equally";\n')
            f.write('rankdir=LR;\n')
            f.write('bgcolor=white;\n')
            for j in range(len(All_pathways)):
                test_dict = All_pathways_num_type[j]
                for k in test_dict:
                    #print(k, test_dict[k])
                    if str(test_dict[k]) == str(i+1):
                        pathway_t = All_pathways[j]
                        pathway_r = All_pathways_rates[j]
                        for m in range(len(pathway_t)):
                            if (spec_proc_temp.count(pathway_t[m]) == 0):
                                spec_proc_temp.append(pathway_t[m])
                            if m < len(pathway_t) - 1:
                                #linewidth = abs(int((float(pathway_r[m])*10)/float(Maximum_rate))) + 5
                                linewidth = min(max(int((math.log10(float(pathway_r[m]))*5) + 12),1),14)
                                #linewidth = int((math.log10(float(pathway_r[m]))*5) + 12)
                                #arrowsize = abs(int((float(pathway_r[m])*10)/(float(Maximum_rate)*12))) + 1
                                #arrowsize = int((math.log10(float(pathway_r[m]))/10) + 2)
                                if str(All_pathways_RLS_reactant[j]) == str(pathway_t[m]) and str(All_pathways_RLS_product[j]) == str(pathway_t[m+1]):
                                    f.write('edge[dir="forward",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,label="   ' + str(pathway_r[m]) + str('*') + '"];\n')
                                    f.write('"' + str(pathway_t[m]) + '" -> "' + str(pathway_t[m+1]) + '"\n')
                                else:
                                    f.write('edge[dir="forward",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,label="   ' + str(pathway_r[m]) + '"];\n')
                                    f.write('"' + str(pathway_t[m]) + '" -> "' + str(pathway_t[m+1]) + '"\n')
            for n in range(len(spec_proc_temp)):
            #Species_Processed[i] = Species_Processed[i].strip('\'')
                f.write('"' + str(spec_proc_temp[n]) + '"[width=5, height=5, fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(spec_proc_temp[n])]) + '.png", label = "",URL="' + str("Species_pathways\\") + str(int(spec_proc_temp[n])) + '.svg"];\n')
        
            
            f.write('}\n')
            f.close()
        
            check_call(['dot', '-Tsvg', fname, '-o', fname_svg], shell=True)
        
        
        #Creating species files
        
        for i in range(len(Species_Processed)):
            speciescounter = int(Species_Processed[i])
            spec_proc_temp = []
            fname = str(species_output_dir) + str(speciescounter) + str('.txt')
            fname_svg = str(species_output_dir) + str(speciescounter) + str('.svg')
            print_header_species(fname, 8*Rank_Sep, 2*Node_Sep)
            f = open(fname, "a+")
            f.write('"' + str(speciescounter) + '"[width=3, height=3, fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(speciescounter)]) + '.png", label = "",URL="' + str(int(speciescounter)) + '.svg"];\n')
            
            for j in range(len(All_pathways)):
                pathway_t = All_pathways[j]
                pathway_r = All_pathways_rates[j]
                pathway_fwd_r = All_pathways_fwd_rates[j]
                pathway_rev_r = All_pathways_rev_rates[j]
                for k in range(len(pathway_t)):
                    if k > 0 and str(pathway_t[k]) == str(speciescounter):
                        if (spec_proc_temp.count(pathway_t[k-1]) == 0):
                            spec_proc_temp.append(pathway_t[k-1])
                        #linewidth = abs(int((float(pathway_r[k-1])*10)/float(Maximum_rate))) + 5
                        #linewidth = int((math.log10(float(pathway_r[k-1]))*5) + 12)
                        linewidth = min(max(int((math.log10(float(pathway_r[k-1]))*5) + 12),1),14)
                        netrate = abs(float(pathway_fwd_r[k-1]) - float(pathway_rev_r[k-1]))
                        linewidth_d = min(max(int((math.log10(float(netrate))*5) + 12),1),14)
                        #arrowsize = abs(int((float(pathway_r[k-1])*10)/(float(Maximum_rate)*12))) + 1
                        #arrowsize = int((math.log10(float(pathway_r[k-1]))/10) + 2)
                        if str(All_pathways_RLS_reactant[j]) == str(pathway_t[k-1]) and str(All_pathways_RLS_product[j]) == str(pathway_t[k]):
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,label="   ' + str(pathway_r[k-1]) + str('*') + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal,color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,headlabel="  ' + str(pathway_fwd_r[k-1]) + str('*') + '   ",label = " ", taillabel="     ' + str(pathway_rev_r[k-1]) + str('*') +'"];\n')
                            f.write('"' + str(pathway_t[k-1]) + '" -> "' + str(pathway_t[k]) + '"\n')
                        else:
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,label="   ' + str(pathway_r[k-1]) + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal, color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,headlabel="    ' + str(pathway_fwd_r[k-1]) + '   ",label = " ", taillabel="    ' + str(pathway_rev_r[k-1]) +'"];\n')
                            f.write('"' + str(pathway_t[k-1]) + '" -> "' + str(pathway_t[k]) + '"\n')                    
                    if k < len(pathway_t) - 1 and str(pathway_t[k]) == str(speciescounter):
                        if (spec_proc_temp.count(pathway_t[k+1]) == 0):
                            spec_proc_temp.append(pathway_t[k+1])
                        #linewidth = abs(int((float(pathway_r[k])*10)/float(Maximum_rate))) + 5
                        #linewidth = int((math.log10(float(pathway_r[k]))*5) + 12)
                        linewidth = min(max(int((math.log10(float(pathway_r[k]))*5) + 12),1),14)
                        netrate = abs(float(pathway_fwd_r[k]) - float(pathway_rev_r[k]))
                        linewidth_d = min(max(int((math.log10(float(netrate))*5) + 12),1),14)
                        #arrowsize = abs(int((float(pathway_r[k])*10)/(float(Maximum_rate)*12))) + 1
                        #arrowsize = int((math.log10(float(pathway_r[k]))/10) + 2)
                        if str(All_pathways_RLS_reactant[j]) == str(pathway_t[k]) and str(All_pathways_RLS_product[j]) == str(pathway_t[k+1]):
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="dashed",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,label="   ' + str(pathway_r[k]) + str('*') + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="dashed",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal,color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,headlabel="  ' + str(pathway_fwd_r[k]) + str('*') + '   ",label = " ", taillabel="     ' + str(pathway_rev_r[k]) + str('*') +'"];\n')
                            f.write('"' + str(pathway_t[k]) + '" -> "' + str(pathway_t[k+1]) + '"\n')
                        else:
                            if (arrow_type == 'single'):
                                f.write('edge[dir="forward",style="solid",penwidth="' + str(linewidth) + '",color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,label="   ' + str(pathway_r[k]) + '"];\n')
                            elif (arrow_type == 'double'):
                                f.write('edge[dir="both",style="solid",penwidth="' + str(linewidth_d) + '",labeldistance=10, labelangle=-30, arrowhead = lnormal, arrowtail = lnormal, color=' + str(color_scheme[j+1]) + ',fontcolor=' + str(color_scheme[j+1]) + ',weight=2,headlabel="    ' + str(pathway_fwd_r[k]) + '   ",label = " ", taillabel="    ' + str(pathway_rev_r[k]) +'"];\n')
                            f.write('"' + str(pathway_t[k]) + '" -> "' + str(pathway_t[k+1]) + '"\n')
           
            for m in range(len(spec_proc_temp)):
            #Species_Processed[i] = Species_Processed[i].strip('\'')
                if (arrow_type == 'single'):
                    f.write('"' + str(spec_proc_temp[m]) + '"[width=3, height=3, fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(spec_proc_temp[m])]) + '.png", label = "",URL="' + str(int(spec_proc_temp[m])) +'.svg"];\n')
                elif (arrow_type == 'double'):
                    f.write('"' + str(spec_proc_temp[m]) + '"[width=3, height=3, margin=1,fixedsize=true, imagescale = true, shape=box,image="' + str(species_directory[int(spec_proc_temp[m])]) + '.png", label = "",URL="' + str(int(spec_proc_temp[m])) + '.svg"];\n')
        
            
            f.write('"Original"[shape=rectangle,width=4,height=1,style="filled",fillcolor=grey,fontsize=45,fontcolor=white,label = "All Pathways",URL="..\pathway_visualization.svg"];\n')
            f.write('edge[dir="forward",arrowhead=none,style="invisible",label=""];\n')
            f.write('"Original" -> "' + str(speciescounter) + '"[constraint=false];\n') 
            f.write('}')
            f.close()
            check_call(['dot','-Tsvg', f.name,'-o', fname_svg], shell=True)
            
        src_files = os.listdir('./')
        for file_name in src_files:
            if os.path.isfile(full_file_name) and (file_name.endswith('PNG') or file_name.endswith('png')):
                os.remove(file_name)
        print('Files deleted successfully!')
            
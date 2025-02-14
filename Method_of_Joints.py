#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:37:32 2021

@author: kendrick shepherd
"""

import sys

import Geometry_Operations as geom

# Determine the unknown bars next to this node
def UnknownBars(node):
    bars_next_to_node = node.bars
    my_unknown_bars = []
    for the_current_bar in bars_next_to_node:
        if the_current_bar.is_computed == False:
            my_unknown_bars.append(the_current_bar)
            
    return my_unknown_bars

# Determine if a node if "viable" or not
def NodeIsViable(node):
    my_unknown_bars = UnknownBars(node)
    if len(my_unknown_bars) > 0 and len(my_unknown_bars) <=2:
        return True
    else:
        return False
    
# Compute unknown force in bar due to sum of the
# forces in the x direction
def SumOfForcesInLocalX(node, local_x_bar):
  ## my_unknown_bars = UnknownBars(node)
    ##local_x_bar = my_unknown_bars[0]
    
    local_x_vector = geom.BarNodeToVector(node, local_x_bar)
    
    x_add=0
    #Add x
    x_add+=node.GetNetXForce()*geom.CosineVectors(local_x_vector,[1,0])
    x_add+=node.GetNetYForce()*geom.CosineVectors(local_x_vector,[0,1])
    
    for Bar in node.bars:
        if Bar.is_computed ==True:
            x_add+=Bar.axial_load*geom.CosineBars(local_x_bar, Bar)
            
    other_bar=-x_add
    local_x_bar.axial_load = other_bar
    local_x_bar.is_computed = True
                                                  
    return

# Compute unknown force in bar due to sum of the 
# forces in the y direction
def SumOfForcesInLocalY(node, unknown_bars):
    my_unknown_bars = UnknownBars(node)
    local_x_bar = my_unknown_bars[0]
    other_bar = my_unknown_bars[1]
    local_x_vector = geom.BarNodeToVector(node, local_x_bar)
    
    y_add=0
    
    y_add += node.GetNetXForce()*geom.SineVectors(local_x_vector,[1,0])
    y_add += node.GetNetYForce()*geom.SineVectors(local_x_vector,[0,1])
    for Bar in node.bars:
        if Bar.is_computed == True:
            y_add += Bar.axial_load*geom.SineBars(local_x_bar, Bar)
            
    unknown_force=-1*y_add/geom.SineBars(local_x_bar, other_bar)

    other_bar.axial_load = unknown_force

    other_bar.is_computed = True
    return
    
# Perform the method of joints on the structure
def IterateUsingMethodOfJoints(nodes,bars):
    count=1

    contwhile = False

    for Bar in bars:
        if Bar.is_computed == False:
            contwhile=True
            break
        
    while contwhile == True:
        for Node in nodes:
            if NodeIsViable(Node)==True:
                unknown_bars = UnknownBars(Node)
                if len(unknown_bars)==2:
                        SumOfForcesInLocalY(Node, unknown_bars)
                local_x_bar = unknown_bars[0]
                SumOfForcesInLocalX(Node, local_x_bar)
        contwhile = False
        for Bar in bars:
            if Bar.is_computed == False:
                contwhile=True
                break
        if count<=len(nodes):
            count+=1
        else:
            sys.exit("Infinite Loop")
    return
            

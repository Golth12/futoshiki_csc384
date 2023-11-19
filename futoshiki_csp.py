#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools


def futoshiki_csp_model_1(futo_grid):
    #create the vallues do a list of vallues maybe a futogrid of value and a list of tuple with the values and binary constraints
    # with the new grid we have the row and the columns 
    # for each row and column we should have  column  we verify the values that are already given and take them out of the domains no need to take them out of the constraints one 
    # i  can use combination and size to do everything 
   
    grid = []
    ineq_const = []
    var_list = []
    num_row = len(futo_grid)
    num_var =0
    dom = list(range(1, num_row +1))
    csp = CSP("futoshiki_csp_model_1")
    for i in range(num_row):
        row = []
        num_var = 0
        for j in range(len(futo_grid[i])) :
            if type(futo_grid[i][j]) == int:
                if futo_grid[i][j] > 0 :
                    # create a var that is assigned to the element 
                    var =   Variable("{},{}".format(i,num_var), [futo_grid[i][j]])
                    var.assign(futo_grid[i][j])
                    
                else : 
                     var =   Variable("{},{}".format(i,num_var), dom)
                row.append(var)
                # add the value in csp here
                csp.add_var(var)
                num_var +=1
            else:
                if futo_grid[i][j] == ">" or futo_grid[i][j]=="<":
                    tup = (futo_grid[i][j], i , num_var)
                    ineq_const.append(tup)
        grid.append(row)
    # the grid is complete # csp has all the needed values 
    # create the addmissible tupple 
    cons_values = list(range(1, num_var+1 ))
    combinations = list(itertools.permutations(cons_values, 2))
    # constraint creation for row / col binary ineq
    for i in range(len(grid)):
        for j in range(len(grid)):
            responsible_var =grid[i][j]
            for row_index in  range(i + 1, len(grid)):
                con = Constraint("C(Q{},Q{}) and C(Q{},Q{}) ".format(i,j,row_index,j  ),[responsible_var,grid[row_index][j]])
                con.add_satisfying_tuples(combinations)
                csp.add_constraint(con)
            for col_index in  range(j + 1,len(grid)):
                con = Constraint("C(Q{},Q{}) and C(Q{},Q{}) ".format(i,j,row_index,j  ),[responsible_var,grid[i][col_index]]) 
                con.add_satisfying_tuples(combinations)
                csp.add_constraint(con)
            
   
    #create 2 satis_tupple lst so that the first one is i1< i2 and 2nd one is i1>i2
    combination1 = list(tup for tup in combinations if tup[0] < tup[1])
    combinaton2 = list(tup for tup in  combinations if tup[0] > tup[1])
    # constraint creation for row / col binary ineq
     # create the  binary inequality constraints.
    for tup in ineq_const:
        con = Constraint("C(Q{},Q{}) and C(Q{},Q{}) ".format(tup[1],tup[2] -1 ,tup[1],tup[2]  ),[grid[tup[1]][tup[2] -1], grid[tup[1]][tup[2]]])
        if tup[0] =="<":
            con.add_satisfying_tuples(combination1)
        else:
             con.add_satisfying_tuples(combinaton2)
        csp.add_constraint(con)
    return csp, grid
    

    

def futoshiki_csp_model_2(futo_grid):
    grid = []
    ineq_const = []
    var_list = []
    num_row = len(futo_grid)
    dom = list(range(1, num_row + 1))
    num_var =0
    csp = CSP("futoshiki_csp_model_2")
    for i in range(num_row):
        num_var = 0
        row = []
        for j in range(len(futo_grid[i])) :
            if type(futo_grid[i][j]) == int:
                if futo_grid[i][j] > 0 :
                    # create a var that is assigned to the element 
                    var =   Variable("{},{}".format(i,num_var), [futo_grid[i][j]])
                    var.assign(futo_grid[i][j])
                    
                else : 
                     var =   Variable("{},{}".format(i,num_var), dom)
                row.append(var)
                # add the value in csp here
                csp.add_var(var)
                num_var +=1
            else:
                if futo_grid[i][j] == ">" or futo_grid[i][j]=="<":
                    tup = (futo_grid[i][j], i , num_var)
                    ineq_const.append(tup)
        grid.append(row)
    # the grid is complete # csp has all the needed values 
    # create the addmissible tupple 
    cons_values = list(range(1, num_var+1 ))
    combinations = list(itertools.permutations(cons_values, len(cons_values)))
    # constraint creation for row / col binary ineq
    for row_index in range(len(grid)):
        con = Constraint("C(Row Q{} ".format( row_index),grid[row_index])
        con.add_satisfying_tuples(combinations)
        csp.add_constraint(con)
    # colum one 
    for i in range(len(grid)):
        col = []
        for j in range(len(grid)):
           col.append(grid[j][i])
        con = Constraint("Colone Q{} ".format( i),col)
        con.add_satisfying_tuples(combinations)
        csp.add_constraint(con)
            
   
    #create 2 satis_tupple lst so that the first one is i1< i2 and 2nd one is i1>i2
    perm = list(itertools.permutations(cons_values, 2))
    combination1 = list(tup for tup in  perm if tup[0] < tup[1])
    combinaton2 = list(tup for tup in  perm if tup[0] > tup[1])
     # create the  binary inequality constraints.
    for tup in ineq_const:
        con = Constraint("C(Q{},Q{}) and C(Q{},Q{}) ".format(tup[1],tup[2] -1 ,tup[1],tup[2]  ),[grid[tup[1]][tup[2] -1], grid[tup[1]][tup[2]]])
        if tup[0] =="<":
            con.add_satisfying_tuples(combination1)
        else:
             con.add_satisfying_tuples(combinaton2)
        csp.add_constraint(con)
    print(csp.get_all_cons())
    return csp, grid
   

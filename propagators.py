#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    good = True
    pruned = []
    #IMPLEMENT
    if newVar == None :
        constraits = csp.get_all_cons()
    else:
        constraits = csp.get_cons_with_var(newVar)
    for cons in constraits:
        if cons.get_n_unasgn() == 1:

            vars = cons.get_scope()
            var = cons.get_unasgn_vars()[0]
            values = []
            index = vars.index(var)
            for i in range(len(vars)):
                  values.append(vars[i].get_assigned_value())
            currdom = var.domain()
            for val in currdom :
                values[index] = val
                if not cons.check(values):
                    var.prune_value(val)
                    pruned.append((var, val))
            if var.cur_domain_size == 0:
                good = False
        if good == False : 
            return good, pruned
    return good, pruned

    

            
           
            ## now if the var has no value usable we get shit done.

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    # create a q of cons
    good = True
    pruned = []
    #IMPLEMENT
    if newVar == None :
        Q_constraits = csp.get_all_cons()
    else:
        Q_constraits = csp.get_cons_with_var(newVar)
    # loop in the queue and for each constraint find the dom of varssuch that it works. each vars a domain so that the constraint function
    while len(Q_constraits) > 0:
    # each time we change the domain of a var we need to call all the cons that have the var get_cons_with_var(self, var)
        Cur_cons = Q_constraits.pop(0)
        vars = Cur_cons.get_scope()
        for var in vars :
            currdom = var.cur_domain()
            check = False
            for val in currdom:
                if   not Cur_cons.has_support(var, val):
                    var.prune_value(val)
                    pruned.append((var, val))
                    check = True
            if check == True:
                cons_modif = csp.get_cons_with_var(var)
                cons_modif.remove(Cur_cons)
                for cons in cons_modif:
                    if cons not in Q_constraits:
                        Q_constraits.append(cons)
            if var.cur_domain_size() == 0:
                return good, pruned
    return True, pruned

    # we add those cons at the end of the queue if they are not already in the q 
    # if any domain of any var is empty then domain wipe out and return false.
    # So either on domain gon be empty or 

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    vars = csp.get_all_unasgn_vars()
    dom_sizes = []
    for var in vars:
        dom_sizes.append(var.cur_domain_size())
    min_num = min(dom_sizes)
    return vars[dom_sizes.index(min_num)]

	
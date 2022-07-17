

class AgentEnvironment:
    """ 
    'Abstract class' for agents

    Agents: layers of agents in a hierarchical control system are modeled as environments, 
    hence the name of the class 
    """ 

    def initial_percepts(self): 
        """returns the initial percepts for the agent""" 

        raise NotImplementedError("initial_precepts")
    
    def do(self, action):
        """does the action in the environment, and returns the next percepts"""
        
        raise NotImplementedError("do")


class Environment: 
    """ 
    'Abstract class' for environments

    Environments will inherit from this class 
    """ 

    def initial_percepts(self): 
        """returns the initial percepts for the agent""" 

        raise NotImplementedError("initial_precepts")
    
    def do(self, action):
        """does the action in the environment, and returns the next percepts"""
        
        raise NotImplementedError("do")
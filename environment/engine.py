from scienceworld import ScienceWorldEnv
class Engine:
    """Defines the environment function from the generator engine.
       Expects the following:
        - reset() to reset the env a start position(s)
        - step() to make an action and update the game state
        - legal_moves_generator() to generate the list of legal moves
    """
    def __init__(self, input_task:str='1-1') -> None:
        # Define 'universe'
        self.Environment = ScienceWorldEnv()
        taskNames = self.Environment.getTaskNames()
        if input_task == '1-1':
            task = taskNames[0]
            
        self.Environment.load(task, 0, "", generateGoldPath=True) 
        #print(self.Environment.getMaxVariations(taskNames[0]))
        print("\tPossible Simplifications: ", self.Environment.getPossibleSimplifications())
        print("\tTask Description:", self.Environment.getTaskDescription())
        print("---")
        print("\tGold Path: ", self.Environment.getGoldActionSequence())
        print("-------------------------------------------------------")
        
    def reset(self):
        """Fully reset the environment."""
        obs, _ = self.Environment.reset()
        inventory = self.Environment.inventory()
        look = self.Environment.look()
        
        
        obs = obs.replace('\n\t',' ').replace('\n', ' ').replace('  ', ' ')
        inventory = inventory.replace('\n\t',' ').replace('\n', ' ').replace('  ', ' ')
        look = look.replace(': \n\t',': ').replace(':\n\t',': ').replace('\n\t',', ').replace('\n', '. ')
        obs_output = obs + ". " + inventory + '. ' + look 

        reward = 0
        terminated = False
        score = 0
        return obs_output, reward, terminated, score

    
    def step(self, state:any, action:any):
        """Enact an action."""
        # In problems where the agent can choose to reset the env
        if (state=="ENV_RESET")|(action=="ENV_RESET"):
            obs_output, reward, terminated, score = self.reset()
        else:    
            obs, reward, terminated, info = self.Environment.step(action)
            inventory = self.Environment.inventory()

            obs = obs.replace('\n\t',' ').replace('\n', ' ').replace('  ', ' ')
            inventory = inventory.replace('\n\t',' ').replace('\n', ' ').replace('  ', ' ')

            score = info['score']
            
        obs_output = (obs + ". " + inventory + '. ') if obs[-1]!='.'  else (obs + " " + inventory + '. ')
        
        # look = self.Environment.look()
        # look = look.replace(': \n\t',': ').replace(':\n\t',': ').replace('\n\t',', ').replace('\n', '. ')
        # Found spurious reward results - override to reduce impact of this
        if reward<-1:  
            reward=-1
        return obs_output, reward, terminated

    def legal_move_generator(self, obs:any=None):
        """Define legal moves at each position"""
        legal_moves = self.Environment.getValidActionObjectCombinations()
        return legal_moves


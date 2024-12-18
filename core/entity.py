class Entity():

    def __init__(self,data):
        for item in self.items:
            setattr(self,item,data.get(item))
    
    def to_string(self): 
        string = ""
        for key in self.items:
            string += f"{key}: {str(getattr(self,key))};"
        return string
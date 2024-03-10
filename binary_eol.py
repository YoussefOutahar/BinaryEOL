import re
import sys

class Info:
    def __init__(self):
        self.profondeurGauche = 0
        self.profondeurDroite = 0
        self.contiens = False
        self.temps = -1

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.info = Info()
        self.active = False
    
    def get_height(self):
        if self.left and self.right:
            return max(self.left.get_height(), self.right.get_height()) + 1
        elif self.left:
            return self.left.get_height() + 1
        elif self.right:
            return self.right.get_height() + 1
        else:
            return 1
        
    def find_target(self, target):
        if not self:
            return False 
        if self.data == target:
            return True
        else:
            if self.left is not None:
                if self.left.find_target(target):
                    return True
            if self.right is not None:
                if self.right.find_target(target):
                    return True
        return False
    
    def find_false(self):
        if not self:
            return False 
        if self.active == False:
            return True
        else:
            if self.left is not None:
                if self.left.find_false():
                    return True
            if self.right is not None:
                if self.right.find_false():
                    return True
        return False

class Solution:

    resultat = 0

    def read_file(self, filename):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        return content

    def get_node_list_from_file(self, filename):
        # putting the file by line into an array
        nodes = [] 
        content = self.read_file(filename)
        data = re.split(':|,', content[0])
        for line in content:
            data = re.split(':|,', line)
            temp = Node(int(data[0]))
            if data[1] != " None":
                temp.left = Node(int(data[1]))
            else:
                temp.left = None
            if data[2] != " None":
                temp.right = Node(int(data[2]))
            else:
                temp.right = None
            nodes.append(temp)
        return nodes
    
    def fill_tree(self,root,nodes: list,nodes_nbr):
        if len(nodes) == nodes_nbr: 
            root = nodes[0]
            nodes.pop(0)
        for i in range(0,len(nodes)):
            if i-1>len(nodes):
                break
            if root.left is not None:
                if root.left.data == nodes[i].data:
                    root.left = nodes[i]
                    root.left = self.fill_tree(root.left, nodes,nodes_nbr)
                else:
                    if root.left is not None:
                        root.left = self.fill_tree(root.left, nodes,nodes_nbr)
                    if root.right is not None:
                        root.right = self.fill_tree(root.right, nodes,nodes_nbr)
            if root.right is not None:
                if root.right.data == nodes[i].data:
                    root.right = nodes[i]
                    #nodes.pop(i)
                    root.right = self.fill_tree(root.right, nodes,nodes_nbr)
                else:
                    if root.left is not None:
                        root.left = self.fill_tree(root.left, nodes,nodes_nbr)
                    if root.right is not None:
                        root.right = self.fill_tree(root.right, nodes,nodes_nbr)
        return root

    def build_tree_from_file(self, filename):
        racine = Node(None)
        node_list = s.get_node_list_from_file(filename)
        racine = s.fill_tree(racine,node_list,len(node_list))
        return racine
    
    def fill_info_single_node(self, root: Node,cible):
        if root is not None:
            root.info.contiens = root.find_target(cible)
            if root.left is not None:
                root.info.profondeurGauche = root.left.get_height()
            if root.right is not None:
                root.info.profondeurDroite = root.right.get_height()
            if root.left is not None:
                self.fill_info_single_node(root.left,cible)
            if root.right is not None:
                self.fill_info_single_node(root.right,cible)
    
    def fill_info_all_tree(self,noeud,cible):
        if noeud is not None:
            self.fill_info_single_node(noeud,cible)
            self.fill_info_all_tree(noeud.left,cible)
            self.fill_info_all_tree(noeud.left,cible)
    
    def get_activation_time_one_node(self, root, target,delai):
        if root.data == target:
            if root.active == False:
                root.info.temps = target
                root.active = True
                delai = target
                return target
        
        if root.right is not None:
            if root.right.active == True:
                if root.active == False:
                    root.info.temps = delai + root.data
                    root.active = True
                    delai =  root.data
                    return delai
                
        if root.left is not None:
            if root.left.active == True:
                if root.active == False:
                    root.info.temps = delai + root.data
                    root.active = True
                    delai = root.data
                    return delai
                    
        if root is not None:
            if root.active == True:
                if root.left is not None:        
                    if root.left.active == False:
                        root.left.active = True
                        root.left.info.temps = delai + root.left.data
                        delai =  root.left.data
                        return delai
                        
                if root.right is not None:        
                    if root.right.active == False:
                        root.right.active = True
                        root.right.info.temps = delai + root.right.data
                        delai = root.right.data
                        return delai
        return 0
            
    def get_activation_time_all_nodes(self, root, target,delai):
        if root is not None: 
            delai += self.get_activation_time_one_node(root,target,delai)
            if root.left is not None:
                delai = self.get_activation_time_all_nodes(root.left,target,delai)
            if root.right is not None:
                delai = self.get_activation_time_all_nodes(root.right,target,delai)
        return delai

    def calculer_temps(self, noeud, info, cible):
        self.fill_info_all_tree(noeud,cible)
        temp = 0
        while noeud.find_false():
            temp = self.get_activation_time_all_nodes(noeud,cible,temp)
            
        info.profondeurDroite = noeud.info.profondeurDroite
        info.profondeurGauche = noeud.info.profondeurGauche
        info.temps = temp
        return info

    def solve(self, racine, cible):
        info = Info()
        info = self.calculer_temps(racine, info, cible)
        self.resultat = info.temps
        return self.resultat


if __name__ == '__main__':
    
    s = Solution()
    
    # Bout de code qui construit l'arbre donné en exemple dans l'énoncé.
    if len(sys.argv) > 1:
        racine = s.build_tree_from_file(sys.argv[1])
    else:
        racine = s.build_tree_from_file("arbre1.txt")
    
    # code qui active l'arbre est retourne le temps d'activation
    print(s.solve(racine, 256))
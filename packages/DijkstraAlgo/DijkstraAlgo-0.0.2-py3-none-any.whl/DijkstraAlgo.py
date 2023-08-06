
class DijkstraAlgorithm:

    def __init__(self):

        '''Initializing the instances'''

        self.min_dis_index = []
        self.short_dis = []
    
    def minDistance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1
        
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i] 
                min_index = i
        return min_index

    def printPath(self, parent, j):
        if parent[j] == -1:                 # If 'j' is the source
            # print (j+1, end="  ")
            self.min_dis_index.append(j+1)
            return 0
        self.printPath(parent, parent[j])   #If 'j' is not the source, call the recursive function
        self.min_dis_index.append(j+1)
        # print (j+1, end="  ")

    def distance(self):
        '''Return the Distance of the measured path'''

        return self.short_dis

    def path(self):
        '''Return the Shortest Path'''

        return self.min_dis_index

    def dijkstraWithPath(self, graph, src, des):
        source = src - 1
        row = len(graph)
        col = len(graph[0])
        
        dist = [float('Infinity')] * row    # initializing all distances are inifinity
        parent = [-1] * row                 # The parent array where to store the shortest path tree
        
        dist[source] = 0                         # Distance of source from itself is zero
        
        queue = []                              # An empty list to store all vertices in queue
        for i in range(row):
            queue.append(i)
        
        # Find the shortest path for all vertices
        while queue:
            # Select the minimum distance vertex 
            # from the set of vertices 
            # which are still in the queue
            u = self.minDistance(dist, queue)
            queue.remove(u)     # Now remove the minimum distance element which already got
            
            # Consider the vertices which are still in the queue,
            # update the distance and parent index of the adjacent vertices
            # which are selected 
            for i in range(col):
                if graph[u][i] and i in queue:  # If dist[i] in the queue
                    if dist[u] + graph[u][i] < dist[i]: # and if the total weight of path from source to destination is less than the current value of dist[i]
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

        self.short_dis.append(dist[des-1])      #The measured Distance
        return self.printPath(parent, des-1)    
        
        
        
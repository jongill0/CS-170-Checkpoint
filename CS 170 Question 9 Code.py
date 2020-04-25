
# coding: utf-8

# # Calculate Maximum Flow

# In[16]:


class Vertex:
    def __init__(self, name, source=False, sink=False):
        self.name = name
        self.source = source
        self.sink = sink

class Edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0
        self.returnEdge = None

class FlowNetwork:
    def __init__(self):
        self.vertices = []
        self.network = {}

    def getSource(self):
        for vertex in self.vertices:
            if vertex.source == True:
                return vertex
        return None

    def getSink(self):
        for vertex in self.vertices:
            if vertex.sink == True:
                return vertex
        return None

    def getVertex(self, name):
        for vertex in self.vertices:
            if name == vertex.name:
                return vertex

    def vertexInNetwork(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return True
        return False

    def getEdges(self):
        allEdges = []
        for vertex in self.network:
            for edge in self.network[vertex]:
                allEdges.append(edge)
        return allEdges

    def addVertex(self, name, source=False, sink=False):
        if source == True and sink == True:
            return "Vertex cannot be source and sink"
        if self.vertexInNetwork(name):
            return "Duplicate vertex"
        if source == True:
            if self.getSource() != None:
                return "Source already Exists"
        if sink == True:
            if self.getSink() != None:
                return "Sink already Exists"
        newVertex = Vertex(name, source, sink)
        self.vertices.append(newVertex)
        self.network[newVertex.name] = []

    def addEdge(self, start, end, capacity):
        if start == end:
            return "Cannot have same start and end"
        if self.vertexInNetwork(start) == False:
            return "Start vertex has not been added yet"
        if self.vertexInNetwork(end) == False:
            return "End vertex has not been added yet"
        newEdge = Edge(start, end, capacity)
        returnEdge = Edge(end, start, 0)
        newEdge.returnEdge = returnEdge
        returnEdge.returnEdge = newEdge
        vertex = self.getVertex(start)
        self.network[vertex.name].append(newEdge)
        returnVertex = self.getVertex(end)
        self.network[returnVertex.name].append(returnEdge)

    def getPath(self, start, end, path):
        if start == end:
            return path
        for edge in self.network[start]:
            residualCapacity = edge.capacity - edge.flow
            if residualCapacity > 0 and not (edge, residualCapacity) in path:
                result = self.getPath(edge.end, end, path + [(edge, residualCapacity)])
                if result != None:
                    return result

    def calculateMaxFlow(self):
        source = self.getSource()
        sink = self.getSink()
        if source == None or sink == None:
            return "Network does not have source and sink"
        path = self.getPath(source.name, sink.name, [])
        i = 0
        while path != None:
            total_path = []
            for e in path:
                total_path += [e[0].start]
            flow = min(edge[1] for edge in path)
            print(str(i) + ": " + str(total_path), flow)
            i += 1
            for edge, res in path:
                edge.flow += flow
                edge.returnEdge.flow -= flow
            path = self.getPath(source.name, sink.name, [])
        return sum(edge.flow for edge in self.network[source.name])


# # Graph Defined in Question 9

# In[25]:


c = 0
fn = FlowNetwork()
fn.addVertex('s', True, False)
fn.addVertex('t', False, True)
fn.addVertex('a')
fn.addVertex('b')
fn.addVertex('c')
fn.addVertex('d')
fn.addEdge('s', 'a', 100 + c)
fn.addEdge('a', 't', 100 + c)
fn.addEdge('s', 'b', 100 + c)
fn.addEdge('b', 't', 100 + c)
fn.addEdge('c', 'b', 1 + c) # added edge CB
fn.addEdge('s', 'c', 200 + c)
fn.addEdge('c', 't', 200 + c)
fn.addEdge('s', 'd', 200 + c)
fn.addEdge('d', 't', 200 + c)


# In[26]:


vertices = [vertex.name for vertex in fn.vertices]
edges = ['%s -> %s' % (e.start, e.end) for e in fn.getEdges()]


# In[27]:


fn.calculateMaxFlow()


# As you can see, this edge still causes the algorithm to run 402 iterations.

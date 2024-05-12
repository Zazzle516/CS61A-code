from urllib.request import urlopen
webtext = urlopen('http://inst.eecs.berkeley.edu/~cs61a/fa11/shakespeare.txt')
words = set(webtext.read().decode().split())
print ({w for w in words if len(w) >= 5 and w[::-1] in words}) >> out.txt
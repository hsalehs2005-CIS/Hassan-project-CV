with open("example.txt", 'r') as src:
    data= src.read()
with open('destination.txt', 'w') as dest:
    dest.write(data)
print("Content copied from 'example.txt' to 'destination.txt' seccessfully.")

#------ question1
with open("example.txt", 'r') as src:
    data= src.read()
with open('destination.txt', 'w') as dest:
    dest.write(data)
print("Content copied from 'example.txt' to 'destination.txt' seccessfully.")

#-- question2
with open('example.txt', 'r') as file:
    lines= file.readlines()
lines = [line.strip() for line in lines]
print("File lines stored in a list:")
print(lines)

#-----question3
with open ('example.txt', 'r') as file:
    line_count= sum(1 for _ in file)
print(f"The file 'example.txt' has {line_count} lines.")

# question 4
phrases= [ "Learning Python is fun!",
    "File handling is an important concept.",
    "practice comment your code."
    "Always comment your code."]
with open('destination.txt', 'w') as file:
    for phrase in phrases:
        file.write(phrase + "\n")
print("File 'destination.txt' created and written successfully.")

#question 5
with open('example.txt', 'r') as file:
    lines = file.readlines()
line_count= len(lines)
word_count= 0
char_count=0

for line in lines:
    words = line.split()
    word_count += len(words)
    char_count += sum(c.isalpha() for c in line)

print("file: example.txt")
print(f"Total Lines: {line_count}")
print(f"Total Words: {word_count}")
print(f"total alpha char: {char_count}")

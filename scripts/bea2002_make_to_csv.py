
first_line = None

with open('../data/bea2002/IOMakeDetail.txt', 'r', newline='\n') as f:
    i = 0
    for line in f:
        if i == 1:
            first_line = line.strip()
            break
        i += 1

print(first_line)

values = []
feed = first_line
text = ''
spaces = 0
i = 0
while i < len(feed):
    char = feed[i]
    if char == ' ':
        spaces += 1
    if spaces <= 1:
        text += feed[i]
        i += 1
        continue
    else:
        values.append(text.strip())
        text = ''
        spaces = 0
        for k in range(i+1, len(feed)):
            if feed[k] != ' ':
                i = k
                break

values.append(text.strip())
print(values)



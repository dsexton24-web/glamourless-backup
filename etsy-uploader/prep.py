import json,sys
s=json.load(open('/home/claude/etsy/sources.json'))
B='G:\\My Drive\\Glamourless Systems Main\\'
p=[B+s[k][f].replace('/','\\') for k in sys.argv[1:] for f in ('pdf','docx','cover','mockup') if s[k][f]]
print(json.dumps(p))

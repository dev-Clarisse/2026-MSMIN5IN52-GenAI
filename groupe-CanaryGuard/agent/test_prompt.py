from prompt import construire_prompt_systeme, CANARI

p = construire_prompt_systeme()
assert CANARI in p
print(p)
import datetime


ano = 2024
mes = 1
dia  = 29

minha_data = datetime.date(ano, mes, dia)

if minha_data.weekday() ==  5 or  minha_data.weekday() ==6:
    print(f'Não é dia util ' )    
else:
    print(f'É DIA UTIL ' )
    
    

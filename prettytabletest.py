import prettytable

x = prettytable.PrettyTable(['Name','Parent','Child'])
x.add_row(['Juan','x',''])
x.add_row(['Michele','x',''])
x.add_row(['Jordan','','x'])
x.add_row(['Claire','','x'])
x.add_row(['Christopher','','x'])
x.align['Name']='l'
x.align['in']='c'
x.align['out']='c'

print x

x.add_column("Grandparent",['','','','',''])

print x

x.add_row(['Nona','','','x'])

print x.get_html_string()

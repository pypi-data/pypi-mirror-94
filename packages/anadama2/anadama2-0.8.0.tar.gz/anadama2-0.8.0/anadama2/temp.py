def update_path(depends, output_dir, scratch, name=True):
    for index in range(len(depends)):
        if name:
            depends[index].name=depends[index].name.replace(output_dir, scratch)
        else:
            depends[index]=depends[index].replace(output_dir, scratch)
    return depends


a=update_path(["/ab/hello","/ab/hi"],"/ab","/n/scratch", name=False)
print(a)

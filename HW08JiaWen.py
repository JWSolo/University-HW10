def file_reader(path,fields,sep = ',',header = False):
    count = 0
    try:
        fp = open(path,'r')
    except:
        raise FileNotFoundError("FileNotFoundError: can not open",path)
    else:
        with fp:
            for n,line in enumerate(fp,1):
                num = line.rstrip('\n').strip('\t').split(sep)
                if len(num) != fields:
                    raise ValueError(f" {path} has {len(num)} fields on line {n} but except {fields}")        
                elif n ==1 and header:
                    continue
                else :
                    yield tuple(num)

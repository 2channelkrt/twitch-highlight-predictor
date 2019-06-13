import os
from multiprocessing import Pool

method=['rise', 'trendy', 'burst']
step_method=['mov_av', 'naive']
steps=[1,2,3,4,5,6,7,8,9,10]
window=[10,30,50,70,100]


threshold=[10,20,30,40,50,60,70,80,90,100]
duration=[1,2,3,4,5,6,7,8,9,10]

def work(tt):
    cmd='python main.py -method {} -method2 {} -step {} -verbose True'.format('rise', 'naive', tt[0])
    os.system(cmd)
    
if __name__ == '__main__':
    
    pool=Pool(processes=4)

    works=[]

    for step in duration:
        works.append([step])
    
    pool.map(work, works)
    pool.close()
    pool.join()


    '''
    pool.apply_async(work, [])
    for t in threshold:
        for d in duration:
            proc=Process(target=work, args=(t, d))
            procs.append(proc)
            proc.start()

    for proc in procs:
        proc.join()
        '''
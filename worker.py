import os
from multiprocessing import Pool

method=['rise', 'trendy', 'burst']
step_method=['mov_av', 'naive']
steps=[1,2,3,4,5,6,7,8,9,10]


threshold=[10,15,20,25,30,35,40,45,50]
duration=[1,2,3,4,5,6,7,8,9,10]

def work(tt):
    cmd='python main.py -method {} -threshold {} -duration {} -verbose True'.format('burst', tt[0], tt[1])
    os.system(cmd)
    
if __name__ == '__main__':
    
    pool=Pool(processes=4)

    works=[]

    for t in threshold:
        for d in duration:
            works.append([t,d])
    
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
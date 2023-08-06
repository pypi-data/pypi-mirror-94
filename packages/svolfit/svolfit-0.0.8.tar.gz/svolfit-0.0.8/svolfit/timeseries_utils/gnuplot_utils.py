import numpy as np

def greekstrip(x):
    
    y=x.replace('_','-')
    if(x=='mu'):
       y='$\\\\mu$' 
    if(x=='sigma'):
       y='$\\\\sigma$' 
    if(x=='eta'):
       y='$\\\\eta$' 
    if(x=='alpha'):
       y='$\\\\alpha$' 
    if(x=='rho'):
       y='$\\\\rho$' 
    if(x=='xi'):
       y='$\\\\xi$' 
    if(x=='theta'):
       y='$\\\\theta$' 
    if(x=='v0'):
       y='$v_0$' 
    if(x=='vT'):
       y='$v_T$' 
    if(x=='lambda'):
       y='$\\\\lambda$' 
    if(x=='gamma'):
       y='$\\\\gamma$' 
    if(x=='omega'):
       y='$\\\\omega$' 
    if(x=='phi'):
       y='$\\\\phi$' 
    return y


def gnuplot_paramdistplots(NAME,NOSTS,pars,paramstartfilename,paramfinishfilename,gnuplotfilename,obswindow_start,obswindow_finish):
    
    f = open(gnuplotfilename, 'w')

    NOBSS=NOSTS.RunInfo_Nobs.unique()

    header=[]
    header.append('reset\n')
    header.append('set encoding default\n')
    header.append('set terminal epslatex monochrome\n')
    header.append("set datafile separator ','\n")
    header.append('set size 1.0,1.0\n')
#    header.append('set autoscale\n')
    header.append('\n')
    f.writelines(header)

    setup=[]
    setup.append('set key autotitle columnhead\n')
    setup.append('set key outside top right\n')
    setup.append('set xrange ['+str(obswindow_start)+':'+str(obswindow_finish)+']\n')
    setup.append('\n')
#    setup.append('set y2tics\n')
    setup.append('set ytics nomirror\n')
    setup.append('\n')
    f.writelines(setup)


    sloop=[]
    parst=''
    for x in pars:
        parst=parst+' '+x.replace('_','-')
    sloop.append('pars="'+parst+'"\n')
    sloop.append('\n')
    sloop.append('DataFile="'+paramstartfilename+'"\n')
    sloop.append('\n')
#    sloop.append('unset key\n')
#    sloop.append('unset title\n')
    sloop.append('\n')
    for x in pars:
        x1='unk'
        x2=greekstrip(x) 
        if(x[0:4]=='rep_'):
            x1='rep'
            x2=greekstrip(x[4:]) 
        if(x[0:4]=='wrk_'):
            x1='wrk'
            x2=greekstrip(x[4:]) 
        if(x[0:5]=='misc_'):
            x1='misc'
            x2=greekstrip(x[5:]) 
        sloop.append('\n')
        sloop.append('set title "Parameters: '+x1+' '+x2+'"\n')
        sloop.append('set output "'+NAME+'_'+x+'_paramdist_start.tex"\n')
        sloop.append('plot \\\n')
        for Nobs in NOBSS:
            sloop.append('DataFile using "start":"'+x+'_'+str(Nobs)+'" title "'+x1+' '+x2+'-'+str(Nobs)+'" with lines,\\\n')
        sloop.append('\n')
        sloop.append('\n')
    sloop.append('\n')
    f.writelines(sloop)



    sloop=[]
    parst=''
    for x in pars:
        parst=parst+' '+x.replace('_','-')
    sloop.append('pars="'+parst+'"\n')
    sloop.append('\n')
    sloop.append('DataFile="'+paramfinishfilename+'"\n')
    sloop.append('\n')
#    sloop.append('unset key\n')
#    sloop.append('unset title\n')
    sloop.append('\n')
    for x in pars:
        x1='unk'
        x2=greekstrip(x) 
        if(x[0:4]=='rep_'):
            x1='rep'
            x2=greekstrip(x[4:]) 
        if(x[0:4]=='wrk_'):
            x1='wrk'
            x2=greekstrip(x[4:]) 
        if(x[0:5]=='misc_'):
            x1='misc'
            x2=greekstrip(x[5:]) 
        sloop.append('\n')
        sloop.append('set title "Parameters: '+x1+' '+x2+'"\n')
        sloop.append('set output "'+NAME+'_'+x+'_paramdist_finish.tex"\n')
        sloop.append('plot \\\n')
        for Nobs in NOBSS:
            sloop.append('DataFile using "finish":"'+x+'_'+str(Nobs)+'" title "'+x1+' '+x2+'-'+str(Nobs)+'" with lines,\\\n')
        sloop.append('\n')
        sloop.append('\n')
    sloop.append('\n')
    f.writelines(sloop)


    f.close()

    return

def gnuplot_plotvpaths(NAME,NOSTS,assetname,vpathfilename,gnuplotfilename,obswindow_start,obswindow_finish):
    
    f = open(gnuplotfilename, 'w')

    header=[]
    header.append('reset\n')
    header.append('set encoding default\n')
    header.append('set terminal epslatex monochrome\n')
    header.append("set datafile separator ','\n")
    header.append('set size 1.0,1.0\n')
    header.append('set autoscale\n')
    header.append('\n')
    header.append('\n')
    f.writelines(header)

    setup=[]
    setup.append('set key autotitle columnhead\n')
    setup.append('set key outside top right\n')
    setup.append('set xrange ['+str(obswindow_start)+':'+str(obswindow_finish)+']\n')
    setup.append('\n')
#    setup.append('set y2tics\n')
    setup.append('set ytics nomirror\n')
    setup.append('\n')
    setup.append('DataFile="'+vpathfilename+'"\n')
    setup.append('\n')
    setup.append('\n')
    setup.append('unset key\n')
#    setup.append('unset title\n')
    setup.append('\n')
    setup.append('set tmargin 0\n')
    setup.append('set bmargin 0\n')
    setup.append('set lmargin 3\n')
    setup.append('set rmargin 3\n')
    setup.append('\n')
    setup.append('\n')
    f.writelines(setup)

    NOBSS=NOSTS.RunInfo_Nobs.unique()

    for Nobs in NOBSS:
        sloop=[]
        sloop.append('\n')
        sloop.append('unset xtics\n')
        sloop.append('\n')
        sloop.append('set output "'+NAME+'_vpath_'+str(Nobs)+'.tex"\n')
        sloop.append('set multiplot layout 3,1 rowsfirst\n')
        sloop.append('\n')
        sloop.append('set title "asset: '+assetname+'"\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "index":"'+assetname+'" with lines,\\\n')
        sloop.append('\n')
        sloop.append('unset title\n')
        sloop.append('plot \\\n')
        
        STS=NOSTS[NOSTS.RunInfo_Nobs==Nobs].RunInfo_start.unique()
        for start in STS:
            sloop.append('DataFile using "index":"asset-'+str(Nobs)+'-'+str(start-obswindow_start)+'" with lines,\\\n')
        sloop.append('\n')
        sloop.append('\n')
        sloop.append('set xtics\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "index":"'+assetname+'-logret" with lines,\\\n')
        sloop.append('\n')
        sloop.append('unset multiplot\n')
        sloop.append('\n')
        f.writelines(sloop)

    cleanup=[]
    cleanup.append('\n')
    f.writelines(cleanup)

    f.close()

    return

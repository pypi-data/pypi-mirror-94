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

def gnuplot_convergeplots(NAME,NOBSS,pars,statsfilename,gnuplotfilename):
    
    f = open(gnuplotfilename, 'w')

    header=[]
    header.append('reset\n')
    header.append('set encoding default\n')
    header.append('set terminal epslatex monochrome\n')
    header.append("set datafile separator ','\n")
    header.append('set size 1.0,1.0\n')
    header.append('set autoscale\n')
    header.append('\n')
    f.writelines(header)

    setup=[]
    setup.append('set key autotitle columnhead\n')
    setup.append('set key inside top right\n')
    setup.append('set xrange [0:'+str(np.max(NOBSS))+']\n')
    setup.append('\n')
    parst=''
    for x in pars:
        parst=parst+' '+x.replace('_','-')
    setup.append('pars="'+parst+'"\n')
    setup.append('\n')
    setup.append('DataFile="'+statsfilename+'"\n')
    setup.append('\n')
#    setup.append('unset key\n')
#    setup.append('unset title\n')
    setup.append('\n')
    f.writelines(setup)

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
        sloop=[]
        sloop.append('\n')
        sloop.append('set title "Parameter Statistics: '+x1+' '+x2+'"\n')
        sloop.append('set output "'+NAME+'_'+x+'_paramconverge.tex"\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-bias'+'" title "'+x1+' '+x2+'-bias" with lines,\\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-estd'+'" title "'+x1+' '+x2+'-estd" with lines,\\\n')
        sloop.append('\n')
        sloop.append('\n')
        f.writelines(sloop)

    cleanup=[]
    cleanup.append('\n')
    f.writelines(cleanup)

    f.close()

    return

def gnuplot_paramdistplots(NAME,NOBSS,pars,statsfilename,gnuplotfilename):
    
    f = open(gnuplotfilename, 'w')

    header=[]
    header.append('reset\n')
    header.append('set encoding default\n')
    header.append('set terminal epslatex monochrome\n')
    header.append("set datafile separator ','\n")
    header.append('set size 1.0,1.0\n')
    header.append('set autoscale\n')
    header.append('\n')
    f.writelines(header)

    setup=[]
    setup.append('set key autotitle columnhead\n')
    setup.append('set key inside bottom left\n')
    setup.append('set xrange [0:'+str(np.max(NOBSS))+']\n')
    setup.append('\n')
    setup.append('set y2tics\n')
    setup.append('set ytics nomirror\n')
    setup.append('\n')
    parst=''
    for x in pars:
        parst=parst+' '+x.replace('_','-')
    setup.append('pars="'+parst+'"\n')
    setup.append('\n')
    setup.append('DataFile="'+statsfilename+'"\n')
    setup.append('\n')
#    setup.append('unset key\n')
#    setup.append('unset title\n')
    setup.append('\n')
    f.writelines(setup)

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
        sloop=[]
        sloop.append('\n')
        sloop.append('set title "Parameter Statistics: '+x1+' '+x2+'"\n')
        sloop.append('set output "'+NAME+'_'+x+'_paramdist.tex"\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-exp'+'" title "'+x1+' '+x2+'-exp" with lines,\\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-mean'+'" title "'+x1+' '+x2+'-mean" with lines,\\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-std'+'" title "'+x1+' '+x2+'-std" axis x1y2 with lines,\\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-5'+'" title "'+x1+' '+x2+'-5" with lines,\\\n')
        sloop.append('DataFile using "Nobs":"'+x.replace('_','-')+'-95'+'" title "'+x1+' '+x2+'-95" with lines,\\\n')
        sloop.append('\n')
        sloop.append('\n')
        f.writelines(sloop)

    cleanup=[]
    cleanup.append('\n')
    f.writelines(cleanup)

    f.close()

    return

def gnuplot_plotvpaths(NAME,plotpaths,NOBSS,vpathfilename,gnuplotfilename):
    
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
    setup.append('set xrange [0:'+str(np.max(NOBSS))+']\n')
    setup.append('\n')
#    setup.append('set y2tics\n')
    setup.append('set ytics nomirror\n')
    setup.append('\n')
    setup.append('\n')
    setup.append('do for [cc=1:'+str(len(plotpaths))+'] {\n')
    setup.append('\n')
    setup.append('DataFile="'+vpathfilename+'"\n')
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

    for cc in range(0,len(plotpaths)):
        sloop=[]
        sloop.append('\n')
        sloop.append('unset xtics\n')
        sloop.append('\n')
        sloop.append('set output "'+NAME+'_vpath_'+str(plotpaths[cc])+'.tex"\n')
        sloop.append('set multiplot layout 3,1 rowsfirst\n')
        sloop.append('\n')
        sloop.append('set title "asset: '+str(plotpaths[cc])+'"\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "asset-'+str(plotpaths[cc])+'" with lines,\\\n')
        sloop.append('\n')
#        sloop.append('set title "Variance path: '+str(plotpaths[cc])+'"\n')
        sloop.append('unset title\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "variance-'+str(plotpaths[cc])+'" with lines,\\\n')
        for x in NOBSS:
            sloop.append('DataFile using "asset-'+str(plotpaths[cc])+'-'+str(x)+'" with lines,\\\n')
        sloop.append('\n')
#        sloop.append('set title "asset log-returns: '+str(plotpaths[cc])+'"\n')
        sloop.append('\n')
        sloop.append('set xtics\n')
        sloop.append('plot \\\n')
        sloop.append('DataFile using "asset-'+str(plotpaths[cc])+'-logret" with lines,\\\n')
        sloop.append('\n')
        sloop.append('unset multiplot\n')
        sloop.append('\n')
        f.writelines(sloop)

    cleanup=[]
    cleanup.append('\n')
    cleanup.append('}\n')
    cleanup.append('\n')
    f.writelines(cleanup)

    f.close()

    return

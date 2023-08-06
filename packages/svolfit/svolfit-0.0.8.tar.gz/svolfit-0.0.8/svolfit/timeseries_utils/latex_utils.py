
def latex_documentwrite(NAME,NOSTS,pars,latexfilename):
    
    NOBSS=NOSTS.RunInfo_Nobs.unique()
    
    f = open(latexfilename, 'w')

    header=[]
    header.append('\\documentclass[letterpaper,10pt]{article}\n')
    header.append('\n')
    header.append('\\usepackage{graphicx}\n')
    header.append('\\usepackage{csvsimple}\n')
    header.append('\n')
    header.append('\\extrafloats{100}\n')
    header.append('\n')
    header.append('\\begin{document}\n')
    header.append('\n')
    header.append('\\title{'+NAME.replace('_',' ')+'}\n')
    header.append('\\author{Michael A. Clayton}\n')
    header.append('\\maketitle\n')
    header.append('\n')
    header.append('\n')
    f.writelines(header)


    table=[]
    table.append('\n')
    table.append('\\section{Status Message Counts}\n')
    table.append('\n')
    table.append('\\begin{table}[ht]\n')
    table.append('\\begin{tiny}\n')
    table.append('\\begin{tabular}{c}\n')
    table.append('\\csvautotabular[respect all]{'+NAME+'_messages.csv}\n')
    table.append('\\end{tabular}\n')
    table.append('\\caption{Recall: rows will be missing if there is a comma in the message.}\n')
    table.append('\\label{table:}\n')
    table.append('\\end{tiny}\n')
    table.append('\\end{table}\n')
    table.append('\n')
#    table.append('\\clearpage\n')
    table.append('\n')
    table.append('\n')
    f.writelines(table)


#     table=[]
#     table.append('\n')
#     table.append('\\section{Convergence Rates}\n')
#     table.append('\n')
#     table.append('\\begin{table}[ht]\n')
#     table.append('\\begin{tiny}\n')
#     table.append('\\begin{tabular}{c}\n')
#     table.append('\\csvautotabular[respect all]{'+NAME+'_convergence.csv}\n')
#     table.append('\\end{tabular}\n')
#     table.append('\\caption{Parameter accuracy statistics.  Recall that since the term structure is based on estimates from the same paths the results are strongly correlated, so the reported uncertainty in the power will be underestimated.}\n')
#     table.append('\\label{table:}\n')
#     table.append('\\end{tiny}\n')
#     table.append('\\end{table}\n')
#     table.append('\n')
#     table.append('\\clearpage\n')
#     table.append('\n')
#     table.append('\n')
#     f.writelines(table)



# param start loop:
    sloop=[]
    sloop.append('\n')
    sloop.append('\section{parameters by start of window}\n')
    sloop.append('\n')
    for x in pars:    
        sloop.append('\n')
        sloop.append('\\begin{figure}[ht]\n')
        sloop.append('\\input{'+NAME+'_'+x+'_paramdist_start.tex'+'}\n')
        sloop.append('\\caption{Parameter '+x.replace('_','-')+' by start.}\n')
        sloop.append('\\label{fig:}\n')
        sloop.append('\\end{figure}\n')
        sloop.append('\n')
    sloop.append('\n')
    sloop.append('\\clearpage\n')
    sloop.append('\n')
    f.writelines(sloop)

# param finish loop:
    sloop=[]
    sloop.append('\n')
    sloop.append('\section{parameters by finish of window}\n')
    sloop.append('\n')
    for x in pars:    
        sloop.append('\n')
        sloop.append('\\begin{figure}[ht]\n')
        sloop.append('\\input{'+NAME+'_'+x+'_paramdist_finish.tex'+'}\n')
        sloop.append('\\caption{Parameter '+x.replace('_','-')+' by finish.}\n')
        sloop.append('\\label{fig:}\n')
        sloop.append('\\end{figure}\n')
        sloop.append('\n')
    sloop.append('\n')
    sloop.append('\\clearpage\n')
    sloop.append('\n')
    f.writelines(sloop)




# # dist loop:
#     sloop=[]
#     sloop.append('\n')
#     sloop.append('\section{Parameter Convergence}\n')
#     sloop.append('\n')
#     for x in pars:    
#         sloop.append('\n')
#         sloop.append('\\begin{figure}[ht]\n')
#         sloop.append('\\input{'+NAME+'_'+x+'_paramdist.tex'+'}\n')
#         sloop.append('\\caption{Parameter estimator convergence.}\n')
#         sloop.append('\\label{fig:}\n')
#         sloop.append('\\end{figure}\n')
#         sloop.append('\n')
#     sloop.append('\n')
#     sloop.append('\\clearpage\n')
#     sloop.append('\n')
#     f.writelines(sloop)

#     corr=[]
#     # corr.append('\n')
#     # corr.append('\\section{Parameter Estimate Correlations}\n')
#     # corr.append('\n')
#     # corr.append('\n')
#     # for Nobs in ReportCorr:
#     #     corr.append('\\begin{table}[ht]\n')
#     #     corr.append('\\begin{small}\n')
#     #     corr.append('\\begin{tabular}{c}\n')
#     #     corr.append('\\csvautotabular[respect all]{'+NAME+'_corr_'+str(Nobs)+'.csv}\n')
#     #     corr.append('\\end{tabular}\n')
#     #     corr.append('\\caption{Parameter estimator correlation, Nobs= '+str(Nobs)+'.}\n')
#     #     corr.append('\\label{table:}\n')
#     #     corr.append('\\end{small}\n')
#     #     corr.append('\\end{table}\n')
#     #     corr.append('\n')
#     # corr.append('\n')

#     corr.append('\n')
#     for Nobs in ReportCorr:
#         corr.append('\\begin{table}[ht]\n')
#         corr.append('\\begin{small}\n')
#         corr.append('\\begin{tabular}{c}\n')
#         corr.append('\\csvautotabular[respect all]{'+NAME+'_corr_rep_'+str(Nobs)+'.csv}\n')
#         corr.append('\\end{tabular}\n')
#         corr.append('\\caption{Parameter estimator correlation, Nobs= '+str(Nobs)+'.}\n')
#         corr.append('\\label{table:}\n')
#         corr.append('\\end{small}\n')
#         corr.append('\\end{table}\n')
#         corr.append('\n')
#     corr.append('\n')

#     corr.append('\n')
#     for Nobs in ReportCorr:
#         corr.append('\\begin{table}[ht]\n')
#         corr.append('\\begin{small}\n')
#         corr.append('\\begin{tabular}{c}\n')
#         corr.append('\\csvautotabular[respect all]{'+NAME+'_corr_wrk_'+str(Nobs)+'.csv}\n')
#         corr.append('\\end{tabular}\n')
#         corr.append('\\caption{Parameter estimator correlation, Nobs= '+str(Nobs)+'.}\n')
#         corr.append('\\label{table:}\n')
#         corr.append('\\end{small}\n')
#         corr.append('\\end{table}\n')
#         corr.append('\n')
#     corr.append('\n')

#     corr.append('\n')
#     for Nobs in ReportCorr:
#         corr.append('\\begin{table}[ht]\n')
#         corr.append('\\begin{small}\n')
#         corr.append('\\begin{tabular}{c}\n')
#         corr.append('\\csvautotabular[respect all]{'+NAME+'_corr_eigen_rep_'+str(Nobs)+'.csv}\n')
#         corr.append('\\end{tabular}\n')
#         corr.append('\\caption{Parameter estimator correlation eigen-analysis, Nobs= '+str(Nobs)+'.}\n')
#         corr.append('\\label{table:}\n')
#         corr.append('\\end{small}\n')
#         corr.append('\\end{table}\n')
#         corr.append('\n')
#     corr.append('\n')

#     corr.append('\n')
#     for Nobs in ReportCorr:
#         corr.append('\\begin{table}[ht]\n')
#         corr.append('\\begin{small}\n')
#         corr.append('\\begin{tabular}{c}\n')
#         corr.append('\\csvautotabular[respect all]{'+NAME+'_corr_eigen_wrk_'+str(Nobs)+'.csv}\n')
#         corr.append('\\end{tabular}\n')
#         corr.append('\\caption{Parameter estimator correlation eigen-analysis, Nobs= '+str(Nobs)+'.}\n')
#         corr.append('\\label{table:}\n')
#         corr.append('\\end{small}\n')
#         corr.append('\\end{table}\n')
#         corr.append('\n')
#     corr.append('\n')


#     corr.append('\\clearpage\n')
#     corr.append('\n')
#     f.writelines(corr)


#     cov=[]
#     cov.append('\n')
#     for Nobs in ReportCorr:
#         cov.append('\\begin{table}[ht]\n')
#         cov.append('\\begin{tiny}\n')
#         cov.append('\\begin{tabular}{c}\n')
#         cov.append('\\csvautotabular[respect all]{'+NAME+'_cov_rep_'+str(Nobs)+'.csv}\n')
#         cov.append('\\end{tabular}\n')
#         cov.append('\\caption{Parameter estimator covariance, Nobs= '+str(Nobs)+'.}\n')
#         cov.append('\\label{table:}\n')
#         cov.append('\\end{tiny}\n')
#         cov.append('\\end{table}\n')
#         cov.append('\n')
#     cov.append('\n')

#     cov.append('\n')
#     for Nobs in ReportCorr:
#         cov.append('\\begin{table}[ht]\n')
#         cov.append('\\begin{tiny}\n')
#         cov.append('\\begin{tabular}{c}\n')
#         cov.append('\\csvautotabular[respect all]{'+NAME+'_cov_wrk_'+str(Nobs)+'.csv}\n')
#         cov.append('\\end{tabular}\n')
#         cov.append('\\caption{Parameter estimator covariance, Nobs= '+str(Nobs)+'.}\n')
#         cov.append('\\label{table:}\n')
#         cov.append('\\end{tiny}\n')
#         cov.append('\\end{table}\n')
#         cov.append('\n')
#     cov.append('\n')

#     cov.append('\n')
#     for Nobs in ReportCorr:
#         cov.append('\\begin{table}[ht]\n')
#         cov.append('\\begin{tiny}\n')
#         cov.append('\\begin{tabular}{c}\n')
#         cov.append('\\csvautotabular[respect all]{'+NAME+'_cov_eigen_rep_'+str(Nobs)+'.csv}\n')
#         cov.append('\\end{tabular}\n')
#         cov.append('\\caption{Parameter estimator covariance eigen-analysis, Nobs= '+str(Nobs)+'.}\n')
#         cov.append('\\label{table:}\n')
#         cov.append('\\end{tiny}\n')
#         cov.append('\\end{table}\n')
#         cov.append('\n')
#     cov.append('\n')

#     cov.append('\n')
#     for Nobs in ReportCorr:
#         cov.append('\\begin{table}[ht]\n')
#         cov.append('\\begin{tiny}\n')
#         cov.append('\\begin{tabular}{c}\n')
#         cov.append('\\csvautotabular[respect all]{'+NAME+'_cov_eigen_wrk_'+str(Nobs)+'.csv}\n')
#         cov.append('\\end{tabular}\n')
#         cov.append('\\caption{Parameter estimator covariance eigen-analysis, Nobs= '+str(Nobs)+'.}\n')
#         cov.append('\\label{table:}\n')
#         cov.append('\\end{tiny}\n')
#         cov.append('\\end{table}\n')
#         cov.append('\n')
#     cov.append('\n')

#     cov.append('\\clearpage\n')
#     cov.append('\n')
#     f.writelines(cov)




    vpaths=[]
    vpaths.append('\n')
    vpaths.append('\\section{Variance Path Plots}\n')
    vpaths.append('\n')
    NOBSS=NOSTS.RunInfo_Nobs.unique()
    for Nobs in NOBSS:
        vpaths.append('\n')
        vpaths.append('\\begin{figure}[ht]\n')
        vpaths.append('\\input{'+NAME+'_vpath_'+str(Nobs)+'.tex'+'}\n')
        vpaths.append('\\caption{variance path and estimation, Nobs: '+str(Nobs)+'.}\n')
        vpaths.append('\\label{fig:}\n')
        vpaths.append('\\end{figure}\n')
        vpaths.append('\n')
        
    vpaths.append('\n')
    vpaths.append('\\clearpage\n')
    vpaths.append('\n')
    f.writelines(vpaths)

    cleanup=[]
    cleanup.append('\n')
    cleanup.append('\\end{document}\n')
    cleanup.append('\n')
    f.writelines(cleanup)

    f.close()

    return


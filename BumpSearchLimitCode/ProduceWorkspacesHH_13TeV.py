import os
import ROOT as rt
from ROOT import *
ROOT.gROOT.SetBatch(True)

#masses = [1200]
#signals = ["Radion"]
#subtrs = [""]
masses =[1200,1400,1600,1800,2000,2500]
signals = ["Radion", "Graviton"]
subtrs = ["", "_subtr"]

for mass in masses:
  for signalin in signals:
    for subtr in subtrs:

      signal = signalin  + "" + subtr

      outputname = "submit_HH_" + signal + "_"+str(mass)+".src"
      logname = "submit_HH_" + signal + "_"+str(mass)+".log"
      outputfile = open(outputname,'w')
      outputfile.write('#!/bin/bash\n')
      outputfile.write("cd ${CMSSW_BASE}/src/HH4b/BumpSearchLimitCode; eval `scramv1 run -sh`\n")
#      if mass == 1800 && signalin == "Graviton":
      outputfile.write("root -b -q 'R2JJFitterHH_13TeV.cc("+str(mass)+', "' + signal + '",0,0,50000.)'+"'\n")
      outputfile.write("combineCards.py datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_3btag_HPHP_cat1.txt datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_4btag_cat0.txt &>datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_2cat.txt\n")
      outputfile.write("combine datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_2cat.txt -M Asymptotic  -n " + signal +  " -m "+str(mass)+"\n")
    #  outputfile.write("combine datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_3btag_HPLP_cat2.txt -M Asymptotic -n " + signal +  "_3btag_HPLP_cat2 -m "+str(mass)+"\n")
      outputfile.write("combine datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_3btag_HPHP_cat1.txt -M Asymptotic -n " + signal +  "_3btag_HPHP_cat1  -m "+str(mass)+"\n")
      outputfile.write("combine datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_4btag_cat0.txt -M Asymptotic -n " + signal +  "_4btag_cat0 -m "+str(mass)+"\n")
      
      outputfile.write("mv higgsCombine" + signal +  ".Asymptotic.mH"+str(mass)+".root LimitOutput\n")
    #  outputfile.write("mv higgsCombine" + signal +  "_3btag_HPLP_cat2.Asymptotic.mH"+str(mass)+".root LimitOutput\n") 
      outputfile.write("mv higgsCombine" + signal +  "_3btag_HPHP_cat1.Asymptotic.mH"+str(mass)+".root LimitOutput\n") 
      outputfile.write("mv higgsCombine" + signal +  "_4btag_cat0.Asymptotic.mH"+str(mass)+".root LimitOutput\n")
      
    # ============================ Make post nuisance plots ===================
      
      outputfile.write("combine datacards/" + signal +  "CMS_jj_HH_"+str(mass)+"_13TeV_CMS_jj_2cat.txt -M MaxLikelihoodFit  -n " + signal +  "_mjj -m "+str(mass)+"\n")
      outputfile.write("mv mlfit" + signal +  "_mjj.root  nuisances/mlfit" + signal + "_mjj_"+str(mass)+".root \n") 
      outputfile.write("rm higgsCombine" + signal + "_mjj.MaxLikelihoodFit.mH"+str(mass)+".root\n")
      outputfile.write("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a nuisances/mlfit" + signal +  "_mjj_"+str(mass)+".root -g nuisances/plot_PULLS_"+signal+"_mjj_"+str(mass)+".root>nuisances/pulls_"+ signal + "_mjj_"+str(mass)+".txt\n")
      
# ==========================================================================
      
      outputfile.close()
      
      command="rm "+logname
      print command
      os.system(command)
  #command="bsub -q 1nh -o "+logname+" source "+outputname
      command="chmod 755 ./"+outputname+";./"+outputname
      print command
      os.system(command)
      
    # ============================ Make post nuisance plots ===================
    
      fileIN = rt.TFile.Open("nuisances/plot_PULLS_" + signal + "_mjj_"+str(mass)+".root")
      post_fit_errs=fileIN.Get("post_fit_errs;1")
      post_fit_errs.Draw()
      post_fit_errs.SaveAs("nuisances/post_fit_errs_" + signal + "_mjj_"+str(mass)+".pdf")
      post_fit_errs.SaveAs("nuisances/post_fit_errs_" + signal + "_mjj_"+str(mass)+".png")
      nuisancs=fileIN.Get("nuisancs;1")
      nuisancs.Draw()
      nuisancs.SaveAs("nuisances/nuisances_" + signal + "_mjj_"+str(mass)+".pdf")
      nuisancs.SaveAs("nuisances/nuisances_" + signal + "_mjj_"+str(mass)+".png")
      fileIN.Close()

outputname = "make_brazilian_flag.src"
logname = "make_brazilian_flag.log"
outputfile = open(outputname,'w')
outputfile.write('#!/bin/bash\n')
outputfile.write("source RunLimit.sh LimitOutput 0 0\n")
outputfile.write("source RunLimit.sh LimitOutput 0 1\n")
outputfile.close()

command="rm "+logname
print command
os.system(command)
command="chmod 755 ./"+outputname+";./"+outputname
print command
os.system(command)

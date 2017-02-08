import os

#https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SWGuideNonStandardCombineUses#Conventional_bias_studies_with_R

masses =[1200, 1600, 2000, 2500]
ievts =[0,2,5,10]
masses =[1600]
ievts =[0]

start = -1
#itoys = 250
itoys = 100

for mass in masses:
  for ievt in ievts:  
    
    outputname = "bias_HH_Graviton_"+str(mass)+"_"+str(ievt)+".src"
    logname = "bias_HH_Graviton_"+str(mass)+"_"+str(ievt)+".log"
    outputfile = open(outputname,'w')
    outputfile.write('#!/bin/bash\n')
    outputfile.write("cd ${CMSSW_BASE}/src/HH4b/AABH/BiasStudies; eval `scramv1 run -sh`\n")

    outputfile.write("root -b -q 'WSMakerForToys.C(0)'\n")
    outputfile.write("root -b -q 'WSMakerForToys.C(1)'\n")


      
        
    outputfile.write("combine datacards/toys_"+str(mass)+".txt -M GenerateOnly --setPhysicsModelParameters pdf_index=0 --freezeNuisances pdf_index,mjjlin_TT_,mjjlin_LL_ --toysFrequentist -t "+str(itoys)+" --expectSignal " + str(ievt) + " --saveToys -m "+str(mass)+" \n")
    outputfile.write("mv higgsCombineTest.GenerateOnly.mH"+str(mass)+".123456.root toys/higgsCombineTest.GenerateOnly.mH"+str(mass)+"_mu"+str(ievt)+".root\n")
    outputfile.write("combine datacards/toys_"+str(mass)+".txt -M MaxLikelihoodFit --toysFile toys/higgsCombineTest.GenerateOnly.mH"+str(mass)+"_mu"+str(ievt)+".root -t "+str(itoys)+" --rMin -30 --rMax 60 --minimizerTolerance 0.1 --setPhysicsModelParameters pdf_index=0 --freezeNuisances pdf_index,mjjlin_TT_,mjjlin_LL_\n");
        
    outputfile.write("mv mlfit.root toys/mlfit_"+str(mass)+"_mu"+str(ievt)+".root\n")
    outputfile.write("root -b -q 'BiasStudies.C("+str(mass)+", "+str(ievt)+")'\n")  
    outputfile.close()
        
    command="rm "+logname
    print command
    os.system(command)
  #command="bsub -q 1nh -o "+logname+" source "+outputname
    command="chmod 755 ./"+outputname+";./"+outputname
    print command
    os.system(command)
   

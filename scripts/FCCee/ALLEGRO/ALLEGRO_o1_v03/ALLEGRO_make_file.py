import ROOT
from podio import root_io
import dd4hep as dd4hepModule
from ROOT import dd4hep
import argparse
import numpy as np
import os
from dd4hep import Detector
import DDRec


def make_file(args):
  
  # create output ROOT file
  outputFile = ROOT.TFile(args.outputFile, "RECREATE")

  # set file reader
  podio_reader = root_io.Reader(args.inputFile)

  # get detector description for cell id decoding
  #theDetector = Detector.getInstance()
  #theDetector.fromXML(os.environ["$K4GEO"]+"/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml") 
  #idposConv = DDRec.CellIDPositionConverter(theDetector)
                  

  ########## Count Photon Hits #########################

  hist_ccE = ROOT.TH1F("h_CaloCluster_E", "CaloCluster Energy",
                       100, 0, 15)
  hist_ctcE = ROOT.TH1F("h_CaloTopoCluster_E", "CaloTopoCluster Energy",
                        100, 0, 15)
  hist_ecal_totE = ROOT.TH1F("h_ECalBarrelModuleThetaMergedPosition_totE",
                             "ECalBarrelModuleThetaMergedPosition total Energy per evt",
                             100, 0, 15)
  hist_ecal_posX = ROOT.TH1F("h_ECalBarrelModuleThetaMergedPosition_posX",
                             "ECalBarrelModuleThetaMergedPosition position X",
                             150, -2770, 2770)
  hist_ecal_posY = ROOT.TH1F("h_ECalBarrelModuleThetaMergedPosition_posY",
                             "ECalBarrelModuleThetaMergedPosition position Y",
                             150, -2770, 2770)
  hist_ecal_posZ = ROOT.TH1F("h_ECalBarrelModuleThetaMergedPosition_posZ",
                             "ECalBarrelModuleThetaMergedPosition position Z",
                             150, -3100, 3100)
  
  
  # loop over dataset
  for event in podio_reader.get("events"):

    for calo in event.get("CaloClusters"):
      energy =  calo.getEnergy()
      hist_ccE.Fill(energy)

    for calo in event.get("CaloTopoClusters"):
      energy =  calo.energy()
      hist_ctcE.Fill(energy)

    energy = 0
    for ecal in event.get("ECalBarrelModuleThetaMergedPositioned"):
        energy += ecal.energy()
        hist_ecal_posX.Fill(ecal.position().x)
        hist_ecal_posY.Fill(ecal.position().y)
        hist_ecal_posZ.Fill(ecal.position().z)
    hist_ecal_totE.Fill(energy)

  n_evts = len(podio_reader.get("events"))

  if not args.no_norm:
    factor = 1./n_evts
    #hist_ccE.Scale(factor)
    #hist_ctcE.Scale(factor)

  hist_ccE.Write()
  hist_ctcE.Write()
  hist_ecal_totE.Write()
  hist_ecal_posX.Write()
  hist_ecal_posY.Write()
  hist_ecal_posZ.Write()
  
  outputFile.Close()

  return
  

#########################################################################

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
        description="Process simulation"
    )
  parser.add_argument('-f', "--inputFile",  type=str, 
                      help='The name of the simulation file to be processed', default='ARC_sim.root')
  parser.add_argument('-o', "--outputFile", type=str, 
                      help='The name of the ROOT file where to save output histograms', default='ARC_analysis.root')
  parser.add_argument('--no_norm', action='store_true',
                      help='Do not normalize output histograms by number of events')
  args = parser.parse_args()
    
  make_file(args)  
  
  
  
  
  

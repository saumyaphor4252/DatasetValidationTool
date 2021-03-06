import FWCore.ParameterSet.Config as cms
import os
import sys

#arglist = sys.argv
#filename = arglist[2]
#filename='CDC2018Av1.txt'
#basename = os.path.splitext(filename)[0]

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.MagneticField_cff') # B-field map
process.load('Configuration.Geometry.GeometryRecoDB_cff') # Ideal geometry and interface
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff") # Global tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag,'auto:run2_data','')

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000))

import Alignment.CommonAlignment.tools.trackselectionRefitting as trackselRefit
process.seqTrackselRefit = trackselRefit.getSequence(process, 'ALCARECOTkAlCosmicsCTF0T',
                                                     isPVValidation=False, 
                                                     TTRHBuilder='WithAngleAndTemplate',
                                                     usePixelQualityFlag=True,
                                                     openMassWindow=False,
                                                     cosmicsDecoMode=True,
                                                     cosmicsZeroTesla=False,
                                                     momentumConstraint=None,
                                                     cosmicTrackSplitting=False,
                                                     use_d0cut=False)

#import FWCore.Utilities.FileUtils as FileUtils
#readFiles = cms.untracked.vstring()
#readFiles = cms.untracked.vstring( FileUtils.loadListFromFile (os.environ['CMSSW_BASE']+'/src/DatasetValidation/DatasetValidationTool/test/'+str(filename)) )
process.source = cms.Source("PoolSource", #fileNames = readFiles
    fileNames = cms.untracked.vstring(
#'root://cms-xrd-global.cern.ch//store/mc/RunIIWinter19PFCalibDRPremix/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/ALCARECO/TkAlZMuMu-2016Conditions_newPixelConditions_105X_mcRun2_asymptotic_newPixCond_v2-v1/00000/0318507B-70C6-3C49-9CCD-1BB33CD77F07.root'
#'root://cms-xrd-global.cern.ch//store/mc/RunIIWinter19PFCalibDRPremix/DYJetsToMuMu_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/ALCARECO/TkAlZMuMu-2017Conditions_105X_mc2017_realistic_v5-v1/50000/26667A8C-00F9-344A-B1B6-22120103CC6A.root'
#'root://cms-xrd-global.cern.ch//store/mc/RunIIWinter19CosmicDR/TKCosmics_0T/ALCARECO/TkAlCosmics0T-0T_103X_upgrade2018cosmics_realistic_deco_v7-v3/110000/18E5DA07-134D-B247-BFE0-1E3BB01D48EA.root'
#'root://cms-xrd-global.cern.ch//store/mc/RunIIWinter19CosmicDR/TKCosmics_0T/ALCARECO/TkAlCosmics0T-0T_103X_mcRun2cosmics_startup_deco_v3-v1/270000/8E7E5F40-B15D-8A4A-B050-4EAD0A31571C.root'
#        'root://cms-xrd-global.cern.ch//store/data/Run2016A/Cosmics/ALCARECO/TkAlCosmics0T-07Dec2018-v1/20000/783C9E32-480B-E911-92B2-20040FE8ECAC.root',
#        'root://cms-xrd-global.cern.ch//store/data/Run2016H/DoubleMuon/ALCARECO/TkAlZMuMu-07Aug17-v1/90000/FA413FBB-A599-E711-B7AC-0CC47A7C3472.root'
#        'root://cms-xrd-global.cern.ch//store/data/Run2016H/SingleMuon/ALCARECO/TkAlMuonIsolated-07Aug17-v1/90000/FCB1CBE1-0790-E711-8359-3417EBE2F316.root'
#        'root://cms-xrd-global.cern.ch//store/data/Run2016E/ZeroBias/ALCARECO/TkAlMinBias-07Aug17-v1/90000/FEA7EA10-338D-E711-8AB6-003048FFD75A.root'
#         'root://cms-xrd-global.cern.ch//store/data/Run2016A/Cosmics/ALCARECO/TkAlCosmics0T-07Dec2018-v1/20000/783C9E32-480B-E911-92B2-20040FE8ECAC.root',
#         'root://cms-xrd-global.cern.ch//store/data/Run2016D/Cosmics/ALCARECO/TkAlCosmics0T-07Dec2018-v1/20000/8A715B05-EF0A-E911-B731-782BCB20ED64.root',
         'root://cms-xrd-global.cern.ch//store/data/Run2016C/Cosmics/ALCARECO/TkAlCosmics0T-07Dec2018-v1/20000/F443086A-3C0B-E911-AA8F-14187741013C.root',
#         'root://cms-xrd-global.cern.ch//store/data/Run2016C/Cosmics/ALCARECO/TkAlCosmics0T-07Dec2018-v1/20000/10E8FF4A-530B-E911-9150-549F3525BBCC.root'
    )
)

process.demo = cms.EDAnalyzer('DatasetValidationTool',
#     tracks = cms.InputTag("ALCARECOTkAlCosmicsCTF0T"),
      BS = cms.InputTag("offlineBeamSpot"),
      tracks = cms.InputTag("FinalTrackRefitter"),
      vertices= cms.InputTag("offlinePrimaryVertices"),
      IsResonance=cms.bool(True)
#     tracks = cms.InputTag("ALCARECOTkAlMuonIsolated")
#     tracks = cms.InputTag("ALCARECOTkAlMinBias")
)

process.TFileService = cms.Service("TFileService",
     fileName = cms.string('Zmumu_2018.root')
)


process.p = cms.Path(process.seqTrackselRefit*process.demo)

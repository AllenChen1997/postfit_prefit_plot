#created by Fasya Khuzaimah on 2020.05.01
#re-edit by Kung-Hsiang on 2020.05.08
import sys
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv.append( '-b-' )
from ROOT import TFile, TH1F, TGraph, TGraphAsymmErrors


import PlotTemplates
from PlotTemplates import *

import array as arr

RegionList = ['SR', 'TOPE', 'TOPMU', 'WE', 'WMU', 'ZEE', 'ZMUMU']
RegionName = ['SR', 'Top (e) CR', 'Top (mu) CR', 
              'W (e) CR', 'W (mu) CR', 'Z (ee) CR', 'Z (mumu) CR']
nbins = 4
edges = arr.array('f')
filename = TFile("fitDiagnostics.root")

for iRegionList in range(len(RegionList)):
#------------------------ postfit ------------------------------#

	postfit = "shapes_fit_b/"+RegionList[iRegionList]

	#get the histogram inside shapes_fit_b/TOPE

	Temp_postfit = filename.Get(postfit+"/total_background")
	Temp_postfit.SetTitle("post-fit")

	Datatmp = filename.Get(postfit+"/data")
	Temp_data = Temp_postfit.Clone("data")
	Temp_data.Reset()
	nPointsTope = Datatmp.GetN()
	x = ROOT.Double(0)
	y = ROOT.Double(0)
	for i in range(nPointsTope):
		Datatmp.GetPoint(i, x, y)
		k = Temp_data.FindFixBin(x)
		#print "y", y
		Temp_data.SetBinContent(k, y)
		Temp_data.SetBinError(i+1, Datatmp.GetErrorY(i))
	#------------------------ prefit ------------------------------#

	prefit = "shapes_prefit/"+RegionList[iRegionList]
	#get the histogram inside shapes_fit_b/TOPE

	Temp_prefit = filename.Get(prefit+"/total_background")
	Temp_prefit.SetTitle("pre-fit")

	#----------------------postfit prefit plot--------------------------#

	c1 = PlotTemplates.myCanvas()
	h_postfit = PlotTemplates.Save1DHisto(Temp_postfit, c1, "p^{miss}_{T}", "Events")
	# change the axis size
	h_postfit.GetXaxis().SetTitleSize(0.05)
	h_postfit.GetXaxis().SetTitleOffset(0.87)
	h_postfit.GetYaxis().SetTitleSize(0.05)
	h_postfit.GetYaxis().SetTitleOffset(0.9)
	h_postfit.GetXaxis().SetLabelSize(0.05)
	h_postfit.GetYaxis().SetLabelSize(0.05)
	h_postfit.SetLineColor(2)
	h_prefit = PlotTemplates.Save1DHisto(Temp_prefit, c1, "p^{miss}_{T}", "Events")
	h_prefit.SetLineColor(4)
	h_data = PlotTemplates.Save1DHisto(Temp_data, c1, "p^{miss}_{T}", "Events")
	h_data.SetMarkerStyle(20)
	
	# check the maximum of three histo	
	hmax = h_postfit.GetMaximum()
	print 'hmax= ',hmax
	if (hmax < h_prefit.GetMaximum()):
		hmax = h_prefit.GetMaximum()
		print 'hmax= ',hmax
	if (hmax < h_data.GetMaximum()):
		hmax = h_data.GetMaximum()
		print 'hmax= ',hmax
	h_postfit.SetMaximum(hmax)
		
	h_postfit.Draw("HIST E")
	h_prefit.Draw("SAME HIST E")
	h_data.Draw("SAME")

	leg1 = PlotTemplates.SetLegend(coordinate_=[.55,.7,.75,.87])
	leg1.AddEntry(h_postfit, "post-fit")
	leg1.AddEntry(h_prefit, "pre-fit")
	leg1.AddEntry(h_data,"data")
	leg1.Draw()

	text = ROOT.TLatex()
	text.SetTextFont(42)
	text.SetTextSize(0.05)
	#decide where to put the text
	placeX = h_postfit.GetXaxis().GetXmin() + 0.25 * (h_postfit.GetXaxis().GetXmax() - h_postfit.GetXaxis().GetXmin())
	placeY = 0.95 * h_postfit.GetMaximum()
	text.DrawLatex(placeX,placeY,RegionName[iRegionList])

	E1 = PlotTemplates.drawenergy(is2017 = True, data=True)
	# 1 = CMS , change 2 = Internal, change 3 = 41fb-1(13TeV)
	count = 0
	text2 = 'Internal'
	text3 = '41 fb^{-1} (13 TeV)'
	for i in E1:
		count = count + 1
		if ( count == 2 ):
			i.Clear()
			i.AddText(0.15,0.4,text2)
		if ( count == 3 ):
			i.Clear()
			i.AddText(0.55,0.5,text3)
		i.Draw()

	c1.cd()
	c1.Modified()
	c1.Update()
	#c1.SaveAs("pre_post_data_comparison_region"+RegionList[iRegionList]+".pdf")
	if (iRegionList == 0):	
		c1.SaveAs("pre_post_data_comparison.pdf(","pdf")
	elif ( iRegionList == len(RegionList)-1 ):
		c1.SaveAs("pre_post_data_comparison.pdf)","pdf")
	else:
		c1.SaveAs("pre_post_data_comparison.pdf","pdf")

#created by Fasya Khuzaimah on 2020.05.01
#re-edit by Kung-Hsiang on 2020.05.08

import ROOT
from ROOT import TFile, TH1F, TGraph, TGraphAsymmErrors

import PlotTemplates
from PlotTemplates import *

import array as arr

nbins = 4
edges = arr.array('f')
min = 0.0
max = 10.0
file = TFile("fitDiagnostics.root")


#------------------------ postfit ------------------------------#

postfit = "shapes_fit_b/TOPE/"
#getDir = file.cd("shapes_fit_b/TOPE")

#get the histogram inside shapes_fit_b/TOPE

Topepostfit = file.Get(postfit+"total_background")
Topepostfit.SetTitle("post-fit")

Topedata = file.Get(postfit+"data")
dataTope = Topepostfit.Clone("data")
dataTope.Reset()
nPointsTope = Topedata.GetN()
x = ROOT.Double(0)
y = ROOT.Double(0)
for i in range(nPointsTope):
    Topedata.GetPoint(i, x, y)
    k = dataTope.FindFixBin(x)
    print "y", y
    dataTope.SetBinContent(k, y)
    dataTope.SetBinError(i+1, Topedata.GetErrorY(i))
#------------------------ prefit ------------------------------#

prefit = "shapes_prefit/TOPE/"
#get the histogram inside shapes_fit_b/TOPE

Topeprefit = file.Get(prefit+"total_background")
Topeprefit.SetTitle("pre-fit")

Topedata2 = file.Get(prefit+"data")
dataTope2 = Topeprefit.Clone("data")
dataTope2.Reset()
nPointsTope = Topedata2.GetN()
x = ROOT.Double(0)
y = ROOT.Double(0)
for i in range(nPointsTope):
    Topedata2.GetPoint(i, x, y)
    k = dataTope2.FindFixBin(x)
    print "y", y
    dataTope2.SetBinContent(k, y)
    dataTope2.SetBinError(i+1, Topedata2.GetErrorY(i))

#----------------------postfit prefit plot--------------------------#

c1 = PlotTemplates.myCanvas()
h_topepostfit = PlotTemplates.Save1DHisto(Topepostfit, c1, "P^{miss}_{T}", "Events")
h_topepostfit.SetLineColor(2)
h_topeprefit = PlotTemplates.Save1DHisto(Topeprefit, c1, "P^{miss}_{T}", "Events")
h_topeprefit.SetLineColor(4)
h_data = PlotTemplates.Save1DHisto(dataTope, c1, "P^{miss}_{T}", "Events")
h_data.SetMarkerStyle(20)

h_topepostfit.Draw("HIST E")
h_topeprefit.Draw("SAME HIST E")
h_data.Draw("SAME")

leg1 = PlotTemplates.SetLegend(coordinate_=[.25,.7,.57,.87])
leg1.AddEntry(h_topepostfit, "post-fit")
leg1.AddEntry(h_topeprefit, "pre-fit")
leg1.AddEntry(h_data,"data")
leg1.Draw()

text = ROOT.TLatex()
text.SetTextFont(42)
text.SetTextSize(0.05)
text.DrawLatex(700,5,"Top (e) CR ")

E1 = PlotTemplates.drawenergy(is2017 = True, data=True)
# 1 = CMS , change 2 = Internal, change 3 = 41fb-1(13TeV)
count = 0
text2 = 'Internal'
text3 = '41 fb^{-1} (13 TeV)'
for i in E1:
	count = count + 1
	if ( count == 2 ):
		i.Clear()
		i.AddText(0.215,0.4,text2)
	if ( count == 3 ):
		i.Clear()
		i.AddText(0.7,0.5,text3)
	i.Draw()

c1.cd()
c1.Modified()
c1.Update()
c1.SaveAs("Tope_test.pdf")
c1.SaveAs("Tope_test.png")

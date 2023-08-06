import ROOT

# 1. model with Poisson[obs | exp]
def test1():
    print("TEST 1")
    ws = ROOT.RooWorkspace()
    obs = ws.factory('obs[0, 1000]')
    pdf = ws.factory("Poisson:pdf(obs, exp[20, 0, 1000])")
    data_toy = pdf.generate(ROOT.RooArgSet(obs), 1)
    data_toy.Print("V")

    data_asimov = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(pdf, ROOT.RooArgSet(obs))
    data_asimov.Print("V")


# 2. model with Gaus[obs | exp, sigma]
def test2():
    print("TEST 2")
    ws = ROOT.RooWorkspace()
    obs = ws.factory('obs[0, 1000]')
    pdf = ws.factory("RooGaussian:pdf(obs, exp[20, 0, 1000], sigma[3, 1, 10])")
    data_toy = pdf.generate(ROOT.RooArgSet(obs), 1)     # no problem here
    data_toy.Print("V")

    #ws.obj('sigma').setConstant(True)   # <<<---- this solve the issue
    data_asimov = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(pdf, ROOT.RooArgSet(obs))
    
    ### ERROR ###
    ### [#0] ERROR:Generation -- AsymptoticCalculator::SetObsExpected( RooGaussian ) : Has two non-const arguments  
    data_asimov.Print("V")


# 3. model with Gaus[obs | exp, sqrt(exp)]
def test3():
    print("TEST 3")
    ws = ROOT.RooWorkspace()
    obs = ws.factory('obs[0, 1000]')
    sqrt_exp = ws.factory('expr:sqrt_exp("sqrt(@0)", exp[20, 0, 1000])')
    pdf = ws.factory("RooGaussian:pdf(obs, exp, sqrt_exp)")
    data_toy = pdf.generate(ROOT.RooArgSet(obs), 1)    # no problem here
    data_toy.Print("V")

    #ws.obj('exp').setConstant(True)   # <<<---- this solve the issue
    data_asimov = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(pdf, ROOT.RooArgSet(obs))
    #ws.obj('exp').setConstant(False)

    ### ERROR ###
    ### [#0] ERROR:Generation -- AsymptoticCalculator::SetObsExpected( RooGaussian ) : Has two non-const arguments  
    data_asimov.Print("V")


# 4. model with Gaus[obs | exp * 2, sqrt(exp * 2)]
def test4():
    print("TEST 4")
    ws = ROOT.RooWorkspace()
    obs = ws.factory('obs[0, 1000]')
    exp = ws.factory("exp[20, 0, 1000]")
    ws.factory('expr:exp2("2 * @0", exp)')
    ws.factory('expr:sqrt_exp2("sqrt(@0)", exp2)')
    pdf = ws.factory("RooGaussian:pdf(obs, exp2, sqrt_exp2)")
    data_toy = pdf.generate(ROOT.RooArgSet(obs), 1)    # no problem here
    data_toy.Print("V")

    ws.obj('exp').setConstant(True)   # <<<---- this ***do not*** solve the issue
    data_asimov = ROOT.RooStats.AsymptoticCalculator.GenerateAsimovData(pdf, ROOT.RooArgSet(obs))
    ws.obj('exp').setConstant(False)

    ### ERROR ###
    ### [#0] ERROR:Generation -- AsymptoticCalculator::SetObsExpected( RooGaussian ) : Has two non-const arguments  
    data_asimov.Print("V")




#test1()
#test2()  ### [#0] ERROR:Generation -- AsymptoticCalculator::SetObsExpected( RooGaussian ) : Has two non-const arguments  
#test3()  ### [#0] ERROR:Generation -- AsymptoticCalculator::SetObsExpected( RooGaussian ) : Has two non-const arguments  
#test4()  ### [#0] ERROR:Generation -- AsymptoticCalculator::SetObsExpected( RooGaussian ) : Has two non-const arguments  
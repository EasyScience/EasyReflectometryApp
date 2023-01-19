function Controller()
{
  installer.autoRejectMessageBoxes()
  gui.setSilent(true)
}

Controller.prototype.IntroductionPageCallback = function()
{
  console.log("* enter IntroductionPage")
  gui.clickButton(buttons.NextButton)
  console.log("   exit IntroductionPage")
}

Controller.prototype.TargetDirectoryPageCallback = function()
{
  console.log("* enter TargetDirectoryPage")
  gui.clickButton(buttons.NextButton)
  console.log("   exit TargetDirectoryPage")
}

Controller.prototype.ComponentSelectionPageCallback = function()
{
  console.log("* enter ComponentSelectionPage")
  var page = gui.currentPageWidget()
  page.selectAll()
  gui.clickButton(buttons.NextButton)
  console.log("   exit ComponentSelectionPage")
}

Controller.prototype.LicenseAgreementPageCallback = function()
{
  console.log("* enter LicenseAgreementPage")
  var page = gui.currentPageWidget()
  page.AcceptLicenseCheckBox.checked = true
  gui.clickButton(buttons.NextButton)
  console.log("   exit LicenseAgreementPage")
}

Controller.prototype.StartMenuDirectoryPageCallback = function()
{
  console.log("* enter StartMenuDirectoryPage")
  gui.clickButton(buttons.NextButton)
  console.log("   exit StartMenuDirectoryPage")
}

Controller.prototype.ReadyForInstallationPageCallback = function()
{
  console.log("* enter ReadyForInstallationPage")
  gui.clickButton(buttons.NextButton)
  console.log("   exit ReadyForInstallationPage")
}

Controller.prototype.PerformInstallationPageCallback = function()
{
  console.log("* enter PerformInstallationPage")
  gui.clickButton(buttons.NextButton);
  console.log("   exit PerformInstallationPage")
}

Controller.prototype.FinishedPageCallback = function()
{
  console.log("* enter FinishedPage")
  gui.clickButton(buttons.FinishButton)
  console.log("   exit FinishedPage")
}

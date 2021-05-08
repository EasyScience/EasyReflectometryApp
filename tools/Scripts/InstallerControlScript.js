function Controller()
{
}

Controller.prototype.IntroductionPageCallback = function()
{
  var page = gui.currentPageWidget();
  if (page != null)
  {
    if (installer.isInstaller())
    {
      var msg = ""
      msg += "<p>Welcome to the easyReflectometry Setup Wizard.</p>"
      msg += "<p>easyReflectometry is a scientific software for modelling and analysis of the neutron diffraction data.</p>"
      msg += "<p>For more details, visit <a href=\"https://easyReflectometry.org\">https://easyReflectometry.org</a></p>"
      page.MessageLabel.setText(msg)
    }
    if (installer.isUninstaller())
    {
      //gui.clickButton(buttons.NextButton)
    }
    if (installer.isUpdater())
    {
      //gui.clickButton(buttons.NextButton)
    }
  }
}

Controller.prototype.LicenseAgreementPageCallback = function()
{
  var page = gui.currentPageWidget()
  if (page != null)
  {
    page.AcceptLicenseRadioButton.setChecked(true)
  }
}

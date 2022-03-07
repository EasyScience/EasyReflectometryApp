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
      msg += "<p>Welcome to the EasyReflectometry Setup Wizard.</p>"
      msg += "<p>EasyReflectometry is a scientific software for modelling and analysis of the neutron diffraction data.</p>"
      msg += "<p>For more details, visit <a href=\"https://EasyReflectometry.org\">https://EasyReflectometry.org</a></p>"
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

function component(fileName)
{
    const dirPath = Qt.resolvedUrl("../Components")
    //const dirPath = "../../Components"
    const filePath = dirPath + "/" + fileName
    return filePath
}

const exportPoint = artifacts.require('Transaction')
module.exports= function (exportview){
    exportview.deploy(exportPoint)
}
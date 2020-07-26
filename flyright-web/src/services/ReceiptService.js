import Api from '@/services/Api'

export default {
  getReceipts (){
    return Api().get('receipt')
  },
  getReceipt (receiptId){
    return Api().get('receipt/' + receiptId)
  },
  createReceipt (receiptInfo) {
    return Api().post('receipt', receiptInfo)
  },
  updateReceipt (receiptInfo) {
    return Api().put('receipt', receiptInfo)
  },
  destroyReceipt (receiptInfo) {
    return Api().delete('receipt', { data: receiptInfo})
  }
}

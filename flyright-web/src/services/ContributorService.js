import Api from '@/services/Api'

export default {
  getContributorsReceipt (receiptId){
    return Api().get('contributors/receipt/' + receiptId)
  },
  addContributorReceipt (receiptId, userId) {
    return Api().post('contributors/receipt', { receiptId: receiptId, userId: userId})
  },
  removeContributorReceipt (receiptId, userId) {
    return Api().delete('contributors/receipt', { data: { receiptId: receiptId, userId: userId}})
  },
  getContributorsExpense (expenseId){
    return Api().get('contributors/expense/' + expenseId)
  },
  addContributorExpense (expenseId) {
    return Api().post('contributors/expense/' + expenseId)
  },
  removeContributorExpense (expenseId) {
    return Api().delete('contributors/expense/' + expenseId)
  }
}

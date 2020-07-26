import Api from '@/services/Api'

export default {
  getExpenses (receiptId){
    return Api().get('expense/' + receiptId)
  },
  getExpense (receiptId, expenseId){
    return Api().get('expense/' + receiptId + '/' + expenseId)
  },
  createExpense (expenseInfo) {
    return Api().post('expense', expenseInfo)
  },
  updateExpense (expenseInfo) {
    return Api().put('expense', expenseInfo)
  },
  destroyExpense (expenseInfo) {
    return Api().delete('expense', { data: expenseInfo})
  }
}

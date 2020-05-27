function (doc) {
  if (doc.locstatecode) {
    emit(doc.locstatecode, 1);
  }
}
